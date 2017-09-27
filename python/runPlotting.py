"""
7 August 2017
Dan Marley

Called from `RunPlotting.sh` to make comparisons between geometries
"""
import sys
from config import Config
from plotCorrections import PlotCorrections

cfg = Config(sys.argv[1])
cfg.initialize()

pc = PlotCorrections(cfg)
pc.execute()           # configuration file

