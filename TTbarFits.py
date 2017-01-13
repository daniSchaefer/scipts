from ROOT import *
import time

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()


lumi=1000
rebin = 2
files = []
prefix="/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/SFmeas_plots"


f = TFile.Open('ExoDiBosonAnalysis.SFmu_TTJets.root ')
hT = TH1F(f.Get('HadronicTopMass'))

hT.Fit('gaus','','',100.,210.)
c1 = TCanvas('c1', "",800,800)
c1.cd()
hT.Draw()

#
# hW = TH1F(f.Get('HadronicWMass'))
#
# hW.Fit('gaus','','')
# c2 = TCanvas('c2', "",800,800)
# c2.cd()
# hW.Draw("HIST")

time.sleep(100)