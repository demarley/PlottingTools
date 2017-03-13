import ROOT, array, os, sys, re, math, random
from math import *
import numpy as np

sys.path.append(".")
from signConventions import *

execfile("geometryXMLparser.py")
execfile("plotscripts.py")
execfile("tdrStyle.py")

alignmentName = sys.argv[1] 
boolPrintTrue = sys.argv[2] 
xmlfile_ref   = sys.argv[3]
xmlfile1      = "Geometries/"+alignmentName+".xml"

folderName = "RESULT/"+alignmentName+"/"

pngPath = folderName+"/PNG/"
if not os.path.exists(pngPath):
   os.makedirs(pngPath)
pdfPath = folderName+"/PDF/"
if not os.path.exists(pdfPath):
   os.makedirs(pdfPath)

g1 = MuonGeometry(xmlfile1)
g_ref = MuonGeometry(xmlfile_ref)

c1 = ROOT.TCanvas("canvas", "canvas")
c1.SetCanvasSize(900,900)

T1 = ROOT.TLatex()
T1.SetTextFont(43)
T1.SetTextSize(40)

legend = ROOT.TLegend(.17,.935,.9,1.)
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(0)
legend.SetTextFont(42)
legend.SetTextSize(0.045)
legend.SetMargin(0.13)
legend2 = ROOT.TLegend(.22,.85,.9,.9)
legend2.SetFillColor(ROOT.kWhite)
legend2.SetBorderSize(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.019)
legend2.SetMargin(0.13)
legend3 = ROOT.TLegend(.22,.15,.9,.2)
legend3.SetFillColor(ROOT.kWhite)
legend3.SetBorderSize(0)
legend3.SetTextFont(42)
legend3.SetTextSize(0.019)
legend3.SetMargin(0.13)

X_vec=[]; Y_vec=[]; Z_vec=[]; PhiX_vec=[]; PhiY_vec=[]; PhiZ_vec=[];
index=0
for wheel in (-2, -1, 0, 1, 2):
  for station in (1, 2, 3, 4):

    dx_bins, dx_min, dx_max = 1000, -0.4, 0.4
    dy_bins, dy_min, dy_max = 1000, -0.4, 0.4
    dz_bins, dz_min, dz_max = 1000, -1.2, 1.2
    dphix_bins, dphix_min, dphix_max = 1000, -1.5, 1.5
    dphiy_bins, dphiy_min, dphiy_max = 1000, -1.5, 1.5
    dphiz_bins, dphiz_min, dphiz_max = 1000, -0.4, 0.4
    if( wheel==2 or wheel==-2 ):
      dx_bins, dx_min, dx_max = 1000, -0.5, 0.5
      dy_bins, dy_min, dy_max = 1000, -1., 1.
      dz_bins, dz_min, dz_max = 1000, -1.5, 1.5
      dphix_bins, dphix_min, dphix_max = 1000, -1.5, 1.5
      dphiy_bins, dphiy_min, dphiy_max = 1000, -1.5, 1.5
      dphiz_bins, dphiz_min, dphiz_max = 1000, -0.5, 0.5
   
    h_dx_dy = ROOT.TH2F("h_dx_dy_"+str(index), "h_dx_dy", dx_bins, dx_min, dx_max, dy_bins, dy_min, dy_max)
    h_dx_dy.SetXTitle("#delta x (mm)")
    h_dx_dy.SetYTitle("#delta y (mm)")
    h_dx_dy.SetMarkerColor(2)
    h_dx_dy.SetMarkerSize(2)
    h_dx_dy.StatOverflows(ROOT.kTRUE)
    
    h_dx_dz = ROOT.TH2F("h_dx_dz_"+str(index), "h_dx_dz", dx_bins, dx_min, dx_max, dz_bins, dz_min, dz_max)
    h_dx_dz.SetXTitle("#delta x (mm)")
    h_dx_dz.SetYTitle("#delta z (mm)")
    h_dx_dz.SetMarkerColor(2)
    h_dx_dz.SetMarkerSize(2)
    h_dx_dz.StatOverflows(ROOT.kTRUE)
    
    h_dx_dphix = ROOT.TH2F("h_dx_dphix_"+str(index), "h_dx_dphix", dx_bins, dx_min, dx_max, dphix_bins, dphix_min, dphix_max)
    h_dx_dphix.SetXTitle("#delta x (mm)")
    h_dx_dphix.SetYTitle("#delta #phi_{x} (mrad)")
    h_dx_dphix.SetMarkerColor(2)
    h_dx_dphix.SetMarkerSize(2)
    h_dx_dphix.StatOverflows(ROOT.kTRUE)
    
    h_dx_dphiy = ROOT.TH2F("h_dx_dphiy_"+str(index), "h_dx_dphiy", dx_bins, dx_min, dx_max, dphiy_bins, dphiy_min, dphiy_max)
    h_dx_dphiy.SetXTitle("#delta x (mm)")
    h_dx_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
    h_dx_dphiy.SetMarkerColor(2)
    h_dx_dphiy.SetMarkerSize(2)
    h_dx_dphiy.StatOverflows(ROOT.kTRUE)
    
    h_dx_dphiz = ROOT.TH2F("h_dx_dphiz_"+str(index), "h_dx_dphiz", dx_bins, dx_min, dx_max, dphiz_bins, dphiz_min, dphiz_max)
    h_dx_dphiz.SetXTitle("#delta x (mm)")
    h_dx_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
    h_dx_dphiz.SetMarkerColor(2)
    h_dx_dphiz.SetMarkerSize(2)
    h_dx_dphiz.StatOverflows(ROOT.kTRUE)
    
    h_dy_dz = ROOT.TH2F("h_dy_dz_"+str(index), "h_dy_dz", dy_bins, dy_min, dy_max, dz_bins, dz_min, dz_max)
    h_dy_dz.SetXTitle("#delta y (mm)")
    h_dy_dz.SetYTitle("#delta z (mm)")
    h_dy_dz.SetMarkerColor(2)
    h_dy_dz.SetMarkerSize(2)
    h_dy_dz.StatOverflows(ROOT.kTRUE)
    
    h_dy_dphix = ROOT.TH2F("h_dy_dphix_"+str(index), "h_dy_dphix", dy_bins, dy_min, dy_max, dphix_bins, dphix_min, dphix_max)
    h_dy_dphix.SetXTitle("#delta y (mm)")
    h_dy_dphix.SetYTitle("#delta #phi_{x} (mrad)")
    h_dy_dphix.SetMarkerColor(2)
    h_dy_dphix.SetMarkerSize(2)
    h_dy_dphix.StatOverflows(ROOT.kTRUE)
    
    h_dy_dphiy = ROOT.TH2F("h_dy_dphiy_"+str(index), "h_dy_dphiy", dy_bins, dy_min, dy_max, dphiy_bins, dphiy_min, dphiy_max)
    h_dy_dphiy.SetXTitle("#delta y (mm)")
    h_dy_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
    h_dy_dphiy.SetMarkerColor(2)
    h_dy_dphiy.SetMarkerSize(2)
    h_dy_dphiy.StatOverflows(ROOT.kTRUE)
    
    h_dy_dphiz = ROOT.TH2F("h_dy_dphiz_"+str(index), "h_dy_dphiz", dy_bins, dy_min, dy_max, dphiz_bins, dphiz_min, dphiz_max)
    h_dy_dphiz.SetXTitle("#delta y (mm)")
    h_dy_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
    h_dy_dphiz.SetMarkerColor(2)
    h_dy_dphiz.SetMarkerSize(2)
    h_dy_dphiz.StatOverflows(ROOT.kTRUE)
    
    
    h_dz_dphix = ROOT.TH2F("h_dz_dphix_"+str(index), "h_dz_dphix", dz_bins, dz_min, dz_max, dphix_bins, dphix_min, dphix_max)
    h_dz_dphix.SetXTitle("#delta z (mm)")
    h_dz_dphix.SetYTitle("#delta #phi_{x} (mrad)")
    h_dz_dphix.SetMarkerColor(2)
    h_dz_dphix.SetMarkerSize(2)
    h_dz_dphix.StatOverflows(ROOT.kTRUE)
    
    h_dz_dphiy = ROOT.TH2F("h_dz_dphiy_"+str(index), "h_dz_dphiy", dz_bins, dz_min, dz_max, dphiy_bins, dphiy_min, dphiy_max)
    h_dz_dphiy.SetXTitle("#delta z (mm)")
    h_dz_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
    h_dz_dphiy.SetMarkerColor(2)
    h_dz_dphiy.SetMarkerSize(2)
    h_dz_dphiy.StatOverflows(ROOT.kTRUE)
    
    h_dz_dphiz = ROOT.TH2F("h_dz_dphiz_"+str(index), "h_dz_dphiz", dz_bins, dz_min, dz_max, dphiz_bins, dphiz_min, dphiz_max)
    h_dz_dphiz.SetXTitle("#delta z (mm)")
    h_dz_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
    h_dz_dphiz.SetMarkerColor(2)
    h_dz_dphiz.SetMarkerSize(2)
    h_dz_dphiz.StatOverflows(ROOT.kTRUE)
    
   
    h_dphix_dphiy = ROOT.TH2F("h_dphix_dphiy_"+str(index), "h_dphix_dphiy", dphix_bins, dphix_min, dphix_max, dphiy_bins, dphiy_min, dphiy_max)
    h_dphix_dphiy.SetXTitle("#delta #phi_{x} (mrad)")
    h_dphix_dphiy.SetYTitle("#delta #phi_{y} (mrad)")
    h_dphix_dphiy.SetMarkerColor(2)
    h_dphix_dphiy.SetMarkerSize(2)
    h_dphix_dphiy.StatOverflows(ROOT.kTRUE)
    
    h_dphix_dphiz = ROOT.TH2F("h_dphix_dphiz_"+str(index), "h_dphix_dphiz", dphix_bins, dphix_min, dphix_max, dphiz_bins, dphiz_min, dphiz_max)
    h_dphix_dphiz.SetXTitle("#delta #phi_{x} (mrad)")
    h_dphix_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
    h_dphix_dphiz.SetMarkerColor(2)
    h_dphix_dphiz.SetMarkerSize(2)
    h_dphix_dphiz.StatOverflows(ROOT.kTRUE)
    
    
    h_dphiy_dphiz = ROOT.TH2F("h_dphiy_dphiz_"+str(index), "h_dphiy_dphiz", dphiy_bins, dphiy_min, dphiy_max, dphiz_bins, dphiz_min, dphiz_max)
    h_dphiy_dphiz.SetXTitle("#delta #phi_{y} (mrad)")
    h_dphiy_dphiz.SetYTitle("#delta #phi_{z} (mrad)")
    h_dphiy_dphiz.SetMarkerColor(2)
    h_dphiy_dphiz.SetMarkerSize(2)
    h_dphiy_dphiz.StatOverflows(ROOT.kTRUE)
    index=index+1
    ##
    h_dx_dy.Reset("ICESM")
    h_dx_dz.Reset("ICESM")
    h_dx_dphix.Reset("ICESM")
    h_dx_dphiy.Reset("ICESM")
    h_dx_dphiz.Reset("ICESM")
    
    h_dy_dz.Reset("ICESM")
    h_dy_dphix.Reset("ICESM")
    h_dy_dphiy.Reset("ICESM")
    h_dy_dphiz.Reset("ICESM")
    
    h_dz_dphix.Reset("ICESM")
    h_dz_dphiy.Reset("ICESM")
    h_dz_dphiz.Reset("ICESM")
    
    h_dphix_dphiy.Reset("ICESM")
    h_dphix_dphiz.Reset("ICESM")
    
    h_dphiy_dphiz.Reset("ICESM")
    
    if station != 4: sectors = (1,2,3,4,5,6,7,8,9,10,11,12)
    else: sectors = (1,2,3,4,5,6,7,8,9,10,11,12,13,14)
    for sector in sectors:
      dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
      dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
      dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
      dphix_mrad = 1000.0*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)*signConventions["DT", wheel, station, sector][0]
      dphiy_mrad = 1000.0*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)*signConventions["DT", wheel, station, sector][1]
      dphiz_mrad = 1000.0*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)*signConventions["DT", wheel, station, sector][2]
      X_vec.append(dx_mm); Y_vec.append(dy_mm); Z_vec.append(dz_mm); PhiX_vec.append(dphix_mrad); PhiY_vec.append(dphiy_mrad); PhiZ_vec.append(dphiz_mrad);

      h_dx_dy.Fill(dx_mm, dy_mm)
      h_dx_dz.Fill(dx_mm, dz_mm)
      h_dx_dphix.Fill(dx_mm, dphix_mrad)
      h_dx_dphiy.Fill(dx_mm, dphiy_mrad)
      h_dx_dphiz.Fill(dx_mm, dphiz_mrad)
      
      h_dy_dz.Fill(dy_mm, dz_mm)
      h_dy_dphix.Fill(dy_mm, dphix_mrad)
      h_dy_dphiy.Fill(dy_mm, dphiy_mrad)
      h_dy_dphiz.Fill(dy_mm, dphiz_mrad)
      
      h_dz_dphix.Fill(dz_mm, dphix_mrad)
      h_dz_dphiy.Fill(dz_mm, dphiy_mrad)
      h_dz_dphiz.Fill(dz_mm, dphiz_mrad)
      
      h_dphix_dphiy.Fill(dphix_mrad, dphiy_mrad)
      h_dphix_dphiz.Fill(dphix_mrad, dphiz_mrad)

      h_dphiy_dphiz.Fill(dphiy_mrad, dphiz_mrad)

    wheelStr  = str(wheel);
    wheelStr2 = str(wheel);
    if wheel == -2: wheelStr="p2"; wheelStr2="+2"
    if wheel == -1: wheelStr="p1"; wheelStr2="+1"
    if wheel == 1: wheelStr="m1";  wheelStr2="-1"
    if wheel == 1: wheelStr="m2";  wheelStr2="-2"
    if wheel == 0: wheelStr2=" 0"
    plotsLabel  = "MB_" + str(wheelStr) + "_" + str(station)
    plotsHeader = "MB" + str(wheelStr2) + "/" + str(station) + "/All"

    legend.SetHeader(plotsHeader)    
    np_XY = np.vstack((X_vec,Y_vec))
    legend2.SetHeader(str(np.cov(np_XY)) + " " + str(round(sqrt(np.cov(np_XY)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_XY)[1][1]),2)))
    h_dx_dy.Draw()
    legend.Draw();
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_XY))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_XY))[1]),2)) + " c: " + str( np.cov(np_XY)[0][1]/sqrt(np.cov(np_XY)[0][0]*np.cov(np_XY)[1][1] ) ) );
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dx_dy_" + plotsLabel + ".png"
    pdfName = "DT_corr_dx_dy_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_XZ = np.vstack((X_vec,Z_vec))
    legend2.SetHeader(str(np.cov(np_XZ)) + " " + str(round(sqrt(np.cov(np_XZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_XZ)[1][1]),2)))
    h_dx_dz.Draw()
    legend.Draw();
    legend3.SetHeader(str(np.linalg.eigvals(np.cov(np_XZ)))); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_XZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_XZ))[1]),2)) + " c: " + str( np.cov(np_XZ)[0][1]/sqrt(np.cov(np_XZ)[0][0]*np.cov(np_XZ)[1][1] ) ) );
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dx_dz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dx_dz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_XPhiX = np.vstack((X_vec,PhiX_vec))
    legend2.SetHeader(str(np.cov(np_XPhiX)) + " " + str(round(sqrt(np.cov(np_XPhiX)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_XPhiX)[1][1]),2)))
    h_dx_dphix.Draw()
    legend.Draw(); 
    legend3.SetHeader(str(np.linalg.eigvals(np.cov(np_XPhiX)))); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiX))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiX))[1]),2)) + " c: " + str( np.cov(np_XPhiX)[0][1]/sqrt(np.cov(np_XPhiX)[0][0]*np.cov(np_XPhiX)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dx_dphix_" + plotsLabel + ".png"
    pdfName = "DT_corr_dx_dphix_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_XPhiY = np.vstack((X_vec,PhiY_vec))
    legend2.SetHeader(str(np.cov(np_XPhiY)) + " " + str(round(sqrt(np.cov(np_XPhiY)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_XPhiY)[1][1]),2)))
    h_dx_dphiy.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiY))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiY))[1]),2)) + " c: " + str( np.cov(np_XPhiY)[0][1]/sqrt(np.cov(np_XPhiY)[0][0]*np.cov(np_XPhiY)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dx_dphiy_" + plotsLabel + ".png"
    pdfName = "DT_corr_dx_dphiy_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_XPhiZ = np.vstack((X_vec,PhiZ_vec))
    legend2.SetHeader(str(np.cov(np_XPhiZ)) + " " + str(round(sqrt(np.cov(np_XPhiZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_XPhiZ)[1][1]),2)))
    h_dx_dphiz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_XPhiZ))[1]),2)) + " c: " + str( np.cov(np_XPhiZ)[0][1]/sqrt(np.cov(np_XPhiZ)[0][0]*np.cov(np_XPhiZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dx_dphiz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dx_dphiz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)


    np_YZ = np.vstack((Y_vec,Z_vec))
    legend2.SetHeader(str(np.cov(np_YZ)) + " " + str(round(sqrt(np.cov(np_YZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_YZ)[1][1]),2)))
    h_dy_dz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_YZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_YZ))[1]),2)) + " c: " + str( np.cov(np_YZ)[0][1]/sqrt(np.cov(np_YZ)[0][0]*np.cov(np_YZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dy_dz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dy_dz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_YPhiX = np.vstack((Y_vec,PhiX_vec))
    legend2.SetHeader(str(np.cov(np_YPhiX)) + " " + str(round(sqrt(np.cov(np_YPhiX)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_YPhiX)[1][1]),2)))
    h_dy_dphix.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiX))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiX))[1]),2)) + " c: " + str( np.cov(np_YPhiX)[0][1]/sqrt(np.cov(np_YPhiX)[0][0]*np.cov(np_YPhiX)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dy_dphix_" + plotsLabel + ".png"
    pdfName = "DT_corr_dy_dphix_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_YPhiY = np.vstack((Y_vec,PhiY_vec))
    legend2.SetHeader(str(np.cov(np_YPhiY)) + " " + str(round(sqrt(np.cov(np_YPhiY)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_YPhiY)[1][1]),2)))
    h_dy_dphiy.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiY))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiY))[1]),2)) + " c: " + str( np.cov(np_YPhiY)[0][1]/sqrt(np.cov(np_YPhiY)[0][0]*np.cov(np_YPhiY)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dy_dphiy_" + plotsLabel + ".png"
    pdfName = "DT_corr_dy_dphiy_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_YPhiZ = np.vstack((Y_vec,PhiZ_vec))
    legend2.SetHeader(str(np.cov(np_YPhiZ)) + " " + str(round(sqrt(np.cov(np_YPhiZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_YPhiZ)[1][1]),2)))
    h_dy_dphiz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_YPhiZ))[1]),2)) + " c: " + str( np.cov(np_YPhiZ)[0][1]/sqrt(np.cov(np_YPhiZ)[0][0]*np.cov(np_YPhiZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dy_dphiz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dy_dphiz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)


    np_ZPhiX = np.vstack((Z_vec,PhiX_vec))
    legend2.SetHeader(str(np.cov(np_ZPhiX)) + " " + str(round(sqrt(np.cov(np_ZPhiX)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_ZPhiX)[1][1]),2)))
    h_dz_dphix.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiX))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiX))[1]),2)) + " c: " + str( np.cov(np_ZPhiX)[0][1]/sqrt(np.cov(np_ZPhiX)[0][0]*np.cov(np_ZPhiX)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dz_dphix_" + plotsLabel + ".png"
    pdfName = "DT_corr_dz_dphix_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_ZPhiY = np.vstack((Z_vec,PhiY_vec))
    legend2.SetHeader(str(np.cov(np_ZPhiY)) + " " + str(round(sqrt(np.cov(np_ZPhiY)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_ZPhiY)[1][1]),2)))
    h_dz_dphiy.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiY))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiY))[1]),2)) + " c: " + str( np.cov(np_ZPhiY)[0][1]/sqrt(np.cov(np_ZPhiY)[0][0]*np.cov(np_ZPhiY)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dz_dphiy_" + plotsLabel + ".png"
    pdfName = "DT_corr_dz_dphiy_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_ZPhiZ = np.vstack((Z_vec,PhiZ_vec))
    legend2.SetHeader(str(np.cov(np_ZPhiZ)) + " " + str(round(sqrt(np.cov(np_ZPhiZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_ZPhiZ)[1][1]),2)))
    h_dz_dphiz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_ZPhiZ))[1]),2)) + " c: " + str( np.cov(np_ZPhiZ)[0][1]/sqrt(np.cov(np_ZPhiZ)[0][0]*np.cov(np_ZPhiZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dz_dphiz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dz_dphiz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)


    np_PhiXPhiY = np.vstack((PhiX_vec,PhiY_vec))
    legend2.SetHeader(str(np.cov(np_PhiXPhiY)) + " " + str(round(sqrt(np.cov(np_PhiXPhiY)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_PhiXPhiY)[1][1]),2)))
    h_dphix_dphiy.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiXPhiY))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiXPhiY))[1]),2)) + " c: " + str( np.cov(np_PhiXPhiY)[0][1]/sqrt(np.cov(np_PhiXPhiY)[0][0]*np.cov(np_PhiXPhiY)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dphix_dphiy_" + plotsLabel + ".png"
    pdfName = "DT_corr_dphix_dphiy_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)

    np_PhiXPhiZ = np.vstack((PhiX_vec,PhiZ_vec))
    legend2.SetHeader(str(np.cov(np_PhiXPhiZ)) + " " + str(round(sqrt(np.cov(np_PhiXPhiZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_PhiXPhiZ)[1][1]),2)))
    h_dphix_dphiz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiXPhiZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiXPhiZ))[1]),2)) + " c: " + str( np.cov(np_PhiXPhiZ)[0][1]/sqrt(np.cov(np_PhiXPhiZ)[0][0]*np.cov(np_PhiXPhiZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dphix_dphiz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dphix_dphiz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)


    np_PhiYPhiZ = np.vstack((PhiY_vec,PhiZ_vec))
    legend2.SetHeader(str(np.cov(np_PhiYPhiZ)) + " " + str(round(sqrt(np.cov(np_PhiYPhiZ)[0][0]),2)) + " " + str(round(sqrt(np.cov(np_PhiYPhiZ)[1][1]),2)))
    h_dphiy_dphiz.Draw()
    legend.Draw(); 
    legend3.SetHeader( str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiYPhiZ))[0]),2)) + " - " + str(round(sqrt(np.linalg.eigvals(np.cov(np_PhiYPhiZ))[1]),2)) + " c: " + str( np.cov(np_PhiYPhiZ)[0][1]/sqrt(np.cov(np_PhiYPhiZ)[0][0]*np.cov(np_PhiYPhiZ)[1][1] ) ) ); 
    if(boolPrintTrue): legend2.Draw(); legend3.Draw();
    pngName = "DT_corr_dphiy_dphiz_" + plotsLabel + ".png"
    pdfName = "DT_corr_dphiy_dphiz_" + plotsLabel + ".pdf"
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    del X_vec[:]; del Y_vec[:]; del Z_vec[:]; del PhiX_vec[:]; del PhiY_vec[:]; del PhiZ_vec[:];
