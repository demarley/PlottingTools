"""
25 September 2017
Dan Marley

Plot corrections class for DTs
"""
import os
import operator
import importlib

from dtTable import DtTable
from dtGroupTable import dtGroupTable

import info
from util import HTML,TeX
from histoFitDraw import HistoFitDraw
from histogrammer import Hisogrammer
import geometryDiffVisualization as gdv
import signConventions as sc


class PlotCorrectionsDT(object):
    """Class for plotting corrections in the DT"""
    def initialize(self,config):
        self.cfg = config

        dt_info = info.dt()
        self.wheels   = dt_info["wheels"]
        self.stations = dt_info["stations"]
        self.sectors  = dt_info["sectors"]
        self.sectors4 = dt_info["sectors4"]

        self.alignmentName  = self.cfg.alignmentName()
        self.referenceName  = self.cfg.referenceName()
        self.correctionName = self.cfg.correctionName()

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

        self.pngPath  = self.cfg.pngPath()
        self.pdfPath  = self.cfg.pdfPath()
        self.svgPath  = self.cfg.svgPath()
        self.htmlPath = self.cfg.htmlPath()
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
               "dphizRMS","dphizGaussSig"]
          'e':["exMean","exGaussMean","eyMean","eyGaussMean","ezMean","ezGaussMean",
               "ephixMean","ephixGaussMean","ephiyMean","ephiyGaussMean",
               "ephizMean","ephizGaussMean"],
          'p':["pxRMS","pxGaussSig","pyRMS","pyGaussSig","pzRMS","pzGaussSig",
               "pphixRMS","pphixGaussSig","pphiyRMS","pphiyGaussSig",
               "pphizRMS","pphizGaussSig"]
          }

        self.dtGroupTable = dtGroupTable()
        self.setupDtGroupTable()

        self.dtTab = {"d":{"x":DtTable(),"y":DtTable(),"z":DtTable(),
                            "phix":DtTable(),"phiy":DtTable(),"phiz":DtTable()},
                       "e":{"x":DtTable(),"y":DtTable(),"z":DtTable(),
                            "phix":DtTable(),"phiy":DtTable(),"phiz":DtTable()},
                       "p":{"x":DtTable(),"y":DtTable(),"z":DtTable(),
                            "phix":DtTable(),"phiy":DtTable(),"phiz":DtTable()}
                      }

		self.map_ID_Diff = {"x":{},   "y":{},   "z":{},
                            "phix":{},"phiy":{},"phiz":{}}

        if self.isReport:
            rep = importlib.import_module(self.config.reportfile())
               # reportfile1 = "Geometries/"+alignmentName+"_report.py"
            self.report = rep.reports()

        return



    def fitDrawHists(self,type,dof,histTitle,label):
        """Fit and Draw histograms

        @param type       "d","e","p"
        @param dof        x,y,z,phix,phiy,phiz
        @param histTitle
        @param label
        """
        h = self.histo.histograms["h_"+type][dof]
        h.SetTitle(histTitle)
        fit = self.hfd.FitAndDraw(h,label,0)
        self.histo.legend.Draw()
 
        pngName = "{0}/DT_{1}{2}.png".format(self.pngPath,type,dof)
        pdfName = "{0}/DT_{1}{2}.pdf".format(self.pdfPath,type,dof)
        self.histo.c1.SaveAs( pngName )
        self.histo.c1.SaveAs( pdfName )

        return fit


    def fillHistograms(self,wheel,station,sector,rep=None,fillTable=False):
        """
        Fill histograms with some values

        @param rep        report (for errors and pulls)
        @param wheel  
        @param station
        @param sector
        @param fillTable  boolean to fill dtTable
        """
        for i,cc in enumerate(self.dof):
            if cc.startswith("phi"):
                factor    = 1000.
            else:
                factor    = 10.

            g_new = getattr(self.g_new.dt[endcap,disk,ring,chamber],cc)
            g_ref = getattr(self.g_ref.dt[endcap,disk,ring,chamber],cc)

            # correction
            d_mm  = factor
            d_mm *= (g_new - g_ref)
            d_mm *= sc.signConventions["DT",wheel,station,sector][i%3]
            self.histo.histograms["h_d"][cc].Fill(d_mm)
            if fillTable:
                self.dtTab["d"][cc].FillDt(wheel,station,sector,"%.3f" % d_mm)

            # uncertainty & pull
            if rep is not None:
	            if ( cc=="y" and station==4 ): continue

                delta =  getattr(rep,"delta"+cc)
                e_mm  =  factor
                e_mm  *= delta.error
                self.histo.histograms["h_e"][cc].Fill(e_mm)

                if fillTable:
                    self.dtTab["e"][cc].FillDt(wheel,station,sector,"%.3f" % e_mm)

                if fabs(e_mm) > 1e-8:
                    p = d_mm/e_mm
                    self.histo.histograms["h_p"][cc].Fill(p)
                    if fillTable:
                        self.dtTab["p"][cc].FillDt(wheel,station,sector,"%.3f" % p)
            elif rep is None and fillTable:
                #Find worse 50 chambers
                ID_chamber = "chamber_{0}_{1}_{2}".format(wheel,station,sector)
                self.map_ID_Diff[cc][ID_chamber] = round(abs(d_mm),2)

        return



    def execute(self):
        """Execute the code to make the plots!"""
        self.histo.init_corrections()   # h_d
        self.histo.init_uncertainties() # h_e
        self.histo.init_pulls()         # h_p

        for station in self.stations:
            imageName = alignmentName+"-"+referenceName+"__MBs{0}".format(station)
            svgName   = imageName+".svg"
            pngName   = imageName+".png"

            gdv.draw_station(self.g_new,self.g_ref,station,self.svgPath+svgName,length_factor,angle_factor)

            retvalue = os.system("convert -density 104.2 {0} {1}".format(self.svgPath+svgName, self.pngPath+pngName) )

        for wheel in self.wheels:
            imageName = alignmentName+"-"+referenceName+"__MBw{0}".format(wheel)
            svgName   = imageName+".svg"
            pngName   = imageName+".png"

            gdv.draw_wheel(self.g_new,self.g_ref,wheel,self.svgPath+svgName,length_factor,angle_factor)

            retvalue = os.system("convert -density 104.2 {0} {1}".format(self.svgPath+svgName,self.pngPath+pngName) )

        if self.isReport:
            for r1 in self.report:
                if not (r1.status=="PASS" and r1.postal_address[0]=="DT"):
                    continue
				wheel   = r1.postal_address[1]
				station = r1.postal_address[2]
				sector  = r1.postal_address[3]

                self.fillHistograms( wheel,station,sector,rep=r1 )
        else:
            for wheel in self.wheels:
                for station in self.stations:
                    sectors = self.sectors if station != 4 else self.sectors4
                    for sector in sectors:
                        self.fillHistograms( wheel,station,sector )


        systemPrettyName = "MB ALL"
        histTitle = systemPrettyName+": {0}"

        for dof in self.dof:
            self.fitDrawHists("d",dof,histTitle.format(self.text["d"],label))

            if self.isReport:

                ### Uncertainties
                self.fitDrawHists("e",dof,histTitle.format(self.text["e"],self.alignmentName))

                ### Pulls
                self.fitDrawHists("p",dof,histTitle.format(self.text["p"],label))

        for wheel in self.wheels:
            for station in self.stations:
                for dof in self.dof:
                    self.histo.histograms["h_d"][dof].Reset("ICESM")
                    self.histo.histograms["h_e"][dof].Reset("ICESM")
                    self.histo.histograms["h_p"][dof].Reset("ICESM")


                    if self.isReport:
                        for r1 in self.report:
                            if ( r1.status == "PASS" and r1.postal_address[:3]==["DT",wheel,station]):
                                sector = r1.postal_address[3]
                                self.fillHistograms( wheel,station,sector,rep=r1,fillTable=True )

                    else: # if isReport
                        sectors = self.sectors if station != 4 else self.sectors4
                        for sector in sectors:
                            self.fillHistograms( wheel,station,sector,fillTable=True )


                    #****** Corrections: save plots and fill tables over homogeneous chambers ******
                    dtGroupPrettyName = "MB {0}/{1}/ALL".format(wheel,station)
                    histTitle   = dtGroupPrettyName+": {0}"
                    pngName = "DT_{0}{1}_{2}_{3}.png"
                    pdfName = "DT_{0}{1}_{2}_{3}.pdf"

                    for dof in self.dof:
                        pngName_d = pngName.format('d',dof,wheel,station)
                        pdfName_d = pngName.format('d',dof,wheel,station)

                        h = self.histo.histograms["h_d"][dof]
                        h.SetTitle(histTitle.format(self.text['d']))
                        fit = self.hfd.FitAndDraw(h,self.label)
                        self.histo.legend.Draw()

                        self.histo.c1.SaveAs( self.pngPath+"/"+pngName_d )
                        self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_d )

                        sRMS = "%.3f" % h.GetRMS()
                        self.dtGroupTable.FillDtGroup("d{0}RMS".format(dof),endcap,disk,ring,sRMS,self.pngPath+pngName_d)
                        if fit[0]:
                            sSigma = "%.3f" % fit[1].GetParameter(2)
                            self.dtGroupTable.FillDtGroup("d{0}GaussSig".format(dof),endcap,disk,ring,sSigma,self.pngPath+pngName_d)


                    #****** Fit uncert: save plots and fill tables over homogeneous chambers *******
                    #******** Pulls: save plots and fill tables over homogeneous chambers **********

                        if self.isReport:
                            pngName_e = pngName.format('e',dof,wheel,station)
                            pdfName_e = pngName.format('e',dof,wheel,station)

                            ## uncertainties
                            h = self.histo.histograms["h_e"][dof]
                            h.SetTitle(histTitle.format(self.text['e']))
                            fit = self.hfd.FitAndDraw(h,self.alignmentName)
                            self.histo.legend.Draw()
                            self.histo.c1.SaveAs( self.pngPath+"/"+pngName_e )
                            self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_e )

                            sMean = "%.3f" % h.GetMean()
                            self.dtGroupTable.FillDtGroup("e{0}Mean".format(dof),wheel,station,sMean,self.pngPath+pngName_e)
                            if fit[0]:
                                sGaussMean = "%.3f" % fit[1].GetParameter(1)
                                self.dtGroupTable.FillDtGroup("e{0}GaussMean".format(dof),wheel,station,sGaussMean,self.pngPath+pngName_e)

                            pngName_p = pngName.format('p',dof,wheel,station)
                            pdfName_p = pngName.format('p',dof,wheel,station)

                            ## pulls
                            h = self.histo.histograms["h_p"][dof]
                            h.SetTitle(histTitle.format(self.text['p']))
                            fit = self.hfd.FitAndDraw(h,self.label)
                            self.histo.legend.Draw()
                            self.histo.c1.SaveAs( self.pngPath+"/"+pngName_p )
                            self.histo.c1.SaveAs( self.pdfPath+"/"+pdfName_p )

                            sRMS = "%.3f" % h.GetRMS()
                            self.dtGroupTable.FillDtGroup("p{0}RMS".format(dof),wheel,station,sRMS,self.pngPath+pngName_p)
                            if fit[0]:
                                sSigma = "%.3f" % fit[1].GetParameter(2)
                                self.dtGroupTable.FillDtGroup("p{0}GaussSig".format(dof),wheel,station,sSigma,self.pngPath+pngName_p)




        #******************************************************************************#
        #                        Auxiliarly output HTML files                          #
        #                           1. htmlName_d - file for corrections or biases     #
        #                           2. htmlName_e - file for fit uncertainties         #
        #                           3. htmlName_p - file for pulls                     #
        #******************************************************************************#

		## Print 20 worst chambers
		for dof in self.dof:
		    if self.map_ID_Diff[dof]:
    			print "---------------WORSE 20 CHAMBER IN {0}------------------".format(dof)
	    		sorted = sorted(map_ID_Diff[dof].items(), key=operator.itemgetter(1))
		    	sorted.reverse()
			    for iN in range(20):
			        print sorted[iN]


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
            pngName = "DT_"+type+dof+".png"
            self.html.PrintHtmlCode(htmlFile,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName))
            if dof == "z": self.html.PrintHtmlCode(htmlFile,"</tr><tr align=center>")

        self.html.PrintHtmlCode(htmlFile,"</tr>")
        self.html.PrintHtmlCode(htmlFile,"</table>")

		## Visualization
		caption = "<font size=+1>%s visualization</font> <br><font size=-1><pre>%s</pre></font>"%(self.correctionName, label)
		self.html.PrintHtmlCode(htmlFile,"<p>")
		self.html.PrintHtmlCode(htmlFile,"<table border=\"1\" cellpadding=\"5\">")
		self.html.PrintHtmlCode(htmlFile,"<caption>%s</caption>" % caption)
		self.html.PrintHtmlCode(htmlFile,"<tr align=center>")

		for station in self.stations:
		    imageName = self.alignmentName+"-"+self.referenceName+"__MBs{0}".format(station)
		    pngName   = imageName+".png"
		    self.html.PrintHtmlCode(htmlFile,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"500\"></a></td>" % (pngName, pngName))
		    if station == 2:
		        self.html.PrintHtmlCode(htmlFile,"</tr><tr align=center>")

		self.html.PrintHtmlCode(htmlFile,"</tr>")
		self.html.PrintHtmlCode(htmlFile,"</table>")

		self.html.PrintHtmlCode(htmlFile,"<p>")
		self.html.PrintHtmlCode(htmlFile,"<table border=\"1\" cellpadding=\"5\">")
		self.html.PrintHtmlCode(htmlFile,"<caption>%s</caption>" % caption)
		self.html.PrintHtmlCode(htmlFile,"<tr align=center>")

		for wh,wheel in enumerate(self.wheels):
		    imageName = self.alignmentName+"-"+self.referenceName+"__MBw{0}".format(wheel)
		    pngName   = imageName+".png"
		    if wh == 0:
		        self.html.PrintHtmlCode(htmlFile,"<td rowspan=\"2\"><a href=\"{0}/{1}\"><img src=\"{0}/{1}\" alt=\"text\" width=\"300\"></a></td>".format(self.pngPath,pngName))
		    else:
		        self.html.PrintHtmlCode(htmlFile,"<td><a href=\".{0}/{1}\"><img src=\"{0}/{1}\" alt=\"text\" width=\"300\"></a></td>".format(self.pngPath,pngName))

		    if wheel == (len(self.wheels)%2+len(self.wheels)/2): # draw 3 then 2 on the next line
		        self.html.PrintHtmlCode(htmlFile,"</tr><tr align=center>")

		self.html.PrintHtmlCode(htmlFile,"</tr>")
		self.html.PrintHtmlCode(htmlFile,"</table>")


        cap_title = "averaged over homogeneous chambers"
        caption   = "<font size=+1>{0} {1}</font> <br><font size=-1>{2}</font>".format(self.text[type],cap_title,label)

        self.html.PrintHtmlCode(htmlFile,"<p>")
        self.dtGroupTable.PrintHtml(htmlFile,self.groupTableList['e'],caption,0)
        self.html.PrintHtmlCode(htmlFile,"<p>")
        self.dtGroupTable.PrintHtml(htmlFile,self.groupTableListFull['e'],caption,0)


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



            self.dtTab[type][dof].PrintHtml(htmlFile, htmlCaption, 0)
            self.dtTab[type][dof].PrintTex(texFile,   texCaption, "dtTab_"type+dof, 0)

            self.html.PrintHtmlCode(htmlFile,"<p>")
            self.html.PrintHtmlCode(htmlFile,"<table border=\"1\" cellpadding=\"5\">")
            self.html.PrintHtmlCode(htmlFile,"<caption>%s</caption>" % caption)
            self.html.PrintHtmlCode(htmlFile,"<tr align=center><th></th><th><i>Wheel {0}</i></th><th><i>Wheel {1}</i></th><th><i>Wheel {2}</i></th><th><i>Wheel {3}</i></th><th><i>Wheel {4}</i></th>".format(self.wheels[0],self.wheels[1],self.wheels[2],self.wheels[3],self.wheels[4]))
            for station in self.stations:

                self.html.PrintHtmlCode( htmlFile, ("<tr align=center><th><i>Station %s</i></th>" % station) )

                for wheel in self.wheels:
                    pngName = "DT_%s%s_%s_%s.png" % (type,dof,wheel,station)
                    if dof == "y" and station == 4: 
                        self.html.PrintHtmlCode( htmlFile, "<td>None</td>" )
                    else:
                        self.html.PrintHtmlCode( htmlFile, "<td><a href=\"{0}/{1}\"><img src=\"{0}/{1}\" alt=\"text\" width=\"250\"></a></td>".format(self.pngPath,pngName) )

                self.html.PrintHtmlCode(htmlFile,"</tr>")
            self.html.PrintHtmlCode(htmlFile,"</table>")

        self.html.PrintHtmlTrailer(htmlFile)
        self.tex.PrintTexTrailer(htmlFile)

        return


    def setupDtGroupTable(self):
        """Setup the DT group table"""
        self.dtGroupTable.AddDtGroupVar("dxRMS",         "&delta;x (mm) <br>RMS",                           "$RMS(\\delta x)$",                     "mm")
        self.dtGroupTable.AddDtGroupVar("dxGaussSig",    "&delta;x (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta x)$",         "mm")
        self.dtGroupTable.AddDtGroupVar("dyRMS",         "&delta;y (mm) <br>RMS",                           "$RMS(\\delta y)$",                     "mm")
        self.dtGroupTable.AddDtGroupVar("dyGaussSig",    "&delta;y (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta y)$",         "mm")
        self.dtGroupTable.AddDtGroupVar("dzRMS",         "&delta;z (mm) <br>RMS",                           "$RMS(\\delta z)$",                     "mm")
        self.dtGroupTable.AddDtGroupVar("dzGaussSig",    "&delta;z (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta z)$",         "mm")
        self.dtGroupTable.AddDtGroupVar("dphixRMS",      "&delta;&phi;<sub>x</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{x})$",             "mrad")
        self.dtGroupTable.AddDtGroupVar("dphixGaussSig", "&delta;&phi;<sub>x</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{x})$", "mrad")
        self.dtGroupTable.AddDtGroupVar("dphiyRMS",      "&delta;&phi;<sub>y</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{y})$",             "mrad")
        self.dtGroupTable.AddDtGroupVar("dphiyGaussSig", "&delta;&phi;<sub>y</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{y})$", "mrad")
        self.dtGroupTable.AddDtGroupVar("dphizRMS",      "&delta;&phi;<sub>z</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{z})$",             "mrad")
        self.dtGroupTable.AddDtGroupVar("dphizGaussSig", "&delta;&phi;<sub>z</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{z})$", "mrad")

        self.dtGroupTable.AddDtGroupVar("exMean",         "&sigma;<sub>fit</sub>x (mm) <br>Mean",                         "$Mean(\\sigma_{fit} x) $",               "mm")
        self.dtGroupTable.AddDtGroupVar("exGaussMean",    "&sigma;<sub>fit</sub>x (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} x) $",       "mm")
        self.dtGroupTable.AddDtGroupVar("eyMean",         "&sigma;<sub>fit</sub>y (mm) <br>Mean",                         "$Mean(\\sigma_{fit} y) $",               "mm")
        self.dtGroupTable.AddDtGroupVar("eyGaussMean",    "&sigma;<sub>fit</sub>y (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} y) $",       "mm")
        self.dtGroupTable.AddDtGroupVar("ezMean",         "&sigma;<sub>fit</sub>z (mm) <br>Mean",                         "$Mean(\\sigma_{fit} z) $",               "mm")
        self.dtGroupTable.AddDtGroupVar("ezGaussMean",    "&sigma;<sub>fit</sub>z (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} z) $",       "mm")
        self.dtGroupTable.AddDtGroupVar("ephixMean",      "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_x) $",         "mrad")
        self.dtGroupTable.AddDtGroupVar("ephixGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_x) $", "mrad")
        self.dtGroupTable.AddDtGroupVar("ephiyMean",      "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_y) $",         "mrad")
        self.dtGroupTable.AddDtGroupVar("ephiyGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_y) $", "mrad")
        self.dtGroupTable.AddDtGroupVar("ephizMean",      "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_z) $",         "mrad")
        self.dtGroupTable.AddDtGroupVar("ephizGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_z) $", "mrad")

        self.dtGroupTable.AddDtGroupVar("pxRMS","x pull <br>RMS",                                 "$RMS(P x)$",                     None)
        self.dtGroupTable.AddDtGroupVar("pxGaussSig","x pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P x)$",         None)
        self.dtGroupTable.AddDtGroupVar("pyRMS","y pull <br>RMS",                                 "$RMS(P y)$",                     None)
        self.dtGroupTable.AddDtGroupVar("pyGaussSig","y pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P y)$",         None)
        self.dtGroupTable.AddDtGroupVar("pzRMS","z pull <br>RMS",                                 "$RMS(P z)$",                     None)
        self.dtGroupTable.AddDtGroupVar("pzGaussSig","z pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P z)$",         None)
        self.dtGroupTable.AddDtGroupVar("pphixRMS","&phi;<sub>x</sub> pull <br>RMS",              "$RMS(P \\phi_{x})$",             None)
        self.dtGroupTable.AddDtGroupVar("pphixGaussSig","&phi;<sub>x</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{x})$", None)
        self.dtGroupTable.AddDtGroupVar("pphiyRMS","&phi;<sub>y</sub> pull <br>RMS",              "$RMS(P \\phi_{y})$",             None)
        self.dtGroupTable.AddDtGroupVar("pphiyGaussSig","&phi;<sub>y</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{y})$", None)
        self.dtGroupTable.AddDtGroupVar("pphizRMS","&phi;<sub>z</sub> pull <br>RMS",              "$RMS(P \\phi_{z})$",             None)
        self.dtGroupTable.AddDtGroupVar("pphizGaussSig","&phi;<sub>z</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{z})$", None)

        return




## THE END ##
