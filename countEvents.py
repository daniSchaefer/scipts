#!/usr/bin/python
from array import *
from optparse import OptionParser
import ROOT

from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH1F,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad

parser = OptionParser()
parser.add_option('--filename', action="store",type="string",dest = "filename",default="", help="name of txt file containing samples")
parser.add_option('--N',dest="N", type="int",default=0, action="store", help="number of files")
parser.add_option('--ext', action="store_true",default=False,dest="ext", help="use file ending ext1")
parser.add_option('--suffix',action="store",default="QCD",dest="suffix",help = "use files with this name")

(options, args) = parser.parse_args()
suffix = options.suffix

#suffix = "Pt_800to1000"
#suffix = "Pt_1000to1400"
#suffix = "Pt_1400to1800"
#suffix = "Pt_1800to2400"
#suffix = "Pt_2400to3200"
#suffix = "Pt_3200toInf"
#suffix = "Pt_170to300"
#suffix = "Pt_300to470"
#suffix = "Pt_470to600"
#suffix = "Pt_600to800"

#suffix = "HT50to100"
#suffix = "HT100to200"
#suffix = "HT200to300"
#suffix = "HT300to500"
#suffix = "HT500to700"
#suffix = "HT700to1000"
#suffix = "HT1000to1500"
#suffix = "HT1500to2000"
#suffix = "HT2000toInf"

def openRootFile(filename,inputdir):
    f = ROOT.TFile.Open(filename)
    #print "open "+inputdir+filename
    #print f
    return f


def openTxtFile(filename):
    f = open(filename,"r")
    return f

def getFilenameQCD(n):
    filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1-"+str(int(n))+"/flatTuple.root"
    
    filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1-"+str(int(n))+"/flatTuple.root"
    if options.ext ==False:
        filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1-"+str(int(n))+"/flatTuple.root"
        
        filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1-"+str(int(n))+"/flatTuple.root"
        
    return filename

if __name__== '__main__':
    
    
    #f = ROOT.TFile.Open("dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1-1/flatTuple.root")
    nEvents =0
    if options.filename !="":
        infile = openTxtFile(options.filename)
        for line in infile:
            print line
            s = line.split("\n")
            #print s
            rootfile = openRootFile(s[0],"")
            if rootfile == 0:
                continue
            if rootfile.GetSize()>10000:
                nEvents += rootfile.Get("ntuplizer/tree").GetEntries()
    else:
         for i in range(1,options.N+1):
             #print getFilenameQCD(i)
             rootfile = openRootFile(getFilenameQCD(i),"")
             #print rootfile
             if not rootfile:
                print rootfile
                continue
             if rootfile.GetSize()>10000:
                nEvents += rootfile.Get("ntuplizer/tree").GetEntries()
        
    print nEvents
