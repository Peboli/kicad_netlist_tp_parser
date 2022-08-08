# -*- coding: utf-8 -*-

__author__ = "Olivier Cornet"
__appname__ = "Kicad Netlist Parser for checking connection between net and test point"
__version__ = "1.0.1"
__maintainer__ = "Olivier Cornet"

# MIT License
#
# Copyright (c) 2022 Olivier Cornet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Created by Olivier Cornet at 07-08-22 - 11:04
# Title : Kicad Netlist Parser for checking test point vs net
# File : main.py

"""
V1.0.0	07-08-22 - Initial release
V1.0.1  08-08-22 - Refactoring and added summary informations
"""

import sys
import argparse
from pathlib import Path
import xml.etree.ElementTree as Et
import xml


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Kicad Netlist Test Point Parser')
    parser.add_argument('filename', metavar='netlist_file', type=str,
                        help='name of the file to parse')
    parser.add_argument('--prefix', metavar='component_prefix', type=str,
                        help='prefix of component reference, like TP for test point')

    args = parser.parse_args()
    file = Path(args.filename)
    if args.prefix:
        prefix = args.prefix
    else:
        prefix = "TP"
    print(f"Component reference prefix to check: {prefix}")

    if not Path(file).exists():
        print(f"File {args.filename} not found !")
        sys.exit(99)


    def parse_xml_netlist(_file):
        print("Processing, please wait ...")
        tree = None

        try:
            tree = Et.parse(_file)
        except xml.etree.ElementTree.ParseError:
            print("File does not seem to be a valid XML file !")
            sys.exit(99)
        finally:
            root = tree.getroot()
            nets = [[net.get('name'), [node.get('ref') for node in net.iter('node')]] for net in
                    root.find('nets').iter('net')]
            tp = [tp.get("ref") for tp in root.find("components").iter("comp") if tp.get("ref").startswith(prefix)]

            unconnected = [net for net in nets if len(net[1]) == 1]
            connected = [net for net in nets if len(net[1]) > 1]
            connected_wo_tp = [net for net in nets if (not sum(1 for s in net[1] if prefix in s) and len(net[1]) > 1)]
            connected_one_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) == 1]
            connected_more_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) > 1]
            connected_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) >= 1]
            tp_coverage = len(connected_tp) / len(connected)
            # SUMMARY display
            print("\n================= Summary ======================")
            print(f"{'Total TestPoint :': >35} {len(tp)}")
            print(f"{'Total Nets :': >35} {len(nets)}")
            print(f"{'Total connected Nets :': >35} {len(connected)}")
            print(f"{'Unconnected Nets :': >35} {len(unconnected)}")
            print(f"{'Connected Nets with TestPoint :': >35} {len(connected_tp)}")
            print(f"{'Connected Nets without TestPoint :': >35} {len(connected_wo_tp)}")
            print(f"{'TestPoint coverage :': >35} {tp_coverage:.1%}")
            print("\n====== Connected Nets without TestPoint ========")
            for n in connected_wo_tp:
                print(n[0])
            print("\n========= 1 TestPoint connected Nets ===========")
            for n in connected_one_tp:
                print(f"{n[0]} : {', '.join([tp for tp in n[1] if prefix in tp])}")
            print("\n===== More than 1 TestPoint connected Nets =====")
            for n in connected_more_tp:
                print(f"{n[0]} : {', '.join([tp for tp in n[1] if prefix in tp])}")
            print("\n=============== Unconnected Nets ===============")
            for n in unconnected:
                print(n[0])


    if Path(file).suffix == ".xml":
        parse_xml_netlist(file)
    else:
        print(f"File should have .xml extension !")
