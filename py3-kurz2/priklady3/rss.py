import xml.etree.ElementTree as etree
import urllib.request as urllib
rss = urllib.urlopen("http://servis.idnes.cz/rss.aspx?c=zpravodaj")
tree = etree.parse(rss)
root = tree.getroot()
channel = root.find("channel")
print (channel.tag)
print (channel.attrib)
print (channel.text)
items = channel.findall("item")
for item in items:
  title = item.find("title")
  link = item.find("link")
  print (title.text)
  print (link.text+"\n")
