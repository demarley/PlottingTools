"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Write DT group output to tables.
"""
import info
from table import Table


class DtGroupTable(Table):
    """Save DT group information to tables"""
    def __init__(self):
        Table.__init__(self)
        dt_info = info.dt()
        self.wheels   = dt_info["wheels"]
        self.stations = dt_info["stations"]
        self.sectors  = dt_info["sectors"]
        self.sectors4 = dt_info["sectors4"]

        self.nRows = 2


    def AddDtGroupVar(self, varName, varTitle=None, varTitleTex=None, varUnitTex=None):
        if varTitle is None:    varTitle=varName
        if varTitleTex is None: varTitleTex=varName
    
        self.data.append([])
        var = len(self.data) - 1
        self.data[var].append([])
        self.data[var][0].append([])
        self.data[var][0][0] = varName
        self.data[var][0].append([])
        self.data[var][0][1] = varTitle
        self.data[var][0].append([])
        self.data[var][0][2] = varTitleTex
        self.data[var][0].append([])
        self.data[var][0][3] = varUnitTex
        self.data[var].append([])
        for wheel in -2, -1, 0, +1, +2:
            self.data[var][1].append([])
            for station in 1, 2, 3, 4:
                self.data[var][1][wheel+2].append([])
                self.data[var][1][wheel+2][station-1].append([])
                self.data[var][1][wheel+2][station-1][0] = None
                self.data[var][1][wheel+2][station-1].append([])
                self.data[var][1][wheel+2][station-1][1] = None

        return

    def FillDtGroupByIndex(self, varIndex, wheel, station, data, link = None):
        self.data[varIndex][1][wheel+2][station-1][0] = data
        self.data[varIndex][1][wheel+2][station-1][1] = link
        return

    def FillDtGroupByName(self, varName, wheel, station, data, link = None):
        self.FillDtGroupByIndex(self.GetVarIndex(varName), wheel, station, data, link)
        return

    def FillDtGroup(self, varName, wheel, station, data, link = None):
        self.FillDtGroupByName(varName, wheel, station, data, link)
        return


    def PrintHtml(self, htmlFileName, varNamesToPrint="Var", caption="DT Group Table Caption", isComplete=False):
        varIndices = []
        for varName in varNamesToPrint:
            varIndex = self.GetVarIndex(varName)
            varIndices.append(varIndex)
  
        if isComplete:
            self.html.PrintHtmlHeader(htmlFileName)
  
        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
        print >> htmlFile, "<caption>%s</caption>" % caption
  
        print >> htmlFile, "<tr align=center> <th><i>wheels</i></th> <th><i>stations</i></th>"
        for varIndex in varIndices:
            varTitle = self.data[varIndex][0][1]
            print >> htmlFile, "<th><i>%s</i></th>" % varTitle
        print >> htmlFile, "</tr>"
  
        for wheel in self.wheels:
            for station in self.stations:  
                print >> htmlFile, "<tr align=center>"  
                if station == 1:
                    if wheel == 0:   print >> htmlFile, "<th rowspan=\"4\"><i>MB %s</i></th>" % wheel
                    elif wheel >  0: print >> htmlFile, "<th rowspan=\"4\"><i>MB+%s</i></th>" % wheel
                    else:            print >> htmlFile, "<th rowspan=\"4\"><i>MB%s</i></th>" % wheel
                if wheel==0:  print >> htmlFile, "<th><i>MB %s/%s</i></th>" % (wheel,station)
                elif wheel>0: print >> htmlFile, "<th><i>MB+%s/%s</i></th>" % (wheel,station)
                else:         print >> htmlFile, "<th><i>MB%s/%s</i></th>" % (wheel,station)

                for varIndex in varIndices:
                    data = self.data[varIndex][1][wheel+2][station-1][0]
                    link = self.data[varIndex][1][wheel+2][station-1][1]
                    if link is None:
                        print >> htmlFile, "<td>%s</td>" % data
                    else:
                        print >> htmlFile, "<td><a href=\"%s\" style=\"text-decoration: none\">%s</a></td>" % (link, data)
                print >> htmlFile, "</tr>"
  
        print >> htmlFile, "</table>"
        htmlFile.close()
    
        if isComplete:
            self.html.PrintHtmlTrailer(htmlFileName)

        return



    def PrintTex(self, texFileName, varNamesToPrint="Var", caption="DT Group Table Caption", label="dtGroupTable", isComplete=False):
        varIndices = []
        for varName in varNamesToPrint:
            varIndex = self.GetVarIndex(varName)
            varIndices.append(varIndex)
    
        if isComplete:
            self.tex.PrintTexHeader(texFileName)
    
        texFile=open(texFileName, 'a')
        print >> texFile, "%\\begin{landscape}\n"
        print >> texFile, "\\begin{table}[tbh]"
        print >> texFile, "\\caption{"+caption+" \\label{"+label+"}}"
        print >> texFile, "\\begin{footnotesize}"
    
        print >> texFile, "\n\\begin{center}"
        print >> texFile,  "\\begin{tabular}{|c|c|",

        nRows = self.nRows
        for varIndex in varIndices:
            print >> texFile,  "c|",
            nRows+=1

        print >> texFile,  "}"
        print >> texFile, "\\hline"

        print >> texFile, "\\textit{\\textbf{wheels}} & \\textit{\\textbf{stations}}"
        for varIndex in varIndices:
            varTitleTex = self.data[varIndex][0][2]
            print >> texFile, (" & %s " % varTitleTex),

        printRowWithUnits = False
        for varIndex in varIndices:
            varUnitTex = self.data[varIndex][0][3]
            if varUnitTex is not None:
                printRowWithUnits = True
        if printRowWithUnits:
            print >> texFile, "\\\\"
            print >> texFile, " & ",
            for varIndex in varIndices:
                varUnitTex = self.data[varIndex][0][3]
                if varUnitTex is not None:
                    print >> texFile, (" & %s " % varUnitTex),
                else:
                    print >> texFile, (" & "),

        print >> texFile, "\\\\ \\hline \\hline"
    
        for wheel in self.wheels:
            for station in self.stations:  
                if station == 1:
                    if wheel==0:  print >> texFile, "\\multirow{4}{*}{\\textit{\\textbf{MB %s}}}" % wheel,
                    elif wheel>0: print >> texFile, "\\multirow{4}{*}{\\textit{\\textbf{MB+%s}}}" % wheel,
                    else:         print >> texFile, "\\multirow{4}{*}{\\textit{\\textbf{MB%s}}}" % wheel,

                if wheel==0:  print >> texFile, (" & \\textit{\\textbf{MB %s/%s}}" % (wheel,station)),
                elif wheel>0: print >> texFile, (" & \\textit{\\textbf{MB+%s/%s}}" % (wheel,station)),
                else:         print >> texFile, (" & \\textit{\\textbf{MB%s/%s}}" % (wheel,station)),

                for varIndex in varIndices:
                    data = self.data[varIndex][1][wheel+2][station-1][0]
                    print >> texFile, (" & %s" % data),

                if station != 4:
                    print >> texFile, "\\\\ \\cline{2-%s}" % nRows
                else:
                    print >> texFile, "\\\\ \\hline"
    
        print >> texFile, "\\end{tabular}"
        print >> texFile, "\\end{center}\n"
        print >> texFile, "\\end{footnotesize}"
        print >> texFile, "\\end{table}\n"
        print >> texFile, "%\\end{landscape}"
        texFile.close()
      
        if isComplete:
            self.tex.PrintTexTrailer(texFileName)

        return


## THE END ##
