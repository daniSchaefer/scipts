from optparse import OptionParser
import ROOT
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
import array

def print_yields(f,h,k):

   nEvents_ = (ROOT.TH1F(f.Get("nEvents"))).GetBinContent(1);
   
   if nEvents_ == 0:
      print "No events found!"

   error1 = 0
   
   if nEvents_ != 0:      
      nPassedTrigger_	 = (ROOT.TH1F(f.Get("nPassedTrigger"))).GetBinContent(1)
      nPassedFoundMuon_  = (ROOT.TH1F(f.Get("nPassedFoundMuon"))).GetBinContent(1)
      nPassedFoundMET_   = (ROOT.TH1F(f.Get("nPassedFoundMET"))).GetBinContent(1)
      nPassedFoundJet_   = (ROOT.TH1F(f.Get("nPassedFoundJet"))).GetBinContent(1)
      nPassedJetPtTight_ = (ROOT.TH1F(f.Get("nPassedJetPtTight"))).GetBinContent(1)
      nPassedLepJetDR_   = (ROOT.TH1F(f.Get("nPassedLepJetDR"))).GetBinContent(1)
      nPassedJetCSV_	 = (ROOT.TH1F(f.Get("nPassedJetCSV"))).GetBinContent(1)
      nPassedAJetCut_	 = (ROOT.TH1F(f.Get("nPassedAJetCut"))).GetBinContent(1)
      nPassedFoundW_	 = (ROOT.TH1F(f.Get("nPassedFoundW"))).GetBinContent(1) 
      nPassedLepJetDR2_  = (ROOT.TH1F(f.Get("nPassedLepJetDR2"))).GetBinContent(1)
      nPassedMETJetDPhi_ = (ROOT.TH1F(f.Get("nPassedMETJetDPhi"))).GetBinContent(1)
      nPassedJetWDPhi_   = (ROOT.TH1F(f.Get("nPassedJetWDPhi"))).GetBinContent(1)
      nPassedJetMass_	 = (ROOT.TH1F(f.Get("nPassedJetMass"))).GetBinContent(1)
      nPassedExoCandidateMass_	 = (ROOT.TH1F(f.Get("nPassedExoCandidateMass"))).GetBinContent(1)

      print "############ Cut flow: ############"      
      print "number of events					    %.0f" %nEvents_ 
      print "passed trigger					    %.0f --- eff = %.4f" %(nPassedTrigger_,nPassedTrigger_/nEvents_)  
      print "found muon 					    %.0f --- eff = %.4f" %(nPassedFoundMuon_,nPassedFoundMuon_/nEvents_) 
      print "found MET  					    %.0f --- eff = %.4f" %(nPassedFoundMET_,nPassedFoundMET_/nEvents_) 
      print "found jet candidate with pt cut loose (80 GeV)	    %.0f --- eff = %.4f" %(nPassedFoundJet_,nPassedFoundJet_/nEvents_) 
      print "DR(j,l) > 1					    %.0f --- eff = %.4f" %(nPassedLepJetDR_,nPassedLepJetDR_/nEvents_) 
      print "jet pt cut tight (200 GeV) 			    %.0f --- eff = %.4f" %(nPassedJetPtTight_,nPassedJetPtTight_/nEvents_)
      print "jet csv cut					    %.0f --- eff = %.4f" %(nPassedJetCSV_,nPassedJetCSV_/nEvents_) 
      print "additional jets cut				    %.0f --- eff = %.4f" %(nPassedAJetCut_,nPassedAJetCut_/nEvents_) 
      print "found W						    %.0f --- eff = %.4f" %(nPassedFoundW_,nPassedFoundW_/nEvents_) 
      print "DR(j,l) > pi/2					    %.0f --- eff = %.4f" %(nPassedLepJetDR2_,nPassedLepJetDR2_/nEvents_) 
      print "Dphi(MET,j) > 2					    %.0f --- eff = %.4f" %(nPassedMETJetDPhi_,nPassedMETJetDPhi_/nEvents_)
      print "Dphi(j,W) > 2					    %.0f --- eff = %.4f" %(nPassedJetWDPhi_,nPassedJetWDPhi_/nEvents_) 
      print "jet mass cut					    %.0f --- eff = %.4f" %(nPassedJetMass_,nPassedJetMass_/nEvents_) 
      print "WH mass window		                %.0f --- eff = %.4f" %(nPassedExoCandidateMass_,nPassedExoCandidateMass_/nEvents_)

      error1 = ROOT.TMath.Sqrt(nPassedJetMass_)/nPassedJetMass_;

      err = h.Integral()*k*error1
      y = h.Integral()*k
      print "Final yields: %.2f +/- %.2f" %(y,err)
   
      return [y,err]

def get_canvas():

   tdrstyle.setTDRStyle()
   CMS_lumi.lumi_8TeV = "19.7 fb^{-1}"
   CMS_lumi.writeExtraText = 0
   CMS_lumi.extraText = "Preliminary"

   iPos = 0
   if( iPos==0 ): CMS_lumi.relPosX = 0.09

   H_ref = 600; 
   W_ref = 600; 
   W = W_ref
   H  = H_ref

   T = 0.08*H_ref
   B = 0.12*H_ref 
   L = 0.12*W_ref
   R = 0.04*W_ref

   canvas = ROOT.TCanvas("c2","c2",W,H)
   canvas.SetFillColor(0)
   canvas.SetBorderMode(0)
   canvas.SetFrameFillStyle(0)
   canvas.SetFrameBorderMode(0)
   canvas.SetLeftMargin( L/W )
   canvas.SetRightMargin( R/W )
   canvas.SetTopMargin( T/H )
   canvas.SetBottomMargin( B/H )
   canvas.SetTickx()
   canvas.SetTicky()
   
   return canvas

def get_ratio(hdata,histsum):

   ratio = ROOT.TH1F("ratio","ratio",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         r = hdata.GetBinContent(b)/nbkg
         ratio.SetBinContent(b,r)
         err = r*ROOT.TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b)/(ndata*ndata) + histsum.GetBinError(b)*histsum.GetBinError(b)/(nbkg*nbkg) )
         ratio.SetBinError(b,err)   
    
   ratio.SetLineColor(ROOT.TColor.kBlack)      
   ratio.SetLineColor(ROOT.TColor.kBlack)
   ratio.SetMarkerColor(ROOT.TColor.kBlack)
   ratio.SetMarkerStyle(20)
   ratio.SetMarkerSize(1.)
   ratio.SetMinimum(0.)
   ratio.SetMaximum(3.)
   ratio.GetYaxis().SetTitle("Data/MC")
   ratio.GetYaxis().SetNdivisions(4)
   ratio.GetYaxis().SetLabelSize(0.15)
   ratio.GetXaxis().SetLabelSize(0.15)
   ratio.GetYaxis().SetTitleSize(0.2)
   ratio.GetYaxis().SetTitleOffset(0.2)
   ratio.GetYaxis().CenterTitle()
   
   return ratio

def get_pull(hdata,histsum):
   
   pull = ROOT.TH1F("pull","pull",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         err = ROOT.TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b) + histsum.GetBinError(b)*histsum.GetBinError(b) )
         p = (hdata.GetBinContent(b)-nbkg)/err
         pull.SetBinContent(b,p)
         pull.SetBinError(b,1) 
	 #print "bin %i center %.2f pull %.2f" %(b,hdata.GetBinCenter(b),p)  
    
   pull.SetLineColor(ROOT.TColor.kBlack)      
   pull.SetLineColor(ROOT.TColor.kBlack)
   pull.SetMarkerColor(ROOT.TColor.kBlack)
   pull.SetMarkerStyle(20)
   pull.SetMarkerSize(1.)
   pull.SetMinimum(-4.)
   pull.SetMaximum(4.)
   pull.GetYaxis().SetTitle("#frac{Data-MC}{#sigma}")
   pull.GetYaxis().SetNdivisions(4)
   pull.GetYaxis().SetLabelSize(0.15)
   pull.GetXaxis().SetLabelSize(0.15)
   pull.GetYaxis().SetTitleSize(0.2)
   pull.GetYaxis().SetTitleOffset(0.2)
   pull.GetYaxis().CenterTitle()
   
   return pull

def get_chi2(hpull):

   pt = ROOT.TPaveText(0.71,0.34,0.92,0.51,"NDC")
   pt.SetTextFont(42)
   pt.SetTextSize(0.05)
   pt.SetTextAlign(12)
   pt.SetFillColor(0)
   
   chi2 = 0
   for b in xrange(0,hpull.GetNbinsX()):
      chi2+=hpull.GetBinContent(b)*hpull.GetBinContent(b)
   
   ndof = hpull.GetNbinsX()-4  
   pt.AddText("#chi^{2}/ndof = %.2f" %(chi2/ndof))
   return pt
    
def get_line(xmin,xmax,y,style):

   line = ROOT.TLine(xmin,y,xmax,y)
   line.SetLineColor(ROOT.TColor.kRed)
   line.SetLineStyle(style)
   line.SetLineWidth(2)
   return line
            
argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                              help="configuration")
parser.add_option("-p", "--plot", dest="plot", default="stack", action="store",
                              help="plot same or stack")
parser.add_option("-R", "--ratio", dest="ratio", default=False, action="store_true",
                              help="do ratio plot")
parser.add_option("-P", "--pull", dest="pull", default=False, action="store_true",
                              help="do pull plot")
parser.add_option("-S", "--syst", dest="syst", default=False, action="store_true",
                              help="do systematics")
parser.add_option("-s", "--save", dest="save", default=False, action="store_true",
                              help="save canvas")
parser.add_option("-t", "--time", dest="time", default=20, action="store", type="float",
                              help="time sleep")
			      			      			      			      
(opts, args) = parser.parse_args(argv)
print opts.config

config = ConfigParser.ConfigParser()
config.read(opts.config)

prefix = config.get('StackPlots','prefix')
files = eval(config.get('StackPlots','filelist'))
lumi = config.getfloat('StackPlots','lumi')
data = config.get('StackPlots','data')
signal = config.get('StackPlots','signal')
histos = eval(config.get('StackPlots','histos'))
bkgname = eval(config.get('StackPlots','bkg'))
signalname = config.get('StackPlots','signalname')
scalesignal = config.getfloat('StackPlots','scalesignal')
sfwjets = config.getfloat('StackPlots','sfwjets')
rebin = config.getint('StackPlots','rebin')
ttbarunc = config.getfloat('StackPlots','ttbarunc')
doratio = opts.ratio
dopull = opts.pull
dosyst = opts.syst

print "------------------------------------"
print "Lumi = %.1f" %lumi
print "------------------------------------"
print "Input files directory: %s" %prefix
print "------------------------------------"
print "data file : %s" %data
print "signal file : %s" %signal
print "backgrounds : "
print files  
print "------------------------------------"
print "Histos : "
print histos

filelist = []

for f in files:
   filename = prefix + "/" + f
   print f
   print prefix
   print filename
   filetmp = ROOT.TFile.Open(filename,"READ")
   htmp = ROOT.TH1F(filetmp.Get(histos[0]))
   print htmp.Integral()   
   filelist.append(filetmp)
      
if signal != "":
   file_signal = ROOT.TFile.Open(prefix+"/"+signal,"READ")

if data != "":
   file_data = ROOT.TFile.Open(prefix+"/"+data,"READ")

fillStyle = [3018  ,1001  ,1001     ,1001   ,1001 ,1001    ]
fillColor = [1,210,2,4,ROOT.TColor.kCyan,ROOT.TColor.kAzure+8,ROOT.TColor.kPink-7]
lineWidth = [3     ,2     ,2        ,2      ,2    ,2       , 2]
lineStyle = [2,1,1,1,1,1,1]
lineColor = [ROOT.TColor.kBlack,ROOT.TColor.kBlack,ROOT.TColor.kBlack,ROOT.TColor.kBlack,ROOT.TColor.kBlack,ROOT.TColor.kBlack,ROOT.TColor.kBlack]
legendStyle = ['F','F','F','F','F','F','F']
if opts.plot == 'same':
  fillColor = [0,0,0,0,0,0,0]
  lineColor = [ROOT.TColor.kBlack,ROOT.TColor.kRed+1,ROOT.TColor.kSpring-1,ROOT.TColor.kYellow,ROOT.TColor.kBlue,ROOT.TColor.kAzure+8,ROOT.TColor.kPink-7]
  lineWidth = [3     ,3     ,3        ,3      ,3    ,3   , 3    ]
  legendStyle = ['L','L','L','L','L','L','L']
   
      
for h in histos:
    
   sysunc = []
   statunc = []
   
   l = ROOT.TLegend(0.71,0.55,0.92,0.87,"","NDC")
   l.SetLineWidth(2)
   l.SetBorderSize(0)
   l.SetFillColor(0)
   l.SetTextFont(42)
   l.SetTextSize(0.04)
   l.SetTextAlign(12)
             
   if data != "":  
      h_data = ROOT.TH1F(file_data.Get(h)) 
      h_data.Rebin(rebin)   
      h_data.SetLineColor(ROOT.TColor.kBlack)
      h_data.SetLineColor(ROOT.TColor.kBlack);
      h_data.SetMarkerColor(ROOT.TColor.kBlack);
      h_data.SetMarkerStyle(20);
      h_data.SetMarkerSize(1.);
      l.AddEntry(h_data,"CMS Data","P")
   
   if signal != "":
      h_signal = ROOT.TH1F(file_signal.Get(h))
      h_signal.SetLineColor(lineColor[0])
      h_signal.SetLineWidth(lineWidth[0])
      h_signal.SetLineStyle(lineStyle[0])
      h_signal.SetFillStyle(fillStyle[0])
      h_signal.SetFillColor(fillColor[0])
      h_signal.Scale(scalesignal*100)
      l.AddEntry(h_signal,signalname,legendStyle[0])
   
   histolist = []
      
   if opts.plot == 'stack':
      hs = ROOT.THStack("hs", h)     
   
   for f in xrange(0,len(filelist)):
      histolist.append(ROOT.TH1F(filelist[f].Get(h)))
      if dosyst and f == 0:
         n = prefix+"_HtagSysUp/"+files[f]
         fup = ROOT.TFile.Open(n,"READ")
         histoSysUp = ROOT.TH1F(fup.Get(h))
         n = prefix+"_HtagSysDown/"+files[f]
         fdown = ROOT.TFile.Open(n,"READ")
         histoSysDown = ROOT.TH1F(fdown.Get(h))
   
   hsum = ROOT.TH1F("hsum","hsum",histolist[0].GetNbinsX()/rebin,histolist[0].GetXaxis().GetXmin(),histolist[0].GetXaxis().GetXmax())
      
   for j in range(0,len(histolist)):  
      histolist[j].Scale(lumi)
      histolist[j].Rebin(rebin) 
      if j == 0:
         if dosyst:
            histoSysUp.Scale(lumi)
            histoSysUp.Rebin(rebin)
            histoSysDown.Rebin(rebin)
            histoSysDown.Scale(lumi)   
         for b in xrange(1,histolist[j].GetNbinsX()+1):
            sysup = 0.
            sysdown = 0.
	    if dosyst:
               if histolist[j].GetBinContent(b) != 0:
                  sysup = (histoSysUp.GetBinContent(b)-histolist[j].GetBinContent(b))/histolist[j].GetBinContent(b)
                  sysdown = (histolist[j].GetBinContent(b)-histoSysDown.GetBinContent(b))/histolist[j].GetBinContent(b)
            if sysup > sysdown:
               syst = sysup
            else:
               syst = sysdown
            syst2 = histolist[j].GetBinContent(b)*ttbarunc/100.  
            sysunc.append(ROOT.TMath.Sqrt(syst2*syst2+syst*syst))
            print "sf sys %f htag sys %f" %(syst2,syst)
      if j == 1:
         histolist[j].Scale(29.*sfwjets/23.5) #1.8 for mu - 1.71 for ele
      histolist[j].SetLineColor(lineColor[j+1])
      histolist[j].SetLineWidth(lineWidth[j+1])
      histolist[j].SetLineStyle(lineStyle[j+1])
      histolist[j].SetFillStyle(fillStyle[j+1])
      histolist[j].SetFillColor(fillColor[j+1])
      l.AddEntry(histolist[j],bkgname[j],legendStyle[j+1]) 
      hsum.Add(histolist[j])
               
   for b in xrange(1,hsum.GetNbinsX()+1):
      err = ROOT.TMath.Sqrt(hsum.GetBinError(b)*hsum.GetBinError(b)+sysunc[b-1]*sysunc[b-1]) 
      hsum.SetBinError(b,err)
   
   hsum.SetFillColor(ROOT.TColor.kBlack)
   hsum.SetFillStyle(3008)
   hsum.SetLineColor(ROOT.TColor.kWhite)
   l.AddEntry(hsum,"MC Stat + Sys","F")
   
   if opts.plot == 'stack':        
      for j in range(1,len(histolist)+1):   
         hs.Add( histolist[len(histolist)-j],"HIST")

   if signal != "":
      xMin  = h_signal.GetXaxis().GetXmin()
      xMax  = h_signal.GetXaxis().GetXmax()
      nBins = h_signal.GetXaxis().GetNbins()
      xAxisTitle = h_signal.GetXaxis().GetTitle()
   else:
      xMin  = histolist[0].GetXaxis().GetXmin()
      xMax  = histolist[0].GetXaxis().GetXmax()
      nBins = histolist[0].GetXaxis().GetNbins()	
      xAxisTitle = histolist[0].GetXaxis().GetTitle()
   
   yTitle = "Events / %.0f" %((xMax-xMin)/nBins)

   if xAxisTitle.find("GeV") != -1:
      yTitle+=" GeV"
   elif xAxisTitle.find("rad") != -1:
      yTitle+=" rad"
   elif xAxisTitle.find("cm") != -1:
      yTitle+=" cm"

   canv = get_canvas()   
   canv.cd()

   pad0 = ROOT.TPad("pad0","pad0",0.,0.24,0.99,1.)
   pad0.SetBottomMargin(0.15)
   pad0.SetTopMargin(0.08)
   pad0.Draw()
   pad0.cd()
      
   if opts.plot == 'stack':
      hs.Draw()
      hs.GetXaxis().SetTitle( xAxisTitle )
      hs.GetYaxis().SetTitle( yTitle )
      hs.GetXaxis().SetLabelSize(0.04)
      hs.GetYaxis().SetLabelSize(0.04)
      hs.GetYaxis().SetTitleOffset(0.8)
      if data != "":
         hs.SetMaximum(h_data.GetMaximum()+10)
      if data == "":
         hs.SetMaximum(histolist[0].GetMaximum()+10)	 
      if signal != "":
   	 h_signal.Draw("sameHIST")
      if data != "":
   	 h_data.Draw("samePE")
   	 hsum.Draw("E2same")
   elif opts.plot == 'same':
      h_signal.Draw("hist")
      for j in range(0,len(histolist)):
   	 histolist[j].Draw("sameHIST")   

   l.Draw()
   
   canv.Update()
   canv.cd()
   
   pad1 = ROOT.TPad("pad1","pad1",0.,0. ,0.99,0.24) 
   pad1.SetTopMargin(0.05)
   pad1.SetGridy()
   pad1.SetGridx()
   pad1.Draw("same")
   pad1.cd()
   
   if doratio:
      rh = get_ratio(h_data,hsum)
      rh.Draw()
      li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),1,1)
      li.Draw()
      rh.Draw("same")

   if dopull:
      ph = get_pull(h_data,hsum)
      ph.Draw()
      li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),0,1)
      li.Draw()
      ph.Draw("same")
      pad0.cd()
      #t = get_chi2(ph)
      #t.Draw("same")
                
   canv.Update()
   
   pad0.cd()
   CMS_lumi.CMS_lumi(pad0, 2, 0)	   
   pad0.cd()
   pad0.Update()
   pad0.RedrawAxis()
   frame = pad0.GetFrame()
   frame.Draw()   
   canv.cd()
   canv.Update()

   time.sleep(opts.time)
   if opts.save: 
      canvasname = prefix+"/"+h+".pdf"
      canv.Print(canvasname,"pdf")
      #hsum.SaveAs(prefix+"/"+h+"_sum.root")   

data_yields = []
if data != "":
   print ""
   print "================= Yields for data ================= "
   h = ROOT.TH1F(file_data.Get("CA8jetPrunedMass"))
   data_yields = print_yields(file_data,h,1.) 

yields = []
errors = []

if signal != "":
   print ""
   print "================= Yields for %s process ================= " %signalname
   h = ROOT.TH1F(file_signal.Get("CA8jetPrunedMass"))
   tmp = []
   tmp = print_yields(file_signal,h,lumi) 
   yields.append(tmp[0])
   errors.append(tmp[1])

for f in range(0,len(filelist)):
   print ""
   print "================= Yields for %s process ================= " %bkgname[f]
   h = ROOT.TH1F(filelist[f].Get("CA8jetPrunedMass"))
   print filelist[f].GetName()
   print h.Integral()*lumi
   tmp = []
   k = 1.
   if f == 1:
      k = 29.*sfwjets/23.5
   if f == 4:
      k = 1.19   
   tmp = print_yields(filelist[f],h,lumi*k)
   yields.append(tmp[0]) 
   errors.append(tmp[1])

S = 1.
errS = 1.
B = 1.
errSum = 1.
if signal != "":
   S = yields[0]
   errS = errors[0]
   for b in range(1,len(yields)):
      B+=yields[b]
      errSum+=math.pow(errors[b],2)
elif signal == "":
   for b in range(0,len(yields)):
      B+=yields[b]
      errSum+=math.pow(errors[b],2)
      
errB = math.sqrt(errSum)
a = errS/math.sqrt(B)
b = math.pow(B,-1.5)*errB/2.
errSign = math.sqrt(a*a+b*b)
sign = S/math.sqrt(B)
print ""
print "*********************************************"   
print "*********************************************"   

print "****************** TOT BACKGROUND = %.6f +/- %.6f" %(B,errB)
if signal != "":       
   print "****************** SIGNIFICANCE = %.6f +/- %.6f" %(sign,errSign)    

if data != "":
   print "****************** TOT DATA = %.6f +/- %.6f" %(data_yields[0],data_yields[1])   

print "*********************************************"   
print "*********************************************"   

