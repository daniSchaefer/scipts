from optparse import OptionParser
import ROOT
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
from array import array
from ROOT import SetOwnership
import os


def write(fname, histogram):
    """Write the new histogram to disk"""
    base, ext = os.path.splitext(fname)
    outfname = "/shome/thaarres/EXOVVAnalysisRunII/LimitCode/CMSSW_7_1_5/src/DijetCombineLimitCode/input/" + base + ".root"
    print "Saving file %s " %outfname
    fout = ROOT.TFile(outfname,"UPDATE")
    histogram.Write()
    fout.Close()


argv = sys.argv
parser = OptionParser()   
parser.add_option("-L", "--lumi", dest="lumi", default=3000,
                              help="Set lumi")                
parser.add_option("-P", "--usePruned", dest="usePruned", default=False, action="store_true",
                              help="Use pruned mass")
parser.add_option("-S", "--signal", dest="signal", default = "BulkWW",
                  help="input signal", metavar="SIGNAL")                                                                                                                                                                               			      			      			      			      
(opts, args) = parser.parse_args(argv)  

filelist = []

if usePruned:
  masscat = 'Pruned'
else:
  masscat = 'SD'  
    
prefix = '/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/VV/'
files = ['QCD','M-600','M-800','M-1000','M-1200','M-1400','M-1600','M-1800','M-2000','M-2500','M-3000','M-3500','M-4000','M-4500']
h = 'DiBosonInvMass'
lumi = opts.lumi
rebin = 1

histnames= ["DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassHighPuriVV", # VV high purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV", # VV medium purity
            "DijetMassMediumPuriVV" # VV medium purity
          
            #"DijetMassLowPuriVV", # not used
            #"DijetMassHighPuriqV", # qV high purity
            #"DijetMassMediumPuriqV", # qV medium purity
            #"DijetMassLowPuriqV", # not used
            ]


for f in files:
   filename = prefix + "HP/Pruned/" +masscat +'/'+ opts.signal +".ExoDiBosonAnalysis." + f + ".root"
   filetmp = ROOT.TFile.Open(filename,"READ") 
   filelist.append(filetmp)
   filename = prefix + "LP/Pruned/" +masscat +'/'+ opts.signal +".ExoDiBosonAnalysis." + f + ".root"
   filetmp = ROOT.TFile.Open(filename,"READ") 
   filelist.append(filetmp)

histolist = []

for f in filelist:
   histolist.append(f.Get(h))
   
for j in xrange(0,len(histolist)):
   if j == 0 or j == 14:
      histolist[j].Scale(lumi)
   histolist[j].Rebin(rebin)
   histolist[j].SetLineColor(j+2)
   histolist[j].SetLineWidth(2)
   histolist[j].SetName(histnames[j])
   for e in range(1,histolist[j].GetNbinsX()):
      error = math.sqrt(histolist[j].GetBinContent(e))
      histolist[j].SetBinError(e,error)
   histtmp.Draw()   

files += ['QCD','M-600','M-800','M-1000','M-1200','M-1400','M-1600','M-1800','M-2000','M-2500','M-3000','M-3500','M-4000','M-4500']

histolist[0].Draw("")
for h in histolist:
   h.Draw("same")
   
# if lumi == 1000.:
#    names = ['QCD_13TeV_1fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV','QCD_13TeV_1fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV']
# if lumi == 3000.:
#    names = ['QCD_13TeV_3fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV','QCD_13TeV_3fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV']
# if lumi == 10000.:
#    names = ['QCD_13TeV_10fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV','QCD_13TeV_10fb','RS1WW_13TeV_1000GeV','RS1WW_13TeV_2000GeV','RS1WW_13TeV_3000GeV','RS1WW_13TeV_4000GeV']


if lumi == 1000.:
   for j in xrange(0,len(histolist)):
     if(j = 0 or j = 14):
       write(files[j] + '_1fb',histolist[j])
     else:
       write(opts.signal + files[j] + '_1fb',histolist[j])  
else if lumi == 3000.:
   for j in xrange(0,len(histolist)):
      if(j = 0 or j = 14):
        write(files[j] + '_3fb',histolist[j])
      else:
        write(opts.signal + files[j] + '_3fb',histolist[j])
else if lumi == 10000.:
  for j in xrange(0,len(histolist)):
    if(j = 0 or j = 14):
      write(files[j] + '_10fb',histolist[j])
    else:
      write(opts.signal + files[j] + '_10fb',histolist[j])
   
time.sleep(10)

