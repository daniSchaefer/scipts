from ROOT import *
import sys
import time
import math
from array import *

gStyle.SetGridColor(kGray)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()


lumi = 3000.
prefix = ''

# orig_stdout = sys.stdout
# f = file('PrunedOptimisation_L2L3corrected.txt', 'w')
# sys.stdout = f



########## OPENING FILES #########

bkgname = [ 'ExoDiBosonAnalysis.QCD1000to1400.root',
            'ExoDiBosonAnalysis.QCD1400to1800.root',
            'ExoDiBosonAnalysis.QCD170to300.root',
            'ExoDiBosonAnalysis.QCD1800to2400.root',
            'ExoDiBosonAnalysis.QCD2400to3200.root',
            'ExoDiBosonAnalysis.QCD300to470.root',
            'ExoDiBosonAnalysis.QCD470to600.root',
            'ExoDiBosonAnalysis.QCD3200toInf.root',
            'ExoDiBosonAnalysis.QCD600to800.root',
            'ExoDiBosonAnalysis.QCD800to1000.root',
         ]

ngenbkg = 0
bkgfilelist = []
bkgtreelist = []
for bname in bkgname:
  print 'Opening file %s' %bname
  fbkg = TFile.Open(bname)
  bkg = TTree()
  fbkg.GetObject('tree',bkg)
  ngenbkg+=bkg.GetEntries()
  fbkg.SetName(bname)
  bkg.SetName(bname)
  bkgfilelist.append(fbkg)
  bkgtreelist.append(bkg)  

masses = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
        
sigfiles = [            #
            # 'RSWWZZ_1TeV.root',
            # 'RSWWZZ_2TeV.root',
            # 'RSWWZZ_3TeV.root',
            # 'RSWWZZ_4TeV.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-4000.root',
            'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-1000.root',
            'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-2000.root',
            'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-3000.root',
            'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-4000.root',           
            'ExoDiBosonAnalysis.RSGravToWW.Mcorr-1000.root',
            'ExoDiBosonAnalysis.RSGravToWW.Mcorr-2000.root',
            'ExoDiBosonAnalysis.RSGravToWW.Mcorr-3000.root',
            'ExoDiBosonAnalysis.RSGravToWW.Mcorr-4000.root',
            'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-1000.root',
            'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-2000.root',
            'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-3000.root',
            'ExoDiBosonAnalysis.RSGravToZZ.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-1000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-2000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-3000.root',
            # 'ExoDiBosonAnalysis.QstarToQZ.M-4000.root',
            # 'ExoDiBosonAnalysis.QstarToQW.M-1000.root',
            # 'ExoDiBosonAnalysis.QstarToQW.M-2000.root',
            # 'ExoDiBosonAnalysis.QstarToQW.M-3000.root',
            # 'ExoDiBosonAnalysis.QstarToQW.M-4000.root'
          ]  
        
        
sigfilelist = []  
for sigf in sigfiles:
   filename = prefix + sigf
   filetmp = TFile.Open(filename,"READ") 
   sigfilelist.append(filetmp)

ii = 0
for file in sigfilelist:
  print 'File == %s' %file.GetName()
  m = masses[ii]
  ii += 1
  mass = m*1000
  print 'Mass set to %i' %mass
  sig = TTree()
  file.GetObject('tree',sig)
  # ngenbkg = bkg.GetEntries()
  ngensig = sig.GetEntries()
  
  ########## DEFINE CUTS #########
  if file.GetName().find("WW") != -1 or file.GetName().find("QW") != -1:
    massmin = [x*5 for x in range(10,14)]
    massmax = [x*5 for x in range(17,24)]
  elif file.GetName().find("ZZ") != -1 or file.GetName().find("QZ") != -1:
    massmin = [x*5 for x in range(10,14)]
    massmax = [x*5 for x in range(17,24)]  
  elif file.GetName().find("WZ") != -1:
    massmin = [x*5 for x in range(10,14)]
    massmax = [x*5 for x in range(17,24)]  
  elif file.GetName().find("hh") != -1:
    massmin = [x*5 for x in range(19,23)]
    massmax = [x*5 for x in range(24,31)]
  elif file.GetName().find("TT") != -1:
    massmin = [x*5 for x in range(25,35)]
    massmax = [x*5 for x in range(35,44)]

  print "Groomed mass steps:"
  print massmin
  print massmax
  

  # print "tree signal entries: %i" %ngensig
  # print "tree bkg entries: %i" %ngenbkg
  ########## CREATING CANVAS #########
  canv = TCanvas("c", "",800,800)
  canv.cd()
  canv.SetGridx()
  canv.SetGridy()

  num = TH1F('roc','roc curve',1000,0.5,1.)
  den = TH1F('den','den',1000,0.5,1.)

  l = TLegend(.16,.74,.36,.93)
  l.SetBorderSize(0)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetTextFont(42)
  l.SetTextSize(0.04)

  # l2 = TLegend(0.1821608,0.6923077,0.3919598,0.7517483,"","NDC")
  # l2.SetLineWidth(2)
  # l2.SetBorderSize(0)
  # l2.SetFillColor(0)
  # l2.SetTextFont(42)
  # l2.SetTextSize(0.04)
  # l2.SetTextAlign(12)

 


  wwmin = mass-15*mass/100. 
  wwmax = mass+15*mass/100.

  print "WW mass limits:"
  print wwmin,wwmax



  # ########## STARTING SIGNAL EFFICIENY #########
  # hnums = fsig.Get("nPassedMjj")
  # hdens = fsig.Get("nEvents")
  # es_start = hnums.GetBinContent(1)/hdens.GetBinContent(1)
  #
  # cut = 'MVV > %f && MVV < %f' %(wwmin,wwmax)
  # nsig = float(sig.GetEntries(cut))
  # ngensig = float(sig.GetEntries())
  # es = nsig/ngensig
  # print "Starting signal efficiency: %f" %(es_start)
  # a = math.sqrt(nsig)/nsig
  # b = math.sqrt(ngensig)/ngensig
  # ########## STARTING BKG EFFICIENY #########
  # nbkg = 0
  # B = 0
  # for t in treelist:
  #   if t.GetName().find("170to300") != -1:
  #     xSec = 117276.
  #     genEvents = 3364368.
  #   if t.GetName().find("300to470") != -1:
  #     xSec = 7823.
  #     genEvents = 2933611.
  #   if t.GetName().find("470to600") != -1:
  #     xSec = 648.2
  #     genEvents = 1936832.
  #   if t.GetName().find("600to800") != -1:
  #     xSec = 186.9
  #     genEvents = 1878856.
  #   if t.GetName().find("800to1000") != -1:
  #     xSec = 32.293
  #     genEvents = 1937216.
  #   if t.GetName().find("1000to1400") != -1:
  #     xSec = 9.4183
  #     genEvents = 1487136.
  #   if t.GetName().find("1400to1800") != -1:
  #     xSec = 0.84265
  #     genEvents = 197959.
  #   if t.GetName().find("1800to2400") != -1:
  #     xSec = 0.114943
  #     genEvents = 193608.
  #   if t.GetName().find("2400to3200") != -1:
  #     xSec = 0.00682981
  #     genEvents = 194456.
  #   if t.GetName().find("3200toInf") != -1:
  #     xSec = 0.000165445
  #     genEvents = 192944.
  #
  #   lweight = xSec/genEvents
  #   print "Lumiweight %f (%f/%f)" %(lweight,xSec,genEvents)
  #   # file =filelist[f]
  #   # hnumbkg = file.Get("nPassedMjj")
  #   # hdenbkg = file.Get("nEvents")
  #   # eb_start = hnumbkg.GetBinContent(1)/hdenbkg.GetBinContent(1)
  #   # print "Starting bkg efficiency: %f" %(eb_start)
  #   # bkg = TTree()
  #   # file.GetObject('tree',bkg)
  #   nbkg = float(t.GetEntries(cut))
  #   B += nbkg*lweight*lumi
  #   eb = nbkg/ngenbkg
  #
  # print "Default punzi: %f" %(es_start/(1+math.sqrt(B)))
  # print " B = %f" %B
  # print "es = %f" %es

  ########## DO PUNZI #########

  punzi = []
  cuts = []
  signaleffs = []
  bkgeffs = []
  errsignaleffs = []
  bkgyields = []

  i = 0
  for hmin in massmin:
   for hmax in massmax:
    if hmax > hmin:
       i += 1

       cut = '((jet_mass_pruned > %f && jet_mass_pruned < %f))' %(hmin,hmax)
       # print '((jet_mass_pruned > %f && jet_mass_pruned < %f))' %(hmin,hmax)
       cuts.append(cut)
       cut+= ' && (MVV > %f && MVV < %f)' %(wwmin,wwmax)
       cut1 = 'MVV > %f && MVV < %f && jet_mass_pruned > 0' %(wwmin,wwmax)
     

       #nbkg1 = float(bkg.GetEntries(cut))
       #nsig1 = float(sig.GetEntries(cut))

       nbkg = 0
       B = 0
       ngenbkg = 0
       for t in bkgtreelist: 
         if t.GetName().find("170to300") != -1:
           xSec = 117276.
           genEvents = 3364368.   
         if t.GetName().find("300to470") != -1:
           xSec = 7823.
           genEvents = 2933611.   
         if t.GetName().find("470to600") != -1:
           xSec = 648.2
           genEvents = 1936832.   
         if t.GetName().find("600to800") != -1:
           xSec = 186.9
           genEvents = 1878856.    
         if t.GetName().find("800to1000") != -1:
           xSec = 32.293
           genEvents = 1937216.      
         if t.GetName().find("1000to1400") != -1:
           xSec = 9.4183
           genEvents = 1487136.       
         if t.GetName().find("1400to1800") != -1:
           xSec = 0.84265
           genEvents = 197959.     
         if t.GetName().find("1800to2400") != -1:
           xSec = 0.114943
           genEvents = 193608.      
         if t.GetName().find("2400to3200") != -1:
           xSec = 0.00682981
           genEvents = 194456.      
         if t.GetName().find("3200toInf") != -1:
           xSec = 0.000165445
           genEvents = 192944.
         
         lweight = xSec/genEvents
         ng = float(t.GetEntries(cut1))
         ng = ng*lweight*lumi
         ngenbkg += ng
         
         nbkg = float(t.GetEntries(cut))
         nbkg = nbkg*lweight*lumi
         B += nbkg
       
       nsig = float(sig.GetEntries(cut))
       cut1 = 'MVV > %f && MVV < %f && jet_mass_pruned > 0' %(wwmin,wwmax)
       ngensig = float(sig.GetEntries(cut1))
       es = nsig/ngensig
       # print "N sig ALL: %f" %(sig.GetEntries())
       # print "N sig: %f" %(nsig)
       # print "N gen sig: %f" %(ngensig)
       # print "Signal efficiency: %f" %(es)
       # print "Total background: %f" %(B)
       eb = B/ngenbkg
       a = math.sqrt(nsig)/nsig
       b = math.sqrt(ngensig)/ngensig
       err = es*math.sqrt( a*a + b*b )
       
       # punzi.append( (nsig*nsig)/(eb*B) )
       punzi.append(es/(1+math.sqrt(B)))
       signaleffs.append(es)
       errsignaleffs.append(err)
       bkgeffs.append(eb)
       bkgyields.append(B)

       #if lmin==80 and lmax==200 and hmin==100 and hmax==220:
       #print cut
       #print "   * sigeff %.6f - bkg eff %.6f - bkg yields %.6f - punzi %.6f" %(es,eb,B,es/(1+math.sqrt(B)))
       # num.Fill(es,(nsig*nsig)/(eb*B))
       num.Fill(es,es/(1+math.sqrt(B)))
       den.Fill(es)

  tmp = punzi[0]
  index = 0
  for p in range(0,len(punzi)):
     if punzi[p] > tmp:
        index = p
        tmp = punzi[p]


  print "Max significance"
  # print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
  a =  errsignaleffs[index]/signaleffs[index]
  b = 1./(1+math.sqrt(bkgyields[index]))
  err = punzi[index]*math.sqrt(a*a+b*b)
  # print " ---> error +/- %f" %(err)
  print'%s %f %.2f %.2f %i' %(cuts[index],punzi[index],signaleffs[index],bkgeffs[index],bkgyields[index])
  # print punzi[index],cuts[index],signaleffs[index],bkgyields[index]
  # print "one up: "
  # print'%s %f %.1f %.2f %i' %(cuts[index+1],punzi[index+1],signaleffs[index+1],bkgeffs[index+1],bkgyields[index+1])
  # print "one down: "
  # print'%s %f %.1f %.2f %i' %(cuts[index-1],punzi[index-1],signaleffs[index-1],bkgeffs[index-1],bkgyields[index-1])
  print " "
  print " "
   

  # #
  # # tmp = punzi[0]
  # # index = 0
  # # for p in range(0,len(punzi)):
  # #    if punzi[p] < tmp:
  # #       index = p
  # #       tmp = punzi[p]
  # #
  # # print "Min significance"
  # # print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
  # # a =  errsignaleffs[index]/signaleffs[index]
  # # b = 1./(1+math.sqrt(bkgyields[index]))
  # # err = punzi[index]*math.sqrt(a*a+b*b)
  # # print " ---> error +/- %f" %(err)
  # #
  # # tmp = signaleffs[0]
  # # index = 0
  # # for p in range(0,len(signaleffs)):
  # #    if signaleffs[p] > tmp:
  # #       index = p
  # #       tmp = signaleffs[p]
  # #
  # # print "Max signal efficiency"
  # # print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
  # #
  # # tmp = bkgeffs[0]
  # # index = 0
  # # for p in range(0,len(bkgeffs)):
  # #    if bkgeffs[p] < tmp:
  # #       index = p
  # #       tmp = bkgeffs[p]
  # #
  # # print "Max bkg rejection"
  # # print index,punzi[index],cuts[index],bkgeffs[index],signaleffs[index],bkgyields[index]
  # #
  # # print "********************************"
  # # for p in range(0,len(punzi)):
  # #   if punzi[p] > 0.355 and punzi[p]<0.356: print cuts[p],punzi[p],bkgeffs[p],signaleffs[p]
  # #
  # # for e in range(0,len(signaleffs)):
  # #   if signaleffs[e] > 0.94: #and signaleffs[e] < 0.74:
  # #      print punzi[e],cuts[e],bkgeffs[e],signaleffs[e]
  #
  # num.Divide(den)
  # l.AddEntry(num,"G_{RS}(%i TeV)"%m,"P")
  # num.SetMarkerStyle(20)
  # num.SetMarkerColor(kOrange+1)
  # num.Draw("P")
  # num.GetXaxis().SetTitle("Signal efficiency")
  # num.GetXaxis().SetLabelSize(0.04)
  # num.GetYaxis().SetTitle("Punzi significance")
  # num.GetYaxis().SetTitleOffset(1.9)
  # num.GetXaxis().SetTitleOffset(1.5)
  # num.GetYaxis().SetLabelSize(0.04)
  # l.Draw()
  #
  # x = array('d',[])
  # y = array('d',[])
  #
  # # bin = num.GetXaxis().FindBin(0.86176)
  # #
  # # x.append(num.GetBinCenter(bin))
  # # y.append(num.GetBinContent(bin))
  # # gr = TGraph(1,x,y)
  # # gr.SetMarkerStyle(29)
  # # gr.SetMarkerSize(2.4)
  # # l2.AddEntry(gr,'','P')
  # # gr.Draw("P")
  # # l2.Draw()
  #
  #
  #
  # l1 = TLatex()
  # l1.SetTextAlign(13)
  # l1.SetTextFont(42)
  # l1.SetNDC()
  # l1.SetTextSize(0.04)
  # l1.DrawLatex(0.14+0.03,0.25, 'G_{RS}(%i TeV)'%m)
  #
  # l1.SetTextAlign(12)
  # l1.SetTextSize(0.045)
  # l1.SetTextFont(62)
  # l1.DrawLatex(0.78,0.96, "3fb^{-1}")
  #
  # l1.SetTextAlign(12)
  # l1.SetTextSize(0.035)
  # l1.SetTextFont(61)
  # l1.DrawLatex(0.13,0.96, "CMS")
  # l1.SetTextSize(0.03)
  # l1.SetTextFont(52)
  # l1.DrawLatex(0.21,0.96, "Simulation")
  #
  # l1.SetTextFont(42)
  # l1.SetTextSize(0.025)
  # l1.DrawLatex(0.2,0.45, "")
  # l1.DrawLatex(0.2,0.42, 'M_{SD} #in [40,120]')
  #
  # canv.Update()
  # outname = "pruned_WZ%i.pdf"%m
  # canv.SaveAs(outname)
  file.Close()
  file.Delete()

  for index in range(0,len(signaleffs)):
    print cuts[index],punzi[index],bkgeffs[index],signaleffs[index],bkgyields[index]
  
  print " "
  print " "
  print " "
  print " "  
  
# sys.stdout = orig_stdout
f.close()
fbkg.Close()
fbkg.Delete()
# time.sleep(100)
