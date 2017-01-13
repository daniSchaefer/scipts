from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
from array import array
from ROOT import SetOwnership
  
gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetOptTitle(0)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

def sigmoid(x,p):
    max_eff = 1.
    return max_eff/(1+math.exp(-p[1]*(x[0]-p[0])))
    # return max_eff/(p[1]+math.exp(-p[0]*x[0]))
    return sigmoid
    # k == 1/sigma*Ethres, x0 = EThreshold

fname = 'lowerPM_ExoDiBosonAnalysis.QCD.TriggerStudy.root'
#----------------as a function on M(jj)--------------------------#
hdenname = 'TriggerEffPruningCut'
# hnumname1 = 'jjTriggerEffMjj_HLT_AK8PFJet360TrimMod'
# hnumname2 = 'jjTriggerEffMjj_HLT_PFHT900'
hnumname2 = 'TriggerEff_ALL_wPruningCut'
hnumname3 = 'TriggerEff_HT_wPruningCut'

# hdenname  = 'jjTriggerEffMjjPruningCut'
# hnumname1 = 'jjTriggerEffMjj_HLT_AK8PFJet360TrimMod_wPruningCut'
# hnumname2 = 'jjTriggerEffMjj_HLT_PFHT900_wPruningCut'
# hnumname3 = 'jjTriggerEffMjj_both_wPruningCut'

# hdenname = 'jjTriggerEffMjjSoftdropCut'
# hnumname1 = 'jjTriggerEffMjj_HLT_AK8PFJet360TrimMod_wSoftDropCut'
# hnumname2 = 'jjTriggerEffMjj_HLT_PFHT900_wSoftDropCut'
# hnumname3 = 'jjTriggerEffMjj_both_wSoftDropCut'

# hdenname = 'jjTriggerEffMjjTau21Cut'
# hnumname1 = 'jjTriggerEffMjj_HLT_AK8PFJet360TrimMod_wTau21Cut'
# hnumname2 = 'jjTriggerEffMjj_HLT_PFHT900_wTau21Cut'

#----------------as a function on Pruned/SD mass------------------#

# hdenname = 'TriggerEffPrunedMassDen'
# hdenname = 'TriggerEffSoftdropMassDen'
# hdenname = 'TriggerEffPrunedMassDen_PtCut'
# hdenname = 'TriggerEffSoftdropMassDen_PtCut'
# hnumname1 = 'TriggerEffPrunedMass_HLT_AK8PFJet360TrimMod_wMjjCut'
# hnumname1 = 'TriggerEffSoftdropMass_HLT_AK8PFJet360TrimMod_wMjjCut'
# hnumname1 = 'TriggerEffPrunedMass_HLT_AK8PFJet360TrimMod_PtCut'
# hnumname1 = 'TriggerEffSoftdropMass_HLT_AK8PFJet360TrimMod_PtCut'
#--------------------------------------------------------#

# hnum1 = ROOT.TH1F(ROOT.TFile.Open(fname).Get(hnumname1))
hnumALL = TH1F(TFile.Open(fname).Get(hnumname2))
hnumHT = TH1F(TFile.Open(fname).Get(hnumname3))
hden  = TH1F(TFile.Open(fname).Get(hdenname))
 


# fit_x2 = ROOT.TF1("fit_x2", "1/( 1+math.exp(-(x-[1])/([0]*[1])) )", 1., 50.)
# fit_x2.SetParameters(5, 20)           # Remember to give good starting values!
# h_efficiency.Fit("fit_x2","+")

# hnum1.Rebin(10)
hnumALL.Rebin(40)
hnumHT.Rebin(40)
hden.Rebin(40)

fit_x3 = TF1("fit_x3", sigmoid, 0., 2000., 2)
fit_x3.SetParameters(1.0,0.01)      

#--------------------------------------------------------#
# h_efficiency = hnum1
# h_efficiency.Divide(hden)
#
#
# h_efficiency.Fit(fit_x3, "+","",30.,200.)
# h_efficiency.Draw()
#
# fit = h_efficiency.GetFunction("fit_x3")
# mass = fit.GetX(0.990, 40., 2000., 1.E-10, 100, False)
# print hnum1.GetTitle()
# print mass
# print "#################"
# time.sleep(10)

#--------------------------------------------------------#

h_efficiencyHT =  TGraphAsymmErrors()
h_efficiencyHT.Divide(hnumHT,hden)
h_efficiencyHT.SetMarkerStyle(20)
h_efficiencyHT.SetMarkerColor(kRed)
h_efficiencyHT.SetLineColor( kBlack)

h_efficiencyALL =  TGraphAsymmErrors()
h_efficiencyALL.Divide(hnumALL,hden)
h_efficiencyALL.SetMarkerStyle(20)
h_efficiencyALL.SetMarkerColor(kBlue)
h_efficiencyALL.SetLineColor( kBlack)

h_efficiencyHT.GetXaxis().SetRangeUser(200.,1500.)
h_efficiencyALL.GetXaxis().SetRangeUser(200.,1500.)
# h_efficiencyHT = hnumHT
# h_efficiencyHT.Divide(hden)
h_efficiencyHT.Fit(fit_x3, "+","",800.,1200.)

# h_efficiencyALL = hnumALL
# h_efficiencyALL.Divide(hden)
h_efficiencyALL.Fit(fit_x3, "+","",500.,1200.)

c = TCanvas("c", "",800,800)
c.cd()


h_efficiencyHT.Draw("AP")
h_efficiencyALL.Draw("Psame")

c.Update()

c.SetGridx()
c.SetGridy()
# h_efficiencyHT.SetMarkerColor(kRed)
# h_efficiencyHT.SetMarkerStyle(22)
# h_efficiencyALL.SetMarkerColor(kBlack)
# h_efficiencyALL.SetMarkerStyle(26)
h_efficiencyHT.SetMaximum(1.35)
h_efficiencyHT.GetXaxis().SetTitleOffset(1.2)
h_efficiencyHT.GetYaxis().SetTitleOffset(1.5)
h_efficiencyHT.GetYaxis().SetNdivisions(1010)

# mg.GetXaxis().SetTitle("Softdrop M_{j} [GeV]")
# mg.GetXaxis().SetTitle("M_{jj}")
# mg.GetXaxis().SetTitle("Softdrop Mass_{Leading jet} [GeV]")
h_efficiencyHT.GetXaxis().SetTitle("M_{jj} [GeV]")

xMin  = h_efficiencyHT.GetXaxis().GetXmin()
xMax  = h_efficiencyHT.GetXaxis().GetXmax()
nBins = h_efficiencyHT.GetXaxis().GetNbins()	

h_efficiencyHT.GetYaxis().SetTitle("Efficiency")

#--------------------------------------------------------#

fit = h_efficiencyALL.GetFunction("fit_x3")
massALL = fit.GetX(0.990, 40., 2000., 1.E-10, 100, False)
print "ALL"
print massALL
print "#################"
time.sleep(7)

fit = h_efficiencyHT.GetFunction("fit_x3")
massHT = fit.GetX(0.9900, 40., 2000., 1.E-10, 100, False)
print "HT only"
print massHT
print "#################"

l = TLegend(.16,.77,.36,.85)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)
l.AddEntry(h_efficiencyHT, "OR (HT triggers only) (>99 %% for M_{jj} > %.0f GeV)" %massHT, "lep" )
l.AddEntry(h_efficiencyALL, "OR (including substructure triggers) (>99 %% for M_{jj} > %.0f GeV)" %massALL, "lep" )
l.Draw()



# l1 = TLatex()
# l1.SetTextAlign(13)
# l1.SetTextFont(42)
# l1.SetNDC()
# l1.SetTextSize(0.04)
# l1.DrawLatex(0.12+0.03,0.88, "HT taggers only: >99 %%: M_{jj} > %.1f GeV" %massHT)
# l1.DrawLatex(0.12+0.03,0.88, "Including substr. taggers: >99 %%: M_{jj} > %.1f GeV" %massALL)
c.Update()



time.sleep(100)