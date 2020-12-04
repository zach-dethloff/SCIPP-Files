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

signal = uproot.open(args.input)[args.inputTree]

val = signal.arrays()

mjj_mask = val[b'mjj']>1000

MET_mask = val[b'MET']>200

JET_mask = val[b'njet']>2

Elec_mask = val[b'nElec']==0

Muon_mask = val[b'nMuon']==0

background = uproot.open(args.background)[args.inputTree]

b1 = background.arrays()

bmjj_mask = b1[b'mjj']>1000

bMET_mask = b1[b'MET']>200

bJET_mask = b1[b'njet']>2

bElec_mask = b1[b'nElec']==0

bMuon_mask = b1[b'nMuon']==0

background2 = uproot.open(args.background2)[args.inputTree]

b2 = background2.arrays()

b2mjj_mask = b2[b'mjj']>1000

b2MET_mask = b2[b'MET']>200

b2JET_mask = b2[b'njet']>2

b2Elec_mask = b2[b'nElec']==0

b2Muon_mask = b2[b'nMuon']==0

back_mask = bmjj_mask & bMET_mask & bJET_mask & bElec_mask & bMuon_mask

big_mask = mjj_mask & MET_mask & JET_mask & Elec_mask & Muon_mask

back2_mask = b2mjj_mask & b2MET_mask & b2JET_mask & b2Elec_mask & b2Muon_mask

MET_val = val[b'MET'][big_mask]

back_val = b1[b'MET'][back_mask]

back2_val = b2[b'MET'][back2_mask]

backsum = np.append(back_val, back2_val)

backweights = np.append(b1[b'weight'][back_mask], b2[b'weight'][back2_mask])

plt.hist(MET_val, bins=100, range=(200,600),
	color='g', label='Signal MET', alpha = 0.5,
	weights=val[b'weight'][big_mask])
plt.hist(back_val, bins=100, range=(200,600),
	color = 'r', label='Background MET', alpha=0.5,
	weights=b1[b'weight'][back_mask])
plt.hist(back2_val, bins=100, range=(200,600),
	color = 'b', label = 'Background MET 2',alpha=0.5,
	weights=b2[b'weight'][back2_mask])
plt.hist(backsum, bins = 100, range=(200,600), 
	color='orange', label = 'Background MET sum', alpha = 0.5,
	weights = backweights)
plt.title('MET')
plt.yscale('log')
plt.legend()
plt.show()