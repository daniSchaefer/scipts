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

rebin = 1

bin1 = 110
bin2 = 250
bin3 = 400

name1 = 'newBTAGCALIB/wSF/LeptonicTopMass_B.root'
name2 = 'newBTAGCALIB/wSF/LeptonicTopMass_nonB.root'
# name2 = 'bTagCalib/MljbDepleted.root'
# name1 = 'bTagCalib/MljbEnriched.root'

fname1 = TFile.Open(name1,"READ")
fname2 = TFile.Open(name2,"READ")
#----------------as a function on M(jj)--------------------------#
hB  = fname1.Get( 'hsum' )
hnonB = fname2.Get( "hsum" )

nonBden =  hnonB.Integral()
nonBenr = hnonB.Integral(hnonB.FindBin(bin1),hnonB.FindBin(bin2))
nonBdep = hnonB.Integral(hnonB.FindBin(bin2),hnonB.FindBin(bin3))
F = nonBenr/nonBdep
dF=F*TMath.Sqrt( (1/nonBenr) + (1/nonBdep) )

print "integrating"
Bden =  hB.Integral()
Benr = hB.Integral(hB.FindBin(bin1),hB.FindBin(bin2))
Bdep = hB.Integral(hB.FindBin(bin2),hB.FindBin(bin3))

bPurityEnr = Benr/(Benr+nonBenr)
bPurityDep = Bdep/(Bdep+nonBdep)

print"For scalefactor F: Nr non b in enriched = %f       Nr non b in depleted = %f         F = %f #pm %f" %(nonBenr , nonBdep, F,dF)
print "b-jet purity in          enriched = %f      depleted = %f" %(bPurityEnr,bPurityDep)
print "non b-jet purity in      enriched = %f      depleted = %f" %(1-bPurityEnr,1-bPurityDep)
hB.Rebin(rebin)
hnonB.Rebin(rebin)
# time.sleep(100)

hPur = TH1F( 'hPur', 'hPur', hB.GetNbinsX(), hB.GetXaxis().GetXmin(), hB.GetXaxis().GetXmax() )


for i in range(0,hB.GetNbinsX()):
  if( (hB.GetBinContent(i)+hnonB.GetBinContent(i) )==0 ):
    continue
  hnum = hB.GetBinContent(i)
  hden = hB.GetBinContent(i)+hnonB.GetBinContent(i)
  hPur.SetBinContent(i, hnum/hden)

hPur.SetMarkerColor(kBlack)
hPur.SetMarkerStyle(20)
hPur.SetMarkerSize(1.)

hPur.GetYaxis().SetRangeUser(0.,1.)
hPur.GetXaxis().SetRangeUser(0.,500.)
hPur.GetXaxis().SetTitle('M_{#mu#nub} [GeV]')
hPur.GetYaxis().SetTitle('Purity')


legend = TLegend(.66,.74,.86,.83)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.03)
legend.AddEntry(hPur,"b-jet purity","P")

canv = TCanvas("Cut flow", "",800,800)
canv.SetGridx()
canv.SetGridy()
canv.cd()
# canv.SetLogy()
canv.cd()
hPur.Draw("P")
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