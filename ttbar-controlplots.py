from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
import array

def print_yields(f,h,k):

   nEvents_ = (TH1F(f.Get("nEvents"))).GetBinContent(1);
   
   if nEvents_ == 0:
      print "No events found!"

   error1 = 0
   
   if nEvents_ != 0:      
      nPassedTrigger_	       = (TH1F(f.Get("nPassedTrigger"))).GetBinContent(1)
      nPassedFoundLepton_      = (TH1F(f.Get("nPassedFoundLept"))).GetBinContent(1)
      nPassedFoundMET_         = (TH1F(f.Get("nPassed1Jet"))).GetBinContent(1)
      nPassedFoundW_           = (TH1F(f.Get("nPassed2Jet"))).GetBinContent(1)
      nPassedFoundJet_         = (TH1F(f.Get("nPassed3Jet"))).GetBinContent(1)
      nPassedLepJetDR_         = (TH1F(f.Get("nPassed4Jet"))).GetBinContent(1)
      nPassedJetPtTight_       = (TH1F(f.Get("nPassed1bTag"))).GetBinContent(1)
      nPassedAJetCut_	       = (TH1F(f.Get("nPassed2bTag"))).GetBinContent(1)


      print "############ Cut flow: ############"      
      print "number of events					    %.0f" %nEvents_ 
      print "passed trigger					    %.0f --- eff = %.4f" %(nPassedTrigger_,nPassedTrigger_/nEvents_)  
      print "found lepton 					    %.0f --- eff = %.4f" %(nPassedFoundLepton_,nPassedFoundLepton_/nEvents_) 
      print "found 1 jet  					    %.0f --- eff = %.4f" %(nPassedFoundMET_,nPassedFoundMET_/nEvents_) 
      print "found 2 jets 		                                    %.0f --- eff = %.4f" %(nPassedFoundW_,nPassedFoundW_/nEvents_)
      print "found 3 jets	    %.0f --- eff = %.4f" %(nPassedFoundJet_,nPassedFoundJet_/nEvents_) 
      print "found 4 jets					    %.0f --- eff = %.4f" %(nPassedLepJetDR_,nPassedLepJetDR_/nEvents_) 
      print "1 btag 			    %.0f --- eff = %.4f" %(nPassedJetPtTight_,nPassedJetPtTight_/nEvents_)
      print "2 btags				    %.0f --- eff = %.4f" %(nPassedAJetCut_,nPassedAJetCut_/nEvents_) 


      error1 = TMath.Sqrt(nPassedJetMass_)/nPassedJetMass_;

      err = h.Integral()*k*error1
      y = h.Integral()*k
      print "Final yields: %.2f +/- %.2f" %(y,err)
   
      return [y,err]

def get_canvas():

   tdrstyle.setTDRStyle()
   CMS_lumi.lumi_13TeV = "1.26 fb^{-1}"
   CMS_lumi.writeExtraText = 0
   CMS_lumi.extraText = "Preliminary"

   iPos = 0
   if( iPos==0 ): CMS_lumi.relPosX = 0.15

   H_ref = 600; 
   W_ref = 700; 
   W = W_ref
   H  = H_ref

   T = 0.08*H_ref
   B = 0.12*H_ref 
   L = 0.12*W_ref
   R = 0.06*W_ref

   canvas = TCanvas("c2","c2",W,H)
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

   ratio = TH1F("ratio","ratio",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         r = hdata.GetBinContent(b)/nbkg
         ratio.SetBinContent(b,r)
         err = r*TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b)/(ndata*ndata) + histsum.GetBinError(b)*histsum.GetBinError(b)/(nbkg*nbkg) )
         ratio.SetBinError(b,err)   
    
   ratio.SetLineColor(kBlack)      
   ratio.SetLineColor(kBlack)
   ratio.SetMarkerColor(kBlack)
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
   
   pull = TH1F("pull","pull",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         err = TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b) + histsum.GetBinError(b)*histsum.GetBinError(b) )
         p = (hdata.GetBinContent(b)-nbkg)/err
         pull.SetBinContent(b,p)
         pull.SetBinError(b,1) 
	 #print "bin %i center %.2f pull %.2f" %(b,hdata.GetBinCenter(b),p)  
    
   pull.SetLineColor(kBlack)      
   pull.SetLineColor(kBlack)
   pull.SetMarkerColor(kBlack)
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

   pt = TPaveText(0.71,0.34,0.92,0.51,"NDC")
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

   line = TLine(xmin,y,xmax,y)
   line.SetLineColor(kRed)
   line.SetLineStyle(style)
   line.SetLineWidth(2)
   return line
            
argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                              help="configuration")
parser.add_option("-R", "--ratio", dest="ratio", default=False, action="store_true",
                              help="do ratio plot")
parser.add_option("-P", "--pull", dest="pull", default=False, action="store_true",
                              help="do pull plot")
parser.add_option("-s", "--save", dest="save", default=False, action="store_true",
                              help="save canvas")
parser.add_option("-w", "--write", dest="write", default=False, action="store_true",
                              help="write to file")                              
parser.add_option("-t", "--time", dest="time", default=10, action="store", type="float",
                              help="time sleep")
parser.add_option("-l", "--log", dest="doLog", default=False, action="store_true",
                              help="Plot logY")			
parser.add_option("-a", "--areascale", dest="areaScale", default=False, action="store_true",
                              help="Scale W+jets to area")		                                    			      			      			      
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
xTitle = config.get('StackPlots','xAxisTitle')

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
   filetmp = TFile.Open(filename,"READ") 
   htmp = TH1F(filetmp.Get(histos[0]))
   print htmp.Integral()
   filelist.append(filetmp)
      
if signal != "":
   file_signal = TFile.Open(prefix+"/"+signal,"READ")

if data != "":
   file_data = TFile.Open(prefix+"/"+data,"READ")

fillStyle = [3018  ,1001  ,1001,1001,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
fillColor = [1,210,2,4,kCyan+1,kAzure+8,kPink-7,8,9]
lineWidth = [3     ,2     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2,2]
lineStyle = [2,1,1,1,1,1,1,1,1,1]
lineColor = [kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack]
legendStyle = ['F','F','F','F','F','F','F','F','F','F']   

dataevents  = 0      
for h in histos:
    
   sysunc = []
   statunc = []
   
   l = TLegend(0.68,0.59,0.89,0.86,"","NDC")
   l.SetLineWidth(2)
   l.SetBorderSize(0)
   l.SetFillColor(0)
   l.SetTextFont(42)
   l.SetTextSize(0.04)
   l.SetTextAlign(12)
             
   if data != "":  
      h_data = TH1F(file_data.Get(h)) 
      h_data.Rebin(rebin)   
      h_data.SetLineColor(kBlack)
      h_data.SetLineColor(kBlack);
      h_data.SetMarkerColor(kBlack);
      h_data.SetMarkerStyle(20);
      h_data.SetMarkerSize(1.);
      dataevents = h_data.Integral()
      l.AddEntry(h_data,"CMS Data","P")
   
   if signal != "":
      h_signal = TH1F(file_signal.Get(h))
      h_signal.SetLineColor(lineColor[0])
      h_signal.SetLineWidth(lineWidth[0])
      h_signal.SetLineStyle(lineStyle[0])
      h_signal.SetFillStyle(fillStyle[0])
      h_signal.SetFillColor(fillColor[0])
      h_signal.Scale(scalesignal*lumi)
      h_signal.Rebin(rebin)
      l.AddEntry(h_signal,signalname,legendStyle[0])
   
   histolist = []   
   for f in xrange(0,len(filelist)):
     histolist.append(TH1F(filelist[f].Get(h)))

   hs = THStack("hs", h)
   hsum = TH1F("hsum","hsum",histolist[0].GetNbinsX()/rebin,histolist[0].GetXaxis().GetXmin(),histolist[0].GetXaxis().GetXmax())
   for j in range(0,len(histolist)):
      histolist[j].Scale(lumi)
      print lumi
      histolist[j].Rebin(rebin) 
      histolist[j].SetLineColor(lineColor[j+1])
      histolist[j].SetLineWidth(lineWidth[j+1])
      histolist[j].SetLineStyle(lineStyle[j+1])
      histolist[j].SetFillStyle(fillStyle[j+1])
      histolist[j].SetFillColor(fillColor[j+1])
      l.AddEntry(histolist[j],bkgname[j],legendStyle[j+1]) 
      hsum.Add(histolist[j])
   # print 'integrating from %f to %f' %(hsum.GetBinCenter(5),hsum.GetBinCenter(6))
   # print "Non b = %f percent" %( (hsum.Integral(0,5)+hsum.Integral(7,25) )/hsum.Integral() )
   # print "b = %f percent" %(hsum.GetBinContent(6)/hsum.Integral() )
   # l.AddEntry(hsum,"MC Stat","F")
   
   if sfwjets != 1.:
     print "DATA/MC scalefactor = %f +- SEE ELSEWEHERE" %(sfwjets)
     histolist[2].Scale(sfwjets)
   if data != "":
     print "MC = %i" %hsum.Integral()
     print "DATA = %i" %h_data.Integral()
     diff = h_data.Integral()-hsum.Integral()
     sf = diff/histolist[0].Integral()+1
     histolist[0].Scale(sf)
     error = sf*math.sqrt( (1./h_data.Integral()) + (1./hsum.Integral()) )
     print "DATA/MC scalefactor = %f +- %f" %(sf,error)
     diff = 1/histolist[0].Integral()*(dataevents-hsum.Integral()+histolist[0].Integral())
     print "SF (ttbar) = %f" %diff
   
                
   for j in range(1,len(histolist)+1):   
      hs.Add( histolist[len(histolist)-j],"HIST")
   hsum.SetFillColor(kBlack)
   hsum.SetFillStyle(3008)
   hsum.SetLineColor(kWhite)
   
   if signal != "":
      xMin  = h_signal.GetXaxis().GetXmin()
      xMax  = h_signal.GetXaxis().GetXmax()
      nBins = h_signal.GetXaxis().GetNbins()
      xAxisTitle = h_signal.GetXaxis().GetTitle()
   else:
      xMin  = histolist[0].GetXaxis().GetXmin()
      xMax  = histolist[0].GetXaxis().GetXmax()
      nBins = histolist[0].GetXaxis().GetNbins()	
      if xTitle != "":
        xAxisTitle = xTitle
      else: 
        xAxisTitle = histolist[0].GetXaxis().GetTitle()  
   
   yTitle = "Events / %.2f" %((xMax-xMin)/nBins)
   # yTitle = "Events"

   if xAxisTitle.find("GeV") != -1:
      yTitle+=" GeV"
   elif xAxisTitle.find("rad") != -1:
      yTitle+=" rad"
   elif xAxisTitle.find("cm") != -1:
      yTitle+=" cm"

   canv = get_canvas()   
   canv.cd()


   # pad0 = TPad("pad0","pad0",0.,0.,0.99,1.)
   # pad0.SetBottomMargin(0.15)
   # pad0.SetTopMargin(0.08)
   # pad0.SetRightMargin(0.05)
   # pad0.Draw()
   # pad0.cd()
   pad0 = TPad("pad0","pad0",0.,0.1,0.99,1.)
   # pad0.SetBottomMargin(0.15)
   # pad0.SetTopMargin(0.08)
   # pad0.SetRightMargin(0.05)
   pad0.SetLeftMargin(0.1596424)
   pad0.SetRightMargin(0.03037618)
   pad0.SetTopMargin(0.07964258)
   pad0.SetBottomMargin(0.1451267)
   pad0.Draw()
   pad0.cd()
   
   if opts.doLog:
     pad0.SetLogy()   
   hs.Draw()
   hs.GetXaxis().SetTitle( xAxisTitle )
   hs.GetYaxis().SetTitle( yTitle )
   hs.GetXaxis().SetLabelSize(0.04)
   hs.GetYaxis().SetLabelSize(0.04)
   hs.GetYaxis().SetTitleOffset(1.2)
   hs.GetXaxis().SetTitleOffset(1.1)
   hs.SetMinimum(0.)
   # hsum.Draw("E2same")
   if data != "":
     if(h_data.GetMaximum()<hs.GetMaximum()):
       hs.SetMaximum(hs.GetMaximum()*1.2)
     else:
       hs.SetMaximum(h_data.GetMaximum()*1.2)  
   if data == "":
      hs.SetMaximum(hs.GetMaximum()*1.2)     
   if signal != "":
      h_signal.Draw("sameHIST")
   if data != "":
      h_data.Draw("samePE")

   l.Draw()
   
   canv.Update()
   canv.cd()
   
   if doratio or dopull:
      # pad1 = TPad("pad1","pad1",0.,0. ,0.99,0.24)
      # pad1.SetTopMargin(0.05)
      
      pad1 =  TPad("pad1","pad1",0.,0.,0.99,0.23) 
      
      pad1.SetLeftMargin(0.16)
      pad1.SetRightMargin(0.03)
      pad1.SetTopMargin(0.04)
      pad1.SetBottomMargin(0.37)
      
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
      # pad0.cd()
      #t = get_chi2(ph)
      #t.Draw("same")
                
   canv.Update()
   
   pad0.cd()
   CMS_lumi.CMS_lumi(pad0, 4, 0)	   
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
   if opts.write:
     name = prefix+"/h"+".root"
     f = TFile(name,"RECREATE");
     hs.Write()
     hsum.Write()
     
# data_yields = []
# if data != "":
#    print ""
#    print "================= Yields for data ================= "
#    h = TH1F(file_data.Get("AK8bjetPrunedMass"))
#    data_yields = print_yields(file_data,h,1.)
#
# yields = []
# errors = []
#
# if signal != "":
#    print ""
#    print "================= Yields for %s process ================= " %signalname
#    h = TH1F(file_signal.Get(histos[0]))
#    tmp = []
#    tmp = print_yields(file_signal,h,lumi)
#    yields.append(tmp[0])
#    errors.append(tmp[1])

# for f in range(0,len(filelist)):
#    print ""
#    print "================= Yields for %s process ================= " %bkgname[f]
#    h = TH1F(filelist[f].Get(histos[0]))
#    print filelist[f].GetName()
#    print h.Integral()*lumi
#    tmp = []
#    k = 1.
#    tmp = print_yields(filelist[f],h,lumi*k)
#    yields.append(tmp[0])
#    errors.append(tmp[1])
#
# S = 1.
# errS = 1.
# B = 1.
# errSum = 1.
# if signal != "":
#    S = yields[0]
#    errS = errors[0]
#    for b in range(1,len(yields)):
#       B+=yields[b]
#       errSum+=math.pow(errors[b],2)
# elif signal == "":
#    for b in range(0,len(yields)):
#       B+=yields[b]
#       errSum+=math.pow(errors[b],2)
#
# errB = math.sqrt(errSum)
# a = errS/math.sqrt(B)
# b = math.pow(B,-1.5)*errB/2.
# errSign = math.sqrt(a*a+b*b)
# sign = S/math.sqrt(B)
# print ""
# print "*********************************************"
# print "*********************************************"
#
# print "****************** TOT BACKGROUND = %.6f +/- %.6f" %(B,errB)
# if signal != "":
#    print "****************** SIGNIFICANCE = %.6f +/- %.6f" %(sign,errSign)
#
# if data != "":
#    print "****************** TOT DATA = %.6f +/- %.6f" %(data_yields[0],data_yields[1])
#
# print "*********************************************"
# print "*********************************************"

