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
        if _extension == "xml" or _extension == "xsd":
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
                        node_val = node['element']['attr'][key]
                    except KeyError:
                        # print("Key '{}' not found in element {}".format(key,
                        #                                                 tag))
                        # exit function if non-existing key is requested
                        node_val = ''

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
                # if no tag is given then get data for entire document
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
                output_dict = {'element': node_dict, 'children': []}
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
                _p_dict = {'children': [], 'element': ""}
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
                    _child['element'] = self._node_to_dict(elem)

                else:
                    _child = {'children': [],
                              'element': self._node_to_dict(elem)}
                children.append(_child)
                c_tag = ""
                tag_stack.pop()

            elif len(tag_stack) == len(p_stack):

                _child = p_stack.pop()
                _parent = p_stack.pop()
                _child['element'] = self._node_to_dict(elem)
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
        data = {}
        data['attr'] = {n[0]: n[1] for n in node.items()}
        data['text'] = node.text
        data['tag'] = node.tag
        return data


class XsdtoDict:

    def __init__(self, source=''):
        self.source = source

    def convert_to_dict(self):
        parser = XmlParser(source=self.source)
        xsd_tags = self.get_export_type_data(parser)
        data = {}
        for tag in xsd_tags:
            data[tag['name']] = self.parse_xml_entry(tag, parser)
        return data

    def get_export_type_data(self, validation_parser):

        all_nodes = validation_parser.search_nodes()
        output_types = []
        for nodes in all_nodes:
            if nodes:
                output_types = [{'name': entry['element']['attr']['name'],
                                'tag': entry['element']['tag']}
                                for entry in nodes['children']]
        return output_types

    def parse_xml_entry(self, tag_data, xml_iterator):
        parent_tag = tag_data['tag']
        parent_name = tag_data['name']

        sub_elements = xml_iterator.search_node_attr(tag=parent_tag,
                                                     name=parent_name)
        if 'complexType' in parent_tag:
            output = self.parse_complextypes(sub_elements)
        elif 'simpleType' in parent_tag:
            output = self.parse_simpletypes(sub_elements)
        else:
            output = list(sub_elements)
        return output

    def parse_complextypes(self, complex_iterator):

        output = {}
        for element_data in complex_iterator:
            output['attr'] = element_data['element']['attr']
            output['sequence'] = []
            if element_data['children']:
                for sub_element in element_data['children']:
                    if 'sequence' in sub_element['element']['tag']:
                        sequence_data = self.parse_sequence(sub_element['children'])
                        output['sequence'].append(sequence_data)
                    else:
                        pass

        return output

    def parse_sequence(self, sequence_elements):

        sequence_output = []
        for element in sequence_elements:
            element_data = self.parse_element(element)
            sequence_output.append(element_data)
        return sequence_output

    def parse_element(self, element):
        output = {}

        if 'children' in element:
            output['tag'] = element['element']['tag']
            output['attr'] = element['element']['attr']
            element_children = element['children']
            output['children_data'] = []
            for child in element_children:
                if 'simpleType' in child['element']['tag']:
                    child_data = self.parse_simpletypes(child)
                    output['children_data'].append(child_data)
        else:
            output['tag'] = element['tag']
            output['attr'] = element['attr']
        return output

    def parse_simpletypes(self, simple_element):

        output = {}
        try:
            element_children = simple_element['children']
            for child_element in element_children:
                if 'restriction' in child_element['element']['tag']:
                    output['restrictions'] = {'attr': child_element['element']['attr']}
                    restriction_data = self.parse_restrictions(child_element['children'])
                    output['restrictions']['restrictions'] = restriction_data
        except TypeError:
            element_data = list(simple_element)
            element_data = element_data[0]
            element_children = element_data['children']
            element_children = element_children[0]['children']

            output['restrictions'] = []
            for data in element_children:
                if 'element' in data:
                    output['restrictions'].append(data['element']['attr']) 
                else:
                     if 'minLength' in data['tag']:
                         output['restrictions'].append({'minlength':data['attr']})
                     if 'maxLength' in data['tag']:
                         output['restrictions'].append({'maxlength':data['attr']})
        return output

    def parse_restrictions(self, restriction_iterator):

        output = []
        for restriction in restriction_iterator:
            restriction_data = {}
            restriction_data['enumarations'] = []
            restriction_data['length_data'] = []
            if 'element' in restriction:
                if 'enumeration' in restriction['element']['tag']:
                    enumaration_data = self.parse_enumarations(restriction['children'])
                    restriction_data['enumarations'].append(enumaration_data)
                    restriction_data['attr'] = restriction['element']['attr']
                elif 'Length' in restriction['element']['tag']:
                    restriction_data['attr'] = restriction['element']['attr']
                    restriction_data['length_data'].append(restriction['element']['attr'])
            else:
                restriction_data['attr'] = restriction['attr']

            output.append(restriction_data)

        return output

    def parse_enumarations(self, enumeration_iterator):

        output = {'annotations': ""}
        for enumaration in enumeration_iterator:
            if 'annotation' in enumaration['element']['tag']:
                annotations = enumaration['children']
                annot = {'documentation': []}
                for annotation in annotations:
                    annot['documentation'].append({'attr': annotation['attr'],
                                                   'text': ['text']})

                output['annotations'] = annot
        return output
