"""
13 September 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Fit and draw histograms
"""
import util
import ROOT


class HistoFitDraw(object):
    """Class for fitting and drawing histograms"""
    def __init__(self,config):
        self.fitLineColor = ROOT.kRed
        self.fitLineWidth = 3

        self.config = config

        self.vb = util.VERBOSE()
        self.vb.level = config.verbose_level()
        self.vb.name  = "HISTOFITDRAW"


	def FitAndDraw(histo, littleLabel="", doFit=True):
	    """Fit and draw histogram"""
            self.vb.DEBUG("doFit: {0}".format(doFit))

hEntries = histo.GetEntries()
hNorm    = histo.Integral()*histo.GetBinWidth(0)
		hMean    = histo.GetMean()
		hMeanErr = histo.GetMeanError()
		hRms     = histo.GetRMS()
		hRmsErr  = histo.GetRMSError()
  
		self.vb.DEBUG("Histogram {0} {1}".format(histo.GetName(), histo.GetTitle())
		self.vb.DEBUG("  Entries        = {0}".format(hEntries)
		self.vb.DEBUG("  Normalization  = {0}".format(hNorm)
		self.vb.DEBUG("  Mean           = {0} +- {1}".format(hMean, hMeanErr))
		self.vb.DEBUG("  RMS            = {0} +- {1}".format(hRms, hRmsErr))
  
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
			fit = self.Fit1DGauss(histo)
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
	    """1-D HLine fit"""
		minY = histo.GetMinimum()
		maxY = histo.GetMaximum()
		minX = histo.GetXaxis().GetXmin()
		maxX = histo.GetXaxis().GetXmax()

		self.vb.DEBUG("MinY = {0}".format(minY))
		self.vb.DEBUG("MaxY = {0}".format(maxY))
		self.vb.DEBUG("MinX = {0}".format(minX))
		self.vb.DEBUG("MaxX = {0}".format(maxX))

		fit = ROOT.TF1( "fit","[0]", minX, maxX )
		fit.SetLineColor(self.fitLineColor)
		fit.SetLineWidth(self.fitLineWidth)
		fit.SetParName(0,"value")
		fit.SetParameter(0, (minY + maxY) /2.0 );
		histo.Fit("fit","QR","same")

		self.vb.DEBUG("Value   = {0} +- {1}".format(fit.GetParameter(0),fit.GetParError(0)))

		return fit


	def Fit1DGauss(histo):
        """1-D Gaussian fit"""
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

		self.vb.DEBUG("  Fit parameters:")
		self.vb.DEBUG("    Norm1   = {0} +- {1}".format(norm1, norm1_e))
		self.vb.DEBUG("    Mean1   = {0} +- {1}".format(mean1, mean1_e))
		self.vb.DEBUG("    Sigma1  = {0} +- {1}".format(sigma1, sigma1_e))

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
		self.vb.DEBUG("    Norm1   = {0} +- {1}".format(norm2, norm2_e))
		self.vb.DEBUG("    Mean1   = {0} +- {1}".format(mean2, mean2_e))
		self.vb.DEBUG("    Sigma1  = {0} +- {1}".format(sigma2, sigma2_e))

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
