import my_xml as mx
import xml.etree.ElementTree as et

import unittest


prod_translations = {
    'Product_ID': "Product",
    'Model_Name': "Title",
    'path': "Detail-XML",
    'EAN_UPC': "EAN",
    'HighPic': "Image"
}


class TestXmlParser(unittest.TestCase):

    def setup(self, source):
        self.node= mx.XmlParser(source='test_productindex.xml')


    def test_search_node_attr(self):
        pass

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

        test_node_dict = {} # add new test case

        self.assertDictContainsSubset(control_dict, test_node_dict)
        self.assertIsInstance(test_node_dict['children'],
                              et.Element._element_iterator)

    def test_search_nodes(self):
        pass

    def test_search_node_attr(self):
        pass

    def test_filter_nodes(self):
        pass


if __name__ == '__main__':
    unittest.main()
