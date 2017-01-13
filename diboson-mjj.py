#!/usr/bin/python

from optparse import OptionParser
import os,commands, os.path
import sys
from ROOT import *
import math
import time
import CMS_lumi, tdrstyle
import copy
# ---------------------------------------------------------------------------------------------------------------------------
def write(fname, histogram):
    """Write the new histogram to disk"""
    base = fname
    outfname = "/shome/thaarres/EXOVVAnalysisRunII/CMSSW_7_1_5/src/DijetCombineLimitCode/input/" + base + ".root"
    print "Saving file %s " %outfname
    fout = TFile(outfname,"UPDATE")
    histogram.Write()
    fout.Close()
# ---------------------------------------------------------------------------------------------------------------------------
argv = sys.argv
parser = OptionParser()   
parser.add_option("-L", "--lumi", dest="lumi", default=1263.890,
                              help="Set lumi")                                                                                                                                                                                            			      			      			      			      
(opts, args) = parser.parse_args(argv)  

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "1.26fb^{-1}"
CMS_lumi.writeExtraText = 0
CMS_lumi.extraText = "Preliminary"

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.15

path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned/"
h = 'DiBosonInvMass'
lumi = 1263.890
print lumi
rebin = 1
    
# ---------------------------------------------------------------------------------------------------------------------------  

cmd = "rm /shome/thaarres/EXOVVAnalysisRunII/CMSSW_7_1_5/src/DijetCombineLimitCode/input/*.root"
print cmd
os.system(cmd)
      
i =0
histolist = []
for root, _, files in os.walk(path):
  for f in files:
    fullpath = os.path.join(root, f)
    if not (fullpath.find(".root")!=-1):
      continue
    if (fullpath.find(".TT")!=-1 or fullpath.find(".VJets")!=-1 or fullpath.find("trigger")!=-1  or fullpath.find("GEN")!=-1  or fullpath.find("newPU")!=-1):
      continue  
    print "+++++++++++"
    print fullpath
    if fullpath.find("QCD")!=-1:
      lumi = 1263.890
      print lumi
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      print name
    elif fullpath.find("DATA")!=-1:
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      if fullpath.find("SB")!=-1:
        name1 = fullpath.split(".")[1]
        name = name1.split("_")[0]
        name+= "_SB"  
      lumi = 1.
    else:
      name = fullpath.split(".")[1]+'.'+fullpath.split(".")[2]
      name = name.split(".")[0]
      lumi = 1.
    print name
    filetmp = TFile.Open(fullpath,"READ") 
    histtmp = filetmp.Get(h)
    print lumi
    histtmp.Scale(lumi)
    # histtmp.SetBinErrorOption(TH1.kPoisson)
    # for e in range(1,histtmp.GetNbinsX()):
    #    error = math.sqrt(histtmp.GetBinContent(e))
    #    histtmp.SetBinError(e,error)
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_VV")!=-1 or fullpath.find(".VV.")!=-1) :
      histtmp.SetName("DijetMassHighPuriVV")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_VV")!=-1 or fullpath.find(".VV.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriVV") 
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_VV")!=-1 or fullpath.find(".VV.")!=-1) :
      histtmp.SetName("DijetMassNoPuriVV")
      
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_WW")!=-1 or fullpath.find(".WW.")!=-1) :
      histtmp.SetName("DijetMassHighPuriWW")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_WW")!=-1 or fullpath.find(".WW.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriWW") 
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_WW")!=-1 or fullpath.find(".WW.")!=-1) :
      histtmp.SetName("DijetMassNoPuriWW")
      
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_WZ")!=-1 or fullpath.find(".WZ.")!=-1) :
      histtmp.SetName("DijetMassHighPuriWZ")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_WZ")!=-1 or fullpath.find(".WZ.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriWZ")  
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_WZ")!=-1 or fullpath.find(".WZ.")!=-1) :
      histtmp.SetName("DijetMassNoPuriWZ")  
      
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_ZZ")!=-1 or fullpath.find(".ZZ.")!=-1) :
      histtmp.SetName("DijetMassHighPuriZZ")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_ZZ")!=-1 or fullpath.find(".ZZ.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriZZ")
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_ZZ")!=-1 or fullpath.find(".ZZ.")!=-1) :
      histtmp.SetName("DijetMassNoPuriZZ")
    
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_qV")!=-1 or fullpath.find(".qV.")!=-1) :
      histtmp.SetName("DijetMassHighPuriqV")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_qV")!=-1 or fullpath.find(".qV.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriqV") 
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_qV")!=-1 or fullpath.find(".qV.")!=-1) :   
      histtmp.SetName("DijetMassNoPuriqV")
        
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_qW")!=-1 or fullpath.find(".qW.")!=-1) :
      histtmp.SetName("DijetMassHighPuriqW")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_qW")!=-1 or fullpath.find(".qW.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriqW") 
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_qW")!=-1 or fullpath.find(".qW.")!=-1) :   
      histtmp.SetName("DijetMassNoPuriqW")
      
    if fullpath.find("/HP/")!=-1 and (fullpath.find("_qZ")!=-1 or fullpath.find(".qZ.")!=-1) :
      histtmp.SetName("DijetMassHighPuriqZ")  
    if fullpath.find("/LP/")!=-1 and (fullpath.find("_qZ")!=-1 or fullpath.find(".qZ.")!=-1) :   
      histtmp.SetName("DijetMassLowPuriqZ")
    if fullpath.find("/NP/")!=-1 and (fullpath.find("_qZ")!=-1 or fullpath.find(".qZ.")!=-1) :   
      histtmp.SetName("DijetMassNoPuriqZ")
        
    hist = copy.copy(histtmp)
    hist.Rebin(rebin)
    # hist.SetLineColor(colors[i])
    # hist.SetLineWidth(2)
    # histolist.append(hist)
    # l.AddEntry(hist,name,"l")
    write(name,histtmp)
    i += 1
    filetmp.Close() 
     
# ---------------------------------------------------------------------------------------------------------------------------      

#
#
# canv = TCanvas("c", "",1000,800)
# canv.cd()
#
# pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
# pad0.SetBottomMargin(0.15)
# pad0.SetTopMargin(0.08)
# pad0.SetRightMargin(0.05)
# #pad0.SetLogy()
# pad0.Draw()
# pad0.cd()
#
#
#
# histolist[0].Rebin(50)
# histolist[0].Scale(1./histolist[0].Integral())
# Max = histolist[0].GetMaximum()*3
# histolist[0].Draw('hist')
# histolist[0].SetMaximum(Max)
# histolist[0].GetXaxis().SetRangeUser(900.,7000.)
#
# for j in range(1,len(histolist)):
#   if(histolist[j].Integral()>0):
#     histolist[j].Rebin(50)
#     histolist[j].Scale(1./histolist[j].Integral())
#     if(1.>histolist[j].GetMaximum()>Max):
#       Max = histolist[j].GetMaximum()
#       histolist[0].SetMaximum(Max)
#     histolist[j].Draw('HISTsame')
#   else:
#     print "HAVE EMPTY HISTOGRAM!!!!"
# l.Draw()
# time.sleep(100)

del histolist
        
  
             



