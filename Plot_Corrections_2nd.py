if isDT == False and isCSC == False:
  print "Error! AlignmentName", alignmentName, "not found"
  exit(-1)

g1 = MuonGeometry(xmlfile1)
g_ref = MuonGeometry(xmlfile_ref)

if isReport:
  execfile(reportfile1)
  report1 = reports

if not os.path.exists(folderName):
   os.makedirs(folderName)
htmlPath = folderName
if not os.path.exists(htmlPath):
   os.makedirs(htmlPath)
texPath = folderName+"/TEX/"
if not os.path.exists(texPath):
   os.makedirs(texPath)
pngPath = folderName+"/PNG/"
if not os.path.exists(pngPath):
   os.makedirs(pngPath)
pdfPath = folderName+"/PDF/"
if not os.path.exists(pdfPath):
   os.makedirs(pdfPath)
svgPath = folderName+"/SVG/"
if not os.path.exists(svgPath):
   os.makedirs(svgPath)

htmlName = "index.html"
#htmlName = alignmentName+".html"
htmlName_d = alignmentName+".d.html" # file for correction
if isReport:
  htmlName_e = alignmentName+".e.html"  # file for uncertainties
  htmlName_p = alignmentName+".p.html"  # file for pulls

texName = alignmentName+".tex"
texName_d  = alignmentName+".d.tex"  # file for correction
if isReport:
  texName_e = alignmentName+".e.tex" # file for uncertainties
  texName_p = alignmentName+".p.tex" # file for pulls

execfile("Util_InitAllHistos.py")

legend.SetHeader(plotsHeader)

# ******************************************************************************
#                            DTs                                                
# ******************************************************************************
if isDT:
  execfile("Plot_Corrections_DT.py")

# ******************************************************************************
#                            CSCs                                               
# ******************************************************************************

elif isCSC:
  execfile("Plot_Corrections_CSC.py")

else:
   sys.exit(-1)
   
#*******************************************************************************
#                           Main output HTML file                               
#*******************************************************************************

htmlFile = htmlPath + htmlName
texFile  = texPath  + texName

PrintHtmlHeader(htmlFile)
PrintHtmlCode(htmlFile,"<font size=\"+2\">Summary for %s</font>" % alignmentName)
PrintHtmlCode(htmlFile,"<p>")

if isDT:
  dtGroupTable.PrintHtml(htmlFile,summaryTable,summaryHtmlCaption, 0)
  dtGroupTable.PrintTex(texFile,summaryTable, ("Summary table %s" % alignmentName), ("tab:summary_%s" % alignmentName), 1)
if isCSC:
  cscGroupTable.PrintHtml(htmlFile,summaryTable,summaryHtmlCaption, 0)
  cscGroupTable.PrintTex(texFile,summaryTable, ("Summary table %s" % alignmentName), ("tab:summary_%s" % alignmentName), 1)



PrintHtmlCode(htmlFile,"<p><hr width=\"100%\">")
PrintHtmlCode(htmlFile,"<p>Additional information:<ul>")
PrintHtmlCode(htmlFile,"<li><a href=\"%s\">%s</a></li>" % (htmlName_d,correctionName) )
if isReport:
  PrintHtmlCode(htmlFile,"<li><a href=\"%s\">Alignment fit uncertainties</a></li>" % (htmlName_e) )
  PrintHtmlCode(htmlFile,"<li><a href=\"%s\">Pulls</a></li>" % (htmlName_p) )

PrintHtmlTrailer(htmlFile)
