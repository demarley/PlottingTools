export alignmentName="muonGeometry_DT-Hw-111111_CSC-START53_v14-111111_Local"

runComparison=false
uploadComparison=false
runCorrelation=true
printCorrelationFactors=false

doDT=true
doCSC=false

if [ "$runComparison" = true ]; then
    python PlotConfig_Generic.py > OUTPUT/${alignmentName}.out.txt -b
fi

if [ "$uploadComparison" = true ]; then
    cd RESULT/
    #scp -r $alignmentName USERNAME@lxplus.cern.ch:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/tmp/
    cp -r $alignmentName /afs/cern.ch/user/r/rymuelle/www   
fi

if [ "$doDT" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_2.py $alignmentName $printCorrelationFactors -b
fi

if [ "$doCSC" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_3.py $alignmentName $printCorrelationFactors -b
fi



