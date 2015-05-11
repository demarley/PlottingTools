import ROOT, array, os, re, math, random
from math import *

c1 = ROOT.TCanvas("canvas", "canvas")
c1.SetCanvasSize(900,900)

color = ROOT.TColor
if isDT:
#  fillColor = ROOT.kGreen + 3
  fillColor = color.GetColor("#ffe0a1")
  lineColor = ROOT.kBlack
  yTitle    = "Number of DTs"
elif isCSC:
#  fillColor = ROOT.kBlue -7
  fillColor = color.GetColor("#3ffa3f")
  lineColor = ROOT.kBlack
  yTitle     = "Number of CSCs"
else:
  fillColor = ROOT.kCyan
  lineColor = ROOT.kBlack
  yTitle     = "Number of chambers"

legend = ROOT.TLegend(.17,.935,0.9,1.)
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(0)
legend.SetTextFont(42)
legend.SetTextSize(0.045)
legend.SetMargin(0.13)

# ******************************************************************************
#                     Corrections w.r.t. another geometry                       
# ******************************************************************************

h_dx = ROOT.TH1F("h_dx", "h_dx", d_bins, d_min, d_max)
h_dx.SetXTitle("#delta x (mm)")
h_dx.SetYTitle(yTitle)
h_dx.SetLineColor(lineColor)
h_dx.SetFillColor(fillColor)
h_dx.StatOverflows(ROOT.kTRUE)

h_dy = ROOT.TH1F("h_dy", "h_dy", d_bins, d_min, d_max)
h_dy.SetXTitle("#delta y (mm)")
h_dy.SetYTitle(yTitle)
h_dy.SetLineColor(lineColor)
h_dy.SetFillColor(fillColor)
h_dy.StatOverflows(ROOT.kTRUE)

h_dz = ROOT.TH1F("h_dz", "h_dz", d_bins, d_min, d_max)
h_dz.SetXTitle("#delta z (mm)")
h_dz.SetYTitle(yTitle)
h_dz.SetLineColor(lineColor)
h_dz.SetFillColor(fillColor)
h_dz.StatOverflows(ROOT.kTRUE)

h_dphix = ROOT.TH1F("h_dphix", "h_dphix", d_bins, d_min, d_max)
h_dphix.SetXTitle("#delta #phi_{x} (mrad)")
h_dphix.SetYTitle(yTitle)
h_dphix.SetLineColor(lineColor)
h_dphix.SetFillColor(fillColor)
h_dphix.StatOverflows(ROOT.kTRUE)

h_dphiy = ROOT.TH1F("h_dphiy", "h_dphiy", d_bins, d_min, d_max)
h_dphiy.SetXTitle("#delta #phi_{y} (mrad)")
h_dphiy.SetYTitle(yTitle)
h_dphiy.SetLineColor(lineColor)
h_dphiy.SetFillColor(fillColor)
h_dphiy.StatOverflows(ROOT.kTRUE)

h_dphiz = ROOT.TH1F("h_dphiz", "h_dphiz", d_bins, d_min, d_max)
h_dphiz.SetXTitle("#delta #phi_{z} (mrad)")
h_dphiz.SetYTitle(yTitle)
h_dphiz.SetLineColor(lineColor)
h_dphiz.SetFillColor(fillColor)
h_dphiz.StatOverflows(ROOT.kTRUE)

# ******************************************************************************
#                           Fit Uncertainties                                   
# ******************************************************************************

h_ex = ROOT.TH1F("h_ex", "h_ex", e_bins, e_min, e_max)
h_ex.SetXTitle("#sigma_{fit} x (mm)")
h_ex.SetYTitle(yTitle)
h_ex.SetLineColor(lineColor)
h_ex.SetFillColor(fillColor)
h_ex.StatOverflows(ROOT.kTRUE)

h_ey = ROOT.TH1F("h_ey", "h_ey", e_bins, e_min, e_max)
h_ey.SetXTitle("#sigma_{fit} y (mm)")
h_ey.SetYTitle(yTitle)
h_ey.SetLineColor(lineColor)
h_ey.SetFillColor(fillColor)
h_ey.StatOverflows(ROOT.kTRUE)

h_ez = ROOT.TH1F("h_ez", "h_ez", e_bins, e_min, e_max)
h_ez.SetXTitle("#sigma_{fit} z (mm)")
h_ez.SetYTitle(yTitle)
h_ez.SetLineColor(lineColor)
h_ez.SetFillColor(fillColor)
h_ez.StatOverflows(ROOT.kTRUE)

h_ephix = ROOT.TH1F("h_ephix", "h_ephix", e_bins, e_min, e_max)
h_ephix.SetXTitle("#sigma_{fit} #phi_{x} (mrad)")
h_ephix.SetYTitle(yTitle)
h_ephix.SetLineColor(lineColor)
h_ephix.SetFillColor(fillColor)
h_ephix.StatOverflows(ROOT.kTRUE)

h_ephiy = ROOT.TH1F("h_ephiy", "h_ephiy", e_bins, e_min, e_max)
h_ephiy.SetXTitle("#sigma_{fit} #phi_{y} (mrad)")
h_ephiy.SetYTitle(yTitle)
h_ephiy.SetLineColor(lineColor)
h_ephiy.SetFillColor(fillColor)
h_ephiy.StatOverflows(ROOT.kTRUE)

h_ephiz = ROOT.TH1F("h_ephiz", "h_ephiz", e_bins, e_min, e_max)
h_ephiz.SetXTitle("#sigma_{fit} #phi_{z} (mrad)")
h_ephiz.SetYTitle(yTitle)
h_ephiz.SetLineColor(lineColor)
h_ephiz.SetFillColor(fillColor)
h_ephiz.StatOverflows(ROOT.kTRUE)

# ******************************************************************************
#                                  Pulls                                        
# ******************************************************************************

h_px = ROOT.TH1F("h_px", "h_px", p_bins, p_min, p_max)
h_px.SetXTitle("#delta x / #sigma_{fit} x")
h_px.SetYTitle(yTitle)
h_px.SetLineColor(lineColor)
h_px.SetFillColor(fillColor)
h_px.StatOverflows(ROOT.kTRUE)

h_py = ROOT.TH1F("h_py", "h_py", p_bins, p_min, p_max)
h_py.SetXTitle("#delta y / #sigma_{fit} y")
h_py.SetYTitle(yTitle)
h_py.SetLineColor(lineColor)
h_py.SetFillColor(fillColor)
h_py.StatOverflows(ROOT.kTRUE)

h_pz = ROOT.TH1F("h_pz", "h_pz", p_bins, p_min, p_max)
h_pz.SetXTitle("#delta z / #sigma_{fit} z")
h_pz.SetYTitle(yTitle)
h_pz.SetLineColor(lineColor)
h_pz.SetFillColor(fillColor)
h_pz.StatOverflows(ROOT.kTRUE)

h_pphix = ROOT.TH1F("h_pphix", "h_pphix", p_bins, p_min, p_max)
h_pphix.SetXTitle("#delta #phi_{x} / #sigma_{fit} #phi_{x}")
h_pphix.SetYTitle(yTitle)
h_pphix.SetLineColor(lineColor)
h_pphix.SetFillColor(fillColor)
h_pphix.StatOverflows(ROOT.kTRUE)

h_pphiy = ROOT.TH1F("h_pphiy", "h_pphiy", p_bins, p_min, p_max)
h_pphiy.SetXTitle("#delta #phi_{y} / #sigma_{fit} #phi_{y}")
h_pphiy.SetYTitle(yTitle)
h_pphiy.SetLineColor(lineColor)
h_pphiy.SetFillColor(fillColor)
h_pphiy.StatOverflows(ROOT.kTRUE)

h_pphiz = ROOT.TH1F("h_pphiz", "h_pphiz", p_bins, p_min, p_max)
h_pphiz.SetXTitle("#delta #phi_{z} / #sigma_{fit} #phi_{z}")
h_pphiz.SetYTitle(yTitle)
h_pphiz.SetLineColor(lineColor)
h_pphiz.SetFillColor(fillColor)
h_pphiz.StatOverflows(ROOT.kTRUE)
