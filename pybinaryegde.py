#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import xlsxwriter


def read_input(path):
	d = []
	try:

		with open (path) as f:
			lines = f.readlines()
			for line in lines:
				d.append(line.rstrip('\n'))
			f.close()

	except Exception as exc:
		print ("Error in read_input" + str(exc))
	
	finally:
		return d

def export_results (targets,ports):
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	try:
		print ("Exporting the results in an excel")
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('edgeportal.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "IP")
		worksheet.write(row, col+1, "Ports")
		row += 1
		# Iterate over the data and write it out row by row.
		for target in targets:
				col = 0
				worksheet.write(row, col, target)
				worksheet.write(row, col+1, str(ports[i]).replace('[','').replace(']',''))
				row += 1
				i += 1

		#Close the excel
		workbook.close()


	except Exception as exc:
		print ("Error in export_results" + str(exc))

def manage_response (data,flag):
	ports = []
	try:

		if flag == 1:  #404
			pass
			ports.append('-')  #If result = NULL
		else:
			for port in data['events']:
				print (str(port['port']))
				ports.append(str(port['port']))
	
	except Exception as exc:
		print ("Error in manage_response " + str(exc))

	finally:
		return ports


		
def send_request (url,api):

	response = None
	api_key = {'X-Key' : api}
	flag = 0 #0 = 200, 1=404
	try:

		response = requests.get(url,timeout=20,allow_redirects =True,headers=api_key)
		if response.status_code == 404:
			print ("Not found information of the IP, pass the next")
			flag =1
	except Exception as exc:
		print ("Error in send_request" + str(exc))
	finally:
		return response.json(), flag


def banner():

	print ("""
	** Tool to obtain information about the open ports throught API's binaryedge (app.binaryedge.io)
    	** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    	** DISCLAMER This tool was developed for educational goals. 
    	** The author is not responsible for using to others goals.
    	** A high power, carries a high responsibility!
    	** Version 1.0""")
	
def initial_help():
	print (""" \n This script interactues with the binaryedge's API to obtain the ports opened of a network address. The result by default is exported in xlsx format

				Example of usage: python3 pyapibinaryegde.py ip.txt""")


def main(argv):

	banner()
	flag = 0
	initial_help()
	target = str(sys.argv[1])
	api="your_API"
	r = None
	ports = []
	ports_array =[]
	array = read_input(target) 
	try:
		for ip in array:
			print (ip)
			url ="https://api.binaryedge.io/v2/query/ip/{0}".format(ip)
			#Sent request
			(r,flag) = send_request(url,api)
			# Manage the response
			ports = manage_response(r,flag)
			ports_array.append(ports)
		#Export results		
		export_results(array,ports_array)

	except Exception as exc:
		print ("Error in main function " + str(exc))


if __name__ == "__main__":
    main(sys.argv[1:])