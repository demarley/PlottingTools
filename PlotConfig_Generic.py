execfile("Plot_Corrections_1st.py")

# if alignmentName != "mc_DT-1111-111111_DESRUN2_73_V3_CMSSW_7_3_1_muonGeometry_YuriyStartup_v1_03":
#   print "Error! Mismatch between alignment name \"" + alignmentName + "\" and configuration file name"
#   sys.exit(-1)

#plotsHeader = "CMS Prelim. 2011   #sqrt{s} = 7 TeV   L_{int} = 5.3 fb^{-1}"
#plotsHeader = "CMS 2011   #sqrt{s} = 7 TeV   L_{int} = 5.3 fb^{-1}"
#plotsHeader = "CMS Prelim. 2012 A+B   #sqrt{s} = 8 TeV   L_{int} = 5.7 fb^{-1}"
#plotsHeader = "CMS 2012 A+B   #sqrt{s} = 8 TeV   L_{int} = 5.7 fb^{-1}"
plotsHeader = "CMS Simulation"

isCSC = False
isDT  = True
xmlfile1             = "Geometries/"+alignmentName+".xml"
referenceName        = "MC_53_V14"
xmlfile_ref          = "Geometries/muonGeometry_MC_53_V14_Local.xml" # reference geometry: initial or IDEAL
d_bins, d_min, d_max =  100, -4.0, 4.0 # bins and range for corrections
correctionName       = "Displacements from ideal geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
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
