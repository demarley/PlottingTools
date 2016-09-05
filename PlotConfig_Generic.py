execfile("Plot_Corrections_1st.py")

plotsHeader = "CMS 2016B  #sqrt{s} = 13 TeV   L_{int} = 2. fb^{-1}"
if (str(sys.argv[2])=="true"):
    isDT = True
else:
    isDT = False
if (str(sys.argv[3])=="true"):
    isCSC = True
else:
    isCSC = False

xmlfile_ref        = sys.argv[1]
xmlfile1           = "Geometries/"+alignmentName+".xml"
referenceName      = sys.argv[4]
correctionName     = sys.argv[5]

#d_bins, d_min, d_max =  100, -4.0, 4.0 # bins and range for corrections
d_bins, d_min, d_max =  200, -10.0, 10.0 # bins and range for corrections
length_factor, angle_factor = 200., 200. # factors for visualization
littleLabel = alignmentName+" - "+referenceName
folderName = "RESULT/"+alignmentName+"/"

isReport = False
reportfile1 = "Geometries/"+alignmentName+"_report.py"
e_bins, e_min, e_max  =  50, 0.0, 0.5 # bins and range for fit uncertainties
p_bins, p_min, p_max  =  100, -10.0, 10.0 # bins and range for pulls

summaryTable = ["dxRMS","dyRMS","dzRMS","dphixRMS","dphiyRMS","dphizRMS"]
#summaryTable = ["dxRMS","exMean","pxRMS","dyRMS","eyMean","pyRMS","dphizRMS","ephizMean","pphizRMS"]
#summaryHtmlCaption = ("<font size=+1>%s (<i>&delta;</i>), alignment fit uncertainties (<i>&sigma;<sub>fit</sub></i>) and pulls for DOF used for alignment <br>averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel))
#summaryTable = ["dxRMS","dyRMS","dphizRMS"]
summaryHtmlCaption = ("<font size=+1>%s (<i>&delta;</i>) for all DOF <br>averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel))

execfile("Plot_Corrections_2nd.py")
