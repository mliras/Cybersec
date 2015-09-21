from scapy.all import *
import os

ap_list=[]
total_count=0
def getkey(item):
	return item[2]

def resumen(list):
	os.system('clear')
	print
	print
	print "      AP MAC           -  SSID          -   Beacons"
	print "======================================================="
	for e in sorted(list,key=getkey, reverse=True):
		print " %18s   -   %-20s  - %5d" %(e[0], e[1], e[2])
	print "======================================================="
	print 


def PacketHandler(pkt):
	try:
#Si es un paquete Wireless...
		global total_count

		if pkt.haslayer(Dot11):
			if pkt.type==0 and pkt.subtype==8:
				encontrado=False
				total_count+=1

				for e in ap_list:
					if e[0]==pkt.addr2:	
						e[2]+=1
						if total_count%50 == 0:
							resumen(ap_list)
						encontrado=True 

				if not encontrado:
					if pkt.info=="":
						ap_list.append([pkt.addr2,"<Hidden SSID>",1])
					else:
						ap_list.append([pkt.addr2,pkt.info,1])

		#			print "AP MAC: %s con SSID: %s" %(pkt.addr2, pkt.info)
					if total_count%100 == 0:
						resumen(ap_list)
	except:
		fdesc=open("spse.txt","w")
		fdesc.write(str(ap_list))	


os.system('clear')
sniff(iface="mon0", prn=PacketHandler)
