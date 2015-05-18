# PlottingTools

This code can be used to produce the plots for both the alignment geometry comparisons and also the correlation plots.

Everything can be launched from RunPlotting.sh, you just need to set the alignment name in the file and turn on the flags for whatever you want to run. This can also upload the relevant output to the muon alignment web area: https://cms-mual.web.cern.ch/cms-mual/tmp/[ALIGNMENT_NAME]/[ALIGNMENT_NAME].d.html

This plotting machinery only requires the .xml files from the alignment jobs, and it expects to find these in the Geometries directory.

There is a very simple latex document to show the results of the correlations script (plotCorrelations.tex) - at the moment the path is hard coded so this will need to be fixed (\graphicspath for some reason wasn't working for me, but this is in principle a good option).