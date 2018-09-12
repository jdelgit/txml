import xml.etree.ElementTree as et


class XmlLookup:

    def __init__(self, xmldata=""):
        if xmldata[-4:] == ".xml":
            self.root = et.parse(xmldata).getroot()
        elif xmldata:
            self.tree = et.fromstring(xmldata)
            if type(self.tree) == et.ElementTree:
                self.root = self.tree.getroot()
            else:
                self.root = self.tree
        else:
            self.root = et.fromstring("<foo><bar></bar></foo>")

    def __str__(self):
        return self.root.tag

    def __repr__(self):
        return self.root.tag

    def get_node_keys(self, node=""):

        if node == "":
            node = self.root
        if type(node) == et.Element:
            return node.keys()
        else:
            print("Incorrect type {} for 'node'".format(type(node)))
            return []

    def get_node_attr(self, node="", attr=""):

        if node == "":
            node = self.root
        if type(node) == et.Element:
            return node.attrib.get(attr)
        else:
            print("Incorrect type {} for 'node'".format(type(node)))
            return ""

    def filter_nodes(self, node="", tag="",
                     attr_id="", attr_val=""):

            tagged_nodes = self.get_nodes(node=node, tag=tag)
            filtered_nodes = self.filter_nodes_attr(nodes=tagged_nodes,
                                                    attr_id=attr_id,
                                                    attr_val=attr_val)
            return filtered_nodes

    def get_nodes(self, node="", tag=""):

        if node == "":
            node = self.root
        if type(node) == et.Element:
            if tag:
                matching_nodes = node.iter(tag)
                return matching_nodes
            else:
                print("No tag given ")
        else:
            print("Incorrect type {} for 'node'".format(type(node)))
            return ""

    def filter_nodes_attr(self, nodes=[], attr_id="", attr_val=""):

        for sub_node in nodes:
            if attr_id:
                node_attr_val = sub_node.attrib.get(attr_id)
                if node_attr_val == attr_val:
                    yield self.node_to_dict(sub_node)
            else:
                yield self.node_to_dict(sub_node)

    def node_to_dict(self, node=""):

        if node == "":
            node = self.root
        data = {n[0]: n[1] for n in node.items()}
        data['text'] = node.text
        data['children'] = node.getiterator()
        data['tag'] = node.tag
        return data


test = XmlLookup(xmldata="<file path=\"export/level4/NL/30114.xml\" Product_ID=\"30114\" Updated=\"20150301102709\" Quality=\"ICECAT\" Supplier_id=\"5\" Prod_ID=\"VCT-R640\" Catid=\"587\" On_Market=\"1\" Model_Name=\"Lightweight Tripod VCT-R640\" Product_View=\"32767\" HighPic=\"http://images.icecat.biz/img/norm/high/30114-Sony.jpg\" HighPicSize=\"20782\" HighPicWidth=\"320\" HighPicHeight=\"300\" Date_Added=\"20050715000000\">\
      <M_Prod_ID>ACLS5<b>test</b>.CEE</M_Prod_ID>\
      <EAN_UPCS>\
        <EAN_UPC Value=\"4901780776467\" />\
        <EAN_UPC Value=\"5053460903188\" />\
      </EAN_UPCS>\
      <Country_Markets>\
        <Country_Market Value=\"PL\" />\
        <Country_Market Value=\"IT\" />\
        <Country_Market Value=\"DE\" />\
        <Country_Market Value=\"GB\" />\
        <Country_Market Value=\"US\" />\
        <Country_Market Value=\"ES\" />\
        <Country_Market Value=\"NL\" />\
        <Country_Market Value=\"FR\" />\
        <Country_Market Value=\"ZA\" />\
      </Country_Markets>\
      <TryCData>\
        <![CDATA[cdata text & > hoi]]>\
      </TryCData>\
    </file>")