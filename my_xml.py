from xml.etree.ElementTree import iterparse
# Doesn't support string inputs yet, only .xml files


class XmlParser:

    def __init__(self, source=""):
        self.source = source

    def search_node_attr(self, tag="", get_children=True, **kwargs):
        """[This function filters results from the <search_node> function
            based on given attributes,values]

        Keyword Arguments:
            tag {str} -- [tag of Xml node element] (default: {""})
            get_children {bool} -- [Choice for whether
                                    subnodes should be returned] (default: {True})

        Returns / yields:
            [dict] -- [Dictionary containing all matching nodes]
        """

        if 'kwargs' in kwargs:
            kwargs = kwargs['kwargs']
        for node in self.search_nodes(tag=tag, get_children=get_children):
            if len(kwargs) > 0:
                for key in kwargs:
                    arg = kwargs[key]

                    try:
                        node_val = node['elem'][key]
                    except KeyError:
                        print("Key '{}' not found in element {}".format(key,
                                                                        tag))
                        # exit function if non-existing key is requested
                        return {}

                    if node_val == arg:
                        give_node = True
                    else:
                        # attribute not matching
                        # move on to next node
                        give_node = False
                        break
            else:
                give_node = True
            if give_node:
                yield node

    def search_nodes(self, tag="", get_children=True):
        """[If a tag is specified the function returns an generator with all Xml elements
            which have a matching tag. If tag is not specified, the root node is returned
            When get_children is set, the function returns the subnodes
            nested in a list of dictionaries]

        Keyword Arguments:
            tag {str} -- [tag of Xml node element] (default: {""})
            get_children {bool} -- [Choice for whether subnodes should be returnd] (default: {True})
        """

        if self.source:
            context = iterparse(self.source, events=('start', 'end'))
        else:
            print("No source XML-file provided")
            return
        if get_children:
            children = []
            p_stack = []
            tag_stack = []
            p_tag = ""
            c_tag = ""
            npd = False
        append_children = False
        for event, elem in context:
            if not tag:
                # if no tag is given then get data nor entire document
                tag = elem.tag

            if get_children:
                if elem.tag != tag and append_children:
                    event, elem, p_tag, c_tag, p_stack, \
                        tag_stack, children, npd = \
                        self._stack_state_controller(event=event,
                                                     elem=elem,
                                                     p_tag=p_tag,
                                                     c_tag=c_tag,
                                                     p_stack=p_stack,
                                                     tag_stack=tag_stack,
                                                     children=children,
                                                     npd=npd)

                if elem.tag == tag and event == 'start':
                    append_children = True

            if elem.tag == tag and event == 'end':

                node_dict = self._node_to_dict(elem)
                output_dict = {'elem': node_dict, 'children': []}
                elem.clear()

                if get_children:
                    output_dict['children'] = children
                    children = []
                    append_children = False

                yield output_dict

        del context

    def _stack_state_controller(self, event, elem, p_tag="", c_tag="",
                                p_stack=[], tag_stack=[], children=[],
                                npd=False):
        """[Keeps track of a dictionary stack and a tag stack, and updates them as required.
            This is done based on the start/end triggers from the elements in the Xml format]

        Arguments:
            event {[str]} -- [description]
            elem {[et.etree.ElementTree.Element]} -- [description]

        Keyword Arguments:
            p_tag {str} -- [Current parent tag (top of dict stack). (not used actively) ] (default: {""})
            c_tag {str} -- [Current child tag (top of tag stack)] (default: {""})
            p_stack {list} -- [Stack for holding the parent dictionaries ] (default: {[]})
            tag_stack {list} -- [Stack for holding all the tags] (default: {[]})
            children {list} -- [List for holding all subnodes found] (default: {[]})
            npd {bool} -- [When set new dictionary is appended to stack] (default: {False})

        Returns:
            All arguments passed to it are returned after being updated
        """

        # ndp controls the creation of new dicts in the p_stack
        if (elem.tag != c_tag) and (event == "start"):
            tag_stack.append(elem.tag)
            if npd:
                # add new dictionary when children are confiremed to exist
                _p_dict = {'children': [], 'elem': ""}
                p_stack.append(_p_dict)
            p_tag = c_tag
            c_tag = elem.tag
            npd = True

        elif (elem.tag == c_tag) and (event == "end"):

            if len(tag_stack) == 1:
                # last child on stack
                if len(p_stack) > 0:
                    # child has children
                    _child = p_stack.pop()
                    _child['elem'] = self._node_to_dict(elem)

                else:
                    _child = {'children': [],
                              'elem': self._node_to_dict(elem)}
                children.append(_child)
                c_tag = ""
                tag_stack.pop()

            elif len(tag_stack) == len(p_stack):

                _child = p_stack.pop()
                _parent = p_stack.pop()
                _child['elem'] = self._node_to_dict(elem)
                _parent['children'].append(_child)
                p_stack.append(_parent)

                tag_stack.pop()
                c_tag = tag_stack[-1]
                if len(tag_stack) > 1:
                    p_tag = tag_stack[-2]
                else:
                    p_tag = ""

            else:
                _parent = p_stack.pop()
                _child = self._node_to_dict(elem)
                _parent['children'].append(_child)
                p_stack.append(_parent)

                tag_stack.pop()
                c_tag = tag_stack[-1]
                if len(tag_stack) > 1:
                    p_tag = tag_stack[-2]
                else:
                    p_tag = ""

            npd = False
            elem.clear()

        return [event, elem, p_tag, c_tag, p_stack,
                tag_stack, children, npd]

    def _node_to_dict(self, node=""):
        """[Convert node element attributes to dictionary]

        Keyword Arguments:
            node {et.etree.ElementTree.Element} -- [] (default: {""})

        Returns:
            [dict] -- [Dictionary containing all the attribute,value pairs
                       contained in the node]
        """

        data = {n[0]: n[1] for n in node.items()}
        data['text'] = node.text
        data['tag'] = node.tag
        return data
