from xml.etree.ElementTree import iterparse, ParseError
from io import StringIO
from os.path import isfile
from re import findall


class XmlParser:

    def __init__(self, source=""):
        self.source = source
        self.proces_file = False
        self.use_io = False
        self.encoding = 'UTF-8'
        self.namespaces = {}
        self.namespace_present = False
        self._source_check()

    # see also _get_encoding, _get_namespaces
    def _source_check(self):
        """
        [Function checkes whether the source input is a existing xml file
         or a xml syle formatted string]
        """

        _extension = self.source[-3:]
        if _extension == "xml":
            if isfile(self.source):
                self.proces_file = True
                self._get_encoding()
                self._get_namespaces()
            else:
                print("File not found {}".format(self.source))
        else:
            context_test = iterparse(StringIO("""{}""".format(self.source)))
            try:
                context_test.__next__()
                del context_test
                self.proces_file = True
                self.use_io = True
                self._get_encoding()
                self._get_namespaces()
            except ParseError:
                del context_test
                print("Input is not in supported Xml format")

    def _get_encoding(self):
        if self.proces_file and not self.use_io:
            with open(self.source, 'r') as f:
                l = f.readline()
            if 'encoding' in l:
                match = findall('(encoding=.*\?)', l)
                encoding = match[0].split('=')[1].replace(
                    '?', '').replace('\"', '')
                self.encoding = encoding

    # see also get_all_tags
    def _get_namespaces(self):
        """[Creates a dictionary of the namespaces with their associated tags ]

        Returns:
            [dict] -- [Dictionary with namespaces as keys
                       and the corresponding tags in a list as value ]
        """

        tags = self.get_all_tags()
        namespaces = {}
        for tag in tags:
            namespace = findall('({.{1,}})', tag)
            if len(namespace) > 0:
                namespace = namespace[0]
                formatted_tag = tag.replace(namespace, '')
                try:
                    namespaces[namespace].append(formatted_tag)
                except KeyError:
                    namespaces[namespace] = [formatted_tag]
        if namespaces:
            self.namespace_present = True
        self.namespaces = namespaces
        # return namespaces

    def get_all_tags(self):
        """[All the unique tags available in the Xml
            No hierachy is mainted for the xml structure]

        Returns:
            [list] -- [A list of all the unique tags available in the Xml]
        """

        if self.source and self.proces_file:

            if self.use_io:
                context = iterparse(StringIO("""{}""".format(self.source)),
                                    events=("start",))
            else:
                data = open(self.source, 'r', encoding=self.encoding)
                context = iterparse(data, events=("start",))
        else:
            print("No source XML-file provided")
            return
        tag_set = []
        for event, elem in context:
            tag_set.append(elem.tag)
            elem.clear()
        if self.source and self.proces_file and not self.use_io:
            data.close()  # close filestream
        del context
        tag_set = list(set(tag_set))
        return tag_set

    # see also search_nodes
    def search_namespace_node(self, namespace="", tag=""):
        ntag = "{}{}".format(namespace, tag)
        for node in self.search_nodes(tag=ntag):
            yield node

    # see also search_node_attr
    def search_namespace_attr(self, namespace="", tag="", **kwargs):
        ntag = "{}{}".format(namespace, tag)
        for node in self.search_node_attr(tag=ntag, kwargs=kwargs):
            yield node

    # see also seach_nodes
    def search_node_attr(self, tag="", get_children=True, **kwargs):
        """[This function filters results from the <search_node> function
            based on given attributes,values]

        Keyword Arguments:
            tag {str} -- [tag of Xml node element] (default: {""})
            get_children {bool} -- [Choice for whether subnodes
                                    should be returned] (default: {True})

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

    # see also _node_to_dict and _stack_state_controller
    def search_nodes(self, tag="", get_children=True):
        """[If a tag is specified the function returns an generator
            with all Xml elements which have a matching tag.
            If tag is not specified, the root node is returned
            When get_children is set, the function returns the subnodes
            nested in a list of dictionaries]

        Keyword Arguments:
            tag {str} -- [tag of Xml node element] (default: {""})
            get_children {bool} -- [Choice for whether subnodes
                                    should be returned] (default: {True})
        """

        if self.source and self.proces_file:
            if self.use_io:
                context = iterparse(StringIO("""{}""".format(self.source)),
                                    events=('start', 'end'))
            else:
                data = open(self.source, 'r', encoding=self.encoding)
                context = iterparse(data, events=('start', 'end'))

        else:
            print("Unable to process input")
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
        if self.source and self.proces_file and not self.use_io:
            data.close()  # close filestream
        del data

    # see also node_to_dict
    def _stack_state_controller(self, event, elem, p_tag="", c_tag="",
                                p_stack=[], tag_stack=[], children=[],
                                npd=False):
        """[Keeps track of a dictionary stack and a tag stack, and updates them as required.
            This is done based on the start/end triggers from the elements in the Xml format]

        Arguments:
            event {[str]} -- [start/end points of element]
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
