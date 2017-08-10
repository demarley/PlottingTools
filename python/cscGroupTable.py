"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Write CSC group output to tables.
"""
import info
from table import Table


class CscGroupTable(Table):
    """Save CSC group information to tables"""
    def __init__(self):
        Table.__init__(self)
        csc_info = info.csc()
        self.endcaps = csc_info["endcaps"]
        self.disks   = csc_info["disks"]
        self.rings   = csc_info["rings"]

        self.nRows = 3


    def AddCscGroupVar(self, varName, varTitle=None, varTitleTex=None, varUnitTex=None):
        if varTitle is None:    varTitle    = varName
        if varTitleTex is None: varTitleTex = varName
    
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
        for endcap in self.endcaps:

            self.data[var][1].append([])
            for disk in self.disks:
                self.data[var][1][endcap-1].append([])

                rings = self.rings[disk]
                for ring in rings:
                    self.data[var][1][endcap-1][disk-1].append([])
                    self.data[var][1][endcap-1][disk-1][ring-1].append([])
                    self.data[var][1][endcap-1][disk-1][ring-1][0] = None
                    self.data[var][1][endcap-1][disk-1][ring-1].append([])
                    self.data[var][1][endcap-1][disk-1][ring-1][1] = None

        return


  
    def FillCscGroupByIndex(self, varIndex, endcap, disk, ring, data, link=None):
        self.data[varIndex][1][endcap-1][disk-1][ring-1][0] = data
        self.data[varIndex][1][endcap-1][disk-1][ring-1][1] = link
        return

  
    def FillCscGroupByName(self, varName, endcap, disk, ring, data, link=None):
        self.FillCscGroupByIndex(self.GetVarIndex(varName), endcap, disk, ring, data, link)
        return


    def FillCscGroup(self, varName, endcap, disk, ring, data, link=None):
        self.FillCscGroupByName(varName, endcap, disk, ring, data, link)
        return

  
    def PrintHtml(self, htmlFileName, varNamesToPrint="Var", caption="CSC Group Table Caption", isComplete=False):
        varIndices = []
        for varName in varNamesToPrint:
            varIndex = self.GetVarIndex(varName)
            varIndices.append(varIndex)
    
        if isComplete:
            self.html.PrintHtmlHeader(htmlFileName)
    
        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
        print >> htmlFile, "<caption>%s</caption>" % caption
    
        print >> htmlFile, "<tr align=center> <th><i>endcaps</i></th> <th><i>disks</i></th> <th><i>rings</i></th>"
        for varIndex in varIndices:
            varTitle = self.data[varIndex][0][1]
            print >> htmlFile, "<th><i>%s</i></th>" % varTitle
        print >> htmlFile, "</tr>"
    
    
        for endcap in self.endcaps:
            sEndcap = "+" if endcap==1 else "-"

            for disk in self.disks:
                rings = self.rings[disk]

                for ring in rings:
                    print >> htmlFile, "<tr align=center>"
                    if disk == 1 and ring == 1:
                        print >> htmlFile, "<th rowspan=\"9\"><i>ME%s</i></th>" % sEndcap
                        print >> htmlFile, "<th rowspan=\"3\"><i>ME%s%s</i></th>" % (sEndcap, disk)
                    elif disk!=1 and ring==1:
                        print >> htmlFile, "<th rowspan=\"2\"><i>ME%s%s</i></th>" % (sEndcap, disk)

                    print >> htmlFile, "<th><i>ME%s%s/%s</i></th>" % (sEndcap, disk, ring)

                    for varIndex in varIndices:
                        data = self.data[varIndex][1][endcap-1][disk-1][ring-1][0]
                        link = self.data[varIndex][1][endcap-1][disk-1][ring-1][1]
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


    def PrintTex(self, texFileName, varNamesToPrint="Var", caption="CSC Group Table Caption", label="cscGroupTable", isComplete=0):
        varIndices = []
        for varName in varNamesToPrint:
            varIndex = self.GetVarIndex(varName)
            varIndices.append(varIndex)
    
        if isComplete:
            self.tex.PrintTexHeader(texFileName)
    
        texFile=open(texFileName, 'a')
        print >> texFile, "%\\begin{landscape}"
        print >> texFile, "\\begin{table}[tbh]"
        print >> texFile, "\\caption{"+caption+" \\label{"+label+"}}"
        print >> texFile, "\\begin{footnotesize}"
    
        print >> texFile, "\n\\begin{center}"
        print >> texFile,  "\\begin{tabular}{|c|c|c|",

        nRows = self.nRows
        for varIndex in varIndices:
            print >> texFile,  "c|",
            nRows+=1

        print >> texFile,  "}"
        print >> texFile, "\\hline"

        print >> texFile, "\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}",
        for varIndex in varIndices:
            varTitleTex = self.data[varIndex][0][2]
            print >> texFile, (" & %s" % varTitleTex),
        printRowWithUnits = False
        for varIndex in varIndices:
            varUnitTex = self.data[varIndex][0][3]
            if varUnitTex is not None:
                printRowWithUnits = True
        if printRowWithUnits:
            print >> texFile, "\\\\"
            print >> texFile, " &  & ",
            for varIndex in varIndices:
                varUnitTex = self.data[varIndex][0][3]
                if varUnitTex is not None:
                    print >> texFile, (" & %s " % varUnitTex),
                else:
                    print >> texFile, (" & "),

        print >> texFile, "\\\\ \\hline \\hline"
    
        for endcap in self.endcaps:
            sEndcap = "+" if endcap==1 else "-"

            for disk in self.disks:
                rings = self.rings[disk]
                for ring in rings:
                    if disk==1 and ring==1:
                        print >> texFile, "\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap,
                        print >> texFile, " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk),
                    elif disk!=1 and ring==1:
                        print >> texFile, " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk),
                    else:
                        print >> texFile, " & ",

                    print >> texFile, " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring),

                    for varIndex in varIndices:
                        data = self.data[varIndex][1][endcap-1][disk-1][ring-1][0]
                        print >> texFile, (" & %s" % data),

                    if disk==4 and ring==2:
                        if endcap==1: print >> texFile, "\\\\ \\hline \\hline"
                        else:         print >> texFile, "\\\\ \\hline"
                    else:
                        if (disk == 1 and ring ==3) or (disk != 1 and ring == 2):
                            print >> texFile, "\\\\ \\cline{2-%s}" % nRows
                        else:
                            print >> texFile, "\\\\ \\cline{3-%s}" % nRows
    
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