        htmlPath = self.config.folderName()
        if not os.path.exists(htmlPath):
             os.makedirs(htmlPath)

        texPath = htmlPath+"/TEX/"
        if not os.path.exists(texPath):
             os.makedirs(texPath)

        pngPath = htmlPath+"/PNG/"
        if not os.path.exists(pngPath):
             os.makedirs(pngPath)

        pdfPath = htmlPath+"/PDF/"
        if not os.path.exists(pdfPath):
             os.makedirs(pdfPath)

        svgPath = htmlPath+"/SVG/"
        if not os.path.exists(svgPath):
             os.makedirs(svgPath)


isReport

plotsHeader()) 
            # "CMS 2016X  #sqrt{s} = 13 TeV   L_{int} = X fb^{-1}"

        self.alignmentName = self.cfg.alignmentName()
        self.referenceName = self.cfg.referenceName()
                g_new = gXML.MuonGeometry(self.config.xmlfile("new"))
        g_ref = gXML.MuonGeometry(self.config.xmlfile("reference"))