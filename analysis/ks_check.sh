#!/bin/bash
grep -rn 'DIRECT_MAP_BASE\|DIRECT_MAP_END\|VMEMMAP' /mnt/d/opporoot/exploit/src/ | grep -v kernelsnitch | head -20
