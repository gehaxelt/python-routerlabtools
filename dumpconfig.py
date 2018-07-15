#!/usr/bin/env python3
#####
#
# Quick & Dirty configuration dumping tool written by Sebastian Neef (@gehaxelt)
# More info @ https://github.com/gehaxelt/python-routerlabtools
#
#####
import telnetlib
import sys

MAPPING = {
        'aac-rc1': ('ts4.dmz.routerlab', 7032),
        'aac-rj1': ('ts4.dmz.routerlab', 7029),
        'cgn-rc1': ('ts4.dmz.routerlab', 7027),
        'cgn-sc1': ('ts4.dmz.routerlab', 7026),
}


if len(sys.argv) < 3:
	print("Usage: ./{} aac-rc1 outfile.config".format(sys.argv[0]))
	sys.exit(1)

if not sys.argv[1] in MAPPING.keys():
	print("Host {} not found in our configuration".format(sys.argv[1]))
	sys.exit(1)

device = sys.argv[1].strip()
outfile = sys.argv[2].strip()
host, port = MAPPING[device]
print("[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK")
print("[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/")
print("[*] You chose {}".format(device))
print("[*] Connecting to {}:{}".format(*MAPPING[device]))
tn = telnetlib.Telnet(*MAPPING[device])
#tn.set_debuglevel(1000)

tn.write("\n")
tn.read_some()
tn.write("\n")
if "c" in device[3:]: #cisco
	state = tn.expect(["{}#".format(device)],2) 
	if ">" in state[2]:
		print("[*] Hmm, I need to escalate to higher priveleges...")
		tn.write("enable\r\n")
		tn.expect(["Password:"])
		tn.write("routerlab\r\n")
		state = tn.expect(["{}#".format(device)])
	if "{}#".format(device) not in state[2]:
		print("[-] Failed to enter priv mode")
		sys.exit(1)
	print("[+] I am in privileged mode, woop woop")
	print("[*] Starting dumping process!")
	tn.write("terminal length 0\r\n")
	tn.read_some()
	tn.write("show running-config\r\n")
	
	tn.read_until("!\r\n")
	dump = tn.read_until("!\r\nend\r\n")

	print("[+] finished. writing file {}".format(outfile))
	with open(outfile, "w") as f:
		f.write(dump)

	print("[*] Done! disconnecting.") 
	tn.close()
	sys.exit(0)		
elif "j" in device[3:]: #juniper
	state = tn.expect(["root@{}>".format(device)])
	if "root@{}>".format(device) not in state[2]:
		print("[-] Failed enter CLI")
		sys.exit(1)
	print("[+] Starting dumping process!")
	tn.write("set cli screen-length 0\n")
	tn.expect(["root@{}>".format(device)])
	tn.write("show configuration\n")

	tn.read_until("## Last commit:")
	dump = tn.read_until("}\r\n\r\n")
	print("[+] finished. writing file {}".format(outfile))
	with open(outfile, "w") as f:
		f.write("## Last commit:")
		f.write(dump)

	print("[*] Done! disconnecting.") 
	tn.close()
	sys.exit(0)		
else:
	print("Uknown device. Neither cisco nor juniper")
	sys.exit(1)

print(tn.read_some())
