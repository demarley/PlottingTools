"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Write CSC output to tables.
"""
import info
from table import Table


class CscTable(Table):
    """Class for writing CSC information to TeX and html tables"""
    def __init__(self):
        Table.__init__(self)
        csc_info = info.csc()
        self.endcaps = csc_info["endcaps"]
        self.disks   = csc_info["disks"]
        self.rings   = csc_info["rings"]

        for endcap in self.endcaps:
            self.data.append([])
            for disk in self.disks:
                self.data[endcap-1].append([])

                rings = self.rings[disk]
                for ring in rings:
                    self.data[endcap-1][disk-1].append([])

                    chambers = range(18) if (disk!=1 and ring==1) else range(36)
                    for chamber in chambers:
                        self.data[endcap-1][disk-1][ring-1].append(None)
  
  
    def FillCsc(self, endcap, disk, ring, chamber, data):
        self.data[endcap-1][disk-1][ring-1][chamber-1] = data
        return

    def PrintHtml(self, htmlFileName, caption="Caption", isStandaloneFile=False):
        if isStandaloneFile:
            self.html.PrintHtmlHeader(htmlFileName)

        htmlFile=open(htmlFileName, 'a')
        print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
        print >> htmlFile, "<caption>%s</caption>" % caption
        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th rowspan=\"2\"><i>endcaps</i></th> <th rowspan=\"2\"><i>disks</i></th> <th rowspan=\"2\"><i>rings</i></th> <th colspan=\"36\"><i>chambers</i></th>"
        print >> htmlFile, "</tr>"
        print >> htmlFile, "<tr align=center>"
        for chamber in range(36):
            print >> htmlFile, "<th><i>%s</i></th>" % (chamber+1)
        print >> htmlFile, "</tr>"

        for endcap in self.endcaps:
            sEndcap = "+" if endcap==1 else "-"

            for disk in self.disks:
                rings = self.rings[disk]
                for ring in rings:
                    print >> htmlFile, "<tr align=center>"
                    if disk == 1 and ring == 1:
                        print >> htmlFile, "<th rowspan=\"9\"><i>ME%s</i></th>" % sEndcap
                    if ring == 1:
                        if disk == 1: print >> htmlFile, "<th rowspan=\"3\"><i>ME%s%s</i></th>" % (sEndcap, disk)
                        else: print >> htmlFile, "<th rowspan=\"2\"><i>ME%s%s</i></th>" % (sEndcap, disk)
                    print >> htmlFile, "<th><i>ME%s%s/%s</i></th>" % (sEndcap, disk, ring)

                    if disk!=1 and ring==1:
                        chambers = range(18)
                        for chamber in chambers:
                            print >> htmlFile, "<td colspan=\"2\">%s</td>" % self.data[endcap-1][disk-1][ring-1][chamber]
                    else:
                        chambers = range(36)
                        for chamber in chambers:
                            print >> htmlFile, "<td>%s</td>" % self.data[endcap-1][disk-1][ring-1][chamber]
        print >> htmlFile, "</tr>"

        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th rowspan=\"2\"><i>endcaps</i></th> <th rowspan=\"2\"><i>disks</i></th> <th rowspan=\"2\"><i>rings</i></th>"

        for chamber in range(18):
            print >> htmlFile, "<th colspan=\"2\"><i>%s</i></th>" % (chamber+1)

        print >> htmlFile, "</tr>"
        print >> htmlFile, "<tr align=center>"
        print >> htmlFile, "<th colspan=\"36\"><i>chambers</i></th>"
        print >> htmlFile, "</tr>"

        print >> htmlFile, "</table>"
        htmlFile.close()
    
        if isStandaloneFile:
            self.html.PrintHtmlTrailer(htmlFileName)

        return


    def PrintTex(self, texFileName, caption="CSC Table Caption", label="cscTable", isComplete=False):
        if isComplete:
            self.tex.PrintTexHeader(texFileName)
    
        texFile=open(texFileName, 'a')
        print >> texFile, "\\begin{landscape}"
        print >> texFile, "\\begin{table}[tbh]"
        print >> texFile, "\\cprotect\\caption{"+caption+" \\label{tab:"+label+"}}"
        print >> texFile, "\\begin{center}"
        print >> texFile, "\\begin{tiny}"
        print >> texFile, "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}"
        print >> texFile, "\\hline"

        # Table split in two parts    
        chambers_1_9   = range(1,9+1)
        chambers_10_18 = range(10,18+1)
        chambers_1_18  = range(1,18+1)
        chambers_19_36 = range(19,36+1)

        for part in range(2):
            if not part:
                chambers18 = chambers_1_9
                chambers36 = chambers_1_18
            else:
                chambers18 = chambers_10_18
                chambers36 = chambers_19_36

      
            print >> texFile, (" &  &  & \\multicolumn{18}{c|}{\\textit{\\textbf{chambers}}} \\\\ \\cline{4-21}")
            print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),

            for chamber in chambers36:
                print >> texFile, " & \\textit{\\textbf{%s}}" % (chamber),

            print >> texFile, "\\\\ \\hline \\hline"

            for endcap in self.endcaps:
                sEndcap = "+" if endcap==1 else "-"

                for disk in self.disks:

                    rings = self.rings[disk]
                    for ring in rings:

                        if disk==1 and ring==1:
                            print >> texFile, ("\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap),
                            print >> texFile, ( " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
                        elif disk!=1 and ring==1:
                            print >> texFile, ( " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
                        else:
                            print >> texFile, ( " & " ),

                        print >> texFile, ( " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring) ),

                        if disk!=1 and ring==1:
                            for chamber in chambers18:
                                print >> texFile, " & \\multicolumn{2}{c|}{$%s$}" % self.data[endcap-1][disk-1][ring-1][chamber-1],
                        else:
                            for chamber in chambers36:
                                print >> texFile, " & $%s$" % self.data[endcap-1][disk-1][ring-1][chamber-1],

                        if disk==4 and ring==2:
                            print >> texFile, " \\\\ \\hline \\hline"
                        else:
                            if ( ring==3 and disk==1 ) or ( ring==2 and disk!=1 ):
                                print >> texFile, " \\\\ \\cline{2-21}"
                            else:
                                print >> texFile, " \\\\ \\cline{3-21}"
            print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),

            for chamber in chambers18:
                print >> texFile, " & \\multicolumn{2}{c|}{\\textit{\\textbf{%s}}}" % (chamber),

            print >> texFile, "\\\\ \cline{4-21}"
            print >> texFile, (" &  &  & \\multicolumn{18}{c|}{\\textit{\\textbf{chambers}}} \\\\")
            if not part:
                print >> texFile, "\\hline \\hline"

        print >> texFile, "\\hline"
        print >> texFile, "\\end{tabular}"
        print >> texFile, "\\end{tiny}"
        print >> texFile, "\\end{center}"
        print >> texFile, "\\end{table}"
        print >> texFile, "\\end{landscape}"
        texFile.close()

        if isComplete:
            self.tex.PrintTexTrailer(texFileName)

        return



    def PrintTex2(self, texFileName, caption="CSC Table Caption", label="cscTable", isComplete=False):
        if isComplete:
            self.tex.PrintTexHeader(texFileName)
    
        texFile=open(texFileName, 'a')
        print >> texFile, "\\begin{landscape}"
        print >> texFile, "\\begin{table}[tbh]"
        print >> texFile, "\\cprotect\\caption{"+caption+" \\label{tab:"+label+"}}"
        print >> texFile, "\\begin{center}"
        print >> texFile, "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}"
        print >> texFile, "\\hline"
        print >> texFile, (" &  &  & \\multicolumn{36}{c|}{\\textit{\\textbf{chambers}}} \\\\ \\cline{4-39}")
        print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),

        for chamber in range(36):
            print >> texFile, " & \\textit{\\textbf{%s}}" % (chamber+1),

        print >> texFile, "\\\\ \\hline \\hline"
    
        for endcap in self.endcaps:
            sEndcap = "+" if endcap==1 else "-"

            for disk in self.disks:

                rings = self.rings[disk]
                for ring in rings:
                    if disk == 1 and ring == 1:
                        print >> texFile, ("\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap),
                        print >> texFile, ( " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
                    elif disk!=1 and ring==1:
                        print >> texFile, ( " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
                    else: print >> texFile, ( " & " ),
                    print >> texFile, ( " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring) ),

                    if disk != 1 and ring == 1:
                        chambers = range(18)
                        for chamber in chambers:
                            print >> texFile, " & \\multicolumn{2}{c|}{$%s$}" % self.data[endcap-1][disk-1][ring-1][chamber],
                    else:
                        chambers = range(36)
                        for chamber in chambers:
                            print >> texFile, " & $%s$" % self.data[endcap-1][disk-1][ring-1][chamber],

                    if disk == 4 and ring == 2:
                        print >> texFile, " \\\\ \\hline \\hline"
                    else:
                        if ( ring == 3 and disk == 1 ) or (ring == 2 and disk != 1): print >> texFile, " \\\\ \\cline{2-39}"
                        else: print >> texFile, " \\\\ \\cline{3-39}"

        print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),

        for chamber in range(18):
            print >> texFile, " & \\multicolumn{2}{c|}{\\textit{\\textbf{%s}}}" % (chamber+1),

        print >> texFile, "\\\\ \cline{4-39}"
        print >> texFile, (" &  &  & \\multicolumn{36}{c|}{\\textit{\\textbf{chambers}}} \\\\")
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
