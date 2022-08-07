# KICAD xml Netlist parser

## Description

This script has been developped following a request by user 'xzf16' on the [Kicad forum](https://forum.kicad.info/t/could-anyone-have-a-python-script-to-export-the-relationship-between-net-and-test-point/37024).<br>
The purpose of this script is to check if every net have a testpoint connected to it.

## Environnement
 * Run on Python >=3.5
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
> python netlist_tp_parser.py Example.xml

Component reference prefix to check: TP
Processing, please wait ...
Found 75 tests points
No test point connected to net 'Net-(R406-Pad1)'
No test point connected to net 'Net-(R407-Pad1)'
No test point connected to net 'unconnected-(J401-Pad4)'
No test point connected to net 'unconnected-(U201-Pad3)'
No test point connected to net 'unconnected-(U201-Pad7)'
```

## Versions

1.0.0 created in : August 2022<br>
Last version: https://github.com/Peboli/kicad_netlist_tp_parser  

## Authors
Olivier Cornet aka Peboli on Githib

## License
This script is MIT licensed