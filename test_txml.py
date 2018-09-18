from txml import XmlParser
from xml.etree.ElementTree import fromstring
import unittest


class TestXmlParser(unittest.TestCase):

    def setUp(self):
        self.parser = XmlParser(source='sample.xml')
        self.str_source = "<file path=\"export/level4/NL/30114.xml\" \
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

    def tearDown(self):
        del self.parser

    def test_get_encoding(self):
        self.encoded_parser = XmlParser(source='jan96down.xml')
        control_encoding = 'iso-8859-1'
        test_encoding = self.encoded_parser.encoding
        self.assertEqual(test_encoding, control_encoding)

        control_encoding = 'UTF-8'
        test_encoding = self.parser.encoding
        self.assertEqual(test_encoding, control_encoding)

    def test_source_check(self):
        non_existant_xml = 'some_random_file.xml'
        test_parser = XmlParser(source=non_existant_xml)
        self.assertEqual(test_parser.proces_file, False)
        self.assertEqual(test_parser.use_io, False)

        existing_xml = 'sample.xml'
        test_parser = XmlParser(source=existing_xml)
        self.assertEqual(test_parser.proces_file, True)
        self.assertEqual(test_parser.use_io, False)

        bad_format_str = "Just some random string of words"
        test_parser = XmlParser(source=bad_format_str)
        self.assertEqual(test_parser.proces_file, False)
        self.assertEqual(test_parser.use_io, False)

        proper_format_str = self.str_source
        test_parser = XmlParser(source=proper_format_str)
        self.assertEqual(test_parser.proces_file, True)
        self.assertEqual(test_parser.use_io, True)

    def test_node_to_dict(self):

        test_node = fromstring(self.str_source)
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
                        'text': '        ',
                        'tag': "file"}
        self.assertDictEqual(test_dict, control_dict)

    def test_get_namespaces(self):
        encoded_parser = XmlParser(source='jan96down.xml')
        # encoded_parser._get_namespaces()
        test_dict = encoded_parser.namespaces
        t_key = list(test_dict.keys())[0]
        ts_list = test_dict[t_key]
        ts_list.sort()
        test_dict = {t_key: ts_list}
        control_list = ['Application', 'ParaCurve', 'Metric', 'Start',
                        'Cant', 'Feature', 'Curve', 'CoordGeom',
                        'Alignments', 'Property', 'LandXML', 'CantStation',
                        'Profile', 'End', 'Center', 'Project', 'PVI', 'Units',
                        'Spiral', 'ProfAlign', 'Alignment', 'PI', 'Line']
        control_list.sort()
        control_dict = {'{http://www.landxml.org/schema/LandXML-1.1}': control_list}
        self.assertDictEqual(test_dict, control_dict)

    def test_search_nodes(self):
        products = self.parser.search_nodes(tag='controller')
        products_list = list(products)

        test_num_matches = len(products_list)
        control_num_matches = 3
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
        product = self.parser.search_node_attr(
            tag='controller', type='usb')
        prod_list = list(product)

        test_matches = len(prod_list)
        control_matches = 1
        self.assertEqual(test_matches, control_matches)

        test_product_elem = prod_list[0]['elem']
        control_product_elem = {'type': 'usb', 'index': '0',
                                'text': '\n            ',
                                'tag': 'controller'}
        self.assertEqual(test_product_elem, control_product_elem)

        test_product_children = prod_list[0]['children']
        control_product_children = [{'children': [],
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
                                              'tag': 'address'}}]
        self.assertEqual(test_product_children, control_product_children)

    def test_get_all_tags(self):

        test_list = self.parser.get_all_tags()
        control_list = ['sound', 'memballoon', 'pae', 'currentMemory', 'disk',
                        'mac', 'boot', 'emulator', 'driver', 'graphics',
                        'imagelabel', 'virtualport', 'video', 'on_crash',
                        'resource', 'serial', 'name', 'cpu', 'feature',
                        'alias', 'os', 'address', 'memory', 'channel',
                        'controller', 'console', 'parameters', 'uuid',
                        'devices', 'listen', 'domain', 'interface',
                        'type', 'input', 'label', 'on_poweroff',
                        'features', 'acpi', 'seclabel', 'vcpu', 'clock',
                        'on_reboot', 'apic', 'source', 'protocol',
                        'target', 'model', 'partition']
        control_list.sort()
        test_list.sort()

        self.assertListEqual(test_list, control_list)


if __name__ == '__main__':
    unittest.main()
