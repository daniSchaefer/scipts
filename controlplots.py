import sys
from array import array
  
from ROOT import *
from ROOT import TColor
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

prunedVsSoftdrop = False
addPostfix = False

# files = [ 'ExoDiBosonAnalysis.GEN.RSWW_800.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_1000.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_1200.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_1400.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_2000.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_3000.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_4000.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_4000.root',
#           'ExoDiBosonAnalysis.GEN.RSWW_4000.root'
#         ]

files = [ #'ExoDiBosonAnalysis.Signal.WprimeToWh_2000.root',
          # 'ExoDiBosonAnalysis.Signal.BulkWW_1000.root',
          # 'ExoDiBosonAnalysis.Signal.BulkWW_1000.root',  
          '../AnalysisOutput/80X/SignalMC/ExoDiBosonAnalysis.BulkZZ_13TeV_1200GeV.VV.root',
          # 'ExoDiBosonAnalysis.Signal.RSWW_2000.root',
          # 'ExoDiBosonAnalysis.Signal.RSZZ_2000.root'
        ]




histonames = [  'Softdrop_eta1v2',
                'Softdrop_eta1v8',
                'Softdrop_eta2v4'
              ]



rebin = 1

lineStyle = [1,2,3,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]
# lineStyle = [2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1]
lineColor = [kRed+1, kOrange+1, kCyan+2, kAzure-1, kGreen+1, kMagenta, kBlue, kBlack,kCyan, kOrange, kViolet,]

#lineColor = [ TColor.kRed+1, TColor.kRed+1, TColor.kRed+1, TColor.kOrange+1,TColor.kOrange+1, TColor.kOrange+1,TColor.kCyan+2, TColor.kCyan+2]
# lineStyle = [1,2,1,2,1,2]
l = TLegend(.16,.7,.4,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)


filelist = []
histos = []

for f in files:
   filename = f
   filetmp = TFile.Open(filename,"READ") 
   filelist.append(filetmp)

for f in filelist:
  for h in histonames:
    if (f.GetName().find("WW") != -1 and (h.find("H") != -1 or h.find("Z") != -1)):
      continue
    if (f.GetName().find("ZZ") != -1 and (h.find("H") != -1 or h.find("W") != -1) ):  
      continue
    if (f.GetName().find("Wh") != -1 and h.find("Z") != -1):  
      continue
    histtmp = TH1F(f.Get(h))
    if not prunedVsSoftdrop:
      histtmp.SetName(f.GetName())
    histos.append(histtmp)

fits = []
for j in xrange(0,len(histos)):
  fittmp = TGraphAsymmErrors(histos[j])
  fits.append(histtmp)
  histos[j].SetLineColor(lineColor[j])
  histos[j].SetLineStyle(lineStyle[j])
  histos[j].SetLineWidth(2)
  if histos[j].Integral():
    histos[j].Scale(1./histos[j].Integral())
  histos[j].Rebin(rebin)
  legend = histos[j].GetTitle()
  if addPostfix:
    if histos[j].GetName().find("Bulk") != -1:
       legend+=" (Bulk G#rightarrowWW)"
    elif histos[j].GetName().find("RSWW") != -1:
       legend+=" (RS G#rightarrowWW)"
    elif histos[j].GetName().find("RSZZ") != -1:
       legend+=" (RS G#rightarrowZZ)"
    else:
       legend+=" (W'#rightarrowWH)"
  else:
     if histos[j].GetName().find("Pruned") != -1:
        legend+=" Pruned"
     if histos[j].GetName().find("Softdrop") != -1:
        legend+=" Softdrop"    
  l.AddEntry(histos[j],legend,"l")
  


xMin  = histos[0].GetXaxis().GetXmin()
xMax  = histos[0].GetXaxis().GetXmax()
nBins = histos[0].GetXaxis().GetNbins()
# xAxisTitle = "M_{jj} [GeV]"
if prunedVsSoftdrop:
  xAxisTitle = "M [GeV]"
else:
  xAxisTitle = "M [GeV]"
  
yTitle = "A.U"
   
canv = TCanvas("c", "",800,800)
canv.cd()

pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
pad0.SetBottomMargin(0.15)
pad0.SetTopMargin(0.08)
pad0.SetRightMargin(0.05)
# pad0.SetLogy()
pad0.Draw()
pad0.cd()
histos[0].SetMaximum(0.18)
histos[0].Draw("HIST")
for h in histos:
  h.Draw("sameHIST")
  
histos[0].GetXaxis().SetTitle( xAxisTitle )
histos[0].GetYaxis().SetTitle( yTitle )
histos[0].GetXaxis().SetLabelSize(0.04)
histos[0].GetYaxis().SetLabelSize(0.04)
histos[0].GetYaxis().SetTitleOffset(1.9)
histos[0].GetXaxis().SetTitleOffset(1.2)

l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextFont(42)
l1.SetTextSize(0.04)
# l1.DrawLatex(0.60,0.89, "M_{X} = 2 TeV") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.DrawLatex(0.60,0.89, "Bulk G (2 TeV)#rightarrowWW") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.SetTextSize(0.025)
l1.DrawLatex(0.60,0.84, "AK8")
l1.DrawLatex(0.60,0.80, "p_{T} > 200 GeV, |#eta| < 2.4")
# l1.DrawLatex(0.62,0.80, "M_{jj} > 1040 GeV, |#Delta#eta_{jj}| < 1.3")
# l1.DrawLatex(0.67,0.80,"60 GeV < M_{p} < 100 GeV")
  

   
l.Draw()

canv.Update()

time.sleep(100)
