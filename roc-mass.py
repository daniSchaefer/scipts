import ROOT
import sys
import time
import math

   
fbkg1 = ROOT.TFile.Open('VV/HP/SD/ExoDiBosonAnalysis.QCD.root')
fsig = ROOT.TFile.Open('VV/HP/SD/ExoDiBosonAnalysis.BulkWW.M-1000.root')

bkg1 = ROOT.TTree()
fbkg1.GetObject('tree',bkg1)

sig = ROOT.TTree()
fsig.GetObject('tree',sig)

ngenbkg1 = bkg1.GetEntries()

ngensig = sig.GetEntries()
print "tree signal entries: %i" %ngensig
print "1 - tree qcd entries: %i" %ngenbkg1


canv = get_canvas()
canv.cd()

#num = ROOT.TH1F('roc','roc curve',100,0.,1.)
#den = ROOT.TH1F('den','den',100,0.,1.)

#l = ROOT.TLegend(0.17,0.80,0.38,0.86,"","NDC")
#l.SetLineWidth(2)
#l.SetBorderSize(0)
#l.SetFillColor(0)
#l.SetTextFont(42)
#l.SetTextSize(0.04)
#l.SetTextAlign(12)
   

masscut = [30.,40.,50.,60.,70.,80.,90.,100.,110,120,130,140,10,160,170]

lumi = 10./3.

print "mass steps:"
print masscut

mass = 1000.
wwmin = mass-15*mass/100. 
wwmax = mass+15*mass/100.

print "WW mass limits:"
print wwmin,wwmax

hnums = fsig.Get("nPassedExoCandidateMass")
hdens = fsig.Get("nEvents")

es_start = hnums.GetBinContent(1)/hdens.GetBinContent(1)
print "Starting signal efficiency: %f" %(es_start)

hnumbkg = fbkg1.Get("nPassedExoCandidateMass")
hdenbkg = fbkg1.Get("nEvents")
eb_start = hnumbkg.GetBinContent(1)/hdenbkg.GetBinContent(1)
print "Starting qcd bkg efficiency: %f" %(eb_start)


cut = 'MWH > %f && MWH < %f' %(wwmin,wwmax)
nsig = float(sig.GetEntries(cut))
es = nsig/ngensig

histo = ROOT.TH1F("h","h", 80,  0. ,  200.)
cut = 'lumiweight*%f*(MWH > %f && MWH < %f)' %(lumi,wwmin,wwmax)
B = 0

bkg1.Draw("Mj>>h",cut)
B+=histo.Integral()
print "Starting qcd yield: %f" %(histo.Integral())


print "Default punzi: %f" %(es_start/(1+math.sqrt(B)))
print "B = %f" %B
print "es = %f" %es

punzi = []
cuts = []
signaleffs = []
bkgyields = []

for t in masscut:

 cut = 'mass < %f' %(t)
 cuts.append(cut)
 
 cut2 = 'mass > %f' %(t)
 nsig = float(sig.GetEntries(cut2))
 es = nsig/ngensig
 
 cut3 = 'lumiweight*%f*(mass > %f)' %(lumi,t)
 B = 0
 bkg1.Draw("Mj>>h",cut)
 B+=histo.Integral()

 
 punzi.append(es/(1+math.sqrt(B)))	 
 signaleffs.append(es)
 bkgyields.append(B)
 
 print cut
 print "   * sigeff %.6f - bkg yields %.6f - punzi %.6f" %(es,B,es/(1+math.sqrt(B)))
 #num.Fill(es,es/(1+math.sqrt(B)))
 #den.Fill(es)
      
