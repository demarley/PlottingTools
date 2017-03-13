from geometryDiffVisualization import *
import operator

for station in 1,2,3,4:
  imageName = alignmentName+"-"+referenceName+("__MBs%s" % station)
  svgName = imageName+".svg"
  draw_station(g1, g_ref, station, svgPath+svgName, length_factor, angle_factor)
  pngName = imageName+".png"
  retvalue = os.system("convert -density 104.2 %s %s" % (svgPath+svgName, pngPath+pngName) )

for wheel in -2,-1,0,1,2:
  imageName = alignmentName+"-"+referenceName+("__MBw%s" % wheel)
  svgName = imageName+".svg"
  draw_wheel(g1, g_ref, wheel, svgPath+svgName, length_factor, angle_factor)
  pngName = imageName+".png"
  retvalue = os.system("convert -density 104.2 %s %s" % (svgPath+svgName, pngPath+pngName) )

if isReport:
  for r1 in report1:
    if ( r1.postal_address[0] == "DT" and r1.status == "PASS") :
      wheel   = r1.postal_address[1]
      station = r1.postal_address[2]
      sector  = r1.postal_address[3]
      dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
      h_dx.Fill(dx_mm)
      ex_mm = 10.*r1.deltax.error
      h_ex.Fill(ex_mm)
      if ex_mm != 0.0: h_px.Fill(dx_mm/ex_mm)
      dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
      h_dy.Fill(dy_mm)
      if ( station != 4 ) :
        ey_mm = 10.*r1.deltay.error
        h_ey.Fill(ey_mm)
        if ey_mm != 0.0: h_py.Fill(dy_mm/ey_mm)
      dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
      h_dz.Fill(dz_mm)
      ez_mm = 10.*r1.deltaz.error
      h_ez.Fill(ez_mm)
      if ez_mm != 0.0: h_pz.Fill(dz_mm/ez_mm)
      dphix_mrad = 1000.0*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)*signConventions["DT", wheel, station, sector][0]
      h_dphix.Fill(dphix_mrad)
      ephix_mrad = 1000.*r1.deltaphix.error
      h_ephix.Fill(ephix_mrad)
      if ephix_mrad != 0.0: h_pphix.Fill(dphix_mrad/ephix_mrad)
      dphiy_mrad = 1000.0*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)*signConventions["DT", wheel, station, sector][1]
      h_dphiy.Fill(dphiy_mrad)
      ephiy_mrad = 1000.*r1.deltaphiy.error
      h_ephiy.Fill(ephiy_mrad)
      if ephiy_mrad != 0.0: h_pphiy.Fill(dphiy_mrad/ephiy_mrad)
      dphiz_mrad = 1000.0*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)*signConventions["DT", wheel, station, sector][2]
      h_dphiz.Fill(dphiz_mrad)
      ephiz_mrad = 1000.*r1.deltaphiz.error
      h_ephiz.Fill(ephiz_mrad)
      if ephiz_mrad != 0.0: h_pphiz.Fill(dphiz_mrad/ephiz_mrad)
else:
  for wheel in -2, -1, 0, +1, +2:
    for station in 1, 2, 3, 4:
      if station != 4: sectors = (1,2,3,4,5,6,7,8,9,10,11,12)
      else: sectors = (1,2,3,4,5,6,7,8,9,10,11,12,13,14)
      for sector in sectors:
        dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
        h_dx.Fill(dx_mm)
        dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
        h_dy.Fill(dy_mm)
        dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
        h_dz.Fill(dz_mm)
        dphix_mrad = 1000.0*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)*signConventions["DT", wheel, station, sector][0]
        h_dphix.Fill(dphix_mrad)
        dphiy_mrad = 1000.0*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)*signConventions["DT", wheel, station, sector][1]
        h_dphiy.Fill(dphiy_mrad)
        dphiz_mrad = 1000.0*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)*signConventions["DT", wheel, station, sector][2]
        h_dphiz.Fill(dphiz_mrad)

#*******************************************************************************

systemPrettyName = "MB ALL"
histTitle = systemPrettyName+": "+correctionName

h_dx.SetTitle(histTitle)
fit = FitAndDraw(h_dx, littleLabel, 0)
legend.Draw()
pngName = "DT_dx.png"
pdfName = "DT_dx.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)

h_dy.SetTitle(histTitle)
fit = FitAndDraw(h_dy, littleLabel, 0)
legend.Draw()
pngName = "DT_dy.png"
pdfName = "DT_dy.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)

h_dz.SetTitle(histTitle)
fit = FitAndDraw(h_dz, littleLabel, 0)
legend.Draw()
pngName = "DT_dz.png"
pdfName = "DT_dz.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)

h_dphix.SetTitle(histTitle)
fit = FitAndDraw(h_dphix, littleLabel, 0)
legend.Draw()
pngName = "DT_dphix.png"
pdfName = "DT_dphix.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)

h_dphiy.SetTitle(histTitle)
fit = FitAndDraw(h_dphiy, littleLabel, 0)
legend.Draw()
pngName = "DT_dphiy.png"
pdfName = "DT_dphiy.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)

h_dphiz.SetTitle(histTitle)
fit = FitAndDraw(h_dphiz, littleLabel, 0)
legend.Draw()
pngName = "DT_dphiz.png"
pdfName = "DT_dphiz.pdf"
c1.SaveAs(pngPath+pngName)
c1.SaveAs(pdfPath+pdfName)


#*******************************************************************************

if isReport:
  histTitle = systemPrettyName+": Alignment fit uncertainties"
  
  h_ex.SetTitle(histTitle)
  fit = FitAndDraw(h_ex, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ex.png"
  pdfName = "DT_ex.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_ey.SetTitle(histTitle)
  fit = FitAndDraw(h_ey, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ey.png"
  pdfName = "DT_ey.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_ez.SetTitle(histTitle)
  fit = FitAndDraw(h_ez, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ez.png"
  pdfName = "DT_ez.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_ephix.SetTitle(histTitle)
  fit = FitAndDraw(h_ephix, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ephix.png"
  pdfName = "DT_ephix.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_ephiy.SetTitle(histTitle)
  fit = FitAndDraw(h_ephiy, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ephiy.png"
  pdfName = "DT_ephiy.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_ephiz.SetTitle(histTitle)
  fit = FitAndDraw(h_ephiz, alignmentName, 0)
  legend.Draw()
  pngName = "DT_ephiz.png"
  pdfName = "DT_ephiz.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

  #*******************************************************************************

  histTitle = systemPrettyName+": Pulls"
  
  h_px.SetTitle(histTitle) 
  fit = FitAndDraw(h_px, littleLabel, 1)
  legend.Draw()
  pngName = "DT_px.png"
  pdfName = "DT_px.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_py.SetTitle(histTitle)
  fit = FitAndDraw(h_py, littleLabel, 1)
  legend.Draw()
  pngName = "DT_py.png"
  pdfName = "DT_py.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_pz.SetTitle(histTitle)
  fit = FitAndDraw(h_pz, littleLabel, 1)
  legend.Draw()
  pngName = "DT_pz.png"
  pdfName = "DT_pz.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_pphix.SetTitle(histTitle)
  fit = FitAndDraw(h_pphix, littleLabel, 1)
  legend.Draw()
  pngName = "DT_pphix.png"
  pdfName = "DT_pphix.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_pphiy.SetTitle(histTitle)
  fit = FitAndDraw(h_pphiy, littleLabel, 1)
  legend.Draw()
  pngName = "DT_pphiy.png"
  pdfName = "DT_pphiy.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)
  
  h_pphiz.SetTitle(histTitle)
  fit = FitAndDraw(h_pphiz, littleLabel, 1)
  legend.Draw()
  pngName = "DT_pphiz.png"
  pdfName = "DT_pphiz.pdf"
  c1.SaveAs(pngPath+pngName)
  c1.SaveAs(pdfPath+pdfName)

#*******************************************************************************

dtGroupTable = DtGroupTable()

dtGroupTable.AddDtGroupVar("dxRMS",         "&delta;x (mm) <br>RMS",                           "$RMS(\\delta x)$",                     "mm")
dtGroupTable.AddDtGroupVar("dxGaussSig",    "&delta;x (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta x)$",         "mm")
dtGroupTable.AddDtGroupVar("dyRMS",         "&delta;y (mm) <br>RMS",                           "$RMS(\\delta y)$",                     "mm")
dtGroupTable.AddDtGroupVar("dyGaussSig",    "&delta;y (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta y)$",         "mm")
dtGroupTable.AddDtGroupVar("dzRMS",         "&delta;z (mm) <br>RMS",                           "$RMS(\\delta z)$",                     "mm")
dtGroupTable.AddDtGroupVar("dzGaussSig",    "&delta;z (mm) <br>Gauss Sigma",                   "$\\sigma_{Gauss}(\\delta z)$",         "mm")
dtGroupTable.AddDtGroupVar("dphixRMS",      "&delta;&phi;<sub>x</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{x})$",             "mrad")
dtGroupTable.AddDtGroupVar("dphixGaussSig", "&delta;&phi;<sub>x</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{x})$", "mrad")
dtGroupTable.AddDtGroupVar("dphiyRMS",      "&delta;&phi;<sub>y</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{y})$",             "mrad")
dtGroupTable.AddDtGroupVar("dphiyGaussSig", "&delta;&phi;<sub>y</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{y})$", "mrad")
dtGroupTable.AddDtGroupVar("dphizRMS",      "&delta;&phi;<sub>z</sub> (mrad) <br>RMS",         "$RMS(\\delta \\phi_{z})$",             "mrad")
dtGroupTable.AddDtGroupVar("dphizGaussSig", "&delta;&phi;<sub>z</sub> (mrad) <br>Gauss Sigma", "$\\sigma_{Gauss}(\\delta \\phi_{z})$", "mrad")

dtGroupTable.AddDtGroupVar("exMean",         "&sigma;<sub>fit</sub>x (mm) <br>Mean",                         "$Mean(\\sigma_{fit} x) $",               "mm")
dtGroupTable.AddDtGroupVar("exGaussMean",    "&sigma;<sub>fit</sub>x (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} x) $",       "mm")
dtGroupTable.AddDtGroupVar("eyMean",         "&sigma;<sub>fit</sub>y (mm) <br>Mean",                         "$Mean(\\sigma_{fit} y) $",               "mm")
dtGroupTable.AddDtGroupVar("eyGaussMean",    "&sigma;<sub>fit</sub>y (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} y) $",       "mm")
dtGroupTable.AddDtGroupVar("ezMean",         "&sigma;<sub>fit</sub>z (mm) <br>Mean",                         "$Mean(\\sigma_{fit} z) $",               "mm")
dtGroupTable.AddDtGroupVar("ezGaussMean",    "&sigma;<sub>fit</sub>z (mm) <br>Gauss Mean",                   "$Mean_{Gauss}(\\sigma_{fit} z) $",       "mm")
dtGroupTable.AddDtGroupVar("ephixMean",      "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_x) $",         "mrad")
dtGroupTable.AddDtGroupVar("ephixGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>x</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_x) $", "mrad")
dtGroupTable.AddDtGroupVar("ephiyMean",      "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_y) $",         "mrad")
dtGroupTable.AddDtGroupVar("ephiyGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>y</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_y) $", "mrad")
dtGroupTable.AddDtGroupVar("ephizMean",      "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Mean",       "$Mean(\\sigma_{fit} \\phi_z) $",         "mrad")
dtGroupTable.AddDtGroupVar("ephizGaussMean", "&sigma;<sub>fit</sub>&phi;<sub>z</sub> (mrad) <br>Gauss Mean", "$Mean_{Gauss}(\\sigma_{fit} \\phi_z) $", "mrad")

dtGroupTable.AddDtGroupVar("pxRMS","x pull <br>RMS",                                 "$RMS(P x)$",                     None)
dtGroupTable.AddDtGroupVar("pxGaussSig","x pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P x)$",         None)
dtGroupTable.AddDtGroupVar("pyRMS","y pull <br>RMS",                                 "$RMS(P y)$",                     None)
dtGroupTable.AddDtGroupVar("pyGaussSig","y pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P y)$",         None)
dtGroupTable.AddDtGroupVar("pzRMS","z pull <br>RMS",                                 "$RMS(P z)$",                     None)
dtGroupTable.AddDtGroupVar("pzGaussSig","z pull <br>Gauss Sigma",                    "$\\sigma_{Gauss}(P z)$",         None)
dtGroupTable.AddDtGroupVar("pphixRMS","&phi;<sub>x</sub> pull <br>RMS",              "$RMS(P \\phi_{x})$",             None)
dtGroupTable.AddDtGroupVar("pphixGaussSig","&phi;<sub>x</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{x})$", None)
dtGroupTable.AddDtGroupVar("pphiyRMS","&phi;<sub>y</sub> pull <br>RMS",              "$RMS(P \\phi_{y})$",             None)
dtGroupTable.AddDtGroupVar("pphiyGaussSig","&phi;<sub>y</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{y})$", None)
dtGroupTable.AddDtGroupVar("pphizRMS","&phi;<sub>z</sub> pull <br>RMS",              "$RMS(P \\phi_{z})$",             None)
dtGroupTable.AddDtGroupVar("pphizGaussSig","&phi;<sub>z</sub> pull <br>Gauss Sigma", "$\\sigma_{Gauss}(P \\phi_{z})$", None)

dtTab_dx    = DtTable()
dtTab_dy    = DtTable()
dtTab_dz    = DtTable()
dtTab_dphix = DtTable()
dtTab_dphiy = DtTable()
dtTab_dphiz = DtTable()

dtTab_ex    = DtTable()
dtTab_ey    = DtTable()
dtTab_ez    = DtTable()
dtTab_ephix = DtTable()
dtTab_ephiy = DtTable()
dtTab_ephiz = DtTable()

dtTab_px    = DtTable()
dtTab_py    = DtTable()
dtTab_pz    = DtTable()
dtTab_pphix = DtTable()
dtTab_pphiy = DtTable()
dtTab_pphiz = DtTable()

map_ID_Diff_x={}
map_ID_Diff_y={}
map_ID_Diff_z={}
map_ID_Diff_phix={}
map_ID_Diff_phiy={}
map_ID_Diff_phiz={}
for wheel in +2, +1, 0, -1, -2:
  for station in 1, 2, 3, 4:
    h_dx.Reset("ICESM")
    h_dy.Reset("ICESM")
    h_dz.Reset("ICESM")
    h_dphix.Reset("ICESM")
    h_dphiy.Reset("ICESM")
    h_dphiz.Reset("ICESM")
    h_ex.Reset("ICESM")
    h_ey.Reset("ICESM")
    h_ez.Reset("ICESM")
    h_ephix.Reset("ICESM")
    h_ephiy.Reset("ICESM")
    h_ephiz.Reset("ICESM")
    h_px.Reset("ICESM")
    h_py.Reset("ICESM")
    h_pz.Reset("ICESM")
    h_pphix.Reset("ICESM")
    h_pphiy.Reset("ICESM")
    h_pphiz.Reset("ICESM")
    
    if isReport:
      for r1 in report1:
        if ( r1.postal_address[0] == "DT" and r1.status == "PASS" and r1.postal_address[1] == wheel and r1.postal_address[2] == station) :
          sector  = r1.postal_address[3]
          dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
          h_dx.Fill(dx_mm)
          dtTab_dx.FillDt(wheel, station, sector,"%.3f" % dx_mm)
          ex_mm = 10.*r1.deltax.error
          h_ex.Fill(ex_mm)
          dtTab_ex.FillDt(wheel, station, sector,"%.3f" % ex_mm)
          if ex_mm != 0.0:
            px = dx_mm/ex_mm
            h_px.Fill(px)
            dtTab_px.FillDt(wheel, station, sector,"%.3f" % px)
          dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
          h_dy.Fill(dy_mm)
          dtTab_dy.FillDt(wheel, station, sector,"%.3f" % dy_mm)
          if ( station != 4 ) :
            ey_mm = 10.*r1.deltay.error
            h_ey.Fill(ey_mm)
            dtTab_ey.FillDt(wheel, station, sector,"%.3f" % ey_mm)
            if ey_mm != 0.0:
              py = dy_mm/ey_mm
              h_py.Fill(py)
              dtTab_py.FillDt(wheel, station, sector,"%.3f" % py)
          dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
          h_dz.Fill(dz_mm)
          dtTab_dz.FillDt(wheel, station, sector,"%.3f" % dz_mm)
          ez_mm = 10.*r1.deltaz.error
          h_ez.Fill(ez_mm)
          dtTab_ez.FillDt(wheel, station, sector,"%.3f" % ez_mm)
          if ez_mm != 0.0:
            pz = dz_mm/ez_mm
            h_pz.Fill(pz)
            dtTab_pz.FillDt(wheel, station, sector,"%.3f" % pz)
          dphix_mrad = 1000.*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)*signConventions["DT", wheel, station, sector][0]
          h_dphix.Fill(dphix_mrad)
          dtTab_dphix.FillDt(wheel, station, sector,"%.3f" % dphix_mrad)
          ephix_mrad = 1000.*r1.deltaphix.error
          h_ephix.Fill(ephix_mrad)
          dtTab_ephix.FillDt(wheel, station, sector,"%.3f" % ephix_mrad)
          if ephix_mrad != 0.0:
            pphix = dphix_mrad/ephix_mrad
            h_pphix.Fill(pphix)
            dtTab_pphix.FillDt(wheel, station, sector,"%.3f" % pphix)
          dphiy_mrad = 1000.*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)*signConventions["DT", wheel, station, sector][1]
          h_dphiy.Fill(dphiy_mrad)
          dtTab_dphiy.FillDt(wheel, station, sector,"%.3f" % dphiy_mrad)
          ephiy_mrad = 1000.*r1.deltaphiy.error
          h_ephiy.Fill(ephiy_mrad)
          dtTab_ephiy.FillDt(wheel, station, sector,"%.3f" % ephiy_mrad)
          if ephiy_mrad != 0.0:
            pphiy = dphiy_mrad/ephiy_mrad
            h_pphiy.Fill(pphiy)
            dtTab_pphiy.FillDt(wheel, station, sector,"%.3f" % pphiy)
          dphiz_mrad = 1000.*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)*signConventions["DT", wheel, station, sector][2]
          h_dphiz.Fill(dphiz_mrad)
          dtTab_dphiz.FillDt(wheel, station, sector,"%.3f" % dphiz_mrad)
          ephiz_mrad = 1000.*r1.deltaphiz.error
          h_ephiz.Fill(ephiz_mrad)
          dtTab_ephiz.FillDt(wheel, station, sector,"%.3f" % ephiz_mrad)
          if ephiz_mrad != 0.0:
            pphiz = dphiz_mrad/ephiz_mrad
            h_pphiz.Fill(pphiz)
            dtTab_pphiz.FillDt(wheel, station, sector,"%.3f" % pphiz)

    else: # if isReport
      if station != 4: sectors = (1,2,3,4,5,6,7,8,9,10,11,12)
      else: sectors = (1,2,3,4,5,6,7,8,9,10,11,12,13,14)
      for sector in sectors:
        dx_mm = 10.0*(g1.dt[wheel, station, sector].x - g_ref.dt[wheel, station, sector].x)*signConventions["DT", wheel, station, sector][0]
        #if(dx_mm>2 or dx_mm<-2): print dx_mm, " in: ", wheel, station, sector
        h_dx.Fill(dx_mm)
        dtTab_dx.FillDt(wheel, station, sector,"%.3f" % dx_mm)
        dy_mm = 10.0*(g1.dt[wheel, station, sector].y - g_ref.dt[wheel, station, sector].y)*signConventions["DT", wheel, station, sector][1]
        h_dy.Fill(dy_mm)
        dtTab_dy.FillDt(wheel, station, sector,"%.3f" % dy_mm)
        dz_mm = 10.0*(g1.dt[wheel, station, sector].z - g_ref.dt[wheel, station, sector].z)*signConventions["DT", wheel, station, sector][2]
        h_dz.Fill(dz_mm)
        dtTab_dz.FillDt(wheel, station, sector,"%.3f" % dz_mm)
        dphix_mrad = 1000.0*(g1.dt[wheel, station, sector].phix - g_ref.dt[wheel, station, sector].phix)*signConventions["DT", wheel, station, sector][0]
        h_dphix.Fill(dphix_mrad)
        dtTab_dphix.FillDt(wheel, station, sector,"%.3f" % dphix_mrad)
        dphiy_mrad = 1000.0*(g1.dt[wheel, station, sector].phiy - g_ref.dt[wheel, station, sector].phiy)*signConventions["DT", wheel, station, sector][1]
        h_dphiy.Fill(dphiy_mrad)
        dtTab_dphiy.FillDt(wheel, station, sector,"%.3f" % dphiy_mrad)
        dphiz_mrad = 1000.0*(g1.dt[wheel, station, sector].phiz - g_ref.dt[wheel, station, sector].phiz)*signConventions["DT", wheel, station, sector][2]
        h_dphiz.Fill(dphiz_mrad)
        dtTab_dphiz.FillDt(wheel, station, sector,"%.3f" % dphiz_mrad)
        #Find worse 50 chambers
        ID_chamber = "chamber_" + str(wheel) + "_" + str(station) + "_" + str(sector)
        map_ID_Diff_x[ID_chamber] = round(abs(dx_mm),2)
        map_ID_Diff_y[ID_chamber] = round(abs(dy_mm),2)
        map_ID_Diff_z[ID_chamber] = round(abs(dz_mm),2)
        map_ID_Diff_phix[ID_chamber] = round(abs(dphix_mrad),2)
        map_ID_Diff_phiy[ID_chamber] = round(abs(dphiy_mrad),2)
        map_ID_Diff_phiz[ID_chamber] = round(abs(dphiz_mrad),2)

#****** Corrections: save plots and fill tables over homogeneous chambers ******
        
    dtGroupPrettyName = "MB %s/%s/ALL" % (wheel , station)
    histTitle = dtGroupPrettyName+": "+correctionName
    
    h_dx.SetTitle(histTitle)
    fit = FitAndDraw(h_dx, littleLabel)
    legend.Draw()
    pngName = "DT_dx_%s_%s.png" % (wheel , station)
    pdfName = "DT_dx_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dx.GetRMS()
    dtGroupTable.FillDtGroup("dxRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dxGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
    h_dy.SetTitle(histTitle)
    fit = FitAndDraw(h_dy, littleLabel)
    legend.Draw()
    pngName = "DT_dy_%s_%s.png" % (wheel , station)
    pdfName = "DT_dy_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dy.GetRMS()
    dtGroupTable.FillDtGroup("dyRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dyGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
    h_dz.SetTitle(histTitle)
    fit = FitAndDraw(h_dz, littleLabel)
    legend.Draw()
    pngName = "DT_dz_%s_%s.png" % (wheel , station)
    pdfName = "DT_dz_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dz.GetRMS()
    dtGroupTable.FillDtGroup("dzRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dzGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
    h_dphix.SetTitle(histTitle)
    fit = FitAndDraw(h_dphix, littleLabel)
    legend.Draw()
    pngName = "DT_dphix_%s_%s.png" % (wheel , station)
    pdfName = "DT_dphix_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dphix.GetRMS()
    dtGroupTable.FillDtGroup("dphixRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dphixGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
    h_dphiy.SetTitle(histTitle)
    fit = FitAndDraw(h_dphiy, littleLabel)
    legend.Draw()
    pngName = "DT_dphiy_%s_%s.png" % (wheel , station)
    pdfName = "DT_dphiy_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dphiy.GetRMS()
    dtGroupTable.FillDtGroup("dphiyRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dphiyGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
    h_dphiz.SetTitle(histTitle)
    fit = FitAndDraw(h_dphiz, littleLabel)
    legend.Draw()
    pngName = "DT_dphiz_%s_%s.png" % (wheel , station)
    pdfName = "DT_dphiz_%s_%s.pdf" % (wheel , station)
    c1.SaveAs(pngPath+pngName)
    c1.SaveAs(pdfPath+pdfName)
    sRMS = "%.3f" % h_dphiz.GetRMS()
    dtGroupTable.FillDtGroup("dphizRMS", wheel, station, sRMS, "./PNG/"+pngName)
    if fit[0]:
      sSigma = "%.3f" % fit[1].GetParameter(2)
      dtGroupTable.FillDtGroup("dphizGaussSig", wheel, station, sSigma, "./PNG/"+pngName)

#****** Fit uncert: save plots and fill tables over homogeneous chambers *******

    if isReport:      
      histTitle = dtGroupPrettyName+": Alignment fit uncertainties"
      
      h_ex.SetTitle(histTitle)
      fit = FitAndDraw(h_ex, alignmentName)
      legend.Draw()
      pngName = "DT_ex_%s_%s.png" % (wheel , station)
      pdfName = "DT_ex_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sMean = "%.3f" % h_ex.GetMean()
      dtGroupTable.FillDtGroup("exMean", wheel, station, sMean, "./PNG/"+pngName)
      if fit[0]:
        sGaussMean = "%.3f" % fit[1].GetParameter(1)
        dtGroupTable.FillDtGroup("exGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
      
      if ( station != 4 ) :
        h_ey.SetTitle(histTitle)
        fit = FitAndDraw(h_ey, alignmentName)
        legend.Draw()
        pngName = "DT_ey_%s_%s.png" % (wheel , station)
        pdfName = "DT_ey_%s_%s.pdf" % (wheel , station)
        c1.SaveAs(pngPath+pngName)
        c1.SaveAs(pdfPath+pdfName)
        sMean = "%.3f" % h_ey.GetMean()
        dtGroupTable.FillDtGroup("eyMean", wheel, station, sMean, "./PNG/"+pngName)
        if fit[0]:
          sGaussMean = "%.3f" % fit[1].GetParameter(1)
          dtGroupTable.FillDtGroup("eyGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
      
      h_ez.SetTitle(histTitle)
      fit = FitAndDraw(h_ez, alignmentName)
      legend.Draw()
      pngName = "DT_ez_%s_%s.png" % (wheel , station)
      pdfName = "DT_ez_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sMean = "%.3f" % h_ez.GetMean()
      dtGroupTable.FillDtGroup("ezMean", wheel, station, sMean, "./PNG/"+pngName)
      if fit[0]:
        sGaussMean = "%.3f" % fit[1].GetParameter(1)
        dtGroupTable.FillDtGroup("ezGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
      
      h_ephix.SetTitle(histTitle)
      fit = FitAndDraw(h_ephix, alignmentName)
      legend.Draw()
      pngName = "DT_ephix_%s_%s.png" % (wheel , station)
      pdfName = "DT_ephix_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sMean = "%.3f" % h_ephix.GetMean()
      dtGroupTable.FillDtGroup("ephixMean", wheel, station, sMean, "./PNG/"+pngName)
      if fit[0]:
        sGaussMean = "%.3f" % fit[1].GetParameter(1)
        dtGroupTable.FillDtGroup("ephixGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
      
      h_ephiy.SetTitle(histTitle)
      fit = FitAndDraw(h_ephiy, alignmentName)
      legend.Draw()
      pngName = "DT_ephiy_%s_%s.png" % (wheel , station)
      pdfName = "DT_ephiy_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sMean = "%.3f" % h_ephiy.GetMean()
      dtGroupTable.FillDtGroup("ephiyMean", wheel, station, sMean, "./PNG/"+pngName)
      if fit[0]:
        sGaussMean = "%.3f" % fit[1].GetParameter(1)
        dtGroupTable.FillDtGroup("ephiyGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
      
      h_ephiz.SetTitle(histTitle)
      fit = FitAndDraw(h_ephiz, alignmentName)
      legend.Draw()
      pngName = "DT_ephiz_%s_%s.png" % (wheel , station)
      pdfName = "DT_ephiz_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sMean = "%.3f" % h_ephiz.GetMean()
      dtGroupTable.FillDtGroup("ephizMean", wheel, station, sMean, "./PNG/"+pngName)
      if fit[0]:
        sGaussMean = "%.3f" % fit[1].GetParameter(1)
        dtGroupTable.FillDtGroup("ephizGaussMean", wheel, station, sGaussMean, "./PNG/"+pngName)
        
#******** Pulls: save plots and fill tables over homogeneous chambers **********
      
      histTitle = dtGroupPrettyName+": Pulls"
      
      h_px.SetTitle(histTitle)
      fit = FitAndDraw(h_px, littleLabel)
      legend.Draw()
      pngName = "DT_px_%s_%s.png" % (wheel , station)
      pdfName = "DT_px_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sRMS = "%.3f" % h_px.GetRMS()
      dtGroupTable.FillDtGroup("pxRMS", wheel, station, sRMS, "./PNG/"+pngName)
      if fit[0]:
        sSigma = "%.3f" % fit[1].GetParameter(2)
        dtGroupTable.FillDtGroup("pxGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
      
      if ( station != 4 ) :
        h_py.SetTitle(histTitle)
        fit = FitAndDraw(h_py, littleLabel)
        legend.Draw()
        pngName = "DT_py_%s_%s.png" % (wheel , station)
        pdfName = "DT_py_%s_%s.pdf" % (wheel , station)
        c1.SaveAs(pngPath+pngName)
        c1.SaveAs(pdfPath+pdfName)
        sRMS = "%.3f" % h_py.GetRMS()
        dtGroupTable.FillDtGroup("pyRMS", wheel, station, sRMS, "./PNG/"+pngName)
        if fit[0]:
          sSigma = "%.3f" % fit[1].GetParameter(2)
          dtGroupTable.FillDtGroup("pyGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
      
      h_pz.SetTitle(histTitle)
      fit = FitAndDraw(h_pz, littleLabel)
      legend.Draw()
      pngName = "DT_pz_%s_%s.png" % (wheel , station)
      pdfName = "DT_pz_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sRMS = "%.3f" % h_pz.GetRMS()
      dtGroupTable.FillDtGroup("pzRMS", wheel, station, sRMS, "./PNG/"+pngName)
      if fit[0]:
        sSigma = "%.3f" % fit[1].GetParameter(2)
        dtGroupTable.FillDtGroup("pzGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
      
      h_pphix.SetTitle(histTitle)
      fit = FitAndDraw(h_pphix, littleLabel)
      legend.Draw()
      pngName = "DT_pphix_%s_%s.png" % (wheel , station)
      pdfName = "DT_pphix_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sRMS = "%.3f" % h_pphix.GetRMS()
      dtGroupTable.FillDtGroup("pphixRMS", wheel, station, sRMS, "./PNG/"+pngName)
      if fit[0]:
        sSigma = "%.3f" % fit[1].GetParameter(2)
        dtGroupTable.FillDtGroup("pphixGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
      
      h_pphiy.SetTitle(histTitle)
      fit = FitAndDraw(h_pphiy, littleLabel)
      legend.Draw()
      pngName = "DT_pphiy_%s_%s.png" % (wheel , station)
      pdfName = "DT_pphiy_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sRMS = "%.3f" % h_pphiy.GetRMS()
      dtGroupTable.FillDtGroup("pphiyRMS", wheel, station, sRMS, "./PNG/"+pngName)
      if fit[0]:
        sSigma = "%.3f" % fit[1].GetParameter(2)
        dtGroupTable.FillDtGroup("pphiyGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
      
      h_pphiz.SetTitle(histTitle)
      fit = FitAndDraw(h_pphiz, littleLabel)
      legend.Draw()
      pngName = "DT_pphiz_%s_%s.png" % (wheel , station)
      pdfName = "DT_pphiz_%s_%s.pdf" % (wheel , station)
      c1.SaveAs(pngPath+pngName)
      c1.SaveAs(pdfPath+pdfName)
      sRMS = "%.3f" % h_pphiz.GetRMS()
      dtGroupTable.FillDtGroup("pphizRMS", wheel, station, sRMS, "./PNG/"+pngName)
      if fit[0]:
        sSigma = "%.3f" % fit[1].GetParameter(2)
        dtGroupTable.FillDtGroup("pphizGaussSig", wheel, station, sSigma, "./PNG/"+pngName)
    
#Print 2`0 worse chambers
if map_ID_Diff_x:
  print "---------------WORSE 20 CHAMBER IN X------------------"
  sorted_x = sorted(map_ID_Diff_x.items(), key=operator.itemgetter(1))
  sorted_x.reverse()
  for iN in range(20):
    print sorted_x[iN]
if map_ID_Diff_y:
  print "---------------WORSE 20 CHAMBER IN Y------------------"
  sorted_y = sorted(map_ID_Diff_y.items(), key=operator.itemgetter(1))
  sorted_y.reverse()
  for iN in range(20):
    print sorted_y[iN]
if map_ID_Diff_z:
  print "---------------WORSE 20 CHAMBER IN Z------------------"
  sorted_z = sorted(map_ID_Diff_z.items(), key=operator.itemgetter(1))
  sorted_z.reverse()
  for iN in range(20):
    print sorted_z[iN]
if map_ID_Diff_phix:
  print "---------------WORSE 20 CHAMBER IN PHIX------------------"
  sorted_phix = sorted(map_ID_Diff_phix.items(), key=operator.itemgetter(1))
  sorted_phix.reverse()
  print sorted_phix
  for iN in range(20):
    print sorted_phix[iN]
if map_ID_Diff_phiy:
  print "---------------WORSE 20 CHAMBER IN PHIY------------------"
  sorted_phiy = sorted(map_ID_Diff_phiy.items(), key=operator.itemgetter(1))
  sorted_phiy.reverse()
  print sorted_phiy
  for iN in range(20):
    print sorted_phiy[iN]
if map_ID_Diff_phiz:
  print "---------------WORSE 20 CHAMBER IN PHIZ------------------"
  sorted_phiz = sorted(map_ID_Diff_phiz.items(), key=operator.itemgetter(1))
  sorted_phiz.reverse()
  print sorted_phiz
  for iN in range(20):
    print sorted_phiz[iN]

#*******************************************************************************
#                        Auxiliarly output HTML files                           
#                           1. htmlName_d - file for corrections or biases      
#                           2. htmlName_e - file for fit uncertainties          
#                           3. htmlName_p - file for pulls                      
#*******************************************************************************

#************************* Corrections: print all DOF **************************

htmlFile_d = htmlPath + htmlName_d
texFile_d  = texPath  + texName_d

PrintHtmlHeader(htmlFile_d)
PrintTexHeader(texFile_d)

PrintHtmlCode(htmlFile_d,"<font size=\"+2\">%s for %s</font>" % (correctionName,alignmentName) )
PrintHtmlCode(htmlFile_d,"<p>")
PrintHtmlCode(htmlFile_d,"<table border=\"1\" cellpadding=\"5\">")
caption = "<font size=+1>%s</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel)
PrintHtmlCode(htmlFile_d,"<caption>%s</caption>" % caption)
PrintHtmlCode(htmlFile_d,"<tr align=center>")
for dof in "x","y","z","phix","phiy","phiz": 
  pngName = "DT_d%s.png" % dof
  PrintHtmlCode(htmlFile_d,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName))
  if dof == "z": PrintHtmlCode(htmlFile_d,"</tr><tr align=center>")
PrintHtmlCode(htmlFile_d,"</tr>")
PrintHtmlCode(htmlFile_d,"</table>")

# Visualization
PrintHtmlCode(htmlFile_d,"<p>")
PrintHtmlCode(htmlFile_d,"<table border=\"1\" cellpadding=\"5\">")
caption = ("<font size=+1>%s visualization</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel) )
PrintHtmlCode(htmlFile_d,"<caption>%s</caption>" % caption)
PrintHtmlCode(htmlFile_d,"<tr align=center>")
for station in 1,2,3,4:
  imageName = alignmentName+"-"+referenceName+("__MBs%s" % station)
  pngName = imageName+".png"
  PrintHtmlCode(htmlFile_d,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"500\"></a></td>" % (pngName, pngName))
  if station == 2: PrintHtmlCode(htmlFile_d,"</tr><tr align=center>")
PrintHtmlCode(htmlFile_d,"</tr>")
PrintHtmlCode(htmlFile_d,"</table>")

PrintHtmlCode(htmlFile_d,"<p>")
PrintHtmlCode(htmlFile_d,"<table border=\"1\" cellpadding=\"5\">")
caption = ("<font size=+1>%s visualization</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel))
PrintHtmlCode(htmlFile_d,"<caption>%s</caption>" % caption)
PrintHtmlCode(htmlFile_d,"<tr align=center>")
for wheel in 0,-1,-2,1,2:
  imageName = alignmentName+"-"+referenceName+("__MBw%s" % wheel)
  pngName = imageName+".png"
  if wheel ==0: PrintHtmlCode(htmlFile_d,"<td rowspan=\"2\"><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"300\"></a></td>" % (pngName, pngName))
  else : PrintHtmlCode(htmlFile_d,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"300\"></a></td>" % (pngName, pngName))
  if wheel == -2: PrintHtmlCode(htmlFile_d,"</tr><tr align=center>")
PrintHtmlCode(htmlFile_d,"</tr>")
PrintHtmlCode(htmlFile_d,"</table>")

PrintHtmlCode(htmlFile_d,"<p>")
caption = ("<font size=+1>%s averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel))
dtGroupTable.PrintHtml(htmlFile_d,["dxRMS","dyRMS","dzRMS","dphixRMS","dphiyRMS","dphizRMS"],caption,0)

PrintHtmlCode(htmlFile_d,"<p>")
caption = ("<font size=+1>%s averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, littleLabel))
dtGroupTable.PrintHtml(htmlFile_d,["dxRMS","dxGaussSig","dyRMS","dyGaussSig","dzRMS","dzGaussSig","dphixRMS","dphixGaussSig","dphiyRMS","dphiyGaussSig","dphizRMS","dphizGaussSig"],caption,0)

#************************* Corrections: print separate DOF *********************

for dof in "x","y","z","phix","phiy","phiz":
  
  PrintHtmlCode(htmlFile_d,"<p>")
  
  if dof == "x":    htmlDof, texDof, unitDof = "&delta;x", "\\delta x", "mm"
  if dof == "y":    htmlDof, texDof, unitDof = "&delta;y", "\\delta y", "mm"
  if dof == "z":    htmlDof, texDof, unitDof = "&delta;z", "\\delta z", "mm"
  if dof == "phix": htmlDof, texDof, unitDof = "&delta;&phi;<sub>x</sub>", "\\delta \\phi_{x}", "mrad"
  if dof == "phiy": htmlDof, texDof, unitDof = "&delta;&phi;<sub>y</sub>", "\\delta \\phi_{y}", "mrad"
  if dof == "phiz": htmlDof, texDof, unitDof = "&delta;&phi;<sub>z</sub>", "\\delta \\phi_{z}", "mrad"
  
  htmlCaption = "<font size=+1>%s <i>%s</i> (%s) </font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, htmlDof, unitDof, littleLabel)
  texCaption  = "%s $%s$~(%s) \\\\ {\\tiny \\verb;%s;}" % (correctionName, texDof, unitDof, littleLabel)
  if dof == "x": 
    dtTab_dx.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dx.PrintTex(texFile_d, texCaption, "dtTab_dx", 0)
  if dof == "y":
    dtTab_dy.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dy.PrintTex(texFile_d, texCaption, "dtTab_dy", 0)
  if dof == "z":
    dtTab_dz.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dz.PrintTex(texFile_d, texCaption, "dtTab_dz", 0)
  if dof == "phix":
    dtTab_dphix.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dphix.PrintTex(texFile_d, texCaption, "dtTab_dphix", 0)
  if dof == "phiy":
    dtTab_dphiy.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dphiy.PrintTex(texFile_d, texCaption, "dtTab_dphiy", 0)
  if dof == "phiz":
    dtTab_dphiz.PrintHtml(htmlFile_d, htmlCaption, 0)
    dtTab_dphiz.PrintTex(texFile_d, texCaption, "dtTab_dphiz", 0)
  
  htmlCaption = ("<font size=+1>%s <i>%s</i> (%s) in homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (correctionName, htmlDof, unitDof, littleLabel) )
  
  PrintHtmlCode(htmlFile_d,"<p>")
  PrintHtmlCode(htmlFile_d,"<table border=\"1\" cellpadding=\"5\">")
  PrintHtmlCode(htmlFile_d,"<caption>%s</caption>" % htmlCaption)
  PrintHtmlCode(htmlFile_d,"<tr align=center><th></th><th><i>Wheel -2</i></th><th><i>Wheel -1</i></th><th><i>Wheel 0</i></th><th><i>Wheel +1</i></th><th><i>Wheel +2</i></th>")
  for station in 1, 2, 3, 4:
    PrintHtmlCode( htmlFile_d, ("<tr align=center><th><i>Station %s</i></th>" % station) )
    for wheel in -2, -1, 0, +1, +2:
      pngName = "DT_d%s_%s_%s.png" % (dof, wheel , station)
      if dof == "y" and station == 4: PrintHtmlCode( htmlFile_d, "<td>None</td>" )
      else: PrintHtmlCode( htmlFile_d, ("<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName)) )
    PrintHtmlCode(htmlFile_d,"</tr>")
  PrintHtmlCode(htmlFile_d,"</table>")

PrintHtmlTrailer(htmlFile_d)
PrintTexTrailer(texFile_d)

#************************* Fit uncert: print all DOF ***************************

if isReport:
  htmlFile_e = htmlPath + htmlName_e
  texFile_e  = texPath  + texName_e
  
  PrintHtmlHeader(htmlFile_e)
  PrintTexHeader(texFile_e)
  
  PrintHtmlCode(htmlFile_e,"<font size=\"+2\">Alignment fit uncertainties (<i>&sigma;<sub>fit</sub></i>) for %s</font>" % alignmentName )
  PrintHtmlCode(htmlFile_e,"<p>")
  PrintHtmlCode(htmlFile_e,"<table border=\"1\" cellpadding=\"5\">")
  htmlCaption = "<font size=+1>Alignment fit uncertainties</font> <br><font size=-1><pre>%s</pre></font>" % alignmentName
  PrintHtmlCode(htmlFile_e,"<caption>%s</caption>" % htmlCaption)
  PrintHtmlCode(htmlFile_e,"<tr align=center>")
  for dof in "x","y","z","phix","phiy","phiz": 
    pngName = "DT_e"+dof+".png"
    PrintHtmlCode(htmlFile_e,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName))
    if dof == "z": PrintHtmlCode(htmlFile_e,"</tr><tr align=center>")
  PrintHtmlCode(htmlFile_e,"</tr>")
  PrintHtmlCode(htmlFile_e,"</table>")

  PrintHtmlCode(htmlFile_e,"<p>")
  htmlCaption = "<font size=+1>Alignment fit uncertainties averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % alignmentName
  dtGroupTable.PrintHtml(htmlFile_e,["exMean","eyMean","ezMean","ephixMean","ephiyMean","ephizMean"],htmlCaption,0)

  PrintHtmlCode(htmlFile_e,"<p>")
  htmlCaption = "<font size=+1>Alignment fit uncertainties averaged over homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % alignmentName
  dtGroupTable.PrintHtml(htmlFile_e,["exMean","exGaussMean","eyMean","eyGaussMean","ezMean","ezGaussMean","ephixMean","ephixGaussMean","ephiyMean","ephiyGaussMean","ephizMean","ephizGaussMean"],htmlCaption,0)

#************************ Fit uncert: print separate DOF *********************

  for dof in "x","y","z","phix","phiy","phiz":
    
    PrintHtmlCode(htmlFile_e,"<p>")
    
    if dof == "x":    htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>x", "\\sigma_{fit} x", "mm"
    if dof == "y":    htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>y", "\\sigma_{fit} y", "mm"
    if dof == "z":    htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>z", "\\sigma_{fit} z", "mm"
    if dof == "phix": htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>&phi;<sub>x</sub>", "\\sigma_{fit} \\phi_{x}", "mrad"
    if dof == "phiy": htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>&phi;<sub>y</sub>", "\\sigma_{fit} \\phi_{y}", "mrad"
    if dof == "phiz": htmlDof, texDof, unitDof = "&sigma;<sub>fit</sub>&phi;<sub>z</sub>", "\\sigma_{fit} \\phi_{z}", "mrad"
    
    htmlCaption = ("<font size=+1><Alignment fit uncertainties <i>%s</i> (%s)</font> <br><font size=-1><pre>%s</pre></font>" % (htmlDof, unitDof, alignmentName))
    texCaption = "Alignment fit uncertainties $%s$~(%s) \\\\ {\\tiny \\verb;%s;}" % (texDof, unitDof, alignmentName)
    
    if dof == "x":
      dtTab_ex.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ex.PrintTex(texFile_e, texCaption, "dtTab_ex", 0)
    if dof == "y":
      dtTab_ey.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ey.PrintTex(texFile_e, texCaption, "dtTab_ey", 0)
    if dof == "z":
      dtTab_ez.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ez.PrintTex(texFile_e, texCaption, "dtTab_ez", 0)
    if dof == "phix":
      dtTab_ephix.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ephix.PrintTex(texFile_e, texCaption, "dtTab_ephix", 0)
    if dof == "phiy":
      dtTab_ephiy.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ephiy.PrintTex(texFile_e, texCaption, "dtTab_ephiy", 0)
    if dof == "phiz":
      dtTab_ephiz.PrintHtml(htmlFile_e, htmlCaption, 0)
      dtTab_ephiz.PrintTex(texFile_e, texCaption, "dtTab_ephiz", 0)
    
    htmlCaption = ("<font size=+1><Alignment fit uncertainties <i>%s</i> (%s) in homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (htmlDof, unitDof, alignmentName))
    
    PrintHtmlCode(htmlFile_e,"<p>")
    PrintHtmlCode(htmlFile_e,"<table border=\"1\" cellpadding=\"5\">")
    PrintHtmlCode(htmlFile_e,"<caption>%s</caption>" % htmlCaption)
    PrintHtmlCode(htmlFile_e,"<tr align=center><th></th><th><i>Wheel -2</i></th><th><i>Wheel -1</i></th><th><i>Wheel 0</i></th><th><i>Wheel +1</i></th><th><i>Wheel +2</i></th>")
    for station in 1, 2, 3, 4:
      PrintHtmlCode( htmlFile_e, ("<tr align=center><th><i>Station %s</i></th>" % station) )
      for wheel in -2, -1, 0, +1, +2:
        pngName = "DT_e%s_%s_%s.png" % (dof, wheel , station)
        if dof == "y" and station ==4: PrintHtmlCode( htmlFile_e, "<td>None</td>" )
        else: PrintHtmlCode( htmlFile_e, ("<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName)) )
      PrintHtmlCode(htmlFile_e,"</tr>")
    PrintHtmlCode(htmlFile_e,"</table>")

  PrintHtmlTrailer(htmlFile_e)
  PrintTexTrailer(texFile_e)

#***************************** Pulls: print all DOF ****************************

  htmlFile_p = htmlPath + htmlName_p
  texFile_p  = texPath  + texName_p
  
  PrintHtmlHeader(htmlFile_p)
  PrintTexHeader(texFile_p)

  PrintHtmlCode(htmlFile_p,"<font size=\"+2\">Pulls for %s</font>" % alignmentName )
  PrintHtmlCode(htmlFile_p,"<p>")
  PrintHtmlCode(htmlFile_p,"<table border=\"1\" cellpadding=\"5\">")
  htmlCaption = "<font size=+1>Pulls</font> <br><font size=-1><pre>%s</pre></font>" % littleLabel
  PrintHtmlCode(htmlFile_p,"<caption>%s</caption>" % htmlCaption)
  PrintHtmlCode(htmlFile_p,"<tr align=center>")
  for dof in "x","y","z","phix","phiy","phiz": 
    pngName = "DT_p%s.png" % dof
    PrintHtmlCode(htmlFile_p,"<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName))
    if dof == "z": PrintHtmlCode(htmlFile_p,"</tr><tr align=center>")
  PrintHtmlCode(htmlFile_p,"</tr>")
  PrintHtmlCode(htmlFile_p,"</table>")

  PrintHtmlCode(htmlFile_p,"<p>")
  caption = "<font size=+1>Pulls averaged over homogeneous chambers (RMSes only)</font> <br><font size=-1><pre>%s</pre></font>" % littleLabel
  dtGroupTable.PrintHtml(htmlFile_p,["pxRMS","pyRMS","pzRMS","pphixRMS","pphiyRMS","pphizRMS"],caption,0)

  PrintHtmlCode(htmlFile_p,"<p>")
  caption = "<font size=+1>Pulls averaged over homogeneous chambers (RMSes compared to Gaussian sigmas)</font> <br><font size=-1><pre>%s</pre></font>" % littleLabel
  dtGroupTable.PrintHtml(htmlFile_p,["pxRMS","pxGaussSig","pyRMS","pyGaussSig","pzRMS","pzGaussSig","pphixRMS","pphixGaussSig","pphiyRMS","pphiyGaussSig","pphizRMS","pphizGaussSig"],caption,0)

#************************ Pulls: print separate DOF *********************

  for dof in "x","y","z","phix","phiy","phiz":
    
    PrintHtmlCode(htmlFile_p,"<p>")
    
    if dof == "x":    htmlDof, texDof = "x", "x"
    if dof == "y":    htmlDof, texDof = "y", "y"
    if dof == "z":    htmlDof, texDof = "z", "z"
    if dof == "phix": htmlDof, texDof = "&phi;<sub>x</sub>", "\\phi_{x}"
    if dof == "phiy": htmlDof, texDof = "&phi;<sub>y</sub>", "\\phi_{y}"
    if dof == "phiz": htmlDof, texDof = "&phi;<sub>z</sub>", "\\phi_{z}"
      
    htmlCaption = ("<font size=+1>Pulls for <i>%s</i></font> <br><font size=-1><pre>%s</pre></font>" % (htmlDof, littleLabel) )
    texCaption = ("Pulls for $%s$ \\\\ {\\tiny \\verb;%s;}" % (htmlDof, littleLabel) )
    
    if dof == "x":
      dtTab_px.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_px.PrintTex(texFile_p, texCaption, "dtTab_px", 0)
    if dof == "y":
      dtTab_py.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_py.PrintTex(texFile_p, texCaption, "dtTab_py", 0)
    if dof == "z":
      dtTab_pz.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_py.PrintTex(texFile_p, texCaption, "dtTab_py", 0)
    if dof == "phix":
      dtTab_pphix.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_pphix.PrintTex(texFile_p, texCaption, "dtTab_pphix", 0)
    if dof == "phiy":
      dtTab_pphiy.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_pphiy.PrintTex(texFile_p, texCaption, "dtTab_pphiy", 0)
    if dof == "phiz":
      dtTab_pphiz.PrintHtml(htmlFile_p, htmlCaption, 0)
      dtTab_pphiz.PrintTex(texFile_p, texCaption, "dtTab_pphiz", 0)
    
    caption = ("Pulls for <i>%s</i> in homogeneous chambers</font> <br><font size=-1><pre>%s</pre></font>" % (htmlDof, littleLabel))
    
    PrintHtmlCode(htmlFile_p,"<p>")
    PrintHtmlCode(htmlFile_p,"<table border=\"1\" cellpadding=\"5\">")
    PrintHtmlCode(htmlFile_p,"<caption>%s</caption>" % caption)
    PrintHtmlCode(htmlFile_p,"<tr align=center><th></th><th><i>Wheel -2</i></th><th><i>Wheel -1</i></th><th><i>Wheel 0</i></th><th><i>Wheel +1</i></th><th><i>Wheel +2</i></th>")
    for station in 1, 2, 3, 4:
      PrintHtmlCode( htmlFile_p, ("<tr align=center><th><i>Station %s</i></th>" % station) )
      for wheel in -2, -1, 0, +1, +2:
        pngName = "DT_p%s_%s_%s.png" % (dof, wheel , station)
        if dof == "y" and station ==4: PrintHtmlCode( htmlFile_p, "<td>None</td>" )
        else: PrintHtmlCode( htmlFile_p, ("<td><a href=\"./PNG/%s\"><img src=\"./PNG/%s\" alt=\"text\" width=\"250\"></a></td>" % (pngName, pngName)) )
      PrintHtmlCode(htmlFile_p,"</tr>")
    PrintHtmlCode(htmlFile_p,"</table>")

  PrintHtmlTrailer(htmlFile_p)
  PrintTexTrailer(texFile_e)
