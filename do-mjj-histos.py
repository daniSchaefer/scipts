
from optparse import OptionParser
import os,commands, os.path
import sys
from ROOT import *
import math
import time
from array import *
# import CMS_lumi, tdrstyle
import copy
# ---------------------------------------------------------------------------------------------------------------------------
def write(fname, histolist):
    """Write the new histogram to disk"""
    base = fname
    outfname = "/shome/thaarres/EXOVVAnalysisRunII/LimitCode/CMSSW_7_1_5/src/DijetCombineLimitCode/input/" + base + ".root"
    # outfname = base + ".root"
    print "Saving file %s " %outfname
    fout = TFile(outfname,"RECREATE")
    for h in histolist:
      h.Write()
    fout.Close()
# ---------------------------------------------------------------------------------------------------------------------------
argv = sys.argv
parser = OptionParser()   
parser.add_option("-L", "--lumi", dest="lumi", default=12900,
                              help="Set lumi")                                                                                                                                                                                            			      			      			      			      
(opts, args) = parser.parse_args(argv)  

path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/"
rebin = 1
    
# ---------------------------------------------------------------------------------------------------------------------------  

# cmd = "rm /shome/thaarres/EXOVVAnalysisRunII/CMSSW_7_1_5/src/DijetCombineLimitCode/input/*.root"
# print cmd
# os.system(cmd)


gROOT.SetBatch(kTRUE)
      
i =0
histolist = []
for root, _, files in os.walk(path):
  for f in files:
    fullpath = os.path.join(root, f)
    if not (fullpath.find(".root")!=-1):
      continue
    if (fullpath.find(".TT")!=-1 or fullpath.find(".VJets")!=-1 or fullpath.find("trigger")!=-1  or fullpath.find("GEN")!=-1):
      continue
    if not fullpath.find("Qstar")!=-1:
      continue
    # if not fullpath.find("Qstar")!=-1:
    #   continue
    # print "+++++++++++"
    print "Working on  file %s" %fullpath
    if fullpath.find("QCD")!=-1:
      lumi = opts.lumi
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      if fullpath.find("_VV")!=-1: 
        name = "QCD_VV"
      if fullpath.find("_qV")!=-1: 
        name = "QCD_qV"
    elif fullpath.find("DATA")!=-1:
      name1 = fullpath.split(".")[1]
      name = name1.split("_")[0]
      if fullpath.find("_VV")!=-1: 
        name+= "_VV"
      if fullpath.find("_qV")!=-1: 
        name+= "_qV"
      if fullpath.find("SB")!=-1:
        name1 = fullpath.split(".")[1]
        name = name1.split("_")[0]
        name+= "_SB"  
      lumi = 1.
    else:
      name = fullpath.split(".")[1]+'.'+fullpath.split(".")[2]
      name = name.split(".")[0]
      lumi = 1.
    print "Will save to filename %s" %name
    filetmp = TFile.Open(fullpath,"READ") 
    intree = filetmp.Get("tree")
    print "Using lumi = %s" %lumi
    
    histolist=[]

    VVHP = TH1F('DijetMassHighPuriVV','DijetMassHighPuriVV',7000,0,7000)
    WWHP = TH1F('DijetMassHighPuriWW','DijetMassHighPuriWW',7000,0,7000)
    WZHP = TH1F('DijetMassHighPuriWZ','DijetMassHighPuriWZ',7000,0,7000)
    ZZHP = TH1F('DijetMassHighPuriZZ','DijetMassHighPuriZZ',7000,0,7000)
    VVLP = TH1F('DijetMassLowPuriVV','DijetMassLowPuriVV',7000,0,7000)
    WWLP = TH1F('DijetMassLowPuriWW','DijetMassLowPuriWW',7000,0,7000)
    WZLP = TH1F('DijetMassLowPuriWZ','DijetMassLowPuriWZ',7000,0,7000)
    ZZLP = TH1F('DijetMassLowPuriZZ','DijetMassLowPuriZZ',7000,0,7000)
    qVHP = TH1F('DijetMassHighPuriqV','DijetMassHighPuriqV',7000,0,7000)
    qWHP = TH1F('DijetMassHighPuriqW','DijetMassHighPuriqW',7000,0,7000)
    qZHP = TH1F('DijetMassHighPuriqZ','DijetMassHighPuriqZ',7000,0,7000)
    qVLP = TH1F('DijetMassLowPuriqV','DijetMassLowPuriqV',7000,0,7000)
    qWLP = TH1F('DijetMassLowPuriqW','DijetMassLowPuriqW',7000,0,7000)
    qZLP = TH1F('DijetMassLowPuriqZ','DijetMassLowPuriqZ',7000,0,7000)
    VVNP = TH1F('DijetMassNoPuriVV','DijetMassNoPuriVV',7000,0,7000)
    WWNP = TH1F('DijetMassNoPuriWW','DijetMassNoPuriWW',7000,0,7000)
    WZNP = TH1F('DijetMassNoPuriWZ','DijetMassNoPuriWZ',7000,0,7000)
    ZZNP = TH1F('DijetMassNoPuriZZ','DijetMassNoPuriZZ',7000,0,7000)
    qVNP = TH1F('DijetMassNoPuriqV','DijetMassNoPuriqV',7000,0,7000)
    qWNP = TH1F('DijetMassNoPuriqW','DijetMassNoPuriqW',7000,0,7000)
    qZNP = TH1F('DijetMassNoPuriqZ','DijetMassNoPuriqZ',7000,0,7000)
    
    histolist.append(VVHP)
    histolist.append(WWHP)
    histolist.append(WZHP)
    histolist.append(ZZHP)
    histolist.append(VVLP)
    histolist.append(WWLP)
    histolist.append(WZLP)
    histolist.append(ZZLP)
    histolist.append(VVNP)
    histolist.append(WWNP)
    histolist.append(WZNP)
    histolist.append(ZZNP)
    histolist.append(qVHP)
    histolist.append(qWHP)
    histolist.append(qZHP)
    histolist.append(qVLP)
    histolist.append(qWLP)
    histolist.append(qZLP)
    histolist.append(qVNP)
    histolist.append(qWNP)
    histolist.append(qZNP)
    
    # intree.SetBranchAddress('jet_mass_pruned_jet1'  , jet_mass_pruned_jet1  )
    #
    # nentries = intree.GetEntries()
    # n = 0
    # for e in range(nentries):
    #    intree.GetEntry(e)
    #
    #    print jet_mass_pruned_jet1[0]
    #
    #
    for event in intree:
      
      if ( event.MVV < 965): continue
      
      if  event.category == 0:
        VVHP.Fill(event.MVV,event.weight) #VVHP

      if event.category == 1:
         VVLP.Fill(event.MVV,event.weight) #VVLP

      if event.category == 0 or event.category == 1 or event.category == 4:
         VVNP.Fill(event.MVV,event.weight) #VVNP

      if event.channel == 2:
         WWHP.Fill(event.MVV,event.weight) #WWHP

      if event.channel == 3:
         WWLP.Fill(event.MVV,event.weight) #WWLP

      if event.channel == 2 or event.channel == 3 or event.channel == 14:
         WWNP.Fill(event.MVV,event.weight) #WWNP

      if event.channel == 4:
         WZHP.Fill(event.MVV,event.weight) #WZHP

      if event.channel == 5:
         WZLP.Fill(event.MVV,event.weight) #WZLP

      if event.channel == 4 or event.channel == 5 or event.channel == 15:
         WZNP.Fill(event.MVV,event.weight) #WZNP

      if event.channel == 6:
         ZZHP.Fill(event.MVV,event.weight) #ZZHP

      if event.channel == 7:
         ZZLP.Fill(event.MVV,event.weight) #ZZLP

      if event.channel == 6 or event.channel == 7 or event.channel == 16:
         ZZNP.Fill(event.MVV,event.weight) #ZZNP

      if event.category == 2:
         qVHP.Fill(event.MVV,event.weight) #qVHP

      if event.category == 3:
         qVLP.Fill(event.MVV,event.weight) #qVLP

      if event.category == 2 or event.category == 3 or event.category == 5:
         qVNP.Fill(event.MVV,event.weight) #qVNP

      if event.channel == 10:
         qWHP.Fill(event.MVV,event.weight) #qWHP

      if event.channel == 11:
         qWLP.Fill(event.MVV,event.weight) #qWLP

      if event.channel == 10 or event.channel == 11 or event.channel == 17:
         qWNP.Fill(event.MVV,event.weight) #qWNP

      if event.channel == 12:
         qZHP.Fill(event.MVV,event.weight) #qZHP

      if event.channel == 13:
         qZLP.Fill(event.MVV,event.weight) #qZLP

      if event.channel == 12 or event.channel == 13 or event.channel == 18:
         qZNP.Fill(event.MVV,event.weight) #qZNP


    for h in histolist:
      print "Scaling histogram to %f pb"%lumi
      print "Saving histogram %s" %h.GetName()
      h.Scale(lumi)
      h.Sumw2() 
    write(name,histolist)
    filetmp.Close()
    del intree
    del histolist

