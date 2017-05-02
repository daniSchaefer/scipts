import sys
from array import *
  
from ROOT import *
import time
import math

import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
# gROOT.SetBatch(True)

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4
def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#de77ae','#a6dba0','#4393c3','#4393c3']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
 
palette = get_palette('gv')
col = TColor()
Signal="Bulk"
outdir="/shome/dschafer/AnalysisOutput/figures/testTau21Cut/"
prefix="/shome/dschafer/AnalysisOutput/80X/SignalMC/Summer16/"
rebin = 5
lumi = 1000.
bfname = '/shome/dschafer/AnalysisOutput/80X/Bkg/Summer16/QCD_pythia8_VVdijet_SR.root'
hnames = 'Tau21_punzi'
hnameb = ['Tau21_punzi1TeV','Tau21_punzi1v2TeV','Tau21_punzi1v6TeV','Tau21_punzi1v8TeV','Tau21_punzi2TeV','Tau21_punzi2v5TeV','Tau21_punzi3TeV','Tau21_punzi4TeV']
fbkg = TFile.Open(bfname,"READ")

orig_stdout = sys.stdout
f = file(outdir+Signal+'WW.txt', 'w')
sys.stdout = f

masses = [1,1.2,2,2.5,3]
fillStyle = [3018  ,3002  ,3005, 3003,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
lineColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
lineStyle = [1,1,1,1,2,2,2,2]
markerStyles = [20,22,26,31]

        
sigfiles = [
            # 'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_1000GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_1200GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_1400GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_1800GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_2000GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_2500GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_3000GeV.VV.root',
 #            'ExoDiBosonAnalysis.'+Signal+'ZZ_13TeV_4000GeV.VV.root',
            'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1000GeV.VV.root',
            'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1200GeV.VV.root',
            #'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1600GeV.VV.root',
            #'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1800GeV.VV.root',
            'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_2000GeV.VV.root',
            'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_2500GeV.VV.root',
            'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_3000GeV.VV.root',
            #'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_4000GeV.VV.root'
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_1000GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_1200GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_1600GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_1800GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_1800GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_2500GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_3000GeV.VV.root',
            # 'ExoDiBosonAnalysis.WprimeWZ_13TeV_4000GeV.VV.root',
          ]  
        
        
sigfilelist = []  
for sigf in sigfiles:
   filename = prefix+sigf
   print filename
   filetmp = TFile.Open(filename,"READ") 
   sigfilelist.append(filetmp)



histos = []
ii = 0
maxmass = array('d',[])
maxpunzi = array('d',[])
maxcuts = array('d',[])
maxes = array('d',[])
maxB = array('d',[])

cut075punzi = array('d',[])
cut075 = array('d',[])

cut06punzi = array('d',[])
cut06 = array('d',[])

cut05punzi = array('d',[])
cut05 = array('d',[])

cut055punzi = array('d',[])
cut055 = array('d',[])

cut045  = array('d',[])
cut045punzi = array('d',[])


for file in sigfilelist:
  print 'BKG hist == %s' %hnameb[ii]
  hbkg = fbkg.Get(hnameb[ii])
  hbkg.Scale(lumi)
  print "Integral after scaling = %f" %hbkg.Integral()
  print 'Signal file == %s' %file.GetName()
  m = masses[ii]
  mass = m*1000
  print 'Mass set to %i' %mass
  hsig = file.Get(hnameb[ii])
  histos.append(hsig)
  
  
  punzi = array('d',[])
  cuts = array('d',[])
  ES = array('d',[])
  B = array('d',[])
  i = 0
  denBKG = hbkg.Integral()
  print "ALL BKG = %f" %denBKG
  denSIG = hsig.Integral()
  print "ALL SIG = %f" %denSIG

  for x in range(4,20):
    cut = x/20.
    numBKG = hbkg.Integral(0,hbkg.FindBin(cut))
    eb = numBKG/denBKG   
    numSIG = hsig.Integral(0,hsig.FindBin(cut))
    es = numSIG/denSIG
    ps = es/(1+math.sqrt(numBKG))
    punzi.append(ps)
    cuts.append(cut)
    ES.append(es)
    B.append(numBKG)
    if (x==15):
      cut075punzi.append(ps)  
      cut075.append(cut)
    if (x==12):
      cut06punzi.append(ps)  
      cut06.append(cut)  
    if (x==11):
      cut055punzi.append(ps)  
      cut055.append(cut)
    if (x==10):
      cut05punzi.append(ps)  
      cut05.append(cut)    
    if (x==9):
      cut045punzi.append(ps)  
      cut045.append(cut)  
    print " Cut = %0.2f"%cut
    print "Signal numerator: %i" %numSIG
    print "Signal denominator: %i" %denSIG
    print "Signal efficiency: %0.3f" %(es)
    print "Total background: %i" %(numBKG)
    print "PUNZI: %f" %(ps)
    print "---------------------------"
  
  del hbkg
  del hsig
  tmp = punzi[0]
  index = 0
  for p in range(0,len(punzi)):
     print'%0.2f %f %f %i' %(cuts[p],punzi[p],ES[p],B[p])  
     if punzi[p] > tmp:
        index = p
        tmp = punzi[p]   

  print "Max significance"
  print'%0.2f %f %f %i' %(cuts[index],punzi[index],ES[index],B[index])  
  print "######################"
  maxpunzi.append(punzi[index])
  maxcuts.append(cuts[index])
  maxmass.append(m)
  maxes.append(ES[index])
  maxB.append(B[index])
  ii += 1
  
  del punzi[:]
  del cuts[:]
  del ES[:]
  del B[:]

l2 = TLegend(.6,.3,.73,.4)
l2.SetBorderSize(0)
l2.SetFillColor(0)
l2.SetTextFont(42)
l2.SetTextSize(0.035)


cut045punziRatio = array('d',[])
cut05punziRatio = array('d',[])
cut055punziRatio = array('d',[])
cut06punziRatio = array('d',[])
cut075punziRatio = array('d',[])
for i in range (0,len(maxpunzi)):
  cut045punziRatio.append(cut045punzi[i]/maxpunzi[i])
  cut05punziRatio.append(cut05punzi[i]/maxpunzi[i])
  cut055punziRatio.append(cut055punzi[i]/maxpunzi[i])
  cut06punziRatio.append(cut06punzi[i]/maxpunzi[i])
  cut075punziRatio.append(cut075punzi[i]/maxpunzi[i])
  
  
  


l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)

c2 = TCanvas("c2", "",800,800)
c2.cd()
c2.SetGridx()
c2.SetGridy()

g = TGraph(len(maxcuts), maxmass,maxcuts)
g.GetXaxis().SetTitle('M_{X} (TeV)')
g.GetYaxis().SetTitle("Optimal cut")
g.SetMarkerStyle(22)
g.SetMarkerSize(3)
g.SetMarkerColor(kRed-3)
g.GetYaxis().SetRangeUser(0.,1.)
if not Signal=="Wprime":l2.AddEntry(g,"G_{%s}: Optimal #tau_{21} cut"%Signal,"p")
if Signal=="Wprime":l2.AddEntry(g,"W': Optimal #tau_{21} cut","p")
# l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
# l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
# l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
# l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
# l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")

g.Draw("A*L")
l2.Draw()

l1.SetTextFont(42)
l1.SetTextSize(0.031)
l1.DrawLatex(0.6,0.81, "0.8 #times M_{X} < M_{jj} < 1.2 #times M_{X}")
l1.DrawLatex(0.6,0.77, "65 GeV < M_{p} < 105 GeV")
CMS_lumi.CMS_lumi(c2, iPeriod, iPos)
c2.Update()

# l3 = TLegend(.2,.6,.4,.8)
l3 = TLegend(.2,.7,.4,.9)
l3.SetBorderSize(0)
l3.SetFillColor(0)
l3.SetTextFont(42)
l3.SetTextSize(0.035)
c3 = TCanvas("c3", "",800,800)
c3.cd()
c3.SetGridx()
c3.SetGridy()

g2 = TGraph(len(cut05), maxmass,cut05punziRatio)
g3 = TGraph(len(cut055),maxmass,cut055punziRatio)
g4 = TGraph(len(cut06), maxmass,cut06punziRatio)
g5 = TGraph(len(cut075), maxmass,cut075punziRatio)
g6 = TGraph(len(cut045), maxmass,cut045punziRatio)
g2.GetXaxis().SetTitle('M_{X} (TeV)')
# g2.GetYaxis().SetTitle("#epsilon_{S}/(1+#sqrt{B})")
g2.GetYaxis().SetTitle("Sign / Sign_{Opt. cut}")
g2.GetYaxis().SetRangeUser(0.5,1.2)
g2.SetMarkerColor(col.GetColor(palette[0]))
g3.SetMarkerColor(col.GetColor(palette[1]))
g4.SetMarkerColor(col.GetColor(palette[2]))
g5.SetMarkerColor(col.GetColor(palette[3]))
g2.SetLineColor(col.GetColor(palette[0]))
g3.SetLineColor(col.GetColor(palette[1]))
g4.SetLineColor(col.GetColor(palette[2]))
g5.SetLineColor(col.GetColor(palette[3]))
g2.SetMarkerStyle(markerStyles[0])
g3.SetMarkerStyle(markerStyles[1])
g4.SetMarkerStyle(markerStyles[2])
g5.SetMarkerStyle(markerStyles[3])
l3.AddEntry(g6,"#tau_{21} < 0.45","p")
l3.AddEntry(g2,"#tau_{21} < 0.50","p")
l3.AddEntry(g3,"#tau_{21} < 0.55","p")
l3.AddEntry(g4,"#tau_{21} < 0.60","p")
l3.AddEntry(g5,"#tau_{21} < 0.75","p")
# l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
# l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
# l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
# l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
# l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")

g2.Draw("APL")
g3.Draw("PLsame")
g4.Draw("PLsame")
g5.Draw("PLsame")
g6.Draw("PLsame")
l3.Draw()
CMS_lumi.CMS_lumi(c3, iPeriod, iPos)
c3.Update()
time.sleep(10)





l = TLegend(.59,.62,.80,.9)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.035)


c = TCanvas("c", "",800,800)
c.cd()

hbkg = fbkg.Get(hnames)
hbkg.Scale(lumi)
hbkg.GetXaxis().SetTitle('#tau_{21}')
hbkg.GetYaxis().SetTitle("Events")
hbkg.Rebin(rebin)
hbkg.SetFillStyle(3002)
hbkg.SetFillColor(kBlack)
hbkg.SetLineColor(kBlack)
hbkg.GetXaxis().SetRangeUser(0.,1.)
hbkg.SetMaximum(1.7*hbkg.GetMaximum())
hbkg.Draw("HIST")
l.AddEntry(hbkg,"QCD","f")
k = 0
for h in histos:
  h.Rebin(rebin)
  h.GetXaxis().SetRangeUser(0.,2.5);
  h.SetLineColor(col.GetColor(palette[k %4]))
  h.SetLineStyle(lineStyle[k])
  h.SetLineWidth(2)
  sf = 1E7
  sf = hbkg.Integral()/h.Integral()
  h.Scale(sf)
  h.Draw("sameHIST")
  # l.AddEntry(h,"RS G (%i TeV)#rightarrow ZZ (norm)" %(masses[k]),"l")
  if not Signal=="Wprime":l.AddEntry(h,"G_{%s}(%.1f TeV)#rightarrow WW"%(Signal,masses[k]),"l")
  if Signal=="Wprime":l.AddEntry(h,"W'(%.1f TeV)#rightarrow WZ"%(masses[k]),"l")
# l.AddEntry(histos[1],"RS1 G #rightarrow WW (norm)","l")
# l.AddEntry(histos[2],"RS1 G #rightarrow ZZ (norm)","l")
# l.AddEntry(histos[3],"q* (%i TeV)#rightarrow qZ (norm)" %(masses[1]),"l")
# l.AddEntry(histos[9],"q*#rightarrow qW","l")
  k += 1

l.Draw()  
l1.DrawLatex(0.2,0.89, "0.85 #times M_{X} < M_{jj} < 1.15 #times M_{X}")
l1.DrawLatex(0.2,0.84, "65 GeV < M_{p} < 105 GeV")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.Update()

canvasname =outdir+Signal+"WW.pdf"
print "saving to Canvas  %s" %canvasname
c.Print(canvasname,"pdf")
c.Print(canvasname.replace("pdf","root"),"root")
canvasname =outdir+Signal+"WWPunzi.pdf"
c2.Print(canvasname,"pdf")
c2.Print(canvasname.replace("pdf","root"),"root")
canvasname =outdir+Signal+"WWSignvsM.pdf"
c3.Print(canvasname,"pdf")
c3.Print(canvasname.replace("pdf","root"),"root")
sys.stdout = orig_stdout

time.sleep(100)

del maxpunzi
del maxcuts
del histos
del hbkg
del sigfilelist
del fbkg
