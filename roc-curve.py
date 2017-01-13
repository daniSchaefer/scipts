import ROOT
import sys
import time
import math
import CMS_lumi, tdrstyle
from array import *

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()




bkgname = ['ExoDiBosonAnalysis.QCD170to300.root','ExoDiBosonAnalysis.QCD300to470.root','ExoDiBosonAnalysis.QCD470to600.root',
           'ExoDiBosonAnalysis.QCD600to800.root','ExoDiBosonAnalysis.QCD1000to1400.root','ExoDiBosonAnalysis.QCD1000to1400.root',
           'ExoDiBosonAnalysis.QCD1000to1400.root','ExoDiBosonAnalysis.QCD1000to1400.root','ExoDiBosonAnalysis.QCD1000to1400.root',]   
fbkg = ROOT.TFile.Open('ExoDiBosonAnalysis.QCD.root')
fsig = ROOT.TFile.Open('../ExoDiBosonAnalysis/ExoDiBosonAnalysis.BulkWW.M-1000.root')

bkg = ROOT.TTree()
fbkg.GetObject('tree',bkg)
sig = ROOT.TTree()
fsig.GetObject('tree',sig)

ngenbkg = bkg.GetEntries()
ngensig = sig.GetEntries()
print "tree signal entries: %i" %ngensig
print "tree bkg entries: %i" %ngenbkg

canv = TCanvas("c", "",800,800)
canv.cd()
canv.SetGridx()
canv.SetGridy()

num = ROOT.TH1F('roc','roc curve',100,0.,1.)
den = ROOT.TH1F('den','den',100,0.,1.)

l = ROOT.TLegend(0.17,0.80,0.38,0.86,"","NDC")
l.SetLineWidth(2)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetTextFont(42)
l.SetTextSize(0.04)
l.SetTextAlign(12)

l2 = ROOT.TLegend(0.1821608,0.6923077,0.3919598,0.7517483,"","NDC")
l2.SetLineWidth(2)
l2.SetBorderSize(0)
l2.SetFillColor(0)
l2.SetTextFont(42)
l2.SetTextSize(0.04)
l2.SetTextAlign(12)  
htopmin = [x*10 for x in range(4,9)]
htopmax = [x*10 for x in range(9,15)]

  
if bkgname.find("_170to300_") != -1:
  xSec_ = 117276.
  genEvents_ = 3364368.   
   
if bkgname.find("_300to470_") != -1:
  xSec_ = 7823.
  genEvents_ = 2933611.   
   
if bkgname.find("_470to600_") != -1:
  xSec_ = 648.2
  genEvents_ = 1936832.   
   
if bkgname.find("_600to800_") != -1:
  xSec_ = 186.9
  genEvents_ = 1878856.   
   
if bkgname.find("_800to1000_") != -1:
  xSec_ = 32.293
  genEvents_ = 1937216.   
   
if bkgname.find("_1000to1400_") != -1:
  xSec_ = 9.4183
  genEvents_ = 1487136.   
     
if bkgname.find("_1400to1800_") != -1:
  xSec_ = 0.84265
  genEvents_ = 197959.   
   
if bkgname.find("_1800to2400_") != -1:
  xSec_ = 0.114943
  genEvents_ = 193608.   
   
if bkgname.find("_2400to3200_") != -1:
  xSec_ = 0.00682981
  genEvents_ = 194456.   
   
if bkgname.find("_3200toInf_") != -1:
  xSec_ = 0.000165445
  genEvents_ = 192944.   
   
lweight = xSec_/genEvents_   
lumi = 10000.

print "top mass steps:"
print htopmin
print htopmax

mass = 1000.
wwmin = mass-15*mass/100. 
wwmax = mass+15*mass/100.

print "WW mass limits:"
print wwmin,wwmax

hnums = fsig.Get("nPassedMjj")
hdens = fsig.Get("nEvents")
hnumbkg = fbkg.Get("nPassedMjj")
hdenbkg = fbkg.Get("nEvents")

es_start = hnums.GetBinContent(1)/hdens.GetBinContent(1)
eb_start = hnumbkg.GetBinContent(1)/hdenbkg.GetBinContent(1)

print "Starting signal efficiency: %f" %(es_start)
print "Starting bkg efficiency: %f" %(eb_start)

cut = 'MVV > %f && MVV < %f' %(wwmin,wwmax)
nbkg = float(bkg.GetEntries(cut))
nsig = float(sig.GetEntries(cut))
B = nbkg*lweight*lumi
es = nsig/ngensig
eb = nbkg/ngenbkg
a = math.sqrt(nsig)/nsig
b = math.sqrt(ngensig)/ngensig

print "Default punzi: %f" %(es_start/(1+math.sqrt(B)))
print "B = %f" %B
print "es = %f" %es

punzi = []
cuts = []
signaleffs = []
bkgeffs = []
errsignaleffs = []
bkgyields = []

for hmin in htopmin:
 for hmax in htopmax:
  if hmax > hmin:
  
     cut = '((jet_mass_softdrop > %f && jet_mass_softdrop < %f))' %(hmin,hmax)
     cuts.append(cut)
     #cut+= ' && (MWH > %f && MWH < %f)' %(wwmin,wwmax)
     
     #nbkg1 = float(bkg.GetEntries(cut))
     #nsig1 = float(sig.GetEntries(cut))
     
     cut2 = '!((jet_mass_softdrop > %f && jet_mass_softdrop < %f) )' %(hmin,hmax)
     #cut2+= ' && (MWH > %f && MWH < %f)' %(wwmin,wwmax)
     nbkg = float(bkg.GetEntries(cut2))
     nsig = float(sig.GetEntries(cut2))
     lweight= bkg.GetWeight()
     
     B = nbkg*lweight*lumi
     es = nsig/ngensig
     eb = nbkg/ngenbkg
     a = math.sqrt(nsig)/nsig
     b = math.sqrt(ngensig)/ngensig
     err = es*math.sqrt( a*a + b*b )
     
     punzi.append(es/(1+math.sqrt(B)))       
     signaleffs.append(es)
     errsignaleffs.append(err)
     bkgeffs.append(eb)
     bkgyields.append(B)
     
     #if lmin==80 and lmax==200 and hmin==100 and hmax==220:
     #print cut
     #print "   * sigeff %.6f - bkg eff %.6f - bkg yields %.6f - punzi %.6f" %(es,eb,B,es/(1+math.sqrt(B)))
     num.Fill(es,es/(1+math.sqrt(B)))
     den.Fill(es)
    
tmp = punzi[0]
index = 0
for p in range(0,len(punzi)):
   if punzi[p] > tmp:
      index = p
      tmp = punzi[p]

print "Max significance"
print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
a =  errsignaleffs[index]/signaleffs[index]
b = 1./(1+math.sqrt(bkgyields[index]))
err = punzi[index]*math.sqrt(a*a+b*b)
print " ---> error +/- %f" %(err)

tmp = punzi[0]
index = 0
for p in range(0,len(punzi)):
   if punzi[p] < tmp:
      index = p
      tmp = punzi[p]

print "Min significance"
print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
a =  errsignaleffs[index]/signaleffs[index]
b = 1./(1+math.sqrt(bkgyields[index]))
err = punzi[index]*math.sqrt(a*a+b*b)
print " ---> error +/- %f" %(err)

tmp = signaleffs[0]
index = 0
for p in range(0,len(signaleffs)):
   if signaleffs[p] > tmp:
      index = p
      tmp = signaleffs[p]

print "Max signal efficiency"
print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
 
tmp = bkgeffs[0]
index = 0
for p in range(0,len(bkgeffs)):
   if bkgeffs[p] < tmp:
      index = p
      tmp = bkgeffs[p]

print "Max bkg rejection"
print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
 
print "********************************"
#for p in range(0,len(punzi)):
#   if punzi[p] > 0.355 and punzi[p]<0.356: print cuts[p],punzi[p],bkgeffs[p],signaleffs[p]
            
#for e in range(0,len(signaleffs)):
#   if signaleffs[e] > 0.94: #and signaleffs[e] < 0.74:
#      print punzi[e],cuts[e],bkgeffs[e],signaleffs[e]  
                
num.Divide(den)
l.AddEntry(num,"M_{G} = 1 TeV","P")
num.SetMarkerStyle(20)
num.SetMarkerColor(ROOT.kPink-1)
num.Draw("P")
num.GetXaxis().SetTitle("Signal efficiency")
num.GetXaxis().SetLabelSize(0.04)
num.GetYaxis().SetTitle("Punzi significance")
num.GetYaxis().SetTitleOffset(1.)
num.GetYaxis().SetLabelSize(0.04)
l.Draw()

x = array('d',[])
y = array('d',[])

bin = num.GetXaxis().FindBin(0.86176)

x.append(num.GetBinCenter(bin))
y.append(num.GetBinContent(bin))
gr = ROOT.TGraph(1,x,y)
gr.SetMarkerStyle(29)
gr.SetMarkerSize(2.4)
l2.AddEntry(gr,'','P')
gr.Draw("P")
l2.Draw()

pt = ROOT.TPaveText(0.2324121,0.6328671,0.4422111,0.7395105,"NDC")
pt.SetTextFont(42)
pt.SetTextSize(0.03)
pt.SetTextAlign(12)
pt.SetFillColor(0)
pt.SetBorderSize(0)
pt.SetFillStyle(0)  

text = pt.AddText('Optimal cut:')
text.SetTextFont(62)
pt.AddText('')
pt.AddText('m_{SD} #in [50,120]')
pt.Draw()

canv.Update()

time.sleep(1000)	 

fbkg.Close()
fbkg.Delete()
fsig.Close()
fsig.Delete()
