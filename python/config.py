"""
Created:       2 August    2017
Last Updated: 26 September 2017

Dan Marley
daniel.edison.marley@cernSPAMNOT.ch
Texas A&M University
Fermi National Accelerator Laboratory
-----

Configuration class for getting/setting parameters
to use in the alignment.
"""
import os
import sys
import util
from copy import deepcopy



class Config(object):
    """Configuration object that handles the setup"""
    def __init__(self,configfile,script='createJobs.py',verbose_level="INFO"):
        self.filename = configfile

        self.vb = util.VERBOSE()
        self.vb.level = verbose_level
        self.vb.name  = "CONFIG"

        self.configuration = {}      # hold all values in dictionary (as strings)
        self.script        = script  # the script that calls this class (e..g, createJobs.py)

        self.set_defaults()


    def initialize(self):
        """Initialize the configuration"""
        self.setConfigurations()     # set the configuration options


        self.xmlfile = {"reference":self.get("xmlfile_ref"),
                        "new":self.get("xmlfile_new")}
        
        # Setup paths
        self.htmlPath = self.config.folderName()
        if not os.path.exists(self.htmlPath):
             os.makedirs(self.htmlPath)

        self.texPath = self.htmlPath+"/TEX/"
        if not os.path.exists(self.texPath):
             os.makedirs(self.texPath)

        self.pngPath = self.htmlPath+"/PNG/"
        if not os.path.exists(self.pngPath):
             os.makedirs(self.pngPath)

        self.pdfPath = self.htmlPath+"/PDF/"
        if not os.path.exists(self.pdfPath):
             os.makedirs(self.pdfPath)

        self.svgPath = self.htmlPath+"/SVG/"
        if not os.path.exists(self.svgPath):
             os.makedirs(self.svgPath)

        return


    def setConfigurations(self):
        """Read the configuration file and set arguments"""
        file = open(self.filename,'r').readlines()
        for line in file:
            param,value = line.split(' ')
            value       = value.rstrip('\n')

            self.configuration[param] = value

        return


    def get(self,param):
        """Return values of the configuration to the user"""
        value = None

        try:
            value = self.configuration[param]
        except KeyError:
            self.vb.WARNING("The configuration file does not contain {0}".format(param))
            self.vb.WARNING("Using default value.")
            try:
                value = self.defaults[param]
            except KeyError:
                raise KeyError("There is no default value for {0}.\n"
                               "Please set this parameter in the configuration file.".format(param))

        return value


    def set_defaults(self):
        """Set default values for configurations"""
        self.defaults = {
			'alignmentName':"",
			'xmlfile_ref':"",
			'xmlfile_new':"",
			'referenceName':"IDEAL_Geo",
			'correctionName':"Displacements from ideal geometry",
			'runComparison':"False",
			'uploadComparison':"False",
			'runCorrelation':"False",
			'printCorrelationFactors':"False",
            'doCSC':"False", 
            'doDT':"False", 
			'isReport':"False",
			'plotsHeader':r"CMS 2016X  #sqrt{s} = 13 TeV   L_{int} = X fb^{-1}",
			'corrections_bins':{"bins":200,"min":-10,"max":10.0},
			'uncertainties_bins':{"bins": 50,"min":  0,"max": 0.5},
			'pulls_bins':{"bins":100,"min":-10,"max":10.0},
			'folderName':'',
			'htmlPath':'.',
			'texPath':'.',
			'pngPath':'.',
			'pdfPath':'.',
			'svgPath':'.',
		}

        self.configuration = deepcopy(self.defaults)

        return



    def verbose_level(self):
        """Verbosity of output"""
        return self.get("verbose_level")

    def doCSC(self):
        """Process the CSC endcap chambers"""
        return util.str2bool( self.get("doCSC") )

    def doDT(self):
        """if invoked, DT barrel chambers would not be processed"""
        return util.str2bool( self.get("doDT") )

    def corrections_binning(self):
        """Return the binning for correction histograms"""
        return self.get("corrections_bins")

    def uncertainties_binning(self):
        """Return the binning for correction histograms"""
        return self.get("corrections_bins")

    def pulls_binning(self):
        """Return the binning for correction histograms"""
        return self.get("corrections_bins")

    def xmlfile(self,type):
        """Obtain the XML file for different geometries"""
        return self.xmlfile(type)

    def __str__(self):
        """Specialized print statement for this class"""
        command = """ Track-Based Muon Alignment : Configuration

./%(prog)s <configuration>

Creates (overwrites) a directory for each of the iterations and creates (overwrites)
'submitJobs.sh' with the submission sequence and dependencies.
""" % {'prog': self.source}

        keys = configuration.keys()
        keys.sort()
        max_len = max( len(i) for i in keys )+2


        for i in keys:
            neededlength = max_len-len(i)
            whitespace   = ' '*neededlength

            try:
                command+="   ** {0}{1}= {2:.4f}\n".format(i,whitespace,self.__dict__[i])
            except ValueError:
                continue

        return command


## THE END ##