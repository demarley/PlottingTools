"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Write DT output to tables.
"""
import info
from table import Table

class DtTable(Table):
    """Class for writing DT information to TeX and html tables"""
    def __init__(self):
        Table.__init__(self)
        dt_info = info.dt()
        self.wheels   = dt_info["wheels"]
        self.stations = dt_info["stations"]
        self.sectors  = dt_info["sectors"]
        self.sectors4 = dt_info["sectors4"]

        for wheel in self.wheels:
            self.data.append([])

            for station in self.stations:
                self.data[wheel+2].append([])

                if station!=4:
                    for sector in self.sectors:
                        self.data[wheel+2][station-1].append(None)
                else:
                    for sector in self.sectors4:
                        self.data[wheel+2][station-1].append(None)


    def FillDt(self, wheel, station, sector, data):
        self.data[wheel+2][station-1][sector-1] = data
        return

    def PrintHtml(self, htmlFileName, caption="DT Table Caption", isComplete=False):
        if isComplete:
            self.html.PrintHtmlHeader(htmlFileName)
    
        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
        print >> htmlFile, "<caption>%s</caption>" % caption
        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th rowspan=\"2\"><i>wheels</i></th> <th rowspan=\"2\"><i>stations</i></th> <th colspan=\"14\"><i>sectors in stations 1,2,3</i></th>"
        print >> htmlFile, "</tr>"
        print >> htmlFile, "<tr align=center>"

        for sector in self.sectors:
            if sector == 4 or sector == 10:
                print >> htmlFile, "<th colspan=\"2\"><i>%s</i></th>" % sector
            else:
                print >> htmlFile, "<th><i>%s</i></th>" % sector
        print >> htmlFile, "</tr>"

        for wheel in self.wheels:
            for station in self.stations:
                print >> htmlFile, "<tr align=center>"
                if station == 1: print >> htmlFile, "<th rowspan=\"4\"><i>MB%s</i></th>" % wheel
                print >> htmlFile, "<th><i>MB%s/%s</i></th>" % (wheel, station)

                if station != 4:
                    for sector in self.sectors:
                        if sector == 4 or sector == 10:
                            print >> htmlFile, "<td colspan=\"2\">%s</td>" % self.data[wheel+2][station-1][sector-1]
                        else:
                            print >> htmlFile, "<td>%s</td>" % self.data[wheel+2][station-1][sector-1]
                else:
                    for sector in self.sectors4:
                        print >> htmlFile, "<td>%s</td>" % self.data[wheel+2][station-1][sector-1]
            print >> htmlFile, "</tr>"

        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th rowspan=\"2\"><i>wheels</i></th> <th rowspan=\"2\"><i>stations</i></th>"

        for sector in self.sectors:
            print >> htmlFile, "<th><i>%s</i></th>" % sector

        print >> htmlFile, "</tr>"
        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th colspan=\"14\"><i>sectors in station 4</i></th>"
        print >> htmlFile, "</tr>"
        print >> htmlFile, "</table>"
        htmlFile.close()
    
        if isComplete:
            self.html.PrintHtmlTrailer(htmlFileName)
        
        return


  
    def PrintTex(self, texFileName, caption="DT Table Caption", label="dtTable", isComplete=False):
        if isComplete:
            self.tex.PrintTexHeader(texFileName)
    
        texFile=open(texFileName, 'a')
        print >> texFile, "\\begin{landscape}"
        print >> texFile, "\\begin{table}[tbh]"
        print >> texFile, "\\cprotect\\caption{"+caption+" \\label{tab:"+label+"}}"
        print >> texFile, "\\begin{center}"
        print >> texFile, "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}"
        print >> texFile, "\\hline"
        print >> texFile, (" &  & \\multicolumn{14}{c|}{\\textit{\\textbf{sectors in stations 1,2,3}}} \\\\ \\cline{3-16}")
        print >> texFile, ("\\textit{\\textbf{wheels}} & \\textit{\\textbf{stations}}"),

        for sector in range(1,13):
            if sector == 4 or sector == 10:
                print >> texFile, (" & \\multicolumn{2}{c|}{\\textit{\\textbf{%s}}}" % sector),
            else:
                print >> texFile, (" & \\textit{\\textbf{%s}}" % sector),
        print >> texFile, "\\\\ \\hline \\hline"

        for wheel in [-2, -1, 0, 1, 2]:
            for station in 1, 2, 3, 4:
                if station == 1: print >> texFile, ("\\multirow{4}{*}{\\textit{\\textbf{MB%s}}}" % wheel),
                print >> texFile, (" & \\textit{\\textbf{MB%s/%s}}" % (wheel, station)),
                if station != 4:
                    for sector in range(1,13):
                        if sector == 4 or sector == 10:
                            print >> texFile, (" & \\multicolumn{2}{c|}{$%s$}" % self.data[wheel+2][station-1][sector-1]),
                        else:
                            print >> texFile, (" & $%s$" % self.data[wheel+2][station-1][sector-1]),
                else:
                    for sector in 1,2,3,13,4,5,6,7,8,9,14,10,11,12:
                        print >> texFile, (" & $%s$" % self.data[wheel+2][station-1][sector-1]),
                if station != 4: print >> texFile, " \\\\ \cline{2-16}"
                else:            print >> texFile, " \\\\ \hline \hline"

        print >> texFile, ("\\textit{\\textbf{wheels}}"),
        print >> texFile, (" & \\textit{\\textbf{stations}}"),
        for sector in 1,2,3,13,4,5,6,7,8,9,14,10,11,12:
            print >> texFile, (" & \\textit{\\textbf{%s}}" % sector),
        print >> texFile, "\\\\ \cline{3-16}"
        print >> texFile, (" &  & \\multicolumn{14}{c|}{\\textit{\\textbf{sectors in station 4}}} \\\\")
        print >> texFile, "\\hline"
        print >> texFile, "\\end{tabular}"
        print >> texFile, "\\end{center}"
        print >> texFile, "\\end{table}"
        print >> texFile, "\\end{landscape}"
        texFile.close()
    
        if isComplete:
            self.tex.PrintTexTrailer(texFileName)
        
        return


## THE END ##
