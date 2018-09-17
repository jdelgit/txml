# txml

**txml** is a module to parse XML files to a dictionary-like object

## Usage

Reading  and searching throug an **.xml** file or string
Using 'sample.xml'

```python
>>> from my_xml import XmlParser
>>> source = 'sample.xml'
>>> parser = XmlParser(source=source)
>>> products = parser.search_nodes(tag='controller')
```

The **products** object is a _generator_ of all matched instances of the tag **controller**.
The results can only be accessed once. If the results require multiple accesses
then the generator should be converted to a list.


```python
>>> product_list = list(product)
>>> len(product_list)
3
```

Let's look at the first entry. A dictionary of the element is returned containing the elements attributes in a nested dictionary **elem** and a dictionary containing the a _list_ of all of the elements child nodes in **children**. Even sub nodes(grandchildren) are returned.

```python
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
```

The **txml** module can also search for node which match a set of **attributes**. Any number of attributes can be passed and the function will return any node containing the matching attributes.

```python
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
```


## Installation

Clone this repo, and enjoy.

## License

'txml' is released under the terms of the [MIT license](http://opensource.org/licenses/MIT)

## Links

+ [Github](https://github.com/jdelgit/txml)


## To Do

+ Performance tests
+ Support for namespaces