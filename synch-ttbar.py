
from optparse import OptionParser
import os,commands, os.path
import sys
from ROOT import *
import math
import time
from array import *
# import CMS_lumi, tdrstyle
import copy


gROOT.SetBatch( True )

path1 = "/shome/jngadiub/EXOVVAnalysisRunII/CMSSW_5_3_13/src/boostedWWAnalysis_old/AnaSigTree_forTT/"
path2 = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Wtag/WWTree_"
path3 = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Wtag/lowMass/WWTree_"

channels1=["mu","el"]
channels2=["mu","el"]
samples1=["TTBARpowheg","SingleTop","VV","WJetsPt180","data"]
samples2=["TTbar","STop","VV","WJets","data"]
histolist=[]

i=-1
for ch in channels2:
  i+=1
  print ""
  print ""
  print ""
  print ""
  print "-------------"
  print "- %s channel: -" %ch
  print "-------------"
  j=-1
  for sample in samples2:
    print ""
    print "%s" %sample
    print "-------------"
    j+=1
    fname1 = path1 + channels1[i] + "/treeEDBR_"+samples1[j]+"_xww.root"
    file1 = TFile.Open(fname1,"READ")
    intree1 = file1.Get("tree")
    print "Entries:"
    print "Jen = %i" %intree1.GetEntries()
  
    fname2 = path2 + channels2[i] + "/ExoDiBosonAnalysis.WWTree_"+samples2[j]+".root"
    file2 = TFile.Open(fname2,"READ")
    intree2 = file2.Get("tree")
    print "Me = %i" %intree2.GetEntries()
    fname3 = path3 + channels2[i] + "/ExoDiBosonAnalysis.WWTree_"+samples2[j]+".root"
    file3 = TFile.Open(fname3,"READ")
    intree3 = file3.Get("tree")
    print "LowMass = %i" %intree3.GetEntries()
    print "-------------"
    
    print "weights:"
    intree1.Draw("weight")
    print "Jen = %f" %htemp.GetMean()
    del htemp
    intree2.Draw("weight")
    print "Me = %f" %htemp.GetMean()
    del htemp
    print "-------------"
    intree1.Draw("puweight")
    print "Jen = %f" %htemp.GetMean()
    del htemp
    intree2.Draw("puweight")
    print "Me = %f" %htemp.GetMean()
    del htemp
    print "-------------"
    intree1.Draw("lumiweight")
    print "Jen = %f" %htemp.GetMean()
    del htemp
    intree2.Draw("lumiweight")
    print "Me = %f" %htemp.GetMean()
    del htemp
    print "-------------"
    intree1.Draw("genweight")
    print "Jen = %f" %htemp.GetMean()
    del htemp
    intree2.Draw("genweight")
    print "Me = %f" %htemp.GetMean()
    del htemp
    print "-------------"
  
  


# hRun = TH1F('hRun','hRun',7000,0,7000)
# hEvent = TH1F('hEvent','hEvent',7000,0,7000)
# hMVV = TH1F('hMVV','hMVV',700,0,7000)
# hPrunedM = TH1F('hPrunedM','hPrunedM',500,0,500)
# hl_pt = TH1F('hl_pt','hl_pt',3000,0,3000)
# hl_eta = TH1F('hl_eta','hl_eta',100,-3.1,73.1)
#
#
# histolist.append(hRun)
# histolist.append(hEvent)
# histolist.append(hMVV)
# histolist.append(hPrunedM)
# histolist.append(hl_pt)
# histolist.append(hl_eta)
#
# events1=[]
# i =-1
# for event in intree1:
#   if i == 2:
#     break
#   if (500. < event.MWW < 501.):
#     i+=1
#     events1.append(event.event)
#     print "----- JENS TREE -----"
#     print "Event = %i" %event.event
#     print "MWW = %f" %event.MWW
#     print "Pruned mass = %f" %event.Mjpruned
#     print "lepton pT = %f" %event.lept_pt
#     print "MET = %f" %event.met
#
#
# print ""
# print ""
# print ""
# print ""
# print ""
# print events1
# for event in intree2:
#  for ev in events1:
#    if event.event==ev:
#       print "----- MY TREE -----"
#       print "Event = %i" %event.event
#       print "MWW = %f" %event.MWW
#       print "Pruned mass = %f" %event.Mjpruned
#       print "lepton pT = %f" %event.lept_pt
#       print "MET = %f" %event.pfMET
#
#   # hRun.Fill(event.run)
#   # hEvent.Fill(event.event)
#   # hMVV.Fill(event.MWW)
#   # hPrunedM.Fill(event.Mjpruned)
#   # hl_pt.Fill(event.lept_pt)
#   # hl_eta.Fill(event.lept_eta)
#
#
# # for h in histolist:
# #    print "Scaling histogram to %f pb"%lumi
# #    print "Saving histogram %s" %h.GetName()
# #    h.Scale(lumi)
# #  write(name,histolist)
# #  filetmp.Close()
# #  del intree
# #  del histolist
#
