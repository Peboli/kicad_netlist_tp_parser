# KICAD xml Netlist parser

## Description

This script has been developped following a request by user 'xzf16' on the [Kicad forum](https://forum.kicad.info/t/could-anyone-have-a-python-script-to-export-the-relationship-between-net-and-test-point/37024).<br>
The purpose of this script is to check if every net have a testpoint connected to it.

## Environnement
 * Run on Python >=3.6
 * No specific module

## Usage

```shell
> python netlist_tp_parser.py

usage: netlist_tp_parser.py [-h] [--prefix component_prefix] netlist_file
```

The argument `--prefix` may be used to specify the component reference prefix.<br>
If not specified, the default prefix is `TP` like Test Point.

## Example

```shell
> python3 netlist_tp_parser.py part_net_relation.xml
Component reference prefix to check: TP
Processing, please wait ...

================= Summary ======================
                  Total TestPoint : 6
                       Total Nets : 8
             Total connected Nets : 6
                 Unconnected Nets : 2
    Connected Nets with TestPoint : 5
 Connected Nets without TestPoint : 1
               TestPoint coverage : 83.3%

====== Connected Nets without TestPoint ========
Net-(J1-Pad4)

========= 1 TestPoint connected Nets ===========
Net-(J1-Pad1) : TP1
Net-(J1-Pad2) : TP2
Net-(J1-Pad5) : TP4
Net-(J1-Pad6) : TP5

===== More than 1 TestPoint connected Nets =====
Net-(J1-Pad3) : TP3, TP6

=============== Unconnected Nets ===============
unconnected-(J3-Pad1)
unconnected-(J3-Pad2)


```

## Versions

1.0.1 created in August 8, 2022<br>
Last version: https://github.com/Peboli/kicad_netlist_tp_parser  

## Author
Olivier Cornet aka Peboli on Github

## License
This script is [MIT licensed](https://github.com/Peboli/kicad_netlist_tp_parser/blob/main/LICENSE)
