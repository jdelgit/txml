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
            # children_tree = []
        append_children = False
        for event, elem in context:
            if tag:
                if get_children:
                    if append_children:
                        # if elem.tag != tag and event == 'start':
                            # children_tree.append((elem.tag, event))

                        if elem.tag != tag and event == 'end':
                            # children_tree.append((elem.tag, event))
                            node_dict = self._node_to_dict(elem)
                            elem.clear()
                            children.append(node_dict)
                    if elem.tag == tag and event == 'start':
                        append_children = True

                if elem.tag == tag and event == 'end':

                    node_dict = self._node_to_dict(elem)
                    elem.clear()

                    if get_children:
                        node_dict['children'] = children
                        # node_dict['children_tree'] = children_tree
                        children = []
                        # children_tree = []
                        append_children = False

                    yield node_dict
            else:
                node_dict = self._node_to_dict(elem)
                elem.clear()

                yield node_dict
        del context

    def _node_to_dict(self, node=""):
        data = {n[0]: n[1] for n in node.items()}
        data['text'] = node.text
        data['tag'] = node.tag
        return data


source = 'test_productindex.xml'
xm = XmlParser(source)
files = xm.search_nodes(tag='file', get_children=True)
match = xm.search_node_attr(tag='file', attr_id='Catid', attr_val='587', get_children=True)
m = list(match)

