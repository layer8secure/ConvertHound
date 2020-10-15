#!/usr/bin/python3

import sys
import os
import argparse
import json
from zipfile import ZipFile

dashline = "-" * 75

def color(text):

	if text.startswith('[+]'):
		return "\033[%d;3%dm%s\033[0m" % (0, 2, text)
	if text.startswith('[-]'):
		return "\033[%d;3%dm%s\033[0m" % (0, 1, text)
	if text.startswith('[*]'):
		return "\033[%d;3%dm%s\033[0m" % (0, 3, text)

def banner():
    print(r"""
  _____                      __  __ __                  __
 / ___/__  ___ _  _____ ____/ /_/ // /__  __ _____  ___/ /
/ /__/ _ \/ _ \ |/ / -_) __/ __/ _  / _ \/ // / _ \/ _  / 
\___/\___/_//_/___/\__/_/  \__/_//_/\___/\_,_/_//_/\_,_/  
                                                          

            author: Cory Wolff <OGloki aka visnet
                                aka iwaslokibeforeallofthesemovies
                                aka the '84 kid>
            company: Layer 8 <layer8security.com>
    """)
    print(dashline + "\n")

def python_check():
    if sys.version_info.major != 3:
        print(color("[-] Please run with Python 3. Python 2 is ded."))
        exit()

def create_computers_xml(filename_prefix, raw_json):

    data = json.loads(raw_json)
    new_file_name = './converthound/' + filename_prefix + '_computers.xml'
    new_file = open(new_file_name, "w")
    
    xml_header = ['<?xml version="1.0"?><?xml-stylesheet href="file:///usr/local/bin/../share/nmap/nmap.xsl" type="text/xsl"?><!-- Nmap 5.59BETA3 scan initiated Fri Sep  9 18:33:41 2011 as:nmap -T4 -A -p 1-1000 -oX - scanme.nmap.org --><nmaprun scanner="nmap" args="nmap -T4 -A -p 1-1000 -oX - scanme.nmap.org" start="1315618421" startstr="Fri Sep  9 18:33:41 2011" version="5.59BETA3" xmloutputversion="1.03"><scaninfo type="syn" protocol="tcp" numservices="1000" services="1-1000"/><verbose level="0"/><debugging level="0"/>']
    new_file.writelines(xml_header)

    for c in data['computers']:
        hostname = c['Properties']['name']
        os = c['Properties']['operatingsystem'] or "n/a"

        new_host = ['<host starttime="1315618421" endtime="1315618434">',
                    '<status state="up" reason="echo-reply"/>',
                    '<address addr="' + hostname +'" addrtype="ipv4"/>',
                    '<hostnames>',
                    '<hostname name="' + hostname + '" type="FQDN"/>',
                    '</hostnames>',
                    '<ports>',
                    '<extraports state="closed" count="997">',
                    '<extrareasons reason="resets" count="997"/>',
                    '</extraports>',
                    '</ports>',
                    '<os>',
                    '<portused state="closed" proto="tcp" portid="1"/>',
                    '<portused state="closed" proto="udp" portid="31289"/>',
                    '<osclass type="general purpose" vendor="Microsoft" osfamily="Windows" accuracy="100">',
                    '</osclass>',
                    '<osmatch name="' + os + '" accuracy="100" line="39278"/>',
                    '</os>',
                    '<uptime seconds="23450" lastboot="Fri Sep  9 12:03:04 2011"/>',
                    '<distance value="11"/>',
                    '<times srtt="26517" rttvar="19989" to="106473"/>',
                    '</host>']

        new_file.writelines(new_host)

    xml_footer = ['<runstats><finished time="1315618434" timestr="Fri Sep  9 18:33:54 2011" elapsed="13.66" summary="Nmap done at Fri Sep  9 18:33:54 2011; 1 IP address (1 host up) scanned in 13.66 seconds" exit="success"/><hosts up="1" down="0" total="1"/></runstats></nmaprun>']
    new_file.writelines(xml_footer)

def create_users_file(filename_prefix, raw_json):
    
    data = json.loads(raw_json)
    new_file_name = './converthound/' + filename_prefix + '_users.csv'
    new_file = open(new_file_name, "w")

    new_file.writelines(['display_name, user_name, domain, email, title, home_directory\n'])

    for u in data['users']:
        new_user = str( u['Properties']['displayname'] or "none") + ',' + \
                    str( u['Properties']['name'] or "none" ) + ',' + \
                    str( u['Properties']['domain'] or "none" ) + ',' + \
                    str( u['Properties']['email'] or "none" ) + ',' + \
                    str( u['Properties']['title'] or "none" ) + ',' + \
                    str( u['Properties']['homedirectory'] or "none" ) + '\n'

        new_file.writelines(new_user)

#
#
# Start of class
#
#
class ConvertHound(object):

    def __init__(self):
        parser = argparse.ArgumentParser(usage='''converthound.py <command> [<args>]
            Possible Commands:
            <convert> // Convert a Bloodhound computers.json to nmap XML

            Try converthound.py <command> -h for help with a particular command.
            ''')
        parser.add_argument('command', help='Command to run')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print (color('[-] Unrecognized command'))
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def convert(self):
        parser = argparse.ArgumentParser(description='Convert a Bloodhound zip file to multiple output files.')
        parser.add_argument('zipfile', type=str)

        args = parser.parse_args(sys.argv[2:])

        filename_prefix = args.zipfile.split("_")[0]
        
        if not (args.zipfile.endswith('.zip')):
            print(color('[-] You sure this is a zip file?'))
            exit()
        
        if not os.path.isdir('./converthound'):
            os.mkdir('converthound')

        try:
            print(color("[+] Reading zip file..."))
            
            with ZipFile(args.zipfile) as bloodzip:
                files = bloodzip.namelist()
                for f in files:
                    if "computers" in f:
                        print(color('[+] Creating computers file...'))
                        computers_file = bloodzip.read(f)
                        create_computers_xml(filename_prefix, computers_file)
                    elif "users" in f:
                        print(color('[+] Creating users file...'))
                        users_file = bloodzip.read(f)
                        create_users_file(filename_prefix, users_file)
            

        except IOError as e:
            errno, strerror = e.args
            print(color("[-] I/O error({0}): {1}".format(errno,strerror)))
        except: #handle other exceptions such as attribute errors
            print(color("[-] Unexpected error:" + sys.exc_info()[0]))
            pass            

            

if __name__ == '__main__':

    banner()
    python_check()

    ConvertHound()