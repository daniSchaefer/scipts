import sys
from array import array
  
from ROOT import *
import time
import math

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetOptTitle(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

bfname = 'ExoDiBosonAnalysis.QCD_VV_HP_SD.root'
sfname = 'ExoDiBosonAnalysis.74X.BulkWW_3000.root'
hname = 'DeltaEta'

l = TLegend(.66,.75,.86,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)
#--------------------------------------------------------#
h_signal = TH1F(TFile.Open(sfname).Get(hname))
h_signal.SetLineColor(1)
h_signal.SetLineWidth(2)
h_signal.SetLineStyle(1)
h_signal.SetFillStyle(3018)
h_signal.SetFillColor(1)
h_signal.Scale(1/h_signal.Integral())
h_signal.Rebin(1)

l.AddEntry(h_signal,'Bulk G (3 TeV)','l')

hbkg = TH1F(TFile.Open(bfname).Get(hname))
hbkg.SetLineColor(2)
hbkg.SetLineWidth(2)
hbkg.SetLineStyle(1)
hbkg.SetFillStyle(101)
hbkg.SetFillColor(2)
hbkg.Scale(1/hbkg.Integral())
hbkg.Rebin(1)

l.AddEntry(hbkg,'QCD','l')

canv = TCanvas("c2","c2",900,1800)
canv.cd()

pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
pad0.SetBottomMargin(0.15)
pad0.SetTopMargin(0.08)
pad0.SetRightMargin(0.05)
pad0.Draw()
pad0.cd()

h_signal.Draw("HIST")
hbkg.Draw("sameHIST")
l.Draw()

h_signal.GetXaxis().SetTitle( "|#Delta#eta_{jj}|")
h_signal.GetYaxis().SetTitle( "AU" )
h_signal.GetXaxis().SetLabelSize(0.04)
h_signal.GetYaxis().SetLabelSize(0.04)
h_signal.GetYaxis().SetTitleOffset(1.9)
h_signal.GetXaxis().SetTitleOffset(1.1)

time.sleep(100)