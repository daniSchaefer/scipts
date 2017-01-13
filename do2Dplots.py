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

prefix =''
doFit = True


files = [#'ExoDiBosonAnalysis.TTbar50ns_GenStudies.root'
         'ExoDiBosonAnalysis.TTbar.root'
        ]

#
legendname = ['Fit t-mass', 'Fit W-mass']

histonames = [  #'Chi2vsbCandFlav',
#'Chi2vsWMass',
               'Chi2vsTMass'
              ]


rebin = 1


l = TLegend(.16,.7,.4,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)




filelist = []
histos = []

for f in files:
   filename = prefix + f
   filetmp = TFile.Open(filename,"READ") 
   filelist.append(filetmp)


for f in filelist:
  for h in histonames:
    histtmp = TH2F(f.Get(h))
    histtmp.SetName( h )

    histos.append(histtmp)

for j in xrange(0,len(histos)):
  # histos[j].SetLineColor(lineColor[j])
  # histos[j].SetLineStyle(lineStyle[j])
  # histos[j].SetLineWidth(2)
  # histos[j].Rebin(rebin)
  # if histos[j].Integral():
  #   histos[j].Scale(1./histos[j].Integral())
  legend = legendname[j]
# l.AddEntry(histos[j],legend,"l")
  

fits = []

xAxisTitle = "#chi^{2}"
  
yTitle = "M_{t}[GeV]"
   

canv = TCanvas("c", "",800,800)
canv.cd()

pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
pad0.SetBottomMargin(0.15)
pad0.SetTopMargin(0.08)
pad0.SetRightMargin(0.05)
pad0.Draw()
pad0.SetLogx()
pad0.cd()

for h in histos:
  h.GetXaxis().SetTitle( xAxisTitle )
  h.GetYaxis().SetTitle( yTitle )
  h.GetXaxis().SetLabelSize(0.04)
  h.GetYaxis().SetLabelSize(0.04)
  h.GetYaxis().SetTitleOffset(2.0)
  h.GetXaxis().SetTitleOffset(1.2)
  # h.GetXaxis().SetRangeUser(0.,500.)
  # h.GetYaxis().SetRangeUser(100.,250.)
  h.Draw("COLZ3SAME")




l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextFont(42)
l1.SetTextSize(0.04)
# l1.DrawLatex(0.60,0.89, "M_{X} = 2 TeV") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.DrawLatex(0.60,0.89, "t#bar{t}+jets (aMC@NLO)") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
# l1.DrawLatex(0.60,0.89, "Run2015D") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.SetTextSize(0.025)
l1.DrawLatex(0.60,0.84, "AK4")
l1.DrawLatex(0.60,0.80, "p_{T} > 30 GeV, |#eta| < 2.1")
# l1.DrawLatex(0.62,0.80, "M_{jj} > 1040 GeV, |#Delta#eta_{jj}| < 1.3")
# l1.DrawLatex(0.67,0.80,"60 GeV < M_{p} < 100 GeV")
  

   
l.Draw()

canv.Update()

time.sleep(100)
