# PlottingTools

This code can be used to produce the plots for both the alignment geometry comparisons and also the correlation plots.

## Updates Setup

27 September 2017  
Dan Marley

The framework has been updated to remove global variables and move to an object-oriented structure.
To run the code, set all configuration options is a text file, see `config.txt` as an example.
All configuration options are listed in `python/configuration.py`.  

Then, execute:
```
python python/runPlotting.py <config_file.txt>
```

where `<config_file.txt` is your text file with the configurations.


## Original Setup

Everything can be launched from `RunPlotting.sh`, 
you just need to set the alignment name in the file and turn on the flags for whatever you want to run. 
This can also upload the relevant output to the muon alignment web area:  
https://cms-mual.web.cern.ch/cms-mual/tmp/[ALIGNMENT_NAME]/[ALIGNMENT_NAME].d.html

This plotting machinery only requires the `*.xml` files from the alignment jobs, and it expects to find these in the `Geometries/` directory.  
There is a very simple latex document to show the results of the correlations script (`plotCorrelations.tex`) - 
at the moment the path is hard coded so this will need to be fixed 
(`\graphicspath` for some reason wasn't working for me, but this is in principle a good option).
