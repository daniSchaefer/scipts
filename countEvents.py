#!/usr/bin/python
from array import *
from optparse import OptionParser
import ROOT

from ROOT import gROOT, TPaveLabel, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH1F,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad

parser = OptionParser()
parser.add_option('--filename', action="store",type="string",dest = "filename",default="", help="name of txt file containing samples")
parser.add_option('--N',dest="N", type="int",default=0, action="store", help="number of files")
parser.add_option('--ext', action="store_true",default=False,dest="ext", help="use file ending ext1")
parser.add_option('--herwig', action="store_true",default=False,dest="herwig", help="use file ending ext1")
parser.add_option('--herwig2', action="store_true",default=False,dest="herwig2", help="use file ending ext1")
parser.add_option('--suffix',action="store",default="QCD",dest="suffix",help = "use files with this name")
parser.add_option('--directory',action="store",default="",dest="directory",help = "use files with this name")
parser.add_option('--signal',action="store",default="",dest="signal",help = "count signal events")
parser.add_option('--mass',action="store",default=1200,dest="mass",help = "signal mass")
parser.add_option('--Wjets',action="store_true",default=False,dest="Wjets")

(options, args) = parser.parse_args()
suffix = options.suffix
directory = options.directory

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
    vx = ""
    if options.ext:
        vx = "_ext"
    filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia820170203_QCD"+vx+"/"+directory+"/0000/flatTuple_"+str(int(n))+".root"
    
    if suffix.find("HT")!=-1:
        filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8820170203_QCD"+vx+"/"+directory+"/0000/flatTuple_"+str(int(n))+".root"
    if options.herwig:
        filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigppQCDherwig/170212_121715/0000/flatTuple_"+str(int(n))+".root"
    if options.herwig2:
        filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp20170203_QCD/170203_133821/0000/flatTuple_"+str(int(n))+".root"
    if options.Wjets:
        filename = getFilenameWJets(n)
    return filename

def getFilenameWJets(n):
    filename = "dcap://t3se01.psi.ch:22125///pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8BulkGHerwig/170220_161227/0000/flatTuple_"+str(n)+".root"
    return filename


def getFilenameSignal(mass,model,direc,n):
    suffix = ''
    if model.find('BulkWW')!=-1:
        suffix = 'BulkGravToWW'
    if model.find('BulkZZ')!=-1:
        suffix = 'BulkGravToZZToZhadZhad'
    if model.find('Zprime')!=-1:
        suffix = 'ZprimeToWW'
    if model.find('Wprime')!=-1:
        suffix = 'WprimeToWZToWhadZhad'
    if model.find('QstarQW')!=-1:
        suffix = 'QstarToQW'
    if model.find('QstarQZ')!=-1:
        suffix = 'QstarToQZ' 

    if model.find('Qstar')==-1:
          filename = 'dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/'+suffix+'_narrow_M-'+str(int(mass))+'_13TeV-madgraph/'+suffix+'_narrow_M-'+str(int(mass))+'_13TeV-madgraph20170203_signal/'+direc+'/0000/flatTuple_'+str(n)+'.root'
        
    else:
            filename ='dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170203/'+suffix+'_M-'+str(int(mass))+'_TuneCUETP8M2T4_13TeV-pythia8/'+suffix+'_M-'+str(int(mass))+'_TuneCUETP8M2T4_13TeV-pythia820170203_signal/'+direc+'/0000/flatTuple_'+str(n)+'.root' 
    

#def getFilenameQCD(n):
    #filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1-"+str(int(n))+"/flatTuple.root"
    
    #filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1-"+str(int(n))+"/flatTuple.root"
    #if options.ext ==False:
        #filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV_pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1-"+str(int(n))+"/flatTuple.root"
        
        #filename = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/hinzmann/jobtmp_QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/QCD_"+suffix+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1-"+str(int(n))+"/flatTuple.root"
        
    return filename

if __name__== '__main__':
    
    
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
             if options.signal =="":
                rootfile = openRootFile(getFilenameQCD(i),"")
             else:
                rootfile = openRootFile(getFilenameSignal(options.mass,options.signal,directory,i),"") 
             #print rootfile
             if not rootfile:
                print rootfile
                continue
             if rootfile.GetSize()>10000:
                nEvents += rootfile.Get("ntuplizer/tree").GetEntries()
        
    print nEvents
