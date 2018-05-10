Routerlab-Tools
======================

This is a small toolset that I've developed for the [routerlab module @ TU berlin](http://www.inet.tu-berlin.de/?id=routerlab). 

# Overview

***This code was developed one wednesday night and SHOULD NOT even be considered alpha.*** 
If it doesn't blow up for you, you're lucky. If it does, you're welcome to open a pull request :=) 

Right now, there are only two scripts to help manage the configuration files for the cisco and juniper devices within the routerlab:

- `dumpconfig.py` dumps a configuration from a device and writes it to a file
- `loadconfig.py` loads a configuration from a file and applies it to a device

# Caveats

- The tools expect the devices to be in the lowest privilege mode, e.g. `user EXEC mode` on cisco or `cli operational mode` on juniper.
- The routerlab allows only one telnet session to a device. Make sure you have closed all connections before running the scripts. (or try `lab -k device`)
- It sometimes takes a while until a configuration is dumped or loaded. When in doubt, uncomment the `tn.set_debuglevel` line and see what is going on.
- Use at your own risk... Routers or switches might explode and kittens might die :-)

# Usage

Clone this repository on cheetah:

```
$> cd ~
$> git clone https://github.com/gehaxelt/python-routerlabtools tools
$> cd tools
```

To dump a configuration from a device, pass the device name and an outfile (it has to be writeable by you!) to the script:

```
group06@cheetah:/home-local/group06/tools$ python dumpconfig.py aac-rc1 test.config 
[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK
[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/
[*] You chose aac-rc1
[*] Connecting to ts4.dmz.routerlab:7032
[+] I am in privileged mode, woop woop
[*] Starting dumping process!
[+] finished. writing file test.config
[*] Done! disconnecting.


group06@cheetah:/home-local/group06/tools$ python dumpconfig.py aac-rj1 test2.config 
[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK
[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/
[*] You chose aac-rj1
[*] Connecting to ts4.dmz.routerlab:7029
[+] Starting dumping process!
[+] finished. writing file test2.config
[*] Done! disconnecting.
```

To load a configuration, run the second tool with the path to the config file and the device name as the arguments. It does some very basic checks if a configuration file is suitable for a device, but you shouldn't trust this check. ***Make sure to pass the right file!***

```
group06@cheetah:~/tools$ python loadconfig.py aac-rj1 test2.config 
[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK
[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/
[+] I read your config file. It was a good read! :=)
[*] You chose aac-rj1
[*] Connecting to ts4.dmz.routerlab:7029
[+] Starting restoring process!
[+] Committing... This could take a while
[*] Done! disconnecting.

group06@cheetah:~/tools$ python loadconfig.py aac-rc1 test.config                                                                                                                                                                              
[--] WARNING: This is more than dirty&quickly written. DO NOT EXPECT IT TO WORK
[--] SWITCHES AND ROUTERS MIGHT EXPLODE AND KITTENS MIGHT DIE :/
[+] I read your config file. It was a good read! :=)
[*] You chose aac-rc1
[*] Connecting to ts4.dmz.routerlab:7032
[+] I am in privileged mode, woop woop
[*] Starting restoring process!
[+] Writing memory. This could take a while
[*] Done! disconnecting.
```

# TODO

As I said, this is code was developed quick and dirty. Maybe other people from this or future routerlab modules (or even the tutors) will find the time to join me and refactor the code and/or extend its functionality.

Anyway, here's a list of todos:

- Extract the `MAPPING` into a separate file and load it from the `dump/load` scripts.
- Add more devices to the `MAPPING` dictionary
- Write better `tn.expect()` rules to catch the following things:
    - The device isn't in its initial state (e.g. user EXEC mode), but already in the global configuration mode. Return to the privileged mode and start from there. Same for juniper.
    - Detect when the hostname does not match the `[(aac|cgn|lev|lan)]-[r|s][c|j]\d+` pattern, e.g. when the hostname was changed.
- Better error handling
- Merge both scripts into one and use python's argument parsing to switch the modes
- Refactor the code and use classes/functions if necessary. 

- Write a script to disable leftover `vlans` from other groups and re-attach the interfaces to vlan 1.

# License
This code is published under MIT. See LICENSE.md