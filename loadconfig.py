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
}

if len(sys.argv) < 3:
	print("Usage: ./{} aac-rc1 infile.config".format(sys.argv[0]))
	sys.exit(1)

if not sys.argv[1] in MAPPING.keys():
	print("Host {} not found in our configuration".format(sys.argv[1]))
	sys.exit(1)

device = sys.argv[1].strip()
infile = sys.argv[2].strip()
host, port = MAPPING[device]

with open(infile, "r") as f:
	config = f.read()

config = config.strip()
if "c" in device[3:]: #cisco
	if not "! Last configuration" in config[:100]:
		print("Config does not start with '! Last configuration'. Probably not cisco?!")
		sys.exit(1)
elif "j" in device[3:]: #juniper
	if not "## Last commit" in config[:100]:
		print("Config does not start with '##Last commit'. Probably not juniper?!")
		sys.exit(1)
else:
	print("Wrong device type.")
	sys.exit(1)

print("[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK")
print("[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/")
print("[+] I read your config file. It was a good read! :=)")
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
	print("[*] Starting restoring process!")
	tn.write("terminal length 0\r\n")
	tn.expect(["{}#".format(device)])
	tn.write("configure terminal\r\n")
	tn.expect(["\(config\)#".format(device)])
	tn.write("{}\r\n".format(config))
	tn.expect(["{}#".format(device)])
	print("[+] Writing memory. This could take a while")
	tn.write("write memory\r\n")
	tn.expect(["[OK]"])
	print("[*] Done! disconnecting.") 
	tn.close()
	sys.exit(0)		
elif "j" in device[3:]: #juniper
	state = tn.expect(["root@.*[>#]".format(device)])
	if ("root@".format(device) not in state[2]) and (">" not in state[2]):
		print("[-] Failed enter CLI")
		sys.exit(1)
	tn.write("configure\r\n")
	tn.expect(["root@.*#".format(device)])
	tn.write("load override terminal\r\n")
	tn.expect(["end input]\r\n"])
	print("[+] Starting restoring process!")
	tn.write("{}\n".format(config))
	tn.write("\x04")
	tn.expect(["root@.*#".format(device)])
	print("[+] Committing... This could take a while")
	tn.write("commit\r\n")
	tn.expect(["commit complete"])
	tn.write("exit\r\n")
	tn.read_some()
	print("[*] Done! disconnecting.") 
	tn.close()
	sys.exit(0)		
else:
	print("Uknown device. Neither cisco nor juniper")
	sys.exit(1)

print(tn.read_some())
