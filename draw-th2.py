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
# gStyle.SetPalette(100)
gROOT.ForceStyle()


file1 = TFile.Open('ExoDiBosonAnalysis.Signal.BulkWW_800.root', "READ")
histoname =  'Tau21vsPt'       
hist1 = TH2F(file1.Get(histoname))

file2 = TFile.Open('ExoDiBosonAnalysis.Signal.BulkWW_2000.root', "READ")      
hist2 = TH2F(file2.Get(histoname))

file3 = TFile.Open('ExoDiBosonAnalysis.Signal.BulkWW_4000.root', "READ")      
hist3 = TH2F(file3.Get(histoname))

l = TLegend(.16,.8,.4,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)
 
l.AddEntry(hist1,"0.8 TeV","f")
l.AddEntry(hist2,"2.0 TeV","f")
l.AddEntry(hist3,"4.0 TeV","f")  

xAxisTitle = "#tau_{21}"
  
yTitle = "p_{T}"
   
canv = TCanvas("c", "",800,800)
canv.cd()

pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
pad0.SetBottomMargin(0.15)
pad0.SetTopMargin(0.08)
pad0.SetRightMargin(0.05)
# pad0.SetLogy()
pad0.Draw()
pad0.cd()

hist1.Rebin2D(4,4)
hist2.Rebin2D(4,4)
hist1.Scale(1./hist1.Integral())
hist2.Scale(1./hist2.Integral())
hist1.SetFillColor(TColor.kRed+1)
hist3.SetFillColor(TColor.kOrange+1)
hist2.SetFillColor(TColor.kCyan+2)
hist2.Draw("BOX")
hist1.Draw("sameBOX")
hist3.Draw("sameBOX")
  
hist2.GetXaxis().SetTitle( xAxisTitle )
hist2.GetYaxis().SetTitle( yTitle )
hist2.GetXaxis().SetLabelSize(0.04)
hist2.GetYaxis().SetLabelSize(0.04)
hist2.GetYaxis().SetTitleOffset(1.9)
hist2.GetXaxis().SetTitleOffset(1.5)

l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextFont(42)
l1.SetTextSize(0.04)
# l1.DrawLatex(0.60,0.89, "M_{X} = 2 TeV") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.DrawLatex(0.60,0.89, "Bulk G#rightarrowWW") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.SetTextSize(0.025)
l1.DrawLatex(0.60,0.84, "AK8")
l1.DrawLatex(0.60,0.80, "p_{T} > 200 GeV, |#eta| < 2.4")
# l1.DrawLatex(0.62,0.80, "M_{jj} > 1040 GeV, |#Delta#eta_{jj}| < 1.3")
# l1.DrawLatex(0.67,0.80,"60 GeV < M_{p} < 100 GeV")
  

   
l.Draw()

canv.Update()

time.sleep(100)
