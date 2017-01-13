from ROOT import *
import time
import math
import CMS_lumi, tdrstyle
import sys
import ConfigParser
import time
import gc


# gStyle.SetGridColor(kGray)
# gStyle.SetOptStat(kFALSE)
# gStyle.SetOptTitle(kFALSE)
# gStyle.SetPadTopMargin(0.07)
# gStyle.SetPadBottomMargin(0.13)
# gStyle.SetPadLeftMargin(0.14)
# gStyle.SetPadRightMargin(0.06)
# gROOT.ForceStyle()

# name = 'ExoDiBosonAnalysis.TTbar.root'
# fname = TFile.Open(name,"READ")

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "1.26 fb^{-1}, W #rightarrow #mu#nu"
CMS_lumi.writeExtraText = 0
CMS_lumi.extraText = "Preliminary"

H_ref = 600; 
W_ref = 700; 
W = W_ref
H  = H_ref

T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.06*W_ref

canvas = TCanvas("c2","c2",W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx()
canvas.SetTicky()
canvas.SetLogy()   

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.15
   
returnEfficiency = False
lumi = 1263.890
filename = ['ExoDiBosonAnalysis.TTbar.root','ExoDiBosonAnalysis.SingleTop.root','ExoDiBosonAnalysis.WJets.root','ExoDiBosonAnalysis.DYJets.root']
bkg = ['t#bar{t}','Single t','W+jets','DY+jets','WW/ZZ/WZ']
data = 'ExoDiBosonAnalysis.SingleMuon25ns_Run2015D.root'
fillStyle = [3018  ,1001  ,1001,1001,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
fillColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
lineWidth = [3     ,2     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2,2]
lineStyle = [2,1,1,1,1,1,1,1,1,1]
lineColor = [kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack]
legendStyle = ['F','F','F','F','F','F','F','F','F','F']   

legend = TLegend(.66,.65,.86,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.04)

Den = 0
j = 0
filelist = []
histolist = []
hs = THStack("hs", "cutflow")
for bname in filename:
  print 'Opening file %s' %bname
  fbkg = TFile.Open(bname)
  filelist.append(fbkg)
if returnEfficiency:
  for fname in filelist:
    hDEN  = (fname.Get( 'nEvents' )).GetBinContent(1)
    Den += hDEN

allMC=0    
for fname in filelist:
  hAll  = fname.Get( 'nEvents' ).GetBinContent(1)
  hCut0 = fname.Get( "nPassedTrigger" ).GetBinContent(1)
  hCut1 = fname.Get( "nPassedFilter" ).GetBinContent(1)
  hCut2 = fname.Get( "nPassedFoundLept" ).GetBinContent(1)
  hCut3 = fname.Get( "nPassedVetoLep" ).GetBinContent(1)
  hCut4 = fname.Get( "nPassedFoundMET" ).GetBinContent(1)
  hCut5 = fname.Get( "nPassed1Jet" ).GetBinContent(1)
  hCut6 = fname.Get( "nPassed2Jet" ).GetBinContent(1)
  hCut7 = fname.Get( "nPassed3Jet" ).GetBinContent(1)
  hCut8 = fname.Get( "nPassed4Jet" ).GetBinContent(1)
  hCut9 = fname.Get( "nPassedChi2" ).GetBinContent(1)
  
  print "File= %s  Passed Trigger = %i" %(fname.GetName(),hCut1*lumi)
  print "File= %s  Passed All = %i" %(fname.GetName(),hCut9*lumi)
  allMC += hCut8*lumi
  print "Passed All, all MC = %i" %allMC
  # hCut7 = fname.Get( "nPassed1bTag" )
  # hCut8 = fname.Get( "nPassed2bTag" )
  if returnEfficiency:
    den = Den
  if not returnEfficiency:
    den = 1./lumi
  h = TH1F( 'hpx%i'%j, 'px%i'%j, 10, 0, 10 )
  # h.SetBinContent(1, hAll/den)
  h.SetBinContent(1, hCut0/den)
  h.SetBinContent(2, hCut1/den)
  h.SetBinContent(3, hCut2/den)
  h.SetBinContent(4, hCut3/den)
  h.SetBinContent(5, hCut4/den)
  h.SetBinContent(6, hCut5/den)
  h.SetBinContent(7, hCut6/den)
  h.SetBinContent(8, hCut7/den)
  h.SetBinContent(9, hCut8/den)
  h.SetBinContent(10, hCut9/den)

  h.SetLineColor(lineColor[j+1])
  h.SetLineWidth(lineWidth[j+1])
  h.SetLineStyle(lineStyle[j+1])
  h.SetFillStyle(fillStyle[j+1])
  h.SetFillColor(fillColor[j+1])
  legend.AddEntry(h,bkg[j],legendStyle[j+1])


  h.GetXaxis().SetBinLabel(1,"Trigger")
  h.GetXaxis().SetBinLabel(2,"Filter") 
  h.GetXaxis().SetBinLabel(3,"FoundLep")
  h.GetXaxis().SetBinLabel(4,"VetoLep")
  h.GetXaxis().SetBinLabel(5,"MET")
  h.GetXaxis().SetBinLabel(6,"#geq1 jet")
  h.GetXaxis().SetBinLabel(7,"#geq2 jet")
  h.GetXaxis().SetBinLabel(8,"#geq3 jet")
  h.GetXaxis().SetBinLabel(9,"#geq4 jet")
  h.GetXaxis().SetBinLabel(10,"chi^{2}")
  h.GetYaxis().SetTitle('Efficiency')
  h.SetName(fname.GetName())
  histolist.append(h)  
  j += 1

for j in range(1,len(histolist)+1):  
  hs.Add( histolist[len(histolist)-j],"HIST")
  
file_data = TFile.Open(data,"READ")
hAll  = file_data.Get( 'nEvents' ).GetBinContent(1)
hCut0 = file_data.Get( "nPassedTrigger" ).GetBinContent(1)
hCut1 = file_data.Get( "nPassedFilter" ).GetBinContent(1)

hCut2 = file_data.Get( "nPassedFoundLept" ).GetBinContent(1)
hCut3 = file_data.Get( "nPassedVetoLep" ).GetBinContent(1)
hCut4 = file_data.Get( "nPassedFoundMET" ).GetBinContent(1)
hCut5 = file_data.Get( "nPassed1Jet" ).GetBinContent(1)
hCut6 = file_data.Get( "nPassed2Jet" ).GetBinContent(1)
hCut7 = file_data.Get( "nPassed3Jet" ).GetBinContent(1)
hCut8 = file_data.Get( "nPassed4Jet" ).GetBinContent(1)
hCut9 = file_data.Get( "nPassedChi2" ).GetBinContent(1)
print "File= %s  Passed Trigger = %i" %(file_data.GetName(),hCut1)
print "File= %s  Passed All = %i" %(file_data.GetName(),hCut8)
if returnEfficiency:
  den = hAll
if not returnEfficiency:
  den = 1.
h_data = TH1F( 'h_data', 'h_data', 10, 0, 10 )
h_data.SetBinContent(1, hCut0/den)
h_data.SetBinContent(2, hCut1/den)
h_data.SetBinContent(3, hCut2/den)
h_data.SetBinContent(4, hCut3/den)
h_data.SetBinContent(5, hCut4/den)
h_data.SetBinContent(6, hCut5/den)
h_data.SetBinContent(7, hCut6/den)
h_data.SetBinContent(8, hCut7/den)
h_data.SetBinContent(9, hCut8/den) 
h_data.SetBinContent(10, hCut9/den) 
h_data.SetLineColor(kBlack)
h_data.SetLineColor(kBlack);
h_data.SetMarkerColor(kBlack);
h_data.SetMarkerStyle(20);
h_data.SetMarkerSize(1.);
legend.AddEntry(h_data,"CMS Data","P")

canvas.cd()
hs.Draw()
hs.SetMaximum(hs.GetMaximum()*1.2)
h_data.Draw("samePE")
legend.Draw()
canvas.Update()
CMS_lumi.CMS_lumi(canvas, 4, 0)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()
canvas.cd()
canvas.Update()
#
# l1 = TLatex()
# l1.SetTextAlign(13)
# l1.SetTextFont(42)
# l1.SetNDC()
# l1.SetTextSize(0.04)
# l1.DrawLatex(0.14+0.03,0.25, 'Run 2015D')
#
# l1.SetTextAlign(12)
# l1.SetTextSize(0.045)
# l1.SetTextFont(62)
# l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")
#
# l1.SetTextAlign(12)
# l1.SetTextSize(0.035)
# l1.SetTextFont(61)
# l1.DrawLatex(0.13,0.96, "CMS")
# l1.SetTextSize(0.03)
# l1.SetTextFont(52)
# l1.DrawLatex(0.21,0.96, "Preliminary")

canvas.Update()
time.sleep(100)