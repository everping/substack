f = open("substack.log", "rb")
f1 = open("teslamotors.com.csv", "ab")
lines = f.readlines()

for line in lines:
	pieces = line.split(" open ports: ")
	domain_ip = pieces[0].split(" ")
	domain = domain_ip[0]
	ip = domain_ip[1].replace("(", "").replace(")", "")
	ports = pieces[1].replace(",", "")
	f1.write("%s,%s,%s" % (domain, ip, ports))