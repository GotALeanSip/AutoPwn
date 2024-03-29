#!/usr/bin/env python3
import argparse
import logging
import os
from pwncli import *

from analysis import inputDetector
from analysis import protectionDetector
from analysis import backdoorDetector
from analysis import overflowDetector_static
from analysis import overflowDetector_dynamic
from exploits import ret2backdoor
from exploits import stackRop
from exploits import stackShellcode

logging.basicConfig()
logging.root.setLevel(logging.INFO)
log = logging.getLogger(__name__)

binary_file_path = ""
input_funcs = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to analyze")
    args = parser.parse_args()
    if args.file is None:
        log.info("[-] Exitting no file specified")
        exit(1)
    binary_file_path = os.path.abspath(args.file)
    input_funcs = inputDetector.getInputFuncs(binary_file_path)
    properties = protectionDetector.getProperties(binary_file_path)
    backdoors = backdoorDetector.getBackdoors(binary_file_path)
    # overflow_list = overflowDetector_static.analysis(binary_file_path,input_funcs)
    # if len(overflow_list) > 0:
    #     log.info("[+] Overflow exist")
    #     if len(backdoors) > 0:
    #         payload = ret2backdoor.exploit(binary_file_path, overflow_list,
    #                                        backdoors)
    #         for p in range(len(payload)):
    #             with open('exp_%s' % p, 'wb') as f:
    #                 f.write(payload[p])
    #     elif properties['RWX']:
    #         stackShellcode.exploit(binary_file_path,properties)
    #     else:
    #         stackRop
    stackShellcode.exploit(binary_file_path,properties)
    # exploitable_state = overflowDetector_dynamic.analysis(binary_file_path)
    # ret2backdoor.exploit_dynamic(exploitable_state,backdoors)
    import IPython
    IPython.embed()
    
    
def stackShellcodeTest():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to analyze")
    args = parser.parse_args()
    binary_file_path = os.path.abspath(args.file)
    properties = protectionDetector.getProperties(binary_file_path)
    stackShellcode.exp(binary_file_path,properties)

def ret2backdoorTest():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to analyze")
    args = parser.parse_args()
    binary_file_path = os.path.abspath(args.file)
    input_funcs = inputDetector.getInputFuncs(binary_file_path)
    properties = protectionDetector.getProperties(binary_file_path)
    backdoors = backdoorDetector.getBackdoors(binary_file_path)
    overflow_list = overflowDetector_static.analysis(binary_file_path,input_funcs)
    payload = ret2backdoor.exploit(binary_file_path, overflow_list,backdoors)
    binary_name = os.path.basename(binary_file_path)
    for p in range(len(payload)):
        filename = '%s-exploit-%s' % (binary_name,p+1)
        with open(filename, 'wb') as f:
            f.write(payload[p])
    print("%s exploit in %s" % (binary_name, filename))
    print("run with `(cat %s; cat -) | %s`" % (filename, binary_file_path))
            
if __name__ == "__main__":
    stackShellcodeTest()
