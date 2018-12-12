
# import libraries
import urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = 'https://projects.fivethirtyeight.com/soccer-predictions/mls/'

req = urllib2.Request(quote_page)
response = urllib2.urlopen(req)

# query the website and return the html to the variable page
page = response
print page

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value

name_box = soup.find('h1')
name = name_box.text.strip()   # strip() is used to remove starting and trailing
print name_box

# get the index price
#name2_box = soup.find('div', attrs={'class': 'logo'})
#print name2_box