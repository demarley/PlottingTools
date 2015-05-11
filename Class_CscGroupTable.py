from Util_Html import *
from Util_Tex import *

class CscGroupTable:
  
  def __init__(self):
    self.data       = []
        
  def AddCscGroupVar(self, varName, varTitle=None, varTitleTex=None, varUnitTex=None):
    if varTitle==None:    varTitle=varName
    if varTitleTex==None: varTitleTex=varName
    
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
    for endcap in 1,2:
      self.data[var][1].append([])
      for disk in 1,2,3,4:
        self.data[var][1][endcap-1].append([])
        if disk == 1: rings = 1,2,3
        else:         rings = 1,2
        for ring in rings:
          self.data[var][1][endcap-1][disk-1].append([])
          self.data[var][1][endcap-1][disk-1][ring-1].append([])
          self.data[var][1][endcap-1][disk-1][ring-1][0] = None
          self.data[var][1][endcap-1][disk-1][ring-1].append([])
          self.data[var][1][endcap-1][disk-1][ring-1][1] = None
  
  def GetVarName(self, varIndex):
    return self.data[varIndex][0][0]
  
  def GetVarIndex(self, varName):
    for varIndex in range( len(self.data) ):
      if self.data[varIndex][0][0] == varName:
        return varIndex
    print "Error! No such variable:", varName
    return -1
  
  def FillCscGroupByIndex(self, varIndex, endcap, disk, ring, data, link = None):
    self.data[varIndex][1][endcap-1][disk-1][ring-1][0] = data
    self.data[varIndex][1][endcap-1][disk-1][ring-1][1] = link
  
  def FillCscGroupByName(self, varName, endcap, disk, ring, data, link = None):
    self.FillCscGroupByIndex(self.GetVarIndex(varName), endcap, disk, ring, data, link)
  
  def FillCscGroup(self, varName, endcap, disk, ring, data, link = None):
    self.FillCscGroupByName(varName, endcap, disk, ring, data, link)
  
  def PrintData(self):
    print self.data
  
  def PrintHtml(self, htmlFileName, varNamesToPrint="Var", caption="CSC Group Table Caption", isComplete=0):
    varIndexes = []
    for varName in varNamesToPrint:
      varIndex = self.GetVarIndex(varName)
      varIndexes.append(varIndex)
    
    if isComplete != 0:
      PrintHtmlHeader(htmlFileName)
    
    htmlFile=open(htmlFileName, 'a')
    print >> htmlFile, "<table border=\"1\" cellpadding=\"5\">"
    print >> htmlFile, "<caption>%s</caption>" % caption
    
    print >> htmlFile, "<tr align=center> <th><i>endcaps</i></th> <th><i>disks</i></th> <th><i>rings</i></th>"
    for varIndex in varIndexes:
      varTitle = self.data[varIndex][0][1]
      print >> htmlFile, "<th><i>%s</i></th>" % varTitle
    print >> htmlFile, "</tr>"
    
    
    for endcap in 1,2:
      if endcap == 1: sEndcap = "+"
      else : sEndcap = "-"
      for disk in 1, 2, 3, 4:
        if disk == 1: rings = 1,2,3
        else:         rings = 1,2
        for ring in rings:
          print >> htmlFile, "<tr align=center>"
          if disk == 1 and ring == 1:
            print >> htmlFile, "<th rowspan=\"9\"><i>ME%s</i></th>" % sEndcap
          if ring == 1:
            if disk == 1: print >> htmlFile, "<th rowspan=\"3\"><i>ME%s%s</i></th>" % (sEndcap, disk)
            else:         print >> htmlFile, "<th rowspan=\"2\"><i>ME%s%s</i></th>" % (sEndcap, disk)
          print >> htmlFile, "<th><i>ME%s%s/%s</i></th>" % (sEndcap, disk, ring)
          for varIndex in varIndexes:
            data = self.data[varIndex][1][endcap-1][disk-1][ring-1][0]
            link = self.data[varIndex][1][endcap-1][disk-1][ring-1][1]
            if link == None: print >> htmlFile, "<td>%s</td>" % data
            else: print >> htmlFile, "<td><a href=\"%s\" style=\"text-decoration: none\">%s</a></td>" % (link, data)
          print >> htmlFile, "</tr>"
    
    print >> htmlFile, "</table>"
    htmlFile.close()
      
    if isComplete != 0:
      PrintHtmlTrailer(htmlFileName)


  def PrintTex(self, texFileName, varNamesToPrint="Var", caption="CSC Group Table Caption", label="cscGroupTable", isComplete=0):
    varIndexes = []
    for varName in varNamesToPrint:
      varIndex = self.GetVarIndex(varName)
      varIndexes.append(varIndex)
    
    if isComplete != 0:
      PrintTexHeader(texFileName)
    
    texFile=open(texFileName, 'a')
    print >> texFile, "%\\begin{landscape}"
    print >> texFile, "\\begin{table}[tbh]"
    print >> texFile, "\\caption{"+caption+" \\label{"+label+"}}"
    print >> texFile, "\\begin{footnotesize}"
    
    print >> texFile, "\n\\begin{center}"
    print >> texFile,  "\\begin{tabular}{|c|c|c|",
    nRows = 3
    for varIndex in varIndexes:
      print >> texFile,  "c|",
      nRows = nRows + 1
    print >> texFile,  "}"
    print >> texFile, "\\hline"

    print >> texFile, "\\textit{\\textbf{endcaps}} & \\textit{\\textbf{disks}} & \\textit{\\textbf{rings}}",
    for varIndex in varIndexes:
      varTitleTex = self.data[varIndex][0][2]
      print >> texFile, (" & %s" % varTitleTex),
    printRowWithUnits = False
    for varIndex in varIndexes:
      varUnitTex = self.data[varIndex][0][3]
      if varUnitTex != None: printRowWithUnits = True
    if printRowWithUnits == True:
      print >> texFile, "\\\\"
      print >> texFile, " &  & ",
      for varIndex in varIndexes:
        varUnitTex = self.data[varIndex][0][3]
        if varUnitTex != None: print >> texFile, (" & %s " % varUnitTex),
        else:                  print >> texFile, (" & "),
    print >> texFile, "\\\\ \\hline \\hline"
    
    for endcap in 1,2:
      if endcap == 1: sEndcap = "+"
      else : sEndcap = "-"
      for disk in 1, 2, 3, 4:
        if disk == 1: rings = 1,2,3
        else:         rings = 1,2
        for ring in rings:
          if disk == 1 and ring == 1:
            print >> texFile, "\\multirow{9}{*}{\\textit{\\textbf{ME%s}}}" % sEndcap,
          if ring == 1:
            if disk == 1: print >> texFile, " & \\multirow{3}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk),
            else:         print >> texFile, " & \\multirow{2}{*}{\\textit{\\textbf{ME%s%s}}}" % (sEndcap, disk),
          else: print >> texFile, " & ",
          print >> texFile, " & \\textit{\\textbf{ME%s%s/%s}}" % (sEndcap, disk, ring),
          for varIndex in varIndexes:
            data = self.data[varIndex][1][endcap-1][disk-1][ring-1][0]
            print >> texFile, (" & %s" % data),
          if disk == 4 and ring == 2:
            if endcap == 1: print >> texFile, "\\\\ \\hline \\hline"
            else:           print >> texFile, "\\\\ \\hline"
          else:
            if (disk == 1 and ring ==3) or (disk != 1 and ring == 2): print >> texFile, "\\\\ \\cline{2-%s}" % nRows
            else: print >> texFile, "\\\\ \\cline{3-%s}" % nRows
    
    print >> texFile, "\\end{tabular}"
    print >> texFile, "\\end{center}\n"
    print >> texFile, "\\end{footnotesize}"
    print >> texFile, "\\end{table}\n"
    print >> texFile, "%\\end{landscape}"
    texFile.close()
      
    if isComplete != 0:
      PrintTexTrailer(texFileName)
