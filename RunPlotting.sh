export alignmentName="mc_DT-1111-110111-100011-stn4_DESRUN2_73_V3_CMSSW_7_3_1_muonGeometry_YuriyStartup_fid80x80y_v1_03"

runComparison=false
uploadComparison=true
runCorrelation=false

doDT=true
doCSC=false

if [ "$runComparison" = true ]; then
    python PlotConfig_Generic.py > OUTPUT/${alignmentName}.out.txt -b
fi

if [ "$uploadComparison" = true ]; then
    cd RESULT/
    scp -r $alignmentName USERNAME@lxplus.cern.ch:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/tmp/
    cd ..
fi

if [ "$doDT" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_2.py $alignmentName -b
fi

if [ "$doCSC" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_3.py $alignmentName -b
fi



