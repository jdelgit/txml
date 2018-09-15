from my_xml import XmlParser
import unittest


class TestXmlParser(unittest.TestCase):

    def setup(self, source):
        self.parser = XmlParser(source='test_productindex.xml')

    def test_node_to_dict(self):
        pass

    def test_search_nodes(self):
        pass

    def test_search_node_attr(self):
        pass

    def test_filter_nodes(self):
        pass


if __name__ == '__main__':
    unittest.main()
