from ROOT import *
import time
import math
import CMS_lumi, tdrstyle
import sys
import ConfigParser
import time
import gc

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "2.1 fb^{-1}, W #rightarrow #mu#nu"
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
lumi = 2100.00
lumi =1
path = "Wtag/WWTree_mu/"
filename = ['ExoDiBosonAnalysis.WWTree_data.root','ExoDiBosonAnalysis.WWTree_data_76X.root']
fillStyle = [3018  ,1001  ,1001,1001,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
fillColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
lineWidth = [2     ,2     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2,2]
lineStyle = [1,1,1,1,1,1,1,1,1,1]
lineColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
legendStyle = ['l','l','l','l','l','l']   

legend = TLegend(.40,.65,.86,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.025)

Den = 0
j = 0
filelist = []
histolist = []
hs = THStack("hs", "cutflow")
for bname in filename:
  fname = path + bname
  print 'Opening file %s' %fname
  fbkg = TFile.Open(fname)
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
  hCut5 = fname.Get( "nPassedFoundW" ).GetBinContent(1)
  hCut6 = fname.Get( "nPassedFoundJet" ).GetBinContent(1)
  hCut7 = fname.Get( "nPassedLepJetDR" ).GetBinContent(1)
  hCut8 = fname.Get( "nPassedPrunedJetMass" ).GetBinContent(1)
  hCut9 = fname.Get( "nPassed1bTag" ).GetBinContent(1)
  print "File= %s  All                   = %i" %(fname.GetName(),hAll*lumi)
  print "File= %s  Passed trigger+filter = %i" %(fname.GetName(),hCut1*lumi)
  if returnEfficiency:
    den = Den
  if not returnEfficiency:
    den = 1./lumi
  h = TH1F( 'hpx%i'%j, 'px%i'%j, 11, 0, 11 )
  h.SetBinContent(1, hAll/den)
  h.SetBinContent(2, hCut0/den)
  h.SetBinContent(3, hCut1/den)
  h.SetBinContent(4, hCut2/den)
  h.SetBinContent(5, hCut3/den)
  h.SetBinContent(6, hCut4/den)
  h.SetBinContent(7, hCut5/den)
  h.SetBinContent(8, hCut6/den)
  h.SetBinContent(9, hCut7/den)
  h.SetBinContent(10, hCut8/den)
  h.SetBinContent(11, hCut9/den)

  h.SetLineColor(lineColor[j+1])
  h.SetLineWidth(lineWidth[j+1])
  h.SetLineStyle(lineStyle[j+1])
  # h.SetFillStyle(fillStyle[j+1])
  # h.SetFillColor(fillColor[j+1])
  legend.AddEntry(h,filename[j],legendStyle[j+1])

  h.GetXaxis().SetBinLabel(1,"All")
  h.GetXaxis().SetBinLabel(2,"Trigger")
  h.GetXaxis().SetBinLabel(3,"Filter") 
  h.GetXaxis().SetBinLabel(4,"FoundLep")
  h.GetXaxis().SetBinLabel(5,"VetoLep")
  h.GetXaxis().SetBinLabel(6,"MET")
  h.GetXaxis().SetBinLabel(7,"FoundW")
  h.GetXaxis().SetBinLabel(8,"Found jet")
  h.GetXaxis().SetBinLabel(9,"LepJet dR")
  h.GetXaxis().SetBinLabel(10,"Pruned mass")
  h.GetXaxis().SetBinLabel(11,"CSVM")
  h.GetYaxis().SetTitle('Efficiency')
  h.SetName(fname.GetName())
  histolist.append(h)  
  j += 1

canvas.cd()
for j in range(1,len(histolist)+1):  
  hs.Add( histolist[len(histolist)-j],"HIST")

histolist[0].Draw()  
histolist[0].SetMaximum(histolist[0].GetMaximum()*1.2)
for j in range(0,len(histolist)):  
  histolist[j].Draw("same")  
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