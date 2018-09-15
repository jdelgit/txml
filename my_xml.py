from xml.etree.ElementTree import iterparse


class XmlParser:

    def __init__(self, source):
        self.source = source

    def search_node_attr(self, tag="", attr_id="",
                         attr_val="", get_children=False):
        for node in self.search_nodes(tag=tag, get_children=get_children):
            if node[attr_id] == attr_val:
                yield node

    def search_nodes(self, tag="", get_children=False):
        context = iterparse(self.source, events=('start', 'end'))
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
                        self._xml_children_handler(event=event,
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
                elem.clear()

                if get_children:
                    node_dict['children'] = children
                    children = []
                    append_children = False

                yield node_dict

        del context

    def _xml_children_handler(self, event, elem, p_tag="", c_tag="",
                              p_stack=[], tag_stack=[], children=[],
                              npd=False):
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
        data = {n[0]: n[1] for n in node.items()}
        data['text'] = node.text
        data['tag'] = node.tag
        return data
