import my_xml as mx
import xml.etree.ElementTree as et

import unittest


xm = mx.XmlLookup('test_productindex.xml')
matches = xm.get_nodes(tag="file")
for m in matches:
    print(m)

prod_translations = {
    'Product_ID': "Product",
    'Model_Name': "Title",
    'path': "Detail-XML",
    'EAN_UPC': "EAN",
    'HighPic': "Image"
}


class TestXmlLookup(unittest.TestCase):

    def setup(self, xmldata):
        self.prod_node = mx.XmlLookup(xmldata="<file path=\"export/level4/NL/30114.xml\" Product_ID=\"30114\" Updated=\"20150301102709\" Quality=\"ICECAT\" Supplier_id=\"5\" Prod_ID=\"VCT-R640\" Catid=\"587\" On_Market=\"1\" Model_Name=\"Lightweight Tripod VCT-R640\" Product_View=\"32767\" HighPic=\"http://images.icecat.biz/img/norm/high/30114-Sony.jpg\" HighPicSize=\"20782\" HighPicWidth=\"320\" HighPicHeight=\"300\" Date_Added=\"20050715000000\">\
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

    def test_get_node_keys(self):
        test_node_keys = self.prod_node.get_node_keys()
        control_node_keys = ['path', 'Product_ID', 'Updated', 'Quality',
                             'Supplier_id', 'Prod_ID', 'Catid', 'On_Market',
                             'Model_Name', 'Product_View', 'HighPic',
                             'HighPicSize', 'HighPicWidth', 'HighPicHeight',
                             'Date_Added']
        self.assertEqual(test_node_keys, control_node_keys)

    def test_get_node_attr(self):
        attr = 'path'
        control_val = "export/level4/NL/30114.xml"
        test_node_val = self.prod_node.get_node_attr(attr=attr)

        self.assertEqual(test_node_val, control_val)

    def test_node_to_dict(self):

        control_dict = {'path': 'export/level4/NL/30114.xml',
                        'Product_ID': '30114', 'Updated': '20150301102709',
                        'Quality': 'ICECAT', 'Supplier_id': '5',
                        'Prod_ID': 'VCT-R640', 'Catid': '587',
                        'On_Market': '1', 'Model_Name': 'Lightweight Tripod VCT-R640',
                        'Product_View': '32767', 'HighPic': 'http://images.icecat.biz/img/norm/high/30114-Sony.jpg',
                        'HighPicSize': '20782', 'HighPicWidth': '320',
                        'HighPicHeight': '300', 'Date_Added': '20050715000000',
                        'text': '\n      ',
                        'tag': "gile"}
        test_node_dict = self.prod_node.node_to_dict()
        self.assertDictContainsSubset(control_dict, test_node_dict)
        self.assertIsInstance(test_node_dict['children'],
                              et.Element._element_iterator)

    def test_get_nodes(self):

        nodes = self.prod_node.get_nodes(tag="EAN_UPC")
        control_values = set(['4901780776467', '5053460903188'])
        test_node_values = set([self.prod_node.get_node_attr('Value')
                               for n in nodes])
        self.assertSetEqual(control_values, test_node_values)

    def test_filter_nodes_attr(self):
        pass

    def test_filter_nodes(self):
        pass


if __name__ == '__main__':
    unittest.main()
