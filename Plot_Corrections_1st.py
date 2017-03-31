import ROOT, array, os, sys, re, math, random
from math import *
k = sqrt(2.0)

execfile("geometryXMLparser.py")
execfile("plotscripts.py")
execfile("tdrStyle.py")

from Class_DtTable import *
from Class_DtGroupTable import *
from Class_CscTable import *
from Class_CscGroupTable import *

from Histo_FitAndDraw import *

try:  
   alignmentName = os.environ["alignmentName"]
except KeyError: 
   print "Error! Please set the environment variable 'alignmentName'"
   sys.exit(-1)

print "Process", alignmentName

isDT, isCSC = False, False
