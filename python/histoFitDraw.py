"""
8 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Initialize histograms.
"""
import ROOT


class HistoFitDraw(object):
    """Class for fitting and drawing histograms"""
    def __init__(self):
        self.fitLineColor = ROOT.kRed
        self.fitLineWidth = 3

	def FitAndDraw(histo, littleLabel="", doFit=True):
		print "doFit:", doFit

		hEntries = histo.GetEntries()
		hNorm    = histo.Integral()*histo.GetBinWidth(0)
		hMean    = histo.GetMean()
		hMeanErr = histo.GetMeanError()
		hRms     = histo.GetRMS()
		hRmsErr  = histo.GetRMSError()
  
		print "Histogram", histo.GetName(), histo.GetTitle()
		print "  Entries        = ", hEntries
		print "  Normalization  = ", hNorm
		print "  Mean           = ", hMean, "+-", hMeanErr
		print "  RMS            = ", hRms, "+-", hRmsErr
  
		sHEntries = "%d" % hEntries
		sHMean    = "%.3f" % hMean
		sHMeanErr = "%.3f" % hMeanErr
		sHRms     = "%.3f" % hRms
		sHRmsErr  = "%.3f" % hRmsErr
  
		littleLegend = ROOT.TLegend(0.995,0.1,1.0,0.8)
		littleLegend.SetFillColor(ROOT.kWhite)
		littleLegend.SetFillStyle(0)
		littleLegend.SetBorderSize(0)
		littleLegend.SetTextFont(42)
		littleLegend.SetTextSize(0.02)
		littleLegend.SetTextColor(ROOT.kBlack)
		littleLegend.SetTextAlign(11)
		littleLegend.SetTextAngle(90)
		littleLegend.SetMargin(0.0)
		littleLegend.SetHeader(littleLabel)
  
		histLegend = ROOT.TLegend(0.2,0.7,0.5,0.9)
		histLegend.SetFillColor(ROOT.kWhite)
		histLegend.SetFillStyle(0)
		histLegend.SetBorderSize(0)
		histLegend.SetTextFont(42)
		histLegend.SetTextSize(0.035)
		histLegend.SetTextColor(ROOT.kBlack)
		histLegend.SetMargin(0.13)
	  #  histLegend.SetHeader("")
	  #  histLegend.AddEntry(histo,"Histogram:","LF")
		histLegend.AddEntry(histo,histo.GetTitle(),"LF")
		histLegend.AddEntry(histo," Entries = "+sHEntries,"")
		histLegend.AddEntry(histo," Mean = "+sHMean+"#pm"+sHMeanErr,"")
		histLegend.AddEntry(histo," RMS  = "+sHRms+"#pm"+sHRmsErr,"")
  
		maxY = histo.GetMaximum()
  
		if doFit:
			fit = Fit1DGauss(histo)
			fitIsOk     = fit[0]
			fitFunction = fit[1]
			fitLegend   = fit[2]
			if fitIsOk:
				fit_maxY   = fitFunction.GetMaximum()
				if fit_maxY > maxY:
					maxY = fit_maxY
		else:
			fitIsOk = False
			fitFunction = None
			fitLegend = None
  
		histo.SetMaximum(1.4*maxY)
  
		histo.Draw()
		histLegend.Draw()
		littleLegend.Draw()
		if doFit: fitLegend.Draw()
  
		return fitIsOk, fitFunction, fitLegend, histo, histLegend, littleLegend


	def Fit1DHLine(histo):
		minY = histo.GetMinimum()
		maxY = histo.GetMaximum()
		minX = histo.GetXaxis().GetXmin()
		maxX = histo.GetXaxis().GetXmax()

		print "MinY = ", minY
		print "MaxY = ", maxY
		print "MinX = ", minX
		print "MaxX = ", maxX

		fit = ROOT.TF1( "fit","[0]", minX, maxX )
		fit.SetLineColor(self.fitLineColor)
		fit.SetLineWidth(self.fitLineWidth)
		fit.SetParName(0,"value")
		fit.SetParameter(0, (minY + maxY) /2.0 );
		histo.Fit("fit","QR","same")
		val    = fit.GetParameter(0)
		val_e  = fit.GetParError(0)
		print "Value   =", val, "+-", val_e

		return fit


	def Fit1DGauss(histo):

		norm0  = histo.Integral()*histo.GetBinWidth(0)
		mean0  = histo.GetMean()
		sigma0 = histo.GetRMS()

		fit1 = ROOT.TF1( "fit1","[0]/[2]/(2.0*3.14159)^0.5*exp(-0.5*((x-[1])/[2])^2)", mean0-2.0*sigma0, mean0+2.0*sigma0 )
		fit1.SetLineColor(self.fitLineColor)
		fit1.SetLineWidth(self.fitLineWidth)
		fit1.SetParName(0,"norm1");
		fit1.SetParName(1,"mean1");
		fit1.SetParName(2,"sigma1");
		fit1.FixParameter(0, norm0);
		fit1.SetParameter(1, mean0);
		fit1.SetParameter(2, sigma0);
		histo.Fit("fit1","QRLL","same")
		norm1    = fit1.GetParameter(0)
		norm1_e  = fit1.GetParError(0)
		mean1    = fit1.GetParameter(1)
		mean1_e  = fit1.GetParError(1)
		sigma1   = fit1.GetParameter(2)
		sigma1_e = fit1.GetParError(2)
		print "  Fit parameters:"
		print "    Norm1   =", norm1, "+-", norm1_e;
		print "    Mean1   =", mean1, "+-", mean1_e;
		print "    Sigma1  =", sigma1, "+-", sigma1_e;

		fit2 = ROOT.TF1( "fit2","[0]/[2]/(2.0*3.14159)^0.5*exp(-0.5*((x-[1])/[2])^2)", mean1-2.0*sigma1, mean1+2.0*sigma1 );
		fit2.SetLineColor(self.fitLineColor)
		fit2.SetLineWidth(self.fitLineWidth)
		fit2.SetParName(0,"norm2");
		fit2.SetParName(1,"mean2");
		fit2.SetParName(2,"sigma2");
		fit2.FixParameter(0, norm1);
		fit2.SetParameter(1, mean1);
		fit2.SetParameter(2, sigma1);
		res = histo.Fit("fit2","QRLL","same")
		norm2    = fit2.GetParameter(0)
		norm2_e  = fit2.GetParError(0)
		mean2    = fit2.GetParameter(1)
		mean2_e  = fit2.GetParError(1)
		sigma2   = fit2.GetParameter(2)
		sigma2_e = fit2.GetParError(2)
		print "    Norm2   =", norm2, "+-", norm2_e
		print "    Mean2   =", mean2, "+-", mean2_e
		print "    Sigma2  =", sigma2, "+-", sigma2_e

		fitIsOk = False
		if mean2_e > 0.0 and sigma2_e > 0.001 and sigma2 < 10000. and sigma2 > 0.001 and mean2 > -10000. and mean2 < 10000.: fitIsOk = True # data for fit is not empty

		#  sNorm = "Mean = " + str(mean2) + "#pm" + str(mean2_e) % mean2, mean2_e
		sMean    = "%.3f" % mean2
		sMean_e  = "%.3f" % mean2_e
		sSigma   = "%.3f" % sigma2
		sSigma_e = "%.3f" % sigma2_e

		fitLegend = ROOT.TLegend(0.6,0.7,0.9,0.85)
		fitLegend.SetFillColor(ROOT.kWhite)
		fitLegend.SetFillStyle(0)
		fitLegend.SetBorderSize(0)
		fitLegend.SetTextFont(42)
		fitLegend.SetTextSize(0.035)
		fitLegend.SetTextColor(self.fitLineColor)
		fitLegend.SetMargin(0.13)
		#  fitLegend.SetHeader("")
		if fitIsOk:
			fitLegend.AddEntry(fit2,"Gaussian fit:","L")
			fitLegend.AddEntry(fit2, " Mean  = "+sMean+"#pm"+sMean_e, "")
			fitLegend.AddEntry(fit2, " Sigma = "+sSigma+"#pm"+sSigma_e, "")
  
	  return fitIsOk, fit2, fitLegend


## THE END ##