import sys
from array import *
  
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

lower = 0.60
Signals=["Bulk","RS1","Wprime"]
prefix="/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned/VV/HP/"
rebin = 5
lumi = 1000.


orig_stdout = sys.stdout
f = file("PunziOpt/LP0v5WW.txt", 'w')
sys.stdout = f
for Signal in Signals:
  bfname = '/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned/VV/HP/ExoDiBosonAnalysis.QCD.root'
  hnames = 'Tau21_punzi'
  hnameb = ['Tau21_punzi1TeV','Tau21_punzi1v2TeV','Tau21_punzi1v6TeV','Tau21_punzi1v8TeV','Tau21_punzi2TeV','Tau21_punzi2v5TeV','Tau21_punzi3TeV','Tau21_punzi4TeV']
  fbkg = TFile.Open(bfname,"READ")
  
  masses = [1,1.2,1.6,1.8,2,2.5,3,4]
  fillStyle = [3018  ,3002  ,3005, 3003,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
  fillColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
  lineStyle = [1,1,1,1,2,2,2,2]
  lineColor = [kBlack,kBlue,kMagenta,kRed,kBlack,kBlue,kMagenta,kRed]  

  if not Signal=="Wprime":
    sigfiles =['ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1000GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1200GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1600GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_1800GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_2000GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_2500GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_3000GeV.Signal.root',
              'ExoDiBosonAnalysis.'+Signal+'WW_13TeV_4000GeV.Signal.root'
            ]  
          
  if Signal=="Wprime": 
    sigfiles =['ExoDiBosonAnalysis.WprimeToWZ_1000GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_1200GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_1600GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_1800GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_2000GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_2500GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_3000GeV.Signal.root',
              'ExoDiBosonAnalysis.WprimeToWZ_4000GeV.Signal.root'
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

  cut060punzi = array('d',[])
  cut060 = array('d',[])

  cut065punzi = array('d',[])
  cut065 = array('d',[])

  cut070punzi = array('d',[])
  cut070 = array('d',[])

  cut075punzi = array('d',[])
  cut075 = array('d',[])

  cut080punzi = array('d',[])
  cut080 = array('d',[])

  for file in sigfilelist:
    print 'BKG hist == %s' %hnameb[ii]
    hbkg = fbkg.Get(hnameb[ii])
    hbkg.Scale(lumi)
    print 'Signal file == %s' %file.GetName()
    m = masses[ii]
    mass = m*1000
    hsig = file.Get(hnameb[ii])
    print 'SIG hist == %s' %hnameb[ii]
    histos.append(hsig)
    print 'Mass set to %i GeV' %mass
  
    punzi = array('d',[])
    cuts = array('d',[])
    ES = array('d',[])
    B = array('d',[])
    i = 0
    denBKG = hbkg.Integral()
    denSIG = hsig.Integral()
  
    for x in range(8,21):
      cut = x/20.
      if cut<lower: continue
      numBKG = hbkg.Integral(hbkg.FindBin(lower)+1,hbkg.FindBin(cut))
      eb = numBKG/denBKG   
      numSIG = hsig.Integral(hsig.FindBin(lower)+1,hsig.FindBin(cut))
      es = numSIG/denSIG
      ps = es/(1+math.sqrt(numBKG))
      punzi.append(ps)
      cuts.append(cut)
      ES.append(es)
      B.append(numBKG)
      if (cut==0.60):
        cut060punzi.append(ps)
        cut060.append(cut)
      if (cut==0.65):
        cut065punzi.append(ps)
        cut065.append(cut)
      if (cut==0.70):
        cut070punzi.append(ps)
        cut070.append(cut)
      if (cut==0.75):
        cut075punzi.append(ps)
        cut075.append(cut)
      if (cut==0.80):
        cut080punzi.append(ps)
        cut080.append(cut)
      # print " Cut = %0.2f"%cut
      # print "Signal numerator: %i" %numSIG
      # print "Signal denominator: %i" %denSIG
      # print "Signal efficiency: %0.3f" %(es)
      # print "Total background: %i" %(numBKG)
      # print "PUNZI: %f" %(ps)
      # print "---------------------------"
  
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
  l1.DrawLatex(0.72,0.96, "Simulation")
  l1.SetTextFont(42)
  l1.SetTextSize(0.031)
  l1.DrawLatex(0.6,0.81, "0.85 #times M_{X} < M_{jj} < 1.15 #times M_{X}")
  l1.DrawLatex(0.6,0.77, "65 GeV < M_{p} < 105 GeV")


  cut080punziRatio = array('d',[])
  cut070punziRatio = array('d',[])
  cut065punziRatio = array('d',[])
  cut060punziRatio = array('d',[])
  cut075punziRatio = array('d',[])
  for i in range (0,len(maxpunzi)):
    cut080punziRatio.append(cut080punzi[i]/maxpunzi[i])
    cut070punziRatio.append(cut070punzi[i]/maxpunzi[i])
    cut065punziRatio.append(cut065punzi[i]/maxpunzi[i])
    cut060punziRatio.append(cut060punzi[i]/maxpunzi[i])
    cut075punziRatio.append(cut075punzi[i]/maxpunzi[i])

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
  g1 = TGraph(len(maxmass), maxmass,cut060punziRatio)
  g2 = TGraph(len(maxmass),maxmass,cut065punziRatio)
  g3 = TGraph(len(maxmass), maxmass,cut070punziRatio)
  g4 = TGraph(len(maxmass), maxmass,cut075punziRatio)
  g5 = TGraph(len(maxmass), maxmass,cut080punziRatio)
  # g1 = TGraph(len(maxmass), maxmass,cut060punzi)
  # g2 = TGraph(len(maxmass),maxmass,cut065punzi)
  # g3 = TGraph(len(maxmass), maxmass,cut070punzi)
  # g4 = TGraph(len(maxmass), maxmass,cut075punzi)
  # g5 = TGraph(len(maxmass), maxmass,cut080punzi)
  g2.GetXaxis().SetTitle('M_{X} [TeV]')
  # g2.GetYaxis().SetTitle("#epsilon_{S}/(1+#sqrt{B})")
  g2.GetYaxis().SetTitle("#frac{Sign}{Sign_{Opt. cut}}")
  g2.GetYaxis().SetTitleOffset(1.5)
  g2.GetYaxis().SetRangeUser(0.3,1.3)
  g2.SetMarkerColor(kRed-3)
  g3.SetMarkerColor(kMagenta)
  g4.SetMarkerColor(kBlue)
  g5.SetMarkerColor(kGray)
  g2.SetLineColor(kRed-3)
  g3.SetLineColor(kMagenta)
  g4.SetLineColor(kBlue)
  g5.SetLineColor(kGray)
  # l3.AddEntry(g1,"%.2f < #tau_{21} < 0.60"%lower,"p")
  l3.AddEntry(g2,"%.2f < #tau_{21} < 0.65"%lower,"p")
  l3.AddEntry(g3,"%.2f < #tau_{21} < 0.70"%lower,"p")
  l3.AddEntry(g4,"%.2f < #tau_{21} < 0.75"%lower,"p")
  l3.AddEntry(g5,"%.2f < #tau_{21} < 0.80"%lower,"p")
  # l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
  # l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
  # l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
  # l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
  # l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")

  g2.Draw("A*L")
  g3.Draw("*Lsame")
  g4.Draw("*Lsame")
  g5.Draw("*Lsame")
  # g1.Draw("*Lsame")
  l3.Draw()

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
  hbkg.SetTitleOffset(1.2,"X")
  hbkg.SetTitleOffset(1.5,"Y")
  hbkg.Rebin(rebin)
  hbkg.SetFillStyle(3018)
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
    h.SetLineColor(lineColor[k])
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

  canvasname ="PunziOpt/LP0v6RATIO"+Signal+"WW.png"
  print "saving to Canvas  %s" %canvasname
  c.Print(canvasname,"png")
  canvasname ="PunziOpt/LP0v6RATIO"+Signal+"WWPunzi.png"
  c2.Print(canvasname,"png")
  canvasname ="PunziOpt/LP0v6RATIO"+Signal+"WWSignvsM.png"
  c3.Print(canvasname,"png")

  time.sleep(5)

  del maxpunzi
  del maxcuts
  del histos
  del hbkg
  del sigfilelist
  del fbkg
  
sys.stdout = orig_stdout  