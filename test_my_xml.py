from my_xml import XmlParser
from xml.etree.ElementTree import parse
import unittest


class TestXmlParser(unittest.TestCase):

    def setUp(self):
        self.vtc_parser = XmlParser(source='sample.xml')

    def tearDown(self):
        del self.vtc_parser

    def test_node_to_dict(self):
        node2dict_testdata = "<file path=\"export/level4/NL/30114.xml\" \
        Product_ID=\"30114\" Updated=\"20150301102709\" Quality=\"AWESOME\" \
        Supplier_id=\"5\" Prod_ID=\"FLY-734CU\" Catid=\"587\" On_Market=\"1\" \
        Model_Name=\"Mibatsu Monstrosity\" Product_View=\"32767\" \
        HighPic=\"http://images.awesome.biz/img/high/30114-Mibatsu.jpg\" \
        HighPicSize=\"20782\" HighPicWidth=\"320\" HighPicHeight=\"300\" \
        Date_Added=\"20050715000000\">\
        <M_Prod_ID>ACLS5<b>test</b>.CEE</M_Prod_ID>\
        <EAN_UPCS>\
        <EAN_UPC Value=\"4901780776467\" />\
        <EAN_UPC Value=\"5053460903188\" />\
        </EAN_UPCS>\
        <Country_Markets>\
        <Country_Market Value=\"PL\" />\
        <Country_Market Value=\"ES\" />\
        <Country_Market Value=\"NL\" />\
        <Country_Market Value=\"FR\" />\
        <Country_Market Value=\"ZA\" />\
        </Country_Markets>\
        <TryCData>\
        <![CDATA[cdata text & > hoi]]>\
        </TryCData>\
        </file>"

        test_node = parse(source=node2dict_testdata)
        my_parser = XmlParser()
        if hasattr(test_node, 'getroot'):
            test_node = test_node.getroot()
        test_dict = my_parser._node_to_dict(test_node)
        control_dict = {'path': 'export/level4/NL/30114.xml',
                        'Product_ID': '30114', 'Updated': '20150301102709',
                        'Quality': 'AWESOME', 'Supplier_id': '5',
                        'Prod_ID': 'FLY-734CU', 'Catid': '587',
                        'On_Market': '1',
                        'Model_Name': 'Mibatsu Monstrosity',
                        'Product_View': '32767',
                        'HighPic': 'http://images.awesome.biz/img/high/30114-Mibatsu.jpg',
                        'HighPicSize': '20782', 'HighPicWidth': '320',
                        'HighPicHeight': '300', 'Date_Added': '20050715000000',
                        'text': '\n      ',
                        'tag': "gile"}
        self.assertDictEqual(test_dict, control_dict)

    def test_search_nodes(self):
        products = self.vtc_parser.search_nodes(tag='controller')
        products_list = list(products)

        test_num_matches = len(products_list)
        control_num_matches = 2
        self.assertEqual(test_num_matches, control_num_matches)

        test_product = products_list[0]['elem']
        control_product = {'type': 'usb', 'index': '0',
                           'text': '\n            ',
                           'tag': 'controller'}

        self.assertDictEqual(test_product, control_product)

        test_list = products_list[0]['children']
        control_list = [{'children': [],
                         'elem': {'name': 'usb0',
                                  'text': None, 'tag': 'alias'}},
                        {'children': [],
                         'elem': {'type': 'pci', 'domain': '0x0000',
                                  'bus': '0x00', 'slot': '0x01',
                                  'function': '0x2',
                                  'text': None, 'tag': 'address'}}]

        self.assertEqual(test_list, control_list)

    def test_search_node_attr(self):
        product = self.vtc_parser.search_node_attr(
            tag='controller', type='usb')
        prod_list = list(product)

        test_matches = len(prod_list)
        control_matches = 1
        self.assertEqual(test_matches, control_matches)

        test_product = prod_list[0]['elem']
        control_product = {'type': 'usb', 'index': '0',
                           'text': '\n            ', 'tag': 'controller',
                           'children': [{'children': [],
                                         'elem': {'name': 'usb0',
                                                  'text': None,
                                                  'tag': 'alias'}},
                                        {'children': [],
                                         'elem': {'type': 'pci',
                                                  'domain': '0x0000',
                                                  'bus': '0x00',
                                                  'slot': '0x01',
                                                  'function': '0x2',
                                                  'text': None,
                                                  'tag': 'address'}}]}
        self.assertEqual(test_product, control_product)

if __name__ == '__main__':
    unittest.main()
