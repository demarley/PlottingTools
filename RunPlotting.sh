export alignmentName="mc_DT-1100-111111_CMSSW_8_0_17_ideal_45M_8TeV_Sigma16_BADsecNOPhiY_PROVAnoMC_v1_01"


xmlfile_ref="Geometries/muonGeometry_IDEAL_AllZeroes.Ape6x6.StdTags.746p3.DBv2.xml" # reference geometry: initial or IDEAL
#xmlfile_ref="Geometries/data_DT-1100-110001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_03.xml" #Early 2016B Geom DT
#xmlfile_ref="Geometries/data_CSC-1100-100001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_Shifted_03.xml" #Early 2016B CSC
#xmlfile_ref="Geometries/data_DT-1100-110001_SingleMuon_Run2016E_MuAlCalIsolatedMu_276830_277420_8_0_17_v1_03.xml" # 2016E 3 DOF

#referenceName="Iter 1 vs Iter 3"
referenceName="IDEAL_Geo"
#referenceName="2016B_early"
#referenceName="2016E_3DOF"

correctionName="Displacements from ideal geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
#correctionName="Displacements from 2016B geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
#correctionName="Displacements from 2016E with 3DOF"#

runComparison=true
uploadComparison=true
runCorrelation=false
printCorrelationFactors=true

doDT="true"
doCSC="data"

if [ "$runComparison" = true ]; then
    echo output: OUTPUT/${alignmentName}.out.txt
    python PlotConfig_Generic.py $xmlfile_ref $doDT $doCSC $referenceName $correctionName > OUTPUT/${alignmentName}.out.txt -b
fi

if [ "$uploadComparison" = true ]; then
    cd RESULT/
    echo "copying $alignmentName"
    scp -r $alignmentName lpernie@lxplus.cern.ch:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/tmp/
     echo "copied"
    cd ..
fi

if [ "$doDT" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_2.py $alignmentName $printCorrelationFactors $xmlfile_ref -b
fi

if [ "$doCSC" = true -a "$runCorrelation" = true ]; then
    python TMP_CREATE_CORRELATION_PLOTS_3.py $alignmentName $printCorrelationFactors -b
fi
