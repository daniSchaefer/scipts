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

prunedVsSoftdrop = False
addPostfix = True

prefix = 'VV/HP/SD/'

addBKG = False
doFit = True
bkgfile = TFile.Open('VV/HP/SD/ExoDiBosonAnalysis.QCD.root','READ')
bkghist = 'PrunedMass_all'

files = [ 'ExoDiBosonAnalysis.RS1ZZ.M-2000.root',
          #'ExoDiBosonAnalysis.RS1WW.M-600.root',
          #'ExoDiBosonAnalysis.RS1WW.M-800.root',
          # 'ExoDiBosonAnalysis.RS1WW.M-1000.root',
          # 'ExoDiBosonAnalysis.RS1WW.M-1200.root',
          #'ExoDiBosonAnalysis.RS1WW.M-1400.root',
          #'ExoDiBosonAnalysis.RS1WW.M-1600.root',
          #'ExoDiBosonAnalysis.RS1WW.M-1800.root',
          'ExoDiBosonAnalysis.BulkWW.M-2000.root',
          'ExoDiBosonAnalysis.RS1WW.M-2000.root',
          'ExoDiBosonAnalysis.WprimeWH.M-2000.root'
          #'ExoDiBosonAnalysis.RS1WW.M-2500.root',
          #'ExoDiBosonAnalysis.RS1WW.M-3000.root',
          # 'ExoDiBosonAnalysis.RS1WW.M-3500.root',
          # 'ExoDiBosonAnalysis.RS1WW.M-4000.root'
          ]
# legendname = ['1.0 TeV','2.0 TeV','3.0 TeV','4.0 TeV',]

# files = [ #'ExoDiBosonAnalysis.Substructure.M-800.Beta0.root',
#           # 'ExoDiBosonAnalysis.Substructure.M-800.BetaM1.root',
#           # 'ExoDiBosonAnalysis.Substructure.M-800.BetaP1.root',
#           'ExoDiBosonAnalysis.Substructure.M-2000.Beta0.root',
#           # 'ExoDiBosonAnalysis.Substructure.M-2000.BetaDEFAULT.root',
#           'ExoDiBosonAnalysis.Substructure.M-2000.BetaM1.root',
#           'ExoDiBosonAnalysis.Substructure.M-2000.BetaP1.root',
#           # 'ExoDiBosonAnalysis.Substructure.M-4000.Beta0.root'
#           # 'ExoDiBosonAnalysis.Substructure.M-4000.BetaM1.root',
#           # 'ExoDiBosonAnalysis.Substructure.M-4000.BetaP1.root',
#           ]

legendname = ['0.6 TeV','0.8 TeV','1.0 TeV','1.4 TeV','2.0 TeV','3.0 TeV','4.0 TeV']
legendname = ['1.0 TeV Gen','1.0 TeV Reco','4.0 TeV Gen','4.0 TeV Reco']

# legendname = ['0.8 TeV Gen','0.8 TeV Reco','2.0 TeV Gen','2.0 TeV Reco']
#
# legendname = ['#beta = 0','#beta = -1','#beta = +1']

histonames = [  #'genWMass',
                #'genWSoftdropMass',
                #'genWPrunedMass'
                # 'recoWSoftdropMass',
                 'recoWPrunedMass',
                'recoZPrunedMass',
                # 'recoZSoftdropMass',
                #'genHMass',
                'recoHPrunedMass',
                # 'recoHSoftdropMass',
                # 'PrunedMass_all'
              ]
# histonames = [  #'genWMass',
#                 'recoWSoftdropMass',
#                 'recoZSoftdropMass',
#                 #'genHMass',
#                 'recoHSoftdropMass'
#               ]
# histonames = [  'genWMass',
#                 'genZMass',
#                 'genHMass'
#               ]



rebin = 10

lineStyle = [1,2,8,4,1,6,7,8,9,1,2,3,4,5,6,7,8,9]
# lineStyle = [2,1,8,2,1,8,2,1,2,1,2,1,2,1,2,1,2,1]
# lineStyle = [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1]
# lineStyle = [1,1,1,1,1,1,1]
lineColor = [ kRed+1,kCyan+1,kAzure-1, kOrange+1, kViolet-4,kGreen-3,kCyan+1, kAzure-1, kBlack,kMagenta,kBlue, kBlack,kCyan, kOrange,  kViolet]
# lineColor = [kGreen,kGreen, kRed,kRed, kBlack,kBlack,kBlue,kBlue,kCyan,kCyan,kMagenta,kMagenta, kOrange,  kOrange,kAzure,kAzure, kViolet, kViolet]
# lineColor = [ kRed+1, kRed+1,kRed+1,kCyan+2, kCyan+2,kCyan+2, kOrange+1, kOrange+1]
# lineColor = [ kRed+1, kRed+1,kCyan+2, kCyan+2, kOrange+1, kOrange+1]
# lineStyle = [1,2,1,2,1,2]
l = TLegend(.16,.7,.4,.9)
# l = TLegend(.16,.8,.4,.9)
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

if addBKG:
  bkghist = TH1F(bkgfile.Get(bkghist))
  bkghist.SetFillStyle(3003)
  bkghist.SetFillColor(1)
  bkghist.SetLineColor(0)
  bkghist.Scale(1./bkghist.Integral())
  bkghist.Rebin(rebin)
  bkghist.GetXaxis().SetRangeUser(0.,200.)
  bkghist.SetMaximum(0.400)



for f in filelist:
  for h in histonames:
    if (f.GetName().find("WW") != -1 and (h.find("H") != -1 or h.find("Z") != -1 or h.find("all") != -1)):
      continue
    if (f.GetName().find("ZZ") != -1 and (h.find("H") != -1 or h.find("W") != -1 or h.find("all") != -1)):
      continue
    if (f.GetName().find("WH") != -1 and (h.find("Z") != -1 or h.find("all") != -1)):
      continue
    if (f.GetName().find("QCD") != -1 and (h.find("H") != -1 or h.find("Z") != -1 or h.find("W") != -1)):
      continue
    histtmp = TH1F(f.Get(h))
    if not prunedVsSoftdrop:
      histtmp.SetName(f.GetName())
    histos.append(histtmp)
  
for j in xrange(0,len(histos)):
  histos[j].SetLineColor(lineColor[j])
  histos[j].SetLineStyle(lineStyle[j])
  histos[j].SetLineWidth(2)
  if histos[j].Integral():
    histos[j].Scale(1./histos[j].Integral())
  print '%s, %s :' %(histos[j].GetTitle(),histos[j].GetName())
  print 'Integral 60-100 = %f' %histos[j].Integral(histos[j].FindBin(60.),histos[j].FindBin(100.))
  print 'Integral 110-135 = %f' %histos[j].Integral(histos[j].FindBin(100.),histos[j].FindBin(135.))
  print 'Integral All = %f' %histos[j].Integral()
  histos[j].Rebin(rebin)
  legend = histos[j].GetTitle()
  
  if addPostfix:
    if histos[j].GetName().find("Bulk") != -1:
       legend+=" (Bulk G#rightarrowWW)"
    elif histos[j].GetName().find("RS1WW") != -1:
       legend+=" (RS G#rightarrowWW)"
    elif histos[j].GetName().find("RS1ZZ") != -1:
       legend+=" (RS G#rightarrowZZ)"
    else:
       legend+=" (W'#rightarrowWH)"
  if prunedVsSoftdrop:
     if histos[j].GetName().find("Pruned") != -1:
        legend+=" Pruned"
     if histos[j].GetName().find("Softdrop") != -1:
        legend+=" Softdrop"    
  if histos[j].GetName().find("QCD") != -1:
       legend = "QCD"   
  else:
    # legend = legendname[j]
    l.AddEntry(histos[j],legend,"l")
  histos[j].SetName( legend )

fits = []

for h in histos:
  # fittmp = TGraphAsymmErrors(h)
  fittmp = TGraph(h)
  fits.append(fittmp)
    
# l.AddEntry(histos[0],'#beta = 0',"l")
# l.AddEntry(histos[1],'#beta = -1',"l")
# l.AddEntry(histos[2],'#beta = +1',"l")

if addBKG:
  l.AddEntry(bkghist,'QCD',"f")
  
# xAxisTitle = "M_{jj} [GeV]"
if prunedVsSoftdrop:
  xAxisTitle = "M [GeV]"
else:
  xAxisTitle = "M [GeV]"
  
yTitle = "Arbitrary scale"
   
canv = TCanvas("c", "",800,800)
canv.cd()

pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
pad0.SetBottomMargin(0.15)
pad0.SetTopMargin(0.08)
pad0.SetRightMargin(0.05)
# pad0.SetLogy()
pad0.Draw()
pad0.cd()
if addBKG:
    bkghist.Draw('HISTs')
    bkghist.GetXaxis().SetTitle( xAxisTitle )
    bkghist.GetYaxis().SetTitle( yTitle )
    bkghist.GetXaxis().SetLabelSize(0.04)
    bkghist.GetYaxis().SetLabelSize(0.04)
    bkghist.GetYaxis().SetTitleOffset(1.9)
    bkghist.GetXaxis().SetTitleOffset(1.2)
if doFit:
  fits[0].Draw("AC")
  for f in fits:
    f.Draw("Csame")    
  fits[0].GetXaxis().SetTitle( xAxisTitle )
  fits[0].GetYaxis().SetTitle( yTitle )
  fits[0].GetXaxis().SetLabelSize(0.04)
  fits[0].GetYaxis().SetLabelSize(0.04)
  fits[0].GetYaxis().SetTitleOffset(1.9)
  fits[0].GetXaxis().SetTitleOffset(1.2)  
  fits[0].SetMaximum(0.700)
  fits[0].GetXaxis().SetRangeUser(0.,200.)
# else:
#   histos[0].Draw("HIST")
#   histos[0].GetXaxis().SetTitle( xAxisTitle )
#   histos[0].GetYaxis().SetTitle( yTitle )
#   histos[0].GetXaxis().SetLabelSize(0.04)
#   histos[0].GetYaxis().SetLabelSize(0.04)
#   histos[0].GetYaxis().SetTitleOffset(1.9)
#   histos[0].GetXaxis().SetTitleOffset(1.2)
#   histos[0].GetXaxis().SetRangeUser(0.,200.)
#   histos[0].SetMaximum(0.150)
# for h in histos:
#   h.Draw("sameHIST")


l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextFont(42)
l1.SetTextSize(0.04)
# l1.DrawLatex(0.60,0.89, "M_{X} = 2 TeV") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.DrawLatex(0.60,0.89, "G_{RS1}#rightarrowWW") # {#scriptstyle(X=G_{Bulk}/G_{RS}/W')}
l1.SetTextSize(0.025)
l1.DrawLatex(0.60,0.84, "Softdrop AK8")
l1.DrawLatex(0.60,0.80, "p_{T} > 200 GeV, |#eta| < 2.4")
# l1.DrawLatex(0.62,0.80, "M_{jj} > 1040 GeV, |#Delta#eta_{jj}| < 1.3")
# l1.DrawLatex(0.67,0.80,"60 GeV < M_{p} < 100 GeV")
  

   
l.Draw()

canv.Update()

time.sleep(100)
