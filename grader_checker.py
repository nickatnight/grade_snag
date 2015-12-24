#!/usr/bin/env python


import cookielib
import urllib2
import mechanize
import sys
import time
from messenger import send_email
from bs4 import BeautifulSoup

COUNT=2

class GradeCheck:

	def __init__(self):

		self.br = mechanize.Browser()
		self.sess_id = 'CURRENT_SESS_ID'
		self.site = 'https://sunspot.sdsu.edu/AuthenticationService/loginVerifier.html?pc=portal'
		self.post_login = 'https://sunspot.sdsu.edu/pls/webapp/web_menu.main_page?sess_id=' + self.sess_id
		self.cookiejar = cookielib.LWPCookieJar()
		self.br.set_cookiejar( self.cookiejar )

		self.br.set_handle_equiv( True )
		self.br.set_handle_redirect( True )
		self.br.set_handle_referer( True )
		self.br.set_handle_robots( False )
		self.br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
		self.br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]


	def login(self):
		self.br.open(self.site)
		self.br.select_form( nr=0 )
		self.br['userName'] = 'YOUR_REDID'
		self.br['userPassword'] = 'YOUR_PASSWORD'
		self.br.submit()


	def check(self):

		self.br.open(self.post_login)
		self.br.follow_link(text='My Grades')
		html = self.br.response().read()
		soup = BeautifulSoup(html, 'html.parser')

		data = []
		text_body = ''
		table = soup.find('table', attrs={'width': '69%'})
		rows = table.find_all('tr')
		for row in rows:
			cols = row.find_all('td')
			cols = [ele.text.strip() for ele in cols if ele]
			data.append(cols)

		c=0
		for d in data:
			if d[5] =='--':
				c += 1
			print ("%s %s %s %s %s %s" % (d[0],d[1],d[2],d[3],d[4],d[5]))
			text_body += '{0}-{1}\n'.format(d[1],d[5])


		if c < (COUNT):
			send_email( 'YOUR_EMAIL', 'YOUR_PASSWORD', 'YOUR_PHONE@CELL_PROVIDER.com', 'Grades', text_body )

		print "\nGrades successfully checked!\n"


if __name__ == "__main__":
	print 'Initializing browser...\n'
	gc = GradeCheck()

	print 'Browser initialized...logging in...\n'
	gc.login()

	print 'Successful login...checking grades...\n'

	while True:
		gc.check()
		time.sleep(60)



