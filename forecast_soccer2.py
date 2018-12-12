
# import libraries
import urllib2
from bs4 import BeautifulSoup


# specify the url
quote_page = 'http://www.soccer-db.info/index.php?option=com_php&views=php&Itemid=224'

req = urllib2.Request(quote_page)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
response = urllib2.urlopen(req)

# query the website and return the html to the variable page
page = response
print page

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# for i in soup.find_all('form'):
#    print i.attrs['class']

# Take out the <div> of name and get its value

#name_box = soup.find('h3')
#name = name_box.text.strip()   # strip() is used to remove starting and trailing
#print name_box

# get the index price
#name2_box = soup.find('div', attrs={'class': 'logo'})
#print name2_box

for tr in soup.find_all('tr')[2:]:
    tds = tr.find_all('td')
print tds