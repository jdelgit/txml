# txml

'txml' is a module to parse XML files to a dictionary-like object

## Usage
This module currently only supports a '.xml' file as input

'''python
>>> from my_xml import XmlParser

>>> parser = XmlParser()
element = "<file path=\"export/level4/NL/30114.xml\" \
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
        </Country_Markets>\
        <TryCData>\
        <![CDATA[cdata text & > hoi]]>\
        </TryCData>\
        </file>"

>>> type(element) = et.etree.(c)ElementTree.Element
>>> result = parser._node_to_dict(element)
'''
All the attributes are of the element are return, the child elements are ignored

'''python
>>> result

{'path': 'export/level4/NL/30114.xml',
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

'''

Reading  and searching throug an .xml file
Using 'sample.xml'

'''python
>>> from my_xml import XmlParser
>>> source = sample.xml
>>> parser = XmlParser(source=source)
>>> products = parser.search_nodes(tag='controller')
'''

The 'products' object is a generator of all matched instances of the tag 'controller'.
The results can only be accessed once. If the results require multiple accesses
then the generator can be converted to a list.

'''python

>>> product_list = list(product)
>>> len(product_list)
2
'''

Let's look at the first entry
'''python
>>> product_list[0]
{'elem': {'type': 'usb', 'index': '0',
          'text': '\n            ',
          'tag': 'controller'}
 'children': [{'children': [],
               'elem': {'name': 'usb0',
                        'text': None, 'tag': 'alias'}},
               {'children': [],
                'elem': {'type': 'pci', 'domain': '0x0000',
                         'bus': '0x00', 'slot': '0x01',
                         'function': '0x2',
                         'text': None, 'tag': 'address'}}] }

'''

The txml module can also search for node which match a set of attributes.
'''python
>>> product = parser.search_node_attr(tag='controller', type='usb')
>>> len(list(product))
1

>>> product
{'elem': {'type': 'usb', 'index': '0',
          'text': '\n            ',
          'tag': 'controller'}
 'children': [{'children': [],
               'elem': {'name': 'usb0',
                        'text': None, 'tag': 'alias'}},
               {'children': [],
                'elem': {'type': 'pci', 'domain': '0x0000',
                         'bus': '0x00', 'slot': '0x01',
                         'function': '0x2',
                         'text': None, 'tag': 'address'}}] }

'''
## Installation
Clone this repo

## License
'txml' is released under the terms of the [MIT license](http://opensource.org/licenses/MIT)

## Links
* [Github]  (https://github.com/jdelgit/txml)


## To Do
*Check unit tests
*Finish README
*Performance tests
*Support for string input formats