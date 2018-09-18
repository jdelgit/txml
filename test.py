from txml import XmlParser


source = 'jan96down.xml'
tf = XmlParser(source=source)
t = tf.search_nodes(tag='Project')
list(t)

s2 = 'archive\\test_productindex.xml'
sf = XmlParser(source=s2)
r = sf.search_nodes(tag='file')
list(r)

