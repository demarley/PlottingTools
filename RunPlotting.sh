export alignmentName="data_DT-1100-111111_SingleMuon_Run2016D_MuAlCalIsolatedMu_276315_276811_8_0_8_v1_03"

#xmlfile_ref="Geometries/mc_DT-1100-110001_CMSSW_8_0_8_patch1_ideal_45M_8TeV_Twisted_v4_03.xml" # 3 DOF after CONICAL
#xmlfile_ref="Geometries/DTGeometry_coneInLocalZvsGlobalZ.xml" # CONICAL
#xmlfile_ref="Geometries/muonGeometry_IDEAL_AllZeroes.Ape6x6.StdTags.746p3.DBv2.xml" # reference geometry: initial or IDEAL
xmlfile_ref="Geometries/data_DT-1100-110001_SingleMuon_Run2015D-PromptReco-v3_RECO_CMSSW_7_4_12_patch4_pt20_pakhotin_v2_03.xml" # Nov 2015 Geom DT
#xmlfile_ref="Geometries/data_DT-1100-110001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_03.xml" # 2016 Geom DT
#xmlfile_ref="Geometries/data_CSC-1100-100001_SingleMuon_Run2015D-PromptReco-v3_RECO_CMSSW_7_4_12_patch4_pt20_pakhotin_v5_03.xml" # Nov 2015 Geom CSC
#xmlfile_ref="Geometries/data_CSC-1100-100001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_Shifted_02.xml" # 2016 shifted Geom CSC
#xmlfile_ref="Geometries/data_DT-1100-110001_SingleMuon_Run2016D_MuAlCalIsolatedMu_276315_276811_8_0_8_v1_03.xml" # 2016D 3DOF

#referenceName="3 DOF after Conical"
#referenceName="Conical"
#referenceName="Iter 1 vs Iter 3"
#referenceName="IDEAL_808_p1"
#referenceName="NOV_2015"
referenceName="May_2016"

#correctionName="Displacements from 3 DOF after Conical"
#correctionName="Displacements from Conical"
#correctionName="Displacements from Iter 1" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
#correctionName="Displacements from ideal geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
#correctionName="Displacements from 2015 Nov. geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries
correctionName="Displacements from 2016 May geometry" # 'corrections" if difference between initial and final geometries; 'displacements' if difference between IDEAL and final geometries

runComparison=true
uploadComparison=true
runCorrelation=false
printCorrelationFactors=false

doDT="true"
doCSC="false"

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
