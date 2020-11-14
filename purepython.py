#!/usr/bin/env python

import sys
import math
import array
import argparse
import os
import matplotlib.pyplot as plt 
import numpy as np 
import boost_histogram as bh 
import uproot

parser = argparse.ArgumentParser()
parser.add_argument('--input', action='store', default="input.txt")
parser.add_argument('--background', action='store', default="input.txt")
parser.add_argument('--background2', action='store', default="input.txt")
parser.add_argument('--inputTree', action='store', default="allev/hftree")
parser.add_argument('--output', action='store', default="hist.root")
parser.add_argument('--lumi',action='store', default=1000.) # 1 fb-1
parser.add_argument('--debug',action='store_true')
args=parser.parse_args()



root = uproot.open(args.input)['allev/hftree']

background = uproot.open(args.background)['allev/hftree']

background2 = uproot.open(args.background2)['allev/hftree']


a = root.array(args.inputTree)
b = background.array(args.inputTree)
c = background2.array(args.inputTree)

plt.hist(b, bins=100, color = 'green', label='background1', alpha=0.5)
plt.hist(c, bins=100, color = 'red', label='background2', alpha=0.5)
plt.hist(a, bins=100, color = 'blue', label='signal', alpha=0.5)
plt.legend()
plt.show()




