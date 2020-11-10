import sys
import ROOT
import math
import array
import argparse
import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)

parser = argparse.ArgumentParser() #basically this section allows us to set command line prompts and inputs, here the files we want to interact with.
parser.add_argument('--input', action='store', default="input.txt") #example, this specifies a new command line command --input [] where instead of brackets we place the input file of our choosing.
parser.add_argument('--inputTree', action='store', default="allev/hftree") # the other 2 bits store parts of those files
parser.add_argument('--background', action='store', default="background.txt")
parser.add_argument('--backgroundTree', action='store', default="allev/hftree")
parser.add_argument('--background2', action='store', default="background2.txt")
parser.add_argument('--backgroundTree2', action='store', default="allev/hftree")
parser.add_argument('--output', action='store', default="hist.root")
parser.add_argument('--lumi',action='store', default=1000.) # 1 fb-1
parser.add_argument('--debug',action='store_true')
args=parser.parse_args()




chain = ROOT.TChain(args.inputTree) #these chains allow us to run over the values in our Ttrees, which is where the data is stored, each file gets a tree, which contains all the information
chain2 = ROOT.TChain(args.backgroundTree) ##create second and third chain analysis for background info
chain3 = ROOT.TChain(args.backgroundTree2)

if ( args.input[-4:] == 'root' ):  #input file loop to be compared
	print ( "Running over single root file:" )
	print ( "   > %s" % args.input )
	chain.Add(args.input) #the meat of the loop, put all the input arguments into a the chain.
else:
	print ( "Running over list of root files:" )
	for line in open(args.input):
		print ("   > " + line.rstrip('\n'))
		chain.Add(line.rstrip('\n'))

if ( args.background[-4:] == 'root' ):   ##iteration for background file 1
	print ( "Running over single root file:" )
	print ( "   > %s" % args.background )
	chain2.Add(args.background)
else:
	print ( "Running over list of root files:" )
	for line in open(args.background):
		print ("   > " + line.rstrip('\n'))
		chain2.Add(line.rstrip('\n'))
	
if ( args.background2[-4:] == 'root' ):   ##iteration for background file 2
	print ( "Running over single root file:" )
	print ( "   > %s" % args.background2 )
	chain3.Add(args.background2)
else:
	print ( "Running over list of root files:" )
	for line in open(args.background2):
		print ("   > " + line.rstrip('\n'))
		chain3.Add(line.rstrip('\n'))
	
numFiles=chain.GetNtrees()  
numFiles2=chain2.GetNtrees()
numFiles3=chain3.GetNtrees()
print ( "Loaded %s chains..." % numFiles )

# Prevent the canvas from displaying
ROOT.gROOT.SetBatch(True)

# a histogram for our output
outfile=ROOT.TFile.Open(args.output,"RECREATE")




# make a histogram

### Loop through all events in chain
h_MET = []
h_weight = []

b_MET1 = []
b_weight1 = []

b_MET2 = []
b_weight2 = []

h_jPT = []
h_weightj = []

b_jPT1 = []
b_weight3 = []

b_jPT2 = []
b_weight4 = []
###Loops for MET (Missing Transverse Energy) and filling those histograms.
entry = 0
for event in chain:
	entry += 1

	if ( entry != 0 and entry%10000 == 0 ):	
		print ("%d events processed" % entry)
		sys.stdout.flush()

  # this is how we know how much this event "counts" when looking at large collections of events.
	weight=event.weight/numFiles

  # missing transverse energy (MET)
	MET=event.MET #to make a new event to analyze, simply add a new variable and call for event.[insert variable here]
	jPT=event.j1PT

  # require event to have some properties.
	if event.mjj > 100:
	# if the event passes, fill the histogram.
		h_MET.append(MET)
		h_weight.append(weight)
		h_jPT.append(jPT)
		h_weightj.append(weight)


entry2 = 0
for event2 in chain2:
	entry2 += 1 

	if ( entry2 != 0 and entry2%10000 == 0 ):
		print ("%d events processed" % entry2)
		sys.stdout.flush()

  # this is how we know how much this event "counts" when looking at large collections of events.
	weight2=event2.weight/numFiles2

  # missing transverse energy (MET)
	bMET1=event2.MET
	bjPT1=event2.j1PT

  # require event to have some properties.
	if event2.mjj > 100:
	# if the event passes, fill the histogram.
		b_MET1.append(bMET1)
		b_weight1.append(weight2)
		b_jPT1.append(bjPT1)
		b_weight3.append(weight2)

	
entry3 = 0
for event3 in chain3:
	entry3 += 1

	if ( entry3 != 0 and entry3%10000 == 0 ):
		print ("%d events processed" % entry3)
		sys.stdout.flush()

  # this is how we know how much this event "counts" when looking at large collections of events.
	weight3=event3.weight/numFiles3

  # missing transverse energy (MET)
	bMET2=event3.MET
	bjPT2=event3.j1PT

  # require event to have some properties.
	if event3.mjj > 100:
	# if the event passes, fill the histogram.
		b_MET2.append(bMET2)
		b_weight2.append(weight3)
		b_jPT2.append(bjPT2)
		b_weight4.append(weight3)
	



Backgroundsum = b_MET1+b_MET2 
Backweight = b_weight1+b_weight2

Backgroundsum2 = b_jPT1+b_jPT2
Backweight2 = b_weight3+b_weight4


outfile.Close()
  
print ("Done!")

class DisplayControl(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)

		
		tk.Tk.wm_title(self, "ROOT file's output")
		
		
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

		
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self, text="Navigation Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button = ttk.Button(self, text="Visit Background Sum",
							command=lambda: controller.show_frame(PageOne))
		button.pack()

		button2 = ttk.Button(self, text="Visit Missing Transverse Energy",
							command=lambda: controller.show_frame(PageTwo))
		button2.pack()

		button3 = ttk.Button(self, text="Graph Jet Background",
							command=lambda: controller.show_frame(PageThree))
		button3.pack()

		button4 = ttk.Button(self, text="JPT comparison", command=lambda: controller.show_frame(PageFour))
		button4.pack()


class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Background Sum", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text="Back to Main",
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Missing Transverse Energy",
							command=lambda: controller.show_frame(PageTwo))
		button2.pack()

		button3 = ttk.Button(self, text="Graph Jet Background",
							command=lambda: controller.show_frame(PageThree))
		button3.pack()

		button4 = ttk.Button(self, text="JPT comparison", command=lambda: controller.show_frame(PageFour))
		button4.pack()

		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_axes([0.1,0.1,0.8,0.8])

		a.hist(np.array(b_MET2), weights=np.array(b_weight2),color="Green", label='Background: MET2', alpha=0.5,bins=100)
		a.hist(np.array(b_MET1), weights=np.array(b_weight1),color="Red", label='Background: MET1', alpha=0.5,bins=100)
		a.hist(np.array(Backgroundsum), color="Orange", label='Backgroundsum', alpha=0.5,bins=100, weights=np.array(Backweight))
		
		a.legend()
		a.semilogy()
		a.set_xlim(0,600)
		

		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Missing Transverse Energy", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text="Back to Main",
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Background Sum",
							command=lambda: controller.show_frame(PageOne))
		button2.pack()

		button3 = ttk.Button(self, text="Graph Jet Background",
							command=lambda: controller.show_frame(PageThree))
		button3.pack()

		button4 = ttk.Button(self, text="JPT comparison", command=lambda: controller.show_frame(PageFour))
		button4.pack()

		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_axes([0.1,0.1,0.8,0.8])


		a.hist(np.array(h_MET), color="Red", label='h_MET', weights=np.array(h_weight), alpha=0.5,bins=100)
		a.hist(np.array(Backgroundsum), color="Orange", label='Background sum: MET', alpha=0.5,bins=100, weights=np.array(Backweight))
		a.legend()
		a.semilogy()
		a.set_xlim(0,600)

		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Jet Background", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text="Back to Main",
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button2 = ttk.Button(self, text="Background Sum",
							command=lambda: controller.show_frame(PageOne))
		button2.pack()

		button3 = ttk.Button(self, text="Missing Transverse Energy",
							command=lambda: controller.show_frame(PageTwo))
		button3.pack()

		button4 = ttk.Button(self, text="JPT comparison", command=lambda: controller.show_frame(PageFour))
		button4.pack()

		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_axes([0.1,0.1,0.8,0.8])



		a.hist(np.array(Backgroundsum2), color="Orange", label='Backgroundsum: jPT', alpha=0.5,bins=100, weights = np.array(Backweight2))
		a.hist(np.array(b_jPT2), color="Green", label='Background jPT2', weights=np.array(b_weight4), alpha=0.5,bins=100)
		a.hist(np.array(b_jPT1), color="Red", label='Background jPT1', weights=np.array(b_weight3), alpha=0.5,bins=100)
		a.legend()
		a.semilogy()
		a.set_xlim(0,600)		

		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class PageFour(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="JPT comparison", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = ttk.Button(self, text="Back to Main",
							command=lambda: controller.show_frame(StartPage))
		button1.pack()

		button = ttk.Button(self, text="Visit Background Sum",
							command=lambda: controller.show_frame(PageOne))
		button.pack()

		button2 = ttk.Button(self, text="Visit Missing Transverse Energy",
							command=lambda: controller.show_frame(PageTwo))
		button2.pack()

		button3 = ttk.Button(self, text="Graph Jet Background",
							command=lambda: controller.show_frame(PageThree))
		button3.pack()


		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_axes([0.1,0.1,0.8,0.8])

		

		a.hist(np.array(Backgroundsum2), color="Orange", label='Backgroundsum: jPT', alpha=0.5,bins=100, weights=np.array(Backweight2))
		a.hist(np.array(h_jPT), color="Red", label='h_jPT', weights=np.array(h_weightj), alpha=0.5,bins=100) 
		a.legend()    
		a.semilogy() 
		a.set_xlim(0,600)

		canvas = FigureCanvasTkAgg(f, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

		

app = DisplayControl()
app.mainloop()