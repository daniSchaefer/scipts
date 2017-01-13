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

files.append('ExoDiBosonAnalysis.SingleTop.root ')
files.append('ExoDiBosonAnalysis.WJets.root ')
files.append('ExoDiBosonAnalysis.TTJets.root ')
histos = ["WmassLeptonic","LeptonicbCSV","LeptonicbFlavor","bCandCSV","bCandFlavor","HadronicTop","WmassHadronic","WtransvMassHadronic","WptLeptonic","WptHadronic","WmassLeptonic","LeptonicTop","WmassLeptonic2","LeptonicTop2"]

for h in histos:
  
  legend = TLegend(.76,.74,.86,.87)
  legend.SetBorderSize(0)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetTextFont(42)
  legend.SetTextSize(0.021)
  
  histolist = []
  hs =  THStack("hs", h)
  for fname in files:
    f = TFile.Open(fname)
    histolist.append( TH1F(f.Get(h)))

  colors = [ kGreen+2, kRed, kBlue, kBlack, kMagenta, kOrange+2, kCyan ]
  sample = [ "Single top","W+jets", "TT+jets","TT+jets", "W+jets","TT+jets", "W+jets", ]

  for j in range(0,len(histolist)):
    histolist[j].Scale(lumi)
    histolist[j].Rebin(rebin)
    histolist[j].SetFillColor(colors[j])
    histolist[j].SetLineColor(colors[j])
    # histolist[j].SetLineStyle(2)
    hs.Add(histolist[j],"hist")
    legend.AddEntry(histolist[j], sample[j],"f")
  c = TCanvas(h, "",800,800)
  c.cd()
  hs.Draw("HIST")
  legend.Draw()
  c.SetGridx()
  c.SetGridy()
  l1 = TLatex()
  l1.SetNDC()
  l1.SetTextAlign(12)
  l1.SetTextSize(0.045)
  l1.SetTextFont(62)
  l1.DrawLatex(0.82,0.96, "1.26 fb^{-1}")
  # canvasname = prefix+"/"+h+".png"
  # c.Print(canvasname,"png")
  time.sleep(100)

#
#
# # hs.GetXaxis().SetTitle(xAxisTitle )
# # hs.GetYaxis().SetTitle( yTitle )
# hs.GetXaxis().SetLabelSize(0.04)
# hs.GetYaxis().SetLabelSize(0.04)
# hs.GetYaxis().SetTitleOffset(1.5)
# hs.GetXaxis().SetTitleOffset(1.2)



# if (fLogy):
#   c.SetLogy()
#   legend.Draw()
#   l1 = TLatex()
#   l1.SetTextAlign(13)
#   l1.SetTextFont(42)
#   l1.SetNDC()
#   l1.SetTextSize(0.04)
#   l1.DrawLatex(0.14+0.03,0.85, fTitle)
#
#   l1.SetTextAlign(12)
#   l1.SetTextSize(0.045)
#   l1.SetTextFont(62)
#   l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")
#
#   l1.SetTextFont(42)
#   l1.SetTextSize(0.025)
#   l1.DrawLatex(0.2,0.42, fExtraInfo)
#
#   c.SaveAs(fOutputFile)

time.sleep(100)