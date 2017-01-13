from ROOT import *
import time
import math
from array import array
from ROOT import SetOwnership

gStyle.SetGridColor(kGray)
gStyle.SetOptTitle(kFALSE)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

histoname ='recoWSoftdropMass'
rebin = 1
lumi = 3000.
prefix = 'VV/HP/SD/'

files = ['ExoDiBosonAnalysis.BulkWW.M-1000.root','ExoDiBosonAnalysis.BulkWW.M-1200.root','ExoDiBosonAnalysis.BulkWW.M-1400.root','ExoDiBosonAnalysis.BulkWW.M-2000.root','ExoDiBosonAnalysis.BulkWW.M-3000.root','ExoDiBosonAnalysis.BulkWW.M-4000.root']
files = ['ExoDiBosonAnalysis.BulkWW.M-1000.root','ExoDiBosonAnalysis.BulkWW.M-2000.root','ExoDiBosonAnalysis.BulkWW.M-3000.root','ExoDiBosonAnalysis.BulkWW.M-4000.root']
mass = [1.0,1.2,1.4,2.0,3.0,4.0]
mass=[1,2,3,4]
filelist = []
for f in files:
   tmpname= prefix + f
   filetmp = TFile.Open(tmpname,"READ") 
   filelist.append(filetmp)
   
fnameQCD = prefix + 'ExoDiBosonAnalysis.QCD.root'
filetmp = TFile.Open(fnameQCD,"READ") 
hbkg =  filetmp.Get('SoftdropMass_all')
hbkg.Scale(lumi)    
bAll = hbkg.Integral(1,hbkg.GetNbinsX(),"width")

histos = []
for j in range(0,len(filelist)):
  hname = "histos_%d" % (j) # Each histogram must have a unique name
  htitle = ""
  histos.append( TH1F(hname, htitle, 800, 50., 250.) )  
  
hsiglist = []
for f in filelist:
   hsiglist.append(f.Get(histoname))


# lineColor = [kBlack, kRed, kGreen+2,kBlue, ]

lineColor = [ kGreen+2, kRed, kBlack, kBlue, kMagenta, kBlack, kBlack, kAzure, kOrange]

l = TLegend(.16,.75,.36,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.021)

     
i = -1    
for hsig in hsiglist:
  i += 1
  hsig.Scale(lumi)
  histos[i] =  TH1F("histo_%d" % (i),"histo_%d" % (i) ,hsig.GetNbinsX(),hsig.GetXaxis().GetXmin(),hsig.GetXaxis().GetXmax() )
  histos[i].SetLineColor(lineColor[i])
  histos[i].SetLineStyle(2)
  histos[i].SetLineWidth(2)  
  histos[i].GetXaxis().SetTitle( '|#Delta#eta_{jj}|' )
  histos[i].GetYaxis().SetTitleOffset( 2.2 )
  histos[i].GetYaxis().SetTitle( '#frac{#epsilon_{S}}{1+#sqrt{B}}' )
  
  sAll = hsig.Integral(1,hsig.GetNbinsX(),"width")
  sEff, bEff = array( 'f' ), array( 'f' )
  
  cutL=[10,20,30,40,50,60,70,80,90,100,110]
  cutL=[50]
  # cutH=[110,100,90,80,70,60]
 
  #for b in range(1,hsig.GetNbinsX()):
  for l in range(0,len(cutL)):
    for h in range(0,len(cutH)):
      intS = hsig.Integral(hsig.FindBin(cutL[l]),i),"width")
      sEff.append(intS/sAll)
      intB = hbkg.Integral(hbkg.FindBin(cutL[l]),i),"width")
       # bEff.append(1-(intB/bAll))
      punzi = sEff[h]/(1.0+math.sqrt(intB))
       # punzi = sEff[b-1]/(1+math.sqrt(bAll))
      histos[i].SetBinContent(i, punzi) 
     
  # print "sEff size = %.2f" %len(sEff)
  # roc =  TGraph(hsig.GetNbinsX()-1, sEff, bEff)
  # roc.SetLineColor( 2 )
  # roc.SetLineWidth( 2 )
  # roc.SetMarkerColor( 2 )
  # roc.SetMarkerStyle( 21 )
  # roc.SetTitle( 'M_{G_{RS}} = 2000 GeV' )
  # roc.GetXaxis().SetTitle( 'Signal efficiency' )
  # roc.GetYaxis().SetTitle( '1 - bkg. efficiency' )

# c = TCanvas("c", "",800,800)
# c.cd()
# roc.Draw()

canv = TCanvas("canv", "",800,800)
canv.cd()
max = []

histos[0].Draw("")
histos[0].SetMaximum(histos[0].GetMaximum()*1.5)
for h in histos:
  max.append(h.GetXaxis().GetBinCenter(h.GetMaximumBin()) )
  h.Draw("same")

l = TLegend(.62,.73,.76,.560)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.025)
for j in range(0,len(histos)):
  l.AddEntry(histos[j], "G_{Bulk} (%.1f TeV), cut = %.2f" %(mass[j],max[j]), "lep" )
l.Draw()

t =  TLatex()
t.SetTextAlign(13)
t.SetTextFont(42)
t.SetNDC()
t.SetTextSize(0.04)

t.SetTextAlign(12)
t.SetTextSize(0.045)
t.SetTextFont(62)
t.DrawLatex(0.62,0.96, "3 fb^{-1}(#sqrt{s} = 13 TeV)")

t.SetTextFont(42)
t.SetTextSize(0.025)
t.DrawLatex(0.625,0.90, "M_{jj} > 1040 GeV")
t.DrawLatex(0.625,0.86, "p_{T} > 200 GeV, |#eta| < 2.4")


time.sleep(100)