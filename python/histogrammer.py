"""
7 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

Initialize histograms.
"""
import sys
import ROOT



class Histogrammer(object):
    """Make histograms of corrections, uncertainties, or pulls"""
    def __init__(self,cfg,name=""):
        self.config = cfg   # configuration object from MuonAlignmentAlgorithms/scripts/
        self.name   = name

        color = ROOT.TColor
        if self.config.isDT():
            # self.fillColor = ROOT.kGreen + 3
            self.fillColor = color.GetColor("#ffe0a1")
            self.lineColor = ROOT.kBlack
            self.yTitle    = "Number of DTs"
        elif self.config.isCSC():
            # self.fillColor = ROOT.kBlue - 7
            self.fillColor = color.GetColor("#3ffa3f")
            self.lineColor = ROOT.kBlack
            self.yTitle    = "Number of CSCs"
        else:
            self.fillColor = ROOT.kCyan
            self.lineColor = ROOT.kBlack
            self.yTitle    = "Number of chambers"

        self.histograms  = {}
        self.coordinates = ["x","y","z","phix","phiy","phiz"]
        self.units       = {"x":"(mm)","y":"(mm)","z":"(mm)",
                            "phix":"(mrad)","phiy":"(mrad)","phiz":"(mrad)"}
        self.tex_names   = {"x":"x","y":"y","z":"z",
                            "phix":r"#phi_{x}","phiy":r"#phi_{y}","phiz":r"#phi_{z}"}
        self.html_names  = {
                 "x":"&delta;x","y":"&delta;y","z":"&delta;z",
                 "phix":"&delta;&phi;<sub>x</sub>",
                 "phiy":"&delta;&phi;<sub>y</sub>",
                 "phiz":"&delta;&phi;<sub>z</sub>"}

        self.latex_names = {"x":"\\delta x","y":"\\delta y","z":"\\delta z",
                            "phix":"\\delta \\phi_{x}",
                            "phiy":"\\delta \\phi_{x}",
                            "phiz":"\\delta \\phi_{x}"}

        self.correction_label  = r"#delta"
        self.uncertainty_label = r"#sigma_{fit}"



    def initialize(self):
        """Setup parameters"""
        self.c1 = ROOT.TCanvas("canvas", "canvas")
        self.c1.SetCanvasSize(900,900)

        self.legend = ROOT.TLegend(.17,.935,0.9,1.)
        self.legend.SetFillColor(ROOT.kWhite)
        self.legend.SetBorderSize(0)
        self.legend.SetTextFont(42)
        self.legend.SetTextSize(0.045)
        self.legend.SetMargin(0.13)

        return


    def init_corrections(self):
        """Corrections w.r.t. another geometry"""
        h_basename = "h_d"
        h_binning  = self.config.corrections_binning()
        h_xtitle   = dict( (c,"{0} {1} {2}".format(self.correction_label,self.tex_names[c],self.units[c])) \
                           for c in self.coordinates)

        self.init_hists( basename=h_basename,plot_xtitle=h_xtitle,binning=h_binning )

        return


    def init_uncertainties(self):
        """Fit Uncertainties"""
        h_basename = "h_e"
        h_binning  = self.config.uncertainties_binning()
        h_xtitle   = dict( (c,"{0} {1} {2}".format(self.uncertainty_label,self.tex_names[c],self.units[c])) \
                           for c in self.coordinates)

        self.init_hists( basename=h_basename,plot_xtitle=h_xtitle,binning=h_binning )

        return


    def init_pulls(self):
        """Pulls"""
        h_basename = "h_p"
        h_binning  = self.config.pulls_binning()
        h_xtitle   = "%s {0} / %s {0}"%(self.correction_label,self.uncertainty_label)

        self.init_hists( basename=h_basename,plot_xtitle=h_xtitle,binning=h_binning )

        return


    def init_hists(self,basename="h",plot_xtitle="",binning={}):
        """Initialize histograms"""
        self.histograms[basename] = {}

        try:
            bins = binning["bins"]
            min  = binning["min"]
            max  = binning["max"]
        except KeyError:
            self.config.ERROR("HIST : No binning information provided to histogrammer")
            sys.exit(-1)


        for coordinate in self.coordinates:
            name       = "{0}{1}_{2}".format(basename,coordinate,self.name)

            h = ROOT.TH1F(name,name,bins,min,max)
            h.SetXTitle(plot_xtitle.format(self.tex_names[coordinate])
            h.SetYTitle(self.yTitle)
            h.SetLineColor(self.lineColor)
            h.SetFillColor(self.fillColor)
            h.StatOverflows(ROOT.kTRUE)

            self.histograms[basename][coordinate] = h

        return


## THE END ##