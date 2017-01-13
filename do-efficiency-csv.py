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

rebin = 10

bin1 = 110
bin2 = 250
bin3 = 400

name0 = 'Method2_CSV_depleted.root'
name1 = 'Method2_CSV_enriched.root'
name2 = 'LeptonicbCSV.root'
# name2 = 'bTagCalib/MljbDepleted.root'
# name1 = 'bTagCalib/MljbEnriched.root'

fname0 = TFile.Open(name0,"READ")
fname1 = TFile.Open(name1,"READ")
fname2 = TFile.Open(name2,"READ")
fTruth= TFile.Open('CSV_enriched_trueB.root',"READ")

hDepleted  = fname0.Get( 'hsum' )
hEnriched  = fname1.Get( 'hsum' )
hAll = fname2.Get( "hsum" )
hTruth= fTruth.Get( "hsum" )


canv = TCanvas("Cut flow", "",800,800)
canv.SetGridx()
canv.SetGridy()
canv.cd()
# canv.SetLogy()
canv.cd()

hDepleted.Scale(1.19)
hNew = hEnriched
hNew.Add(hDepleted,-1)
# hNew.Rebin(5)
hNew.Scale(1./hNew.Integral())


hNew.SetMarkerColor(kRed+2)
hNew.SetMarkerStyle(20)
hNew.SetMarkerSize(1.)
hNew.GetYaxis().SetRangeUser(-0.1,.8)
hNew.GetXaxis().SetRangeUser(0.,1.)
hNew.GetXaxis().SetTitle('CSV')
hNew.GetYaxis().SetTitle('Efficiency')




# hTruth.Rebin(5)
hTruth.Scale(1./hTruth.Integral())

legend = TLegend(.16,.74,.36,.83)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.03)
legend.AddEntry(hTruth,"MC truth","l")
legend.AddEntry(hNew,"Estimated #hat#Delta_{b}^{enr}","P")

hNew.Draw("P")
hTruth.Draw("HISTsame")
legend.Draw()

l1 = TLatex()
l1.SetTextAlign(13)
l1.SetTextFont(42)
l1.SetNDC()
l1.SetTextSize(0.04)
# l1.DrawLatex(0.14+0.03,0.25, 'POWHEG t#bar{t}')

l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextAlign(12)
l1.SetTextSize(0.035)
l1.SetTextFont(61)
l1.DrawLatex(0.13,0.96, "CMS")
l1.SetTextSize(0.03)
l1.SetTextFont(52)
l1.DrawLatex(0.21,0.96, "Simulation")


hAll = hTruth
hEnriched=hNew

denom_S  = float( hAll.Integral())

print hAll.Integral()
hPur = TH1F( 'hPur', 'hPur', hAll.GetNbinsX(), hAll.GetXaxis().GetXmin(), hAll.GetXaxis().GetXmax() )


print hAll.GetNbinsX()
for i in range(0,hAll.GetNbinsX()):
  num_S = float( hAll.Integral(100-i,100) )
  hPur.SetBinContent(i, num_S/denom_S)

hPur.SetMarkerColor(kBlack)
hPur.SetMarkerStyle(20)
hPur.SetMarkerSize(1.)
hPur.GetYaxis().SetRangeUser(0.,1.2)
hPur.GetXaxis().SetRangeUser(0.,500.)
hPur.GetXaxis().SetTitle('CSV')
hPur.GetYaxis().SetTitle('Efficiency')



denom_S2  = float( hEnriched.Integral())
hEnr = TH1F( 'hEnr', 'hEnr', hEnriched.GetNbinsX(), hEnriched.GetXaxis().GetXmin(), hEnriched.GetXaxis().GetXmax() )
print hEnriched.GetNbinsX()
for i in range(0,hEnriched.GetNbinsX()):
  num_S2 = float( hEnriched.Integral(100-i,100) )
  hEnr.SetBinContent(i, num_S2/denom_S2)
  
hEnr.SetLineColor(kRed+1)

legend = TLegend(.16,.74,.36,.83)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.03)
# legend.AddEntry(hPur,"b-candidate sample","P")
# legend.AddEntry(hEnr,"b-enriched sample","l")
legend.AddEntry(hPur,"MC truth","P")
legend.AddEntry(hEnr,"Estimated #hat#Delta_{b}^{enr}","l")


hPur.Draw("P")
hEnr.Draw("Histsame")
legend.Draw()

l1 = TLatex()
l1.SetTextAlign(13)
l1.SetTextFont(42)
l1.SetNDC()
l1.SetTextSize(0.04)
# l1.DrawLatex(0.14+0.03,0.25, 'POWHEG t#bar{t}')

l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.72,0.96, "#sqrt{s} = 13 TeV")

l1.SetTextAlign(12)
l1.SetTextSize(0.035)
l1.SetTextFont(61)
l1.DrawLatex(0.13,0.96, "CMS")
l1.SetTextSize(0.03)
l1.SetTextFont(52)
l1.DrawLatex(0.21,0.96, "Simulation")




canv.Update()
time.sleep(100)