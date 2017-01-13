from ROOT import*
import ROOT as rt
import time
import CMS_lumi, tdrstyle
import sys

tdrstyle.setTDRStyle()
rt.gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4


histo = "Mjj"

lineColor = [kRed+1,kRed+1,kRed+1,kRed+1,kAzure+2,kAzure+2,kAzure+2,kAzure+2,kGreen+2,kGreen+2,kGreen+2,kGreen+2,kRed+1,kAzure+2,kGreen+2,kRed+1,kAzure+2,kGreen+2,kRed+1,kAzure+2,kGreen+2,kRed+1,kAzure+2,kGreen+2,]
lineStyle = [1,1,1,1,2,2,2,2,1,1,1,1,8,8,8,8,1,1,1,1,1,1,1,1,1,1,1,8,1,1,1,1,1,1,1,1,8,1,1,1,1,1,1,1,1,8,1,1,1,1,1,1,1,1,8,1,1,1,1,1,1,1]
legends = ["G_{Bulk} #rightarrow WW (MADGRAPH)","G_{Bulk} #rightarrow ZZ(MADGRAPH)","W' #rightarrow WZ (MADGRAPH)"]

prefix = "/mnt/t3nfs01/data01/shome/dschafer/AnalysisOutput/80X/SignalMC/Summer16/"
sigdists = []

fileS = ["ExoDiBosonAnalysis.BulkWW_13TeV_"]
masses=[2000]

ii=-1
for sigfile in fileS:
  for m in masses:
    ii+=1  
    fname = prefix+sigfile+"%iGeV.VV.root"%m
    print fname
    name = "MyHist%i"%ii
    infileS = rt.TFile.Open(fname,"READ")
    hsig = TH1F(infileS.Get(histo).Clone(name))
    hsig.Rebin(2)
    hsig.Scale(1./hsig.Integral())
    hsig.SetLineColor(lineColor[ii])
    hsig.SetLineStyle(lineStyle[ii])
    hsig.SetLineWidth(2)
    print hsig.GetName()
    print hsig
    sigdists.append(hsig)
      
print len(sigdists)
c1 =rt.TCanvas("c1","",600,600)
sigdists[0].GetYaxis().SetTitleSize(0.05)
sigdists[0].GetXaxis().SetTitleSize(0.05)
sigdists[0].GetYaxis().SetTitleOffset(1.50)
sigdists[0].GetYaxis().SetLabelSize(0.04)
sigdists[0].SetMinimum(0.0)
sigdists[0].SetMaximum(0.8)
sigdists[0].GetXaxis().SetRangeUser(1000,5000)
sigdists[0].GetYaxis().SetTitle("Arbitrary scale")
sigdists[0].GetXaxis().SetTitle("Dijet invariant mass [GeV]")
sigdists[0].SetTitle("")
sigdists[0].Draw("HISTC")


legend = rt.TLegend(0.3428188,0.6678322,0.7008725,0.8951049)
legend.SetTextSize(0.038)
legend.SetLineColor(0)
legend.SetShadowColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetMargin(0.35)
#legend.AddEntry(sigdists[8],legends[2],"l")
legend.AddEntry(sigdists[0],legends[0],"l")
#legend.AddEntry(sigdists[4],legends[1],"l")


jj=-1
for h in sigdists:
  jj+=1
  h.Draw("sameHISTC")
  
  
legend.Draw("same")

addInfo = rt.TPaveText(0.6728188,0.5681818,0.9295302,0.6433566,"NDC")
# addInfo.AddText(labels[ii])
addInfo.SetFillColor(0)
addInfo.SetLineColor(0)
addInfo.SetFillStyle(0)
addInfo.SetBorderSize(0)
addInfo.SetTextFont(42)
addInfo.SetTextSize(0.040)
addInfo.SetTextAlign(12)
addInfo.Draw()
CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
c1.Update()
c1.SaveAs("DiBosonInvMass_AllSignals.pdf")
c1.SaveAs("DiBosonInvMass_AllSignals.root")
time.sleep(100)
infileS.Close()
