#!/usr/bin/python
from array import *
from optparse import OptionParser
import ROOT

from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH1F,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad

#parser = OptionParser()
#parser.add_option('--signal', action="store",type="string",dest = "signal",default="", help="")



def openRootFile(filename,inputdir):
    f = ROOT.TFile.Open(filename)
    #print "open "+inputdir+filename
    #print f
    return f


def openTxtFile(filename):
    f = open(filename,"r")
    return f


def genNEvents(tree):
    N = tree.GetEntries()
    return N

def NEventsSR(tree):
    N=0
    for event in tree:
        N += event.weight
        #print event.lumiweight
    return N
        

def NEventsSB(tree):
    l = [0,0]
    for event in tree:
        if ( event.MVV < 1055.): continue
           #===================== qV try new sideband definition: leave q jet as it is, and require V jet to have a mass between 105-200 GeV================
        if ( event.jet_puppi_tau2tau1_jet1 <= 0.40 or event.jet_puppi_tau2tau1_jet2 <= 0.40):
               if event.jet_puppi_tau2tau1_jet1<= 0.40:
                   if (105 < event.jet_puppi_softdrop_jet1 < 200):
                       l[0]+= event.weight
                       continue
               if event.jet_puppi_tau2tau1_jet2 <= 0.40:
                   if (105 < event.jet_puppi_softdrop_jet2 < 200):
                       l[0]+= event.weight
                       
           
        if ((0.40 < event.jet_puppi_tau2tau1_jet1 <= 0.75) or (0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75)):
               if 0.40 < event.jet_puppi_tau2tau1_jet1<= 0.75:
                   if (105 < event.jet_puppi_softdrop_jet1 < 200):
                       l[1]+= event.weight
                       continue
               if 0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75:
                   if (105 < event.jet_puppi_softdrop_jet2 < 200):
                       l[1]+= event.weight
    return l


def NEventsSB_test3(tree):
    l = [0,0]
    for event in tree:
        if ( event.MVV < 1055.): continue
           #===================== qV try new sideband definition: leave q jet as it is, and require V jet to have a mass between 105-200 GeV================
        if ( event.jet_puppi_tau2tau1_jet1 <= 0.40 or event.jet_puppi_tau2tau1_jet2 <= 0.40):
               if event.jet_puppi_tau2tau1_jet1<= 0.40:
                   if (20 < event.jet_puppi_softdrop_jet1 < 65):
                       l[0]+= event.weight
                       continue
               if event.jet_puppi_tau2tau1_jet2 <= 0.40:
                   if (20 < event.jet_puppi_softdrop_jet2 < 65):
                       l[0]+= event.weight
                       
           
        if ((0.40 < event.jet_puppi_tau2tau1_jet1 <= 0.75) or (0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75)):
               if 0.40 < event.jet_puppi_tau2tau1_jet1<= 0.75:
                   if (20 < event.jet_puppi_softdrop_jet1 < 65):
                       l[1]+= event.weight
                       continue
               if 0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75:
                   if (20 < event.jet_puppi_softdrop_jet2 < 65):
                       l[1]+= event.weight
    return l


def NEventsSB_old(tree):
    l = [0,0]
    #nJet1 =0
    #nJet2 =0
    #nTau21HP = 0
    #nTau21LP = 0
    for event in tree:
        #if ( event.MVV < 1055.): continue
        #if ( 20 > event.jet_puppi_softdrop_jet1 or event.jet_puppi_softdrop_jet1 > 200):
            ##nJet1+=event.weight
            #continue
        #if (20 > event.jet_puppi_softdrop_jet2 or event.jet_puppi_softdrop_jet2 > 200):
               ##nJet2+=event.weight
               #continue
        #if (event.jet_puppi_softdrop_jet1 < 65 and event.jet_puppi_softdrop_jet2 > 105) or  (event.jet_puppi_softdrop_jet1 < 65 and event.jet_puppi_softdrop_jet2 > 105):
        #if ( event.jet_puppi_tau2tau1_jet1 <= 0.40):
               #l[0]+=event.weight
        #if ( 0.40 <event.jet_puppi_tau2tau1_jet1 <= 0.75):
               #l[1]+=event.weight
    #print str(nJet1)+"     "+ str(nJet2)
        if event.jet_puppi_tau2tau1_jet2 <= 0.40 or event.jet_puppi_tau2tau1_jet1 <= 0.40 :
        # if (20 < event.jet_puppi_softdrop_jet1 <= 65. and 20 < event.jet_puppi_softdrop_jet2 <= 65.):   
            if ( (20 < event.jet_puppi_softdrop_jet1 <= 65. and 105 < event.jet_puppi_softdrop_jet2) or (20 < event.jet_puppi_softdrop_jet2 <= 65. and 105 < event.jet_puppi_softdrop_jet1)):     
                l[0]+=event.weight #qVHP
        if 0.40 < event.jet_puppi_tau2tau1_jet1 <= 0.75 or 0.40 < event.jet_puppi_tau2tau1_jet2 <= 0.75 :
        # if (20 < event.jet_puppi_softdrop_jet1 <= 65. and 20 < event.jet_puppi_softdrop_jet2 <= 65.):
            if ( (20 < event.jet_puppi_softdrop_jet1 <= 65. and 105 < event.jet_puppi_softdrop_jet2) or (20 < event.jet_puppi_softdrop_jet2 <= 65. and 105 < event.jet_puppi_softdrop_jet1)):     
                l[1]+= event.weight #qVLP
    
    return l
  



if __name__== '__main__':
    
    
    mass = [1200,7000]
    nGen = []
    nSB  = []
    nSB_old =[]
    nSB_test3 =[]
    nSR  = []
    #infile = openTxtFile(options.filename)
    i =0
    j= 0
    for m in mass:
        f =  "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Spring16/QstarToQW_M_7000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_DIGI80X_RECO80X_MiniAODv2_80X_MiniAODv2_PUSpring16RAWAODSIM/EXOVVTree_QstarToQW_M_7000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_DIGI80X_RECO80X_MiniAODv2_80X_MiniAODv2_PUSpring16RAWAODSIM_1.root"
        f2 = "../AnalysisOutput/80X/SignalMC/ExoDiBosonAnalysis.QstarQW_13TeV_"+str(m)+"GeV.qV_SBtest.root"
        f3 = "../AnalysisOutput/80X/SignalMC/ExoDiBosonAnalysis.QstarQW_13TeV_"+str(m)+"GeV.qV.root"
        rootfile_noSelections = openRootFile(f,"")
        rootfile = openRootFile(f2,"")
        rootfileSR = openRootFile(f3,"")
        print rootfile
        if not rootfile:
           print rootfile
           continue
       
       # problem: wie soll signal contamination ausgewertet werden? mit gewichteten events? oder ohne gewichtete events? und wenn gewichtete events verwendet werden, was ist dann mein referenzpunkt? i.e. wie soll der signalbruchteil ausgerechnet werden??
        tree = rootfile_noSelections.Get("ntuplizer/tree")
        tree3 = rootfileSR.Get("tree")
        nAll =  genNEvents(tree)
        nGen.append(nAll)
        tree2 = rootfile.Get("tree")
        nSB.append(NEventsSB(tree2))
        nSB_test3.append(NEventsSB_test3(tree2))
        nSR.append(NEventsSR(tree3))
        nSB_old.append(NEventsSB_old(tree2))
        mvv = rootfileSR.Get("Mjj").Integral()
        print m
        print mvv
        if mvv <1:
            mvv = mvv*nAll
        nGen.append(mvv)
        
    
        print "                          HP                      LP"
        print "sideband definition: V jet in high-mass sideband q jet egal"
        print str(round(nSB[i][0]/nGen[j],2))+"        "+str(round(nSB[i][1]/nGen[j],2))
        print str(round(nSB[i][0]/nGen[j+1],2))+"        "+str(round(nSB[i][1]/nGen[j+1],2))
    
        #print nSB[i][0]
        #print nGen[j]
    
        print "sideband definition: V jet in low-mass sideband q jet egal"
        print str(round(nSB_test3[i][0]/nGen[j],2))+"        "+str(round(nSB_test3[i][1]/nGen[j],2))
        print str(round(nSB_test3[i][0]/nGen[j+1],2))+"        "+str(round(nSB_test3[i][1]/nGen[j+1],2))
        
        print "sideband definition: old sideband definition"
        print str(round(nSB_old[i][0]/nGen[j],2))+"        "+str(round(nSB_old[i][1]/nGen[j],2))
        print str(round(nSB_old[i][0]/nGen[j+1],2))+"        "+str(round(nSB_old[i][1]/nGen[j+1],2))
        
        print " signal region acceptance*efficiency"
        print nSR[i]/nGen[j]
        print nSR[i]/nGen[1+j]
        i+=1
        j=i+1
  
  
  
