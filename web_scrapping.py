import requests
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable
import csv

Table = PrettyTable()
Table.field_names = [ "S.NO.","TITLE","PRIZE","STOCK","STAR" ]
books_info = []
serial_number = 1
for x in range(1,2):

	response = requests.get( "http://books.toscrape.com/catalogue/page-{}.html".format(x) ).text
	soup0 = bs( response , "html.parser" )
	soup1 = soup0.find( "div" , { "class" : "container-fluid page" } )
	soup2 = soup1.find( "div" , { "class" : "row" } )
	soup3 = soup2.find( "div" , { "class" : "col-sm-8 col-md-9" } )
	soup4 = soup3.find( "section" )
	soup5 = soup4.find_all( "div" )[ 1 ]
	soup6 = soup5.find( "ol" )
	soup7 = soup6.find_all( "li" )

	for book in soup7:

		title = book.article.h3.a[ "title" ]
		prize = book.article.find( "div" , { "class" : "product_price" } ).p.text[1:]
		stock = book.article.find( "div" , { "class" : "product_price" } ).find( "p" , { "class" : "instock availability" } ).text.strip()
		stars = book.article.p[ "class" ][ 1 ]
		book_info = [serial_number,title,prize,stock,stars]
		serial_number += 1
		books_info.append( book_info )

		Table.add_row( book_info )

with open( "book_scrape1.csv" , "w" ) as file:
	writer = csv.writer( file )
	writer.writerow( ["S.NO.","TITLE","PRIZE","STOCK","STAR"] )
	for book_info in books_info:
		try:
			writer.writerow( book_info )
		except UnicodeEncodeError:
			pass

# print(Table)