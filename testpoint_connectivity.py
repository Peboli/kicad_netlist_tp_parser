# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = "Olivier Cornet"
__appname__ = "Kicad Plugin for checking connection between nets and testpoints"
__version__ = "1.0.0"
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

# Created by Olivier Cornet at 09-08-22 - 11:00
# Title : Kicad Plugin for checking connections between Nets and Testpoints
# File : testpoint_connectivity.py

# V1.0.0	09-08-22 - Initial release


"""
    @package
    Output: TXT (Text)

    Outputs a summary of Nets and Testpoints informations.
    Un/connected Nets, Nets with and without Testpoints, Testpoints coverage, ...

    Command line:
    python "pathToFile/testpoint_connectivity.py" "%I" "%O_testpoint.txt"
"""


import sys
from pathlib import Path
import xml.etree.ElementTree as Et

prefix = "TP"
tree = None


def prt2file(line):
    print(line)
    if txt_file:
        txt_file.write(line + '\n')


try:
    Path.mkdir(Path(sys.argv[2]).parent, exist_ok=True)
    txt_file = open(sys.argv[2], 'w')
except IOError:
    txt_file = None
    print(f"Can't open file {sys.argv[2]} for writing")

try:
    tree = Et.parse(sys.argv[1])
except Et.ParseError:
    print("File does not seem to be a valid XML file !")
    txt_file.close()
    sys.exit()
finally:
    root = tree.getroot()
    nets = [[net.get('name'), [node.get('ref') for node in net.iter('node')]] for net in root.find('nets').iter('net')]
    tp = [tp.get("ref") for tp in root.find("components").iter("comp") if tp.get("ref").startswith(prefix)]

    unconnected = [net for net in nets if len(net[1]) == 1]
    connected = [net for net in nets if len(net[1]) > 1]
    connected_wo_tp = [net for net in nets if (not sum(1 for s in net[1] if prefix in s) and len(net[1]) > 1)]
    connected_one_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) == 1]
    connected_more_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) > 1]
    connected_tp = [net for net in nets if sum(1 for s in net[1] if prefix in s) >= 1]
    tp_coverage = len(connected_tp) / len(connected)

    # SUMMARY display
    prt2file("\n================= Summary ======================")
    prt2file(f"Total TestPoint : {len(tp)}")
    prt2file(f"Total Nets : {len(nets)}")
    prt2file(f"Total connected Nets : {len(connected)}")
    prt2file(f"Unconnected Nets : {len(unconnected)}")
    prt2file(f"Connected Nets with TestPoint : {len(connected_tp)}")
    prt2file(f"Connected Nets without TestPoint : {len(connected_wo_tp)}")
    prt2file(f"TestPoint coverage : {tp_coverage:.1%}")
    prt2file("\n====== Connected Nets without TestPoint ========")
    for n in connected_wo_tp:
        prt2file(n[0])
    prt2file("\n========= 1 TestPoint connected Nets ===========")
    for n in connected_one_tp:
        prt2file(
            f"{n[0]} : {', '.join([tp for tp in n[1] if prefix in tp])}")
    prt2file("\n===== More than 1 TestPoint connected Nets =====")
    for n in connected_more_tp:
        prt2file(
            f"{n[0]} : {', '.join([tp for tp in n[1] if prefix in tp])}")
    prt2file("\n=============== Unconnected Nets ===============")
    for n in unconnected:
        prt2file(n[0])

if txt_file:
    txt_file.close()
