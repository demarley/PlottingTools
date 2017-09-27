"""
8 August 2017
Dan Marley

Plot corrections class for CSCs
"""
import os
import math

from cscTable import CscTable
from cscGroupTable import CscGroupTable

import info
from util import HTML,TeX
import signConventions as sc
from histoFitDraw import HistoFitDraw
from histogrammer import Histogrammer
import geometryXMLparser as gXML
import geometryDiffVisualization as gdv


class PlotCorrectionsCSC(object):
    """Class for plotting corrections in the CSC"""
    def initialize(self,config):
        self.cfg = config

        csc_info = info.csc()
        self.endcaps = csc_info["endcaps"]
        self.disks   = csc_info["disks"]
        self.rings   = csc_info["rings"]

        self.alignmentName  = self.cfg.alignmentName()
        self.referenceName  = self.cfg.referenceName()
        self.correctionName = self.cfg.correctionName()

        self.g_new = gXML.MuonGeometry(self.cfg.xmlfile("new"))
        self.g_ref = gXML.MuonGeometry(self.cfg.xmlfile("reference"))

        # Setup histogrammer
        self.histo = Histogrammer(self.cfg)
        self.histo.initialize()
        self.histo.legend.SetHeader(self.cfg.plotsHeader()) 
            # "CMS 2016X  #sqrt{s} = 13 TeV   L_{int} = X fb^{-1}"

        self.dof      = self.histo.coordinates    # ["x","y","z","phix","phiy","phiz"]
        self.isReport = self.cfg.isReport()

        self.hfd  = HistoFitDraw(config)
        self.html = HTML()
        self.tex  = TeX()

        self.htmlPath = self.cfg.htmlPath()
        self.pngPath  = self.cfg.pngPath()
        self.pdfPath  = self.cfg.pdfPath()
        self.svgPath  = self.cfg.svgPath()
        self.texPath  = self.cfg.texPath()


        self.label = self.alignmentName+" - "+self.referenceName
        self.text  = {'e':"Fit Uncertainties",
                      'p':"Pulls",
                      'd':self.correctionName}

        self.groupTableList = {
          'd':["dxRMS","dyRMS","dzRMS","dphixRMS","dphiyRMS","dphizRMS"],
          'e':["exMean","eyMean","ezMean","ephixMean","ephiyMean","ephizMean"],
          'p':["pxRMS","pyRMS","pzRMS","pphixRMS","pphiyRMS","pphizRMS"]
          }
        self.groupTableListFull = {
          'd':["dxRMS","dxGaussSig","dyRMS","dyGaussSig","dzRMS","dzGaussSig",
               "dphixRMS","dphixGaussSig","dphiyRMS","dphiyGaussSig",
               "dphizRMS","dphizGaussSig"],
          'e':["exMean","exGaussMean","eyMean","eyGaussMean","ezMean","ezGaussMean",
               "ephixMean","ephixGaussMean","ephiyMean","ephiyGaussMean",
               "ephizMean","ephizGaussMean"],
          'p':["pxRMS","pxGaussSig","pyRMS","pyGaussSig","pzRMS","pzGaussSig",
               "pphixRMS","pphixGaussSig","pphiyRMS","pphiyGaussSig",
               "pphizRMS","pphizGaussSig"]
          }

        self.cscGroupTable = CscGroupTable()
        self.setupCscGroupTable()

        self.cscTab = {"d":{"x":CscTable(),"y":CscTable(),"z":CscTable(),
                            "phix":CscTable(),"phiy":CscTable(),"phiz":CscTable()},
                       "e":{"x":CscTable(),"y":CscTable(),"z":CscTable(),
                            "phix":CscTable(),"phiy":CscTable(),"phiz":CscTable()},
                       "p":{"x":CscTable(),"y":CscTable(),"z":CscTable(),
                            "phix":CscTable(),"phiy":CscTable(),"phiz":CscTable()}
                      }

        if self.isReport:
            rep = __import__(self.cfg.reportfile())
               # importlib.import_module(self.cfg.reportfile()) # not available
               # reportfile1 = "Geometries/"+alignmentName+"_report.py"
            self.report = rep.reports()


        return


    def groupTable(self):
        """Return the group table"""
        return self.cscGroupTable


    def fitDrawHists(self,type,dof,histTitle,label):
        """Fit and Draw histograms

        @param type       "d","e","p"
        @param dof
        @param histTitle
        @param label
        """
        h = self.histo.histograms["h_"+type][dof]
        h.SetTitle(histTitle)
        fit = self.hfd.FitAndDraw(h,label,0)
        self.histo.legend.Draw()
 
        pngName = "{0}/CSC_{1}{2}.png".format(self.pngPath,type,dof)
        pdfName = "{0}/CSC_{1}{2}.pdf".format(self.pdfPath,type,dof)
        self.histo.c1.SaveAs( pngName )
        self.histo.c1.SaveAs( pdfName )

        return fit


    def fillHistograms(self,endcap,disk,ring,chamber,rep=None,fillTable=False):
        """
        Fill histograms with some values

        @param rep        report (for errors and pulls)
        @param endcap  
        @param disk
        @param ring
        @param chamber
        @param fillTable  boolean to fill cscTable
        """
        for i,cc in enumerate(self.dof):
            if cc.startswith("phi"):
                cartesian = False
                factor    = 1000.
            else:
                cartesian = True
                factor    = 10.

            g_new = getattr(self.g_new.csc[endcap,disk,ring,chamber],cc)
            g_ref = getattr(self.g_ref.csc[endcap,disk,ring,chamber],cc)

            # correction
            d_mm  = factor
            d_mm *= (g_new - g_ref)
            if cartesian:
                d_mm *= sc.signConventions["CSC",endcap,disk,ring,chamber][i]
            self.histo.histograms["h_d"][cc].Fill(d_mm)
            if fillTable:
                self.cscTab["d"][cc].FillCsc(endcap,disk,ring,chamber,"%.3f" % d_mm)

            # uncertainty & pull
            if rep is not None:
                delta =  getattr(rep,"delta"+cc)
                e_mm  =  factor
                e_mm  *= delta.error
                self.histo.histograms["h_e"][cc].Fill(e_mm)

                if fillTable:
                    self.cscTab["e"][cc].FillCsc(endcap,disk,ring,chamber,"%.3f" % e_mm)

                if fabs(e_mm) > 1e-8:
                    p = d_mm/e_mm
                    self.histo.histograms["h_p"][cc].Fill(p)
                    if fillTable:
                        self.cscTab["p"][cc].FillCsc(endcap,disk,ring,chamber,"%.3f" % p)

        return



    def execute(self):

        self.histo.init_corrections()   # h_d
        self.histo.init_uncertainties() # h_e
        self.histo.init_pulls()         # h_p


        for endcap in self.endcaps:
            sEndcapPorM = "p" if endcap==1 else "m"

            for disk in self.disks:
                diskPrettyName = "__ME%s%s" % (sEndcapPorM,disk)

                imageName = self.alignmentName+"-"+self.referenceName+diskPrettyName
                svgName   = imageName+".svg"

                gdv.draw_disk(self.g_new,self.g_ref,endcap,disk,self.svgPath+svgName,length_factor,angle_factor)

                pngName  = imageName+".png"
                retvalue = os.system("convert -density 104.2 {0} {1}".format(self.svgPath+svgName,self.pngPath+pngName) )


        if self.isReport:
            for r1 in self.report:
                if not (r1.status=="PASS" and r1.postal_address[0]=="CSC" and r1.postal_address[3]!=4):
                    continue
                endcap  = r1.postal_address[1]
                disk    = r1.postal_address[2]
                ring    = r1.postal_address[3]
                chamber = r1.postal_address[4]

                self.fillHistograms( endcap,disk,ring,chamber,rep=r1 )

        else:
            for endcap in self.endcaps:
                for disk in self.disks:
                    rings = self.rings[disk]
                    for ring in rings:
                        chambers = range(1,19) if (disk!=1 and ring==1) else range(1,37)
                        for chamber in chambers:
                            self.fillHistograms( endcap,disk,ring,chamber )

        systemPrettyName = "ME ALL"
        histTitle = systemPrettyName+": {0}"

        for dof in self.dof:
            self.fitDrawHists("d",dof,histTitle.format(self.text["d"],label))

            if self.isReport:

                ### Uncertainties
                self.fitDrawHists("e",dof,histTitle.format(self.text["e"],self.alignmentName))

                ### Pulls
                self.fitDrawHists("p",dof,histTitle.format(self.text["p"],label))

        for endcap in self.endcaps:
            if endcap == 1:
                sEndcapSign = "+"
                sEndcapPorM = "p"
            else:
                sEndcapSign = "-"
                sEndcapPorM = "m"

            for disk in self.disks:
                rings = self.rings[disk]
                for ring in rings:

                    for dof in self.dof:
                        self.histo.histograms["h_d"][dof].Reset("ICESM")
                        self.histo.histograms["h_e"][dof].Reset("ICESM")
                        self.histo.histograms["h_p"][dof].Reset("ICESM")

                    if self.isReport:
                        for r1 in self.report:
                            if not ( r1.status=="PASS" and r1.postal_address[:4]==["CSC",endcap,disk,ring] ):
                                continue
                            chamber  = r1.postal_address[4]
                            self.fillHistograms( endcap,disk,ring,chamber,rep=r1,fillTable=True )
                    else: # if isReport
                        chambers = range(1,19) if (disk!=1 and ring==1) else range(1,37)
                        for chamber in chambers:
                            self.fillHistograms( endcap,disk,ring,chamber,fillTable=True )


                    #****** Corrections: save plots and fill tables over homogeneous chambers ******
                    cscGroupPrettyName = "ME{0}{1}/{2}/ALL".format(sEndcapSign,disk,ring)
                    histTitle   = cscGroupPrettyName+": {0}"
                    pngName = "CSC_{0}{1}_{2}_{3}_{4}.png"
                    pdfName = "CSC_{0}{1}_{2}_{3}_{4}.pdf"

                    for dof in self.dof:
                        pngName_d = pngName.format('d',dof,sEndcapPorM,disk,ring)
                        pdfName_d = pngName.format('d',dof,sEndcapPorM,disk,ring)

                        h = self.histo.histograms["h_d"][dof]
                        h.SetTitle(histTitle.format(self.text['d']))
                        fit = self.hfd.FitAndDraw(h,self.label)
                        self.histo.legend.Draw()

                        self.histo.c1.SaveAs( self.pngPath+"/"+pngName_d )
                        self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_d )

                        sRMS = "%.3f" % h.GetRMS()
                        self.cscGroupTable.FillCscGroup("d{0}RMS".format(dof),endcap,disk,ring,sRMS,self.pngPath+pngName_d)
                        if fit[0]:
                            sSigma = "%.3f" % fit[1].GetParameter(2)
                            self.cscGroupTable.FillCscGroup("d{0}GaussSig".format(dof),endcap,disk,ring,sSigma,self.pngPath+pngName_d)


                    #****** Fit uncert: save plots and fill tables over homogeneous chambers *******
                    #******** Pulls: save plots and fill tables over homogeneous chambers **********

                        if self.isReport:
                            pngName_e = pngName.format('e',dof,sEndcapPorM,disk,ring)
                            pdfName_e = pngName.format('e',dof,sEndcapPorM,disk,ring)

                            ### Uncertainties
                            h = self.histo.histograms["h_e"][dof]
                            h.SetTitle(histTitle.format(self.text['e']))
                            fit = self.hfd.FitAndDraw(h,self.alignmentName)
                            self.histo.legend.Draw()
                            self.histo.c1.SaveAs( self.pngPath+"/"+pngName_e )
                            self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_e )

                            sMean = "%.3f" % h.GetMean()
                            self.cscGroupTable.FillCscGroup("e{0}Mean".format(dof),endcap,disk,ring,sMean,self.pngPath+pngName_e)
                            if fit[0]:
                                sGaussMean = "%.3f" % fit[1].GetParameter(1)
                                self.cscGroupTable.FillCscGroup("e{0}GaussMean".format(dof),endcap,disk,ring,sGaussMean,self.pngPath+pngName_e)

                            pngName_p = pngName.format('p',dof,sEndcapPorM,disk,ring)
                            pdfName_p = pngName.format('p',dof,sEndcapPorM,disk,ring)

                            ### Pulls
                            h = self.histo.histograms["h_p"][dof]
                            h.SetTitle(histTitle.format(self.text['p']))
                            fit = self.hfd.FitAndDraw(h,self.label)
                            self.histo.legend.Draw()
                            self.histo.c1.SaveAs( self.pngPath+"/"+pngName_p )
                            self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_p )

                            sRMS = "%.3f" % h.GetRMS()
                            self.cscGroupTable.FillCscGroup("p{0}RMS".format(dof),endcap,disk,ring,sRMS,self.pngPath+pngName_p)
                            if fit[0]:
                                sSigma = "%.3f" % fit[1].GetParameter(2)
                                self.cscGroupTable.FillCscGroup("p{0}GaussSig".format(dof),endcap,disk,ring,sSigma,self.pngPath+pngName_p)




        #*******************************************************************************
        #                        Auxiliarly output HTML files                           
        #                           1. htmlName_d - file for corrections or biases      
        #                           2. htmlName_e - file for fit uncertainties          
        #                           3. htmlName_p - file for pulls                      
        #*******************************************************************************
        self.writeData("d")

        if self.isReport:
            self.writeData("e")
            self.writeData("p")

        return



    def writeData(self,type):
        """Write data to HTML and TeX files"""
        htmlFile = self.htmlPath
        texFile  = self.texPath

        if type=="e":
            htmlFile += self.htmlName_e
            texFile  += self.texName_e
            label    =  self.alignmentName
            htmlDofString = ["delta;","sigma;<sub>fit</sub>"]
            texDofString  = ["delta","sigma_{fit}"]
        elif type=="p":
            htmlFile += self.htmlName_p
            texFile  += self.texName_p
            label     = self.label
            htmlDofString = ["&delta;",""]
            texDofString  = ["\\delta ",""]
        else:
            htmlFile += self.htmlName_d
            texFile  += self.texName_d
            label     = self.label
            htmlDofString = ["",""]
            texDofString  = ["",""]


        self.html.PrintHtmlHeader(htmlFile)
        self.tex.PrintTexHeader(texFile)

        self.html.PrintHtmlCode(htmlFile,"<font size=\"+2\">{0} for {1}</font>".format(self.text[type],self.alignmentName) )
        self.html.PrintHtmlCode(htmlFile,"<p>")
        self.html.PrintHtmlCode(htmlFile,"<table border=\"1\" cellpadding=\"5\">")

        caption = "<font size=+1>{0}</font> <br><font size=-1>{1}</font>".format(self.text[type],label)

        self.html.PrintHtmlCode(htmlFile,"<caption>{0}</caption>".format(caption))
        self.html.PrintHtmlCode(htmlFile,"<tr align=center>")

        for dof in self.dof: 
            pngName = "CSC_"+type+dof+".png"
            self.html.PrintHtmlCode(htmlFile,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName))
            if dof == "z": self.html.PrintHtmlCode(htmlFile,"</tr><tr align=center>")

        self.html.PrintHtmlCode(htmlFile,"</tr>")
        self.html.PrintHtmlCode(htmlFile,"</table>")

        # Visualization

        self.html.PrintHtmlCode(htmlFile_d,"<p>")
        self.html.PrintHtmlCode(htmlFile_d,"<table border=\"1\" cellpadding=\"5\">")
        caption = ("<font size=+1>Alignment %s visualization</font> <br><font size=-1>" % self.correctionName ) +alignmentName+" - "+referenceName+"</font>"
        self.html.PrintHtmlCode(htmlFile_d,"<caption>%s</caption>" % caption)
        for endcap in 1,2:
            self.html.PrintHtmlCode(htmlFile_d,"<tr align=center>")
            for disk in 1,2,3,4:
                if endcap == 1: diskPrettyName = "__MEp%s" % disk
                else:           diskPrettyName = "__MEm%s" % disk

                imageName = self.alignmentName+"-"+self.referenceName+diskPrettyName
                pngName   = imageName+".png"

                self.html.PrintHtmlCode(htmlFile_d,"<td><a href=\"{0}/{1}\"><img src=\"{0}/{1}\" alt=\"text\" width=\"300\"></a></td>".format(self.pngPath,pngName))
            self.html.PrintHtmlCode(htmlFile_d,"</tr>")
        self.html.PrintHtmlCode(htmlFile_d,"</table>")


        self.html.PrintHtmlCode(htmlFile,"<p>")
        caption2 = "averaged over homogeneous chambers"
        caption  = "<font size=+1>{0} {1}</font> <br><font size=-1>{2}</font>".format(self.text[type],caption2,label)
        self.cscGroupTable.PrintHtml(htmlFile,self.groupTableList['e'],caption,0)

        self.html.PrintHtmlCode(htmlFile,"<p>")
        self.cscGroupTable.PrintHtml(htmlFile,self.groupTableListFull['e'],caption,0)


        #************************ Separate DOF *********************
        for dof in self.dof:

            htmlDof = self.histo.html_names[dof].replace(htmlDofString[0],htmlDofString[1])
            texDof  = self.histo.latex_names[dof].replace(texDofString[0],texDofString[1])
            unitDof = self.histo.units[dof].strip("(").rstrip(")")

            if type=="e":
                htmlCaption = "<font size=+1><{0} <i>{1}</i> ({2})</font> <br><font size=-1><pre>{3}</pre></font>".format(self.text[type],htmlDof,unitDof,label)
                texCaption  = "%s $%s$~(%s) \\\\ {\\tiny \\verb;%s;}" % (self.text[type],texDof, unitDof, label)
                caption     = "<font size=+1><{0} <i>{1}</i> ({2}) in homogeneous chambers</font> <br><font size=-1><pre>{3}</pre></font>".format(self.text[type],htmlDof,unitDof,label)
            elif type=="p":
                htmlCaption = "<font size=+1>{0} for <i>{1}</i></font> <br><font size=-1><pre>{2}</pre></font>".format(self.text[type],htmlDof, label)
                texCaption  = "%s for $%s$ \\\\ {\\tiny \\verb;%s;}" % (self.text[type],htmlDof,label)
                caption     = "{0} for <i>{1}</i> in homogeneous chambers</font> <br><font size=-1><pre>{2}</pre></font>".format(self.text[type],htmlDof,label)
            else:
                htmlCaption = "<font size=+1>%s <i>%s</i> (%s) </font> <br><font size=-1><pre>%s</pre></font>" % (self.text['d'],htmlDof,unitDof,self.label)
                texCaption  = "%s $%s$~(%s) \\\\ {\\tiny \\verb;%s;}" % (self.text[type], texDof, unitDof, label)
                caption     = "<font size=+1>%s <i>%s</i> (%s) in homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>"%(self.text['d'],htmlDof,unitDof,self.label) 



            self.cscTab[type][dof].PrintHtml(htmlFile, htmlCaption, 0)
            self.cscTab[type][dof].PrintTex(texFile,   texCaption, "cscTab_"+type+dof, 0)

            self.html.PrintHtmlCode(htmlFile,"<p>")
            self.html.PrintHtmlCode(htmlFile,"<table border=\"1\" cellpadding=\"5\">")
            self.html.PrintHtmlCode(htmlFile,"<caption>%s</caption>" % caption)
            self.html.PrintHtmlCode(htmlFile,"<tr align=center><th></th><th></th><th><i>Disk {0}</i></th><th><i>Disk {1}</i></th><th><i>Disk {2}</i></th><th><i>Disk {3}</i></th>".format(self.disks[0],self.disks[1],self.disks[2],self.disks[3]))
            for endcap in self.endcaps:
                sEndcapPorM = "p" if endcap==1 else "m"

                for ring in self.rings[1]:
                    self.html.PrintHtmlCode( htmlFile, "<tr align=center>" )

                    if ring == 1:
                        if endcap == 1: self.html.PrintHtmlCode( htmlFile, "<th rowspan=\"3\"><i>ME+</i></th>" )
                        else:           self.html.PrintHtmlCode( htmlFile, "<th rowspan=\"3\"><i>ME-</i></th>" )
                    self.html.PrintHtmlCode( htmlFile, ("<th><i>Ring %s</i></th>" % ring) )

                    for disk in self.disks:
                        pngName = "CSC_%s%s_%s_%s_%s.png" % (type,dof,sEndcapPorM,disk,ring)
                        if disk != 1 and ring == 3:
                            self.html.PrintHtmlCode( htmlFile, "<td>None</td>" )
                        else:
                            self.html.PrintHtmlCode( htmlFile, ("<td><a href=\"{0}/{1}\"><img src=\"{0}/{1}\" alt=\"text\" width=\"250\"></a></td>".format(self.pngPath,pngName)) )
                self.html.PrintHtmlCode(htmlFile,"</tr>")

            self.html.PrintHtmlCode(htmlFile,"</table>")

        self.html.PrintHtmlTrailer(htmlFile)
        self.tex.PrintTexTrailer(htmlFile)

        return


    def setupCscGroupTable(self):
        """Setup the CSC group table"""
        self.cscGroupTable.AddCscGroupVar("dxRMS",         "&delta;x (mm) <br>RMS",                           "$RMS(\\delta x)$",                     "mm")
        self.cscGroupTable.AddCscGroupVar("dxGaussSig",    "&delta;x (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta x)$",         "mm")
        self.cscGroupTable.AddCscGroupVar("dyRMS",         "&delta;y (mm) <br>RMS",                           "$RMS(\\delta y)$",                     "mm")
        self.cscGroupTable.AddCscGroupVar("dyGaussSig",    "&delta;y (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta y)$",         "mm")
        self.cscGroupTable.AddCscGroupVar("dzRMS",         "&delta;z (mm) <br>RMS",                           "$RMS(\\delta z)$",                     "mm")
        self.cscGroupTable.AddCscGroupVar("dzGaussSig",    "&delta;z (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta z)$",         "mm")
        self.cscGroupTable.AddCscGroupVar("dphixRMS",      "&delta;&phi;<sub>x</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{x})$",             "mrad")
        self.cscGroupTable.AddCscGroupVar("dphixGaussSig", "&delta;&phi;<sub>x</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{x})$", "mrad")
        self.cscGroupTable.AddCscGroupVar("dphiyRMS",      "&delta;&phi;<sub>y</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{y})$",             "mrad")
        self.cscGroupTable.AddCscGroupVar("dphiyGaussSig", "&delta;&phi;<sub>y</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{y})$", "mrad")
        self.cscGroupTable.AddCscGroupVar("dphizRMS",      "&delta;&phi;<sub>z</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{z})$",             "mrad")
        self.cscGroupTable.AddCscGroupVar("dphizGaussSig", "&delta;&phi;<sub>z</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{z})$", "mrad")

        self.cscGroupTable.AddCscGroupVar("exMean",         "&sigma;<sub>fit</sub>x (mm) <br>Mean",                         "$Mean(\\sigma_{fit} x) $",               "mm")
        self.cscGroupTable.AddCscGroupVar("exGaussMean",    "&sigma;<sub>fit</sub>x (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} x) $",       "mm")
        self.cscGroupTable.AddCscGroupVar("eyMean",         "&sigma;<sub>fit</sub>y (mm) <br>Mean",                         "$Mean(\\sigma_{fit} y) $",               "mm")
        self.cscGroupTable.AddCscGroupVar("eyGaussMean",    "&sigma;<sub>fit</sub>y (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} y) $",       "mm")
        self.cscGroupTable.AddCscGroupVar("ezMean",         "&sigma;<sub>fit</sub>z (mm) <br>Mean",                         "$Mean(\\sigma_{fit} z) $",               "mm")
        self.cscGroupTable.AddCscGroupVar("ezGaussMean",    "&sigma;<sub>fit</sub>z (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} z) $",       "mm")
        self.cscGroupTable.AddCscGroupVar("ephixMean",      "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_x) $",         "mrad")
        self.cscGroupTable.AddCscGroupVar("ephixGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_x) $", "mrad")
        self.cscGroupTable.AddCscGroupVar("ephiyMean",      "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_y) $",         "mrad")
        self.cscGroupTable.AddCscGroupVar("ephiyGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_y) $", "mrad")
        self.cscGroupTable.AddCscGroupVar("ephizMean",      "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_z) $",         "mrad")
        self.cscGroupTable.AddCscGroupVar("ephizGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_z) $", "mrad")

        self.cscGroupTable.AddCscGroupVar("pxRMS","x pull <br>RMS",                                 "$RMS(P x)$",                     None)
        self.cscGroupTable.AddCscGroupVar("pxGaussSig","x pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P x)$",         None)
        self.cscGroupTable.AddCscGroupVar("pyRMS","y pull <br>RMS",                                 "$RMS(P y)$",                     None)
        self.cscGroupTable.AddCscGroupVar("pyGaussSig","y pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P y)$",         None)
        self.cscGroupTable.AddCscGroupVar("pzRMS","z pull <br>RMS",                                 "$RMS(P z)$",                     None)
        self.cscGroupTable.AddCscGroupVar("pzGaussSig","z pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P z)$",         None)
        self.cscGroupTable.AddCscGroupVar("pphixRMS","&phi;<sub>x</sub> pull <br>RMS",              "$RMS(P \\phi_{x})$",             None)
        self.cscGroupTable.AddCscGroupVar("pphixGaussSig","&phi;<sub>x</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{x})$", None)
        self.cscGroupTable.AddCscGroupVar("pphiyRMS","&phi;<sub>y</sub> pull <br>RMS",              "$RMS(P \\phi_{y})$",             None)
        self.cscGroupTable.AddCscGroupVar("pphiyGaussSig","&phi;<sub>y</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{y})$", None)
        self.cscGroupTable.AddCscGroupVar("pphizRMS","&phi;<sub>z</sub> pull <br>RMS",              "$RMS(P \\phi_{z})$",             None)
        self.cscGroupTable.AddCscGroupVar("pphizGaussSig","&phi;<sub>z</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{z})$", None)

        return




## THE END ##
