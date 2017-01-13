LD_PRELOAD=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/lhapdf/6.1.6-giojec/lib/libLHAPDF.so sframe_main config/qV_private_80X.xml
ldd ~/SFrame/bin/sframe_main
lhapdf-config --libdir
g++ -O2 -m64  -shared obj/BinomialEff.o obj/JetCandidate.o obj/VCandidate.o obj/InputData.o obj/LHEWeight.o obj/MuonCandidate.o obj/HistosManager.o obj/PredictedDistribution.o obj/METCandidate.o obj/BTagWeight.o obj/NtupleManager.o obj/ExoDiBosonAnalysis.o obj/PUWeight.o obj/LumiWeight.o obj/RecoCandidate.o obj/Utilities.o obj/LeptonCandidate.o obj/HLTWeight.o obj/HiggsCandidate.o obj/MatchingTools.o obj/ExoDiBosonAnalysis_Dict.o -o /mnt/t3nfs01/data01/shome/dschafer/SFrame/lib/libExoDiBosonAnalysis.soq
make -n
touch src/ExoDiBosonAnalysis.cxx
scramv1 tool



