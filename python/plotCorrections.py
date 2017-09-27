"""
7 August 2017
Dan Marley

Plot corrections class
- combination of original `Plot_Corrections_1st.py` and `Plot_corrections_2nd.py`
"""
import os
import sys
import math
import ROOT

import util
import tdrStyle
import plotscripts
import geometryXMLparser as gXML

from dtGroupTable import DtGroupTable
from cscGroupTable import CscGroupTable

from plotCorrectionsCSC import PlotCorrectionsCSC
from plotCorrectionsDT import PlotCorrectionsDT

### FIRST


class PlotCorrections(object):
    """Plot corrections"""
    def __init__(self,cfg):
        self.config = cfg

        self.vb = util.VERBOSE()
        self.vb.level = cfg.verbose_level()
        self.vb.name  = "PLOTCORRECTIONS"  # simple name of this script to recognize the output

        self.alignmentName  = self.config.alignmentName()
        self.referenceName  = self.config.referenceName()
        self.correctionName = self.config.correctionName()

        self.isDT  = self.config.doDT()
        self.isCSC = self.config.doCSC()

        if (not self.isDT and not self.isCSC) or (self.isDT and self.isCSC):
            self.vb.ERROR("DT and CSC set to same value.  Set only one option to 'true'")
            sys.exit(-1)

        self.html = util.HTML()


    def execute(self):
        """Execute code"""
        # what does this do?
        g_new = gXML.MuonGeometry(self.config.xmlfile("new"))
        g_ref = gXML.MuonGeometry(self.config.xmlfile("reference"))

        #*******************************************************************************
        #                           Main output HTML file                               
        #*******************************************************************************
        htmlPath   = self.config.htmlPath()
        htmlName   = "index.html"
        htmlName_d = self.alignmentName+".d.html" # file for correction

        texPath    = self.config.texPath()
        texName    = self.alignmentName+".tex"
        texName_d  = self.alignmentName+".d.tex"  # file for correction

        if self.config.isReport():
            htmlName_e = self.alignmentName+".e.html"  # html file for uncertainties
            htmlName_p = self.alignmentName+".p.html"  # html file for pulls
            texName_e  = self.alignmentName+".e.tex"   # tex file for uncertainties
            texName_p  = self.alignmentName+".p.tex"   # tex file for pulls

        ## Do the plotting 
        if self.isCSC:
            plt_csc = PlotCorrectionsCSC()
            plt_csc.initialize(self.config)
            plt_csc.execute( ) # pass necessary arguments
            groupTable = plt_csc.groupTable()
        else:
            plt_dt = PlotCorrectionsDT()
            plt_dt.initialize(self.config)
            plt_dt.execute( )  # pass necessary arguments
            groupTable = plt_dt.groupTable()

        summaryTable       = self.config.summaryTable()
        summaryHtmlCaption = "<font size=+1>%s (<i>&delta;</i>) for all DOF <br>averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (self.correctionName, self.alignmentName+" - "+self.referenceName)

        texFile = texPath+texName
        groupTable.PrintTex(texFile,summaryTable, ("Summary table %s" % self.alignmentName), ("tab:summary_%s" % self.alignmentName), 1)

        htmlFile = htmlPath+htmlName
        self.html.PrintHtmlHeader(htmlFile)
        self.html.PrintHtmlCode(htmlFile,"<font size=\"+2\">Summary for %s</font>" % self.alignmentName)
        self.html.PrintHtmlCode(htmlFile,"<p>")

        groupTable.PrintHtml(htmlFile,summaryTable,summaryHtmlCaption,0)

        self.html.PrintHtmlCode(htmlFile,"<p><hr width=\"100%\">")
        self.html.PrintHtmlCode(htmlFile,"<p>Additional information:<ul>")
        self.html.PrintHtmlCode(htmlFile,"<li><a href=\"%s\">%s</a></li>" % (htmlName_d,self.correctionName) )

        if self.config.isReport():
            self.html.PrintHtmlCode(htmlFile,"<li><a href=\"%s\">Alignment fit uncertainties</a></li>" % (htmlName_e) )
            self.html.PrintHtmlCode(htmlFile,"<li><a href=\"%s\">Pulls</a></li>" % (htmlName_p) )

        self.html.PrintHtmlTrailer(htmlFile)

        return


## THE END ##
