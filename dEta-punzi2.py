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
# f = file('Tau32Optimisation_L2L3corrected.txt', 'w')
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
            'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-1000.root',
            'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-2000.root',
            'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-3000.root',
            'ExoDiBosonAnalysis.BulkGravToWW.Mcorr-4000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-1000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-2000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-3000.root',
            # 'ExoDiBosonAnalysis.BulkGravTohhTohbbhbb.Mcorr-4000.root',         
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

  massmin = [x*5 for x in range(10,14)]
  massmax = [x for x in range(7,18)]


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


  ########## DO PUNZI #########

  punzi = []
  cuts = []
  signaleffs = []
  bkgeffs = []
  errsignaleffs = []
  bkgyields = []

  i = 0
  for hmax in massmax:
    hmin = 0.
    if hmax > hmin:
       hmax = hmax/10.
       print hmax
       i += 1

       cut = '((jet_deta > %f && jet_deta < %f))' %(hmin,hmax)
       # print '((jet_deta > %f && jet_deta < %f))' %(hmin,hmax)
       cuts.append(cut)
       cut+= ' && (MVV > %f && MVV < %f)' %(wwmin,wwmax)
       cut1 = 'MVV > %f && MVV < %f && jet_deta > 0' %(wwmin,wwmax)
     

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
       cut1 = 'MVV > %f && MVV < %f && jet_deta > 0' %(wwmin,wwmax)
       ngensig = float(sig.GetEntries(cut1))
       es = nsig/ngensig
       # print "N sig ALL: %f" %(sig.GetEntries())
       # print "N sig: %f" %(nsig)
       # print "N gen sig: %f" %(ngensig)
       # print "Signal efficiency: %f" %(es)
       # print "Total background: %f" %(B)
       eb = B/ngenbkg
       if nsig == 0:
         a = 0
         b = 0
         err = 0
       else:   
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
   


  file.Close()
  file.Delete()

  for index in range(0,len(signaleffs)):
    print cuts[index],punzi[index],signaleffs[index],bkgeffs[index],bkgyields[index]
  
  print " "
  print " "
  print " "
  print " "  
  
# sys.stdout = orig_stdout
f.close()
fbkg.Close()
fbkg.Delete()
# time.sleep(100)
