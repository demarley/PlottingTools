from Util_Html import *
from Util_Tex import *

class CscTable:
  
  def __init__(self):
    self.data = []
    for endcap in 1,2:
      self.data.append([])
      for disk in 1, 2, 3, 4:
        self.data[endcap-1].append([])
        if disk == 1: rings = 1,2,3
        else: rings = 1,2
        for ring in rings:
          self.data[endcap-1][disk-1].append([])
          if disk != 1 and ring == 1: chambers = range(18)
          else: chambers = range(36)
          for chamber in chambers:
            self.data[endcap-1][disk-1][ring-1].append(None)
  
  def FillCsc(self, endcap, disk, ring, chamber, data):
    self.data[endcap-1][disk-1][ring-1][chamber-1] = data

  def PrintData(self):
    print self.data

  def PrintHtml(self, htmlFileName, caption="Caption", isStandaloneFile=0):
    if isStandaloneFile != 0:
      PrintHtmlHeader(htmlFileName)

    htmlFile=open(htmlFileName, 'a')
    print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
    print >> htmlFile, "<caption>%s</caption>" % caption
    print >> htmlFile, "<tr align=center>"
    print >> htmlFile, "<th rowspan=\"2\"><i>endcaps</i></th> <th rowspan=\"2\"><i>disks</i></th> <th rowspan=\"2\"><i>rings</i></th> <th colspan=\"36\"><i>chambers</i></th>"
    print >> htmlFile, "</tr>"
    print >> htmlFile, "<tr align=center>"
    for chamber in range(36): print >> htmlFile, "<th><i>%s</i></th>" % (chamber+1)
    print >> htmlFile, "</tr>"
    for endcap in 1,2:
      if endcap == 1: sEndcap = "+"
      else : sEndcap = "-"
      for disk in 1, 2, 3, 4:
        if disk == 1: rings = 1,2,3
        else: rings = 1,2
        for ring in rings:
          print >> htmlFile, "<tr align=center>"
          if disk == 1 and ring == 1:
            print >> htmlFile, "<th rowspan=\"9\"><i>ME%s</i></th>" % sEndcap
          if ring == 1:
            if disk == 1: print >> htmlFile, "<th rowspan=\"3\"><i>ME%s%s</i></th>" % (sEndcap, disk)
            else: print >> htmlFile, "<th rowspan=\"2\"><i>ME%s%s</i></th>" % (sEndcap, disk)
          print >> htmlFile, "<th><i>ME%s%s/%s</i></th>" % (sEndcap, disk, ring)
          if disk != 1 and ring == 1:
            chambers = range(18)
            for chamber in chambers: print >> htmlFile, "<td colspan=\"2\">%s</td>" % self.data[endcap-1][disk-1][ring-1][chamber]
          else:
            chambers = range(36)
            for chamber in chambers: print >> htmlFile, "<td>%s</td>" % self.data[endcap-1][disk-1][ring-1][chamber]
    print >> htmlFile, "</tr>"
    
    print >> htmlFile, "<tr align=center>"
    print >> htmlFile, "<th rowspan=\"2\"><i>endcaps</i></th> <th rowspan=\"2\"><i>disks</i></th> <th rowspan=\"2\"><i>rings</i></th>"
    for chamber in range(18): print >> htmlFile, "<th colspan=\"2\"><i>%s</i></th>" % (chamber+1)
    print >> htmlFile, "</tr>"
    print >> htmlFile, "<tr align=center>"
    print >> htmlFile, "<th colspan=\"36\"><i>chambers</i></th>"
    print >> htmlFile, "</tr>"
    
    print >> htmlFile, "</table>"
    htmlFile.close()
    
    if isStandaloneFile != 0:
      PrintHtmlTrailer(htmlFileName)


  def PrintTex(self, texFileName, caption="CSC Table Caption", label="cscTable", isStandaloneFile = 0):
    if isStandaloneFile != 0:
      PrintTexHeader(texFileName)
    
    texFile=open(texFileName, 'a')
    print >> texFile, "\\begin{landscape}"
    print >> texFile, "\\begin{table}[tbh]"
    print >> texFile, "\\cprotect\\caption{"+caption+" \\label{tab:"+label+"}}"
    print >> texFile, "\\begin{center}"
    print >> texFile, "\\begin{tiny}"
    print >> texFile, "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}"
    print >> texFile, "\\hline"

    # Table splitted in two parts    
    chambers_1_9 = range(1,9+1)
    chambers_10_18 = range(10,18+1)
    chambers_1_18 = range(1,18+1)
    chambers_19_36 = range(19,36+1)
    for part in range(2):
      if part == 0: chambers18 = chambers_1_9
      else: chambers18 = chambers_10_18
      if part == 0: chambers36 = chambers_1_18
      else: chambers36 = chambers_19_36
      
      print >> texFile, (" &  &  & \\multicolumn{18}{c|}{\\textit{\\textbf{chambers}}} \\\\ \\cline{4-21}")
      print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),
      for chamber in chambers36: print >> texFile, " & \\textit{\\textbf{%s}}" % (chamber),
      print >> texFile, "\\\\ \\hline \\hline"
      for endcap in 1,2:
        if endcap == 1: sEndcap = "+"
        else : sEndcap = "-"
        for disk in 1, 2, 3, 4:
          if disk == 1: rings = 1,2,3
          else: rings = 1,2
          for ring in rings:
            if disk == 1 and ring == 1:
              print >> texFile, ("\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap),
            if ring == 1:
              if disk == 1: print >> texFile, ( " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
              else: print >> texFile, ( " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
            else: print >> texFile, ( " & " ),
            print >> texFile, ( " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring) ),
            if disk != 1 and ring == 1:
              for chamber in chambers18: print >> texFile, " & \\multicolumn{2}{c|}{$%s$}" % self.data[endcap-1][disk-1][ring-1][chamber-1],
            else:
              for chamber in chambers36:  print >> texFile, " & $%s$" % self.data[endcap-1][disk-1][ring-1][chamber-1],
            if disk == 4 and ring == 2: print >> texFile, " \\\\ \\hline \\hline"
            else:
              if ( ring == 3 and disk == 1 ) or (ring == 2 and disk != 1): print >> texFile, " \\\\ \\cline{2-21}"
              else: print >> texFile, " \\\\ \\cline{3-21}"
      print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),
      for chamber in chambers18: print >> texFile, " & \\multicolumn{2}{c|}{\\textit{\\textbf{%s}}}" % (chamber),
      print >> texFile, "\\\\ \cline{4-21}"
      print >> texFile, (" &  &  & \\multicolumn{18}{c|}{\\textit{\\textbf{chambers}}} \\\\")
      if part == 0: print >> texFile, "\\hline \\hline"
    
    print >> texFile, "\\hline"
    print >> texFile, "\\end{tabular}"
    print >> texFile, "\\end{tiny}"
    print >> texFile, "\\end{center}"
    print >> texFile, "\\end{table}"
    print >> texFile, "\\end{landscape}"
    texFile.close()
    
    if isStandaloneFile != 0:
      PrintTexTrailer(texFileName)

  def PrintTex2(self, texFileName, caption="CSC Table Caption", label="cscTable", isStandaloneFile = 0):
    if isStandaloneFile != 0:
      PrintTexHeader(texFileName)
    
    texFile=open(texFileName, 'a')
    print >> texFile, "\\begin{landscape}"
    print >> texFile, "\\begin{table}[tbh]"
    print >> texFile, "\\cprotect\\caption{"+caption+" \\label{tab:"+label+"}}"
    print >> texFile, "\\begin{center}"
    print >> texFile, "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}"
    print >> texFile, "\\hline"
    print >> texFile, (" &  &  & \\multicolumn{36}{c|}{\\textit{\\textbf{chambers}}} \\\\ \\cline{4-39}")
    print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),
    for chamber in range(36): print >> texFile, " & \\textit{\\textbf{%s}}" % (chamber+1),
    print >> texFile, "\\\\ \\hline \\hline"
    
    for endcap in 1,2:
      if endcap == 1: sEndcap = "+"
      else : sEndcap = "-"
      for disk in 1, 2, 3, 4:
        if disk == 1: rings = 1,2,3
        else: rings = 1,2
        for ring in rings:
          if disk == 1 and ring == 1:
            print >> texFile, ("\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap),
          if ring == 1:
            if disk == 1: print >> texFile, ( " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
            else: print >> texFile, ( " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk) ),
          else: print >> texFile, ( " & " ),
          print >> texFile, ( " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring) ),
          if disk != 1 and ring == 1:
            chambers = range(18)
            for chamber in chambers: print >> texFile, " & \\multicolumn{2}{c|}{$%s$}" % self.data[endcap-1][disk-1][ring-1][chamber],
          else:
            chambers = range(36)
            for chamber in chambers:  print >> texFile, " & $%s$" % self.data[endcap-1][disk-1][ring-1][chamber],
          if disk == 4 and ring == 2: print >> texFile, " \\\\ \\hline \\hline"
          else:
            if ( ring == 3 and disk == 1 ) or (ring == 2 and disk != 1): print >> texFile, " \\\\ \\cline{2-39}"
            else: print >> texFile, " \\\\ \\cline{3-39}"
    print >> texFile, ("\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}"),
    for chamber in range(18): print >> texFile, " & \\multicolumn{2}{c|}{\\textit{\\textbf{%s}}}" % (chamber+1),
    print >> texFile, "\\\\ \cline{4-39}"
    print >> texFile, (" &  &  & \\multicolumn{36}{c|}{\\textit{\\textbf{chambers}}} \\\\")
    print >> texFile, "\\hline"
    print >> texFile, "\\end{tabular}"
    print >> texFile, "\\end{center}"
    print >> texFile, "\\end{table}"
    print >> texFile, "\\end{landscape}"
    texFile.close()
    
    if isStandaloneFile != 0:
      PrintTexTrailer(texFileName)
