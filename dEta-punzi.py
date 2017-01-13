import sys
from array import *
  
from ROOT import *
import time
import math

# orig_stdout = sys.stdout
# f = file('dEta_optimisation.txt', 'w')
# sys.stdout = f

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetOptTitle(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

rebin = 2
lumi = 1000
bfname = 'ExoDiBosonAnalysis.qcd_puppi_NEW.root'
hname = 'DeltaEta'
hnameb = ['DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV',
          'DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV','DeltaEta_1TeV','DeltaEta_2TeV','DeltaEta_3TeV','DeltaEta_4TeV',]
# hnameb = ['DeltaEta_2TeV','DeltaEta_2TeV','DeltaEta_2TeV','DeltaEta_2TeV','DeltaEta_2TeV']
fbkg = TFile.Open(bfname)


l = TLegend(.46,.7,.76,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.035)

masses = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
fillStyle = [3018  ,3002  ,3005, 3003,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
fillColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
lineWidth = [2     ,2     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2,2]
lineStyle = [2,1,4,3,2,1,4,3,2,1,4,3,2,1,4,3,2,1,4,3,2,1,4,3,]
lineColor = [kBlack,kBlack,kBlack,kBlack,kBlue,kBlue,kBlue,kBlue,kMagenta,kMagenta,kMagenta,kMagenta,kGreen,kGreen,kGreen,kGreen,]
legendStyle = ['F','F','F','F','F','F','F','F','F','F']   

        
sigfiles = [
            # 'RSWWZZ_1TeV.root',
            # 'RSWWZZ_2TeV.root',
            # 'RSWWZZ_3TeV.root',
            # 'RSWWZZ_4TeV.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.RSGravToWW.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.RSGravToWW.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.RSGravToWW.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.RSGravToWW.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-1000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-2000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-3000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-4000.root',
            'ExoDiBosonAnalysis.QstarToQW.M-1000.root',
            'ExoDiBosonAnalysis.QstarToQW.M-2000.root',
            'ExoDiBosonAnalysis.QstarToQW.M-3000.root',
            'ExoDiBosonAnalysis.QstarToQW.M-4000.root'
          ]  
        
        
sigfilelist = []  
for sigf in sigfiles:
   filename = sigf
   filetmp = TFile.Open(filename,"READ") 
   sigfilelist.append(filetmp)


maxpunzi = array('d',[])
maxcuts = array('d',[])

maxmass = array('d',[])
histos = []
  

for file in sigfilelist:
  print 'Signal file == %s' %file.GetName()
  hsig = file.Get(hname)
  histos.append(hsig)
  
ii = 0  
for hsig in histos:  
  print 'BKG hist == %s' %hnameb[ii]
  hbkg = fbkg.Get(hnameb[ii])
  hbkg.Scale(lumi)
  m = masses[ii]
  mass = m*1000
  print 'Mass set to %i' %mass
  ii += 1
  punzi = array('d',[])
  cuts = array('d',[])
  maxes = array('d',[])
  maxB = array('d',[])
  i = 0
  for x in range(0,20):
    cut = x/10.
    numBKG = hbkg.Integral(0,hbkg.FindBin(cut))
    denBKG = hbkg.Integral()
    eb = numBKG/denBKG
    
    numSIG = hsig.Integral(0,hsig.FindBin(cut))
    denSIG = hsig.Integral()
    es = numSIG/denSIG

    a = math.sqrt(numSIG)/numSIG
    b = math.sqrt(denSIG)/denSIG
    err = es*math.sqrt( a*a + b*b )
    
    # punzi.append( (nsig*nsig)/(eb*B) )
    ps = es/(1+math.sqrt(numBKG))
    punzi.append(ps)
    cuts.append(cut)
    maxes.append(es)
    maxB.append(numBKG)
    

    # print "N sig ALL: %f" %denSIG
    # print "N sig: %f" %numSIG
    # print "Signal efficiency: %f" %(es)
    # print "Total background: %f" %(nbkg)
    # print "PUNZI: %f" %(ps)

  tmp = punzi[0]
  index = 0
  for p in range(0,len(punzi)):
     print'%0.1f %f %f %i' %(cuts[p],punzi[p],maxes[p],maxB[p])  
     if punzi[p] > tmp:
        index = p
        tmp = punzi[p]

  print "Max significance"
  print'%0.1f %f %f %i' %(cuts[index],punzi[index],maxes[index],maxB[index])  
  print "######################"
  maxpunzi.append(punzi[index])
  maxcuts.append(cuts[index])
  maxmass.append(mass/1000)
  del punzi
  del cuts
  del maxes
  del maxB

l2 = TLegend(.66,.4,.73,.5)
l2.SetBorderSize(0)
l2.SetFillColor(0)
l2.SetTextFont(42)
l2.SetTextSize(0.035)



l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)



c2 = TCanvas("c2", "",800,800)
c2.cd()
c2.SetGridx()
c2.SetGridy()
g = TGraph(len(maxcuts), maxmass,maxcuts)
g.GetXaxis().SetTitle('M_{X} [TeV]')
g.GetYaxis().SetTitle("Optimal cut")
g.SetMarkerStyle(22)
g.SetMarkerSize(3)
g.SetMarkerColor(kRed-3)
l2.AddEntry(g,"Optimal #Delta#eta_{jj} cut","p")
# l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
# l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
# l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
# l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
# l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")

g.Draw("A*")
l2.Draw()
l1.DrawLatex(0.72,0.96, "Simulation")
l1.SetTextFont(42)
l1.SetTextSize(0.031)
l1.DrawLatex(0.6,0.81, "0.85 #times M_{X} < M_{jj} < 1.15 #times M_{X}")


c = TCanvas("c", "",800,800)
c.cd()
hbkg = fbkg.Get(hname)
hbkg.Scale(lumi)
hbkg.GetXaxis().SetTitle('#Delta#eta_{jj}')
hbkg.GetYaxis().SetTitle("Events")
hbkg.SetTitleOffset(1.2,"X")
hbkg.SetTitleOffset(1.5,"Y")
hbkg.Rebin(rebin)
hbkg.SetFillColor(kRed)
hbkg.SetLineColor(kRed)
hbkg.GetXaxis().SetRangeUser(0.,2.5)
hbkg.SetMaximum(1.5*hbkg.GetMaximum())
hbkg.Draw("HIST")
l.AddEntry(hbkg,"QCD","f")
k = 0
for h in histos:
  h.Rebin(rebin)
  h.GetXaxis().SetRangeUser(0.,2.5);
  h.SetLineColor(lineColor[k])
  h.SetLineWidth(lineWidth[k])
  h.SetLineStyle(lineStyle[k])
  sf = 1E7
  sf = hbkg.Integral()/h.Integral()
  h.Scale(sf)
  h.Draw("sameHIST")
  l.AddEntry(h,"q* (%i TeV)#rightarrow qW (norm)" %(masses[k]),"l")
  k += 1
# l.AddEntry(histos[1],"Bulk G#rightarrow WW","l")
# l.AddEntry(histos[5],"RS1 G#rightarrow WW","l")
# # l.AddEntry(histos[2],"RS1 G (%i TeV)#rightarrow ZZ (norm)" %(masses[1]),"l")
# # l.AddEntry(histos[3],"q* (%i TeV)#rightarrow qZ (norm)" %(masses[1]),"l")
# l.AddEntry(histos[9],"q*#rightarrow qW","l")

l.Draw()  
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextSize(0.045)
l1.SetTextFont(62)
l1.DrawLatex(0.85,0.96, "1 fb^{-1}")
del maxpunzi
del maxcuts
# del histos
# del hbkg
# del sigfilelist
# del fbkg

# sys.stdout = orig_stdout

time.sleep(100)