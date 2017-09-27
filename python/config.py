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
    def __init__(self,configfile,script='runPlotting.py',verbose_level="INFO"):
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


        self.xmlfiles = {"reference":self.get("xmlfile_ref"),
                         "new":self.get("xmlfile_new")}
        
        # Setup paths
        htmlPath = self.get('folderName')+"/RESULT/{0}".format(self.get('alignmentName'))
        if not os.path.exists(htmlPath):
             os.makedirs(htmlPath)

        texPath = htmlPath+"/TEX/"
        if not os.path.exists(texPath):
             os.makedirs(texPath)

        pngPath = htmlPath+"/PNG/"
        if not os.path.exists(pngPath):
             os.makedirs(pngPath)

        pdfPath = htmlPath+"/PDF/"
        if not os.path.exists(pdfPath):
             os.makedirs(pdfPath)

        svgPath = htmlPath+"/SVG/"
        if not os.path.exists(svgPath):
             os.makedirs(svgPath)

        self.configuration['htmlPath'] = htmlPath
        self.configuration['texPath']  = texPath
        self.configuration['pngPath']  = pngPath
        self.configuration['pdfPath']  = pdfPath
        self.configuration['svgPath']  = svgPath

        self.configuration['reportfile'] = "Geometries/{0}_report.py".format(self.get('alignmentName'))

        return


    def setConfigurations(self):
        """Read the configuration file and set arguments"""
        file = open(self.filename,'r').readlines()
        for line in file:
            params = line.split(' ')
            param  = params[0]
            value  = " ".join(params[1:]).rstrip('\n')

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
			'folderName':os.getcwd(),
                        'reportfile':"Geometries/report.py",
			'htmlPath':'.',
			'texPath':'.',
			'pngPath':'.',
			'pdfPath':'.',
			'svgPath':'.',
                        'verbose_level':self.vb.level,
                        'summaryTable':["dxRMS","dyRMS","dzRMS","dphixRMS","dphiyRMS","dphizRMS"],
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
        return self.xmlfiles[type]

    def alignmentName(self):
        """Alignment name"""
        return self.get('alignmentName')

    def referenceName(self):
        """Reference name"""
        return self.get('referenceName')

    def correctionName(self):
        """Correction name"""
        return self.get('correctionName')

    def isReport(self):
        """Report"""
        return util.str2bool(self.get('isReport'))

    def reportfile(self):
        """Report file"""
        return self.get('reportfile')

    def plotsHeader(self):
        """Plot header"""
        return self.get('plotsHeader')

    def htmlPath(self):
        """HTML path"""
        return self.get("htmlPath")

    def texPath(self):
        """TEX path"""
        return self.get("texPath")

    def pngPath(self):
        """PNG path"""
        return self.get("pngPath")

    def pdfPath(self):
        """PDF path"""
        return self.get("pdfPath")

    def svgPath(self):
        """SVG path"""
        return self.get("svgPath")

    def summaryTable(self):
        """Summary table"""
        return self.get("summaryTable")

    def __str__(self):
        """Specialized print statement for this class"""
        command = """ Track-Based Muon Alignment : Plotting Scripts Configuration

python python/%(prog)s <configuration>

Plot results from alignment.
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
