# Python SBT-based testing tool

## Requirements
Python 3.8

## Installation
1. Download the repository
2. From top directory, execute following command to install Python package dependencies.
`pip3 install -r requirements.txt`

## Usage
From the top directory, execute the tool by command `python3 covgen.py <target python file path>`.
Note that `inputs` directory already contains sample python source codes.
Output of the tool can also be access in `outputs` directory, written at `<target filename>.txt`.

## Explanation
The tool first scans all if-else branches to collect conditionals that they perform.
Then, with initial domain as (-INF, INF) for each arguments, partition the domain by each conditionals.
Finally, draw random inputs from possible cases of domains.

Detailed explanation in in the report.