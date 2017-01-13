from optparse import OptionParser
import sys
import ConfigParser
from ROOT import *
import os
import multiprocessing
import array
 
training_vars_float = [
  ]
 
training_vars_int = [
  ""
  ]

argv = sys.argv
parser = OptionParser()
parser.add_option("-w", "--weight", dest="weight", default=False, action="store_true",
                              help="pt-eta reweight")                   
parser.add_option("-f", "--file", dest="filename",
                  help="write to FILE", metavar="FILE")                                                                                                                                                                               			      			      			      			      
(opts, args) = parser.parse_args(argv)  

def train(bdtoptions):

  outFile = TFile('FinalTraining.root', 'RECREATE')
  print "Printing output to %s" %outFile.GetName()

  factory = TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               # "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification"
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification"
                             )
  
  TMVA_tools = TMVA.Tools.Instance()
  treeS = TChain('Fjets')
  treeB = TChain('Fjets')
  treelist = []

  treeB.Add('/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/VV/HP/SD/ExoDiBosonAnalysis.QCD.root')
  treeS.Add('/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/VV/HP/SD/ExoDiBosonAnalysis.BulkWW.M-1000.root')
  factory.AddSignalTree(treeS, 1.)
  factory.AddBackgroundTree(treeB, 1.)
  
  signal_selection = ' '
  print "Signal selection = %s" %signal_selection
  background_selection =''
  print "Bkg selection = %s" %background_selection
  num_pass = treeS.GetEntries(signal_selection)
  num_fail = treeB.GetEntries(background_selection)

  print 'N events signal', num_pass
  print 'N events background', num_fail
  

  for var in training_vars_float:
    print "Adding variable: %s" %var
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable
  
    
  if (opts.weight):
    # factory.AddSpectator("weight_etaPt")
    factory.SetWeightExpression('nbHadrons+1',"Background")
  # else:
    # factory.SetWeightExpression('1.')
    
  
  factory.PrepareTrainingAndTestTree( TCut(signal_selection), TCut(background_selection), 
      # "nTrain_Signal=0::nTest_Signal=0:nTrain_Background=20000:nTest_Background=20000:SplitMode=Random:!V" )
      "nTrain_Signal=0::nTest_Signal=0:nTrain_Background=0:nTest_Background=0:SplitMode=Random:!V" )
      # "nTrain_Signal=30000:nTest_Signal=12000:nTrain_Background=30000:nTest_Background=50000:SplitMode=Random:!V" )
      
  # factory.BookMethod( TMVA.Types.kFisher, "Fisher", "!H:!V:Fisher" )
  factory.BookMethod( TMVA.Types.kCuts,
                      "Cuts",
                      "GA"

  
  factory.TrainAllMethods()
  factory.OptimizeAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()

  outFile.Close()
  
  p.close()
  p.join()

  # gLoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
  # TMVAGui('TMVA_classification.root')
  # raw_input("Press Enter to continue...")




if __name__ == '__main__':
  
    bdtoptions = [ "!H",
                                 "!V",
                                 "NTrees=750",
                                 "MinNodeSize=2.5%",
                                 "BoostType=Grad",
                                 "Shrinkage=0.20",
                                 #"UseBaggedBoost",
                                 #"GradBaggingFraction=0.5",
                                 "nCuts=20",
                                 "MaxDepth=4",
                                 "PruneMethod=CostComplexity",
                                 "PruneStrength=2"
                               ]
 
    train(bdtoptions)

