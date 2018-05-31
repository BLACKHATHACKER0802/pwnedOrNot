#!/usr/bin/env python

import os
import re
import json
import time
import argparse
import requests
import cfscrape

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

try:
	raw_input          # Python 2
except NameError:
	raw_input = input  # Python 3

try:
	unicode            # Python 2
except NameError:
	unicode = str      # Python 3

version = '1.0.5'

# commandline arguments
ap = argparse.ArgumentParser()
ap.add_argument('-e', '--email', required=False,
help='Email account you want to test')
ap.add_argument('-f', '--file', required=False,
help='Load a file with multiple email accounts')

arg = ap.parse_args()

status = False
fparse = False

addr = arg.email
file = arg.file

if arg.email:
	status = True
if arg.file:
	fparse = True
if not status:
	pass

def banner():
	os.system('clear')
	banner = """
	                                  ______       _   __      __
	    ____ _      ______  ___  ____/ / __ \_____/ | / /___  / /_
	   / __ \ | /| / / __ \/ _ \/ __  / / / / ___/  |/ / __ \/ __/
	  / /_/ / |/ |/ / / / /  __/ /_/ / /_/ / /  / /|  / /_/ / /_
	 / .___/|__/|__/_/ /_/\___/\__,_/\____/_/  /_/ |_/\____/\__/
	/_/
	"""
	print (C + banner + W)
	print (C + '	Developed by : ' + W + 'thewhiteh4t')
	print (C + '	Version      : ' + W + version + '\n')

def main():
	global addr
	global file

	print (G + '[+]' + C + ' Bypassing Cloudflare Restriction...' + W + '\n')
	useragent = {'User-Agent' : 'pwnedornot'}
	cookies, user_agent = cfscrape.get_tokens('https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com', user_agent='pwnedornot')

	# starts calculating script runtime
	start = time.time()

	# quit function prints total script runtime and exits
	def quit():
		print ('\n' + G + '[+]' + C + ' Completed in ' + W + str(time.time()-start) + C + ' seconds.' + W)
		exit()

	# skip function is called if no pastebin dumps are present
	def skip():
		print ('\n' + R + '[-]' + C + ' No Dumps Found... :(' + W)
		quit()

	def check():

		# sleep 2 seconds to avoid rate limit
		time.sleep(2)
		# r1 is the query for the account user enters
		r1 = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/{0}'.format(addr), headers= useragent, cookies= cookies, verify = True)
		#check1 is the status code for the account if we get a 404, account is not breached
		check1 = r1.status_code

		if check1 == 404:
			print ( '\n' + R + '[-]' + C + ' Account not pwned... :(' + W)
			exit()
		else:
			print ( '\n' + G + '[!]' + C + ' Account pwned...Listing Breaches...' + W)
			json1 = r1.content.decode('utf8')
			simple1 = json.loads(json1)

			for item in simple1:
				print ( '\n'
					+ G + '[+]' + C + ' Breach      : ' + W + unicode(item['Title']) + '\n'
					+ G + '[+]' + C + ' Domain      : ' + W + unicode(item['Domain']) + '\n'
					+ G + '[+]' + C + ' Date        : ' + W + unicode(item['BreachDate']) + '\n'
					+ G + '[+]' + C + ' Fabricated  : ' + W + unicode(item['IsFabricated']) + '\n'
					+ G + '[+]' + C + ' Verified    : ' + W + unicode(item['IsVerified']) + '\n'
					+ G + '[+]' + C + ' Retired     : ' + W + unicode(item['IsRetired']) + '\n'
					+ G + '[+]' + C + ' Spam        : ' + W + unicode(item['IsSpamList']))
		# r2 is the query for pastebin accounts if we get a 404, account does not have any dumps
		r2 = requests.get('https://haveibeenpwned.com/api/v2/pasteaccount/{0}'.format(addr), headers= useragent, cookies= cookies)
		check2 = r2.status_code

		if check2 != 200:
			print ('\n' + R + '[-]' + C + ' No Dumps Found... :(' + W)
			print ('\n' + G + '[+]' + C + ' Completed in ' + W + str(time.time()-start) + C + ' seconds.' + W)
			exit()

		json2 = r2.content.decode('utf-8')
		simple2 = json.loads(json2)

		# proceed is a flag
		proceed = False
		for item in simple2:
			if item['Source'] != 'Pastebin':
				continue
			if (item['Source']) == 'Pastebin':
				proceed = True
		#proceed tells the script to continue if the source is pastebin also it prevents multiple print statements
		if proceed == True:
			print ('\n' + G + '[+]' + C + ' Dumps Found...!' + W)
			print ('\n' + G + '[+]' + C + ' Looking for Passwords...this may take a while...' + '\n' + W)
		else:
			skip()

		for item in simple2:
			if (item['Source']) == 'Pastebin':
				link = item['Id']
				page = requests.get('https://www.pastebin.com/raw/{0}'.format(link))
				sc = page.status_code

				if not sc == 404:
					search = page.content.decode('utf-8')
					passwd = re.findall('{0}:(\w+)'.format(addr), search)
					if passwd:
						print (G + '[+] ' + W + ' '.join(passwd))

	def filecheck():
		time.sleep(2)
		r3 = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/{0}'.format(addr), headers= useragent, cookies= cookies, verify = True)
		check3 = r3.status_code

		if check3 == 404:
			print ( '\n' + R + '[-]' + C + ' Account not pwned... :(' + W)
		else:
			print ( '\n' + G + '[!]' + C + ' Account pwned...Listing Breaches...' + W)
			json1 = r3.content.decode('utf8')
			simple1 = json.loads(json1)

			for item in simple1:
				print ( '\n'
					+ G + '[+]' + C + ' Breach      : ' + W + unicode(item['Title']) + '\n'
					+ G + '[+]' + C + ' Domain      : ' + W + unicode(item['Domain']) + '\n'
					+ G + '[+]' + C + ' Date        : ' + W + unicode(item['BreachDate']) + '\n'
					+ G + '[+]' + C + ' Fabricated  : ' + W + unicode(item['IsFabricated']) + '\n'
					+ G + '[+]' + C + ' Verified    : ' + W + unicode(item['IsVerified']) + '\n'
					+ G + '[+]' + C + ' Retired     : ' + W + unicode(item['IsRetired']) + '\n'
					+ G + '[+]' + C + ' Spam        : ' + W + unicode(item['IsSpamList']))

			r4 = requests.get('https://haveibeenpwned.com/api/v2/pasteaccount/{0}'.format(addr), headers= useragent, cookies= cookies)
			check4 = r4.status_code

			if check4 != 200:
				print ('\n' + R + '[-]' + C + ' No Dumps Found... :(' + W)
			else:
				json2 = r4.content.decode('utf-8')
				simple2 = json.loads(json2)

				proceed = False
				for item in simple2:
					if item['Source'] != 'Pastebin':
						continue
					if (item['Source']) == 'Pastebin':
						proceed = True

				if proceed == True:
					print ('\n' + G + '[+]' + C + ' Dumps Found...!' + W)
					print ('\n' + G + '[+]' + C + ' Looking for Passwords...this may take a while...' + '\n' + W)

				for item in simple2:
					if (item['Source']) == 'Pastebin':
						link = item['Id']
						page = requests.get('https://www.pastebin.com/raw/{0}'.format(link))
						sc = page.status_code
						if not sc == 404:
							search = page.content.decode('utf-8')
							passwd = re.findall('{0}:(\w+)'.format(addr), search)
							if passwd:
								print (G + '[+] ' + W + ' '.join(passwd))

	if not status and not fparse:
		addr = raw_input(G + '[+]' + C + ' Enter Email Address : ' + W)
		check()
	elif status == True:
		print (G + '[+]' + C + ' Checking Breach status for ' + W + '{}'.format(addr))
		check()
	elif fparse == True:
		print (G + '[+]' + C + ' Reading Emails Accounts from ' + W + '{}'.format(file))
		with open(file) as dict:
			for line in dict:
				line = line.strip()
				addr = line
				print ('\n' + G + '[+]' + C + ' Checking Breach status for ' + W + '{}'.format(addr))
				filecheck()
	quit()
try:
	banner()
	main()
except KeyboardInterrupt:
	print ('\n' + R + '[!]' + C + ' Keyboard Interrupt.' + W)
	exit()
