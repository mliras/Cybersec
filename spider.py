import urllib, socket
from BeautifulSoup import *
from collections import deque
import bisect
import sys
import getopt
import threading

extensions_excluded=['mp4','jpg','avi','zip','rar','epub','pdf','png','gif']
urllist=deque([])
domains=[]
ips=[]
url="http://www.valencia.es/general?limite_pagina=9999999"
u=""

FILE="ips_es.txt"
Verbose=False

#Esta funcion nos saca la extension de una URL. Puede ser pdf, html, zip... cualquier cosa
def get_extension(u):
        k=u.split('.')
        return k[len(k)-1]

def usage():
        print "Syntax: python spider.py [options]"
        print
        print "OPTIONS"
        print "-v --> Verbose. Show more information on what the script is doing"
        print "-h, --help --> Help. Show this information"
        print "-g"

opts, args = getopt.getopt(sys.argv[1:],'vhg')

for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-v':
            Verbose=True
            _debug = 1
        elif opt in ("-g", "--grammar"):
            grammar = arg


global fhandle
fhandle=open(FILE, "r")
for line in fhandle.readlines():
	l=line.split('---')	
	bisect.insort(domains, l[0])
	bisect.insort(ips, l[1])
	u=l[0]

fhandle.close()
#####url="http://"+u
urllist.append(url)

def getDomain(uri):
	dd=re.findall("^http.*://(.+?)/.*", uri)
	if len(dd)>0:
		return dd[0]
	else:
		return None

def isSpanish(dom):
	ll=dom.split('.')
	bool=True
	if (ll[len(ll)-1]=='es' or ll[len(ll)-1]=='es/'):
		bool=True
	else:
		bool=False
	return bool

while urllist:
	url=urllist.popleft()
	if Verbose:
		print "Sacamos de urllist la url " + url
		print "Aun quedan " +str(len(urllist)) + " urls"
	try:
		a=urllib.urlopen(url)
		html=a.read()
		soup=BeautifulSoup(html)
		a_tags=soup('a')
	except:
		continue
		if Verbose:
			print " ERROR: Hubo algun error al parsear: " + url
	
	for tag in a_tags:
		newurl=tag.get('href', None)
		if newurl:
			if re.search("^http", newurl):
		  	    if (not get_extension(newurl) in extensions_excluded) and (not newurl in urllist):
				domain=re.findall("^http.*://(.+?)/.*", newurl)
				if len(domain)>0 and isSpanish(domain[0]) and not getDomain(url)==domain[0]:
					urllist.append(newurl)
					if Verbose:
						print "		De esta URL obtenemos: " + newurl
					if not domain[0] in domains:
						bisect.insort(domains, domain[0])
						try:
       		     					ip = socket.gethostbyname_ex(domain[0])
       		 				except:
       		     					ip=[]
							if Verbose:
								print "		No se pudo obtener la ip de " + domain[0]
						
						if len(ip)>2:
							i=2
							while i<len(ip):
								for j in range(len(ip[i])):
									if ip[i][j] not in ips:
										bisect.insort(ips, ip[i][j])
										if Verbose:
											print "Ya tenemos "+ str(len(ips))+ " IPs"
										print domain[0] + "---" + ip[i][j]		
										fhandle=open(FILE, "a")
										fhandle.write(domain[0] + "---" + ip[i][j]+"\n")
										fhandle.close()
							#ips.append(ip[i])	
								i+=1

	if Verbose:
		print "En domains hay "+ str(len(domains)) + " dominios"
	if len(domains)>10000:
		break
