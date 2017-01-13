from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
import array


tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "36.4 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

W = 900
H = 700
H_ref = 700 
W_ref = 900 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

# gROOT.SetBatch(True)

def printPreSelections(do,x,y):
    text = "|#eta| < 2.5, p_\{T\} > 200 GeV"
    text2= 'M_\{jj\} > 1055 GeV, |#Delta #eta_\{jj\}| < 1.3'
    latex = TLatex()
    latex.SetTextSize(0.03);
    latex.SetTextAlign(12); 
    if do:
        latex.DrawLatex(x,y,text);
        latex.DrawLatex(x,y-y/200.,text2);

def print_yields(f,k):

   nEvents_ = (TH1F(f.Get("nEvents"))).GetBinContent(1);
   
   if nEvents_ == 0:
      print "No events found!"

   error1 = 0
   
   if nEvents_ != 0:      
      nPassedTrigger_	       = (TH1F(f.Get("nPassedTrigger"))).GetBinContent(1)
      nPassedFilters_      = (TH1F(f.Get("nPassedFilter"))).GetBinContent(1)
      nPassedFoundJets_         = (TH1F(f.Get("nPassedFoundJets"))).GetBinContent(1)
      nPassedMjj_           = (TH1F(f.Get("nPassedMjj"))).GetBinContent(1)
      nPassedJetsDEta_         = (TH1F(f.Get("nPassedJetsDEta"))).GetBinContent(1)
      nPassedJetPrunedMass_         = (TH1F(f.Get("nPassedPrunedJetMass"))).GetBinContent(1)
      nPassedTau21Cut_       = (TH1F(f.Get("nPassedTau21Cut"))).GetBinContent(1)



      print "############ Cut flow: ############"      
      print "number of events					    %.0f" %nEvents_ 
      print "passed trigger					    %.0f --- eff = %.4f" %(nPassedTrigger_,nPassedTrigger_/nEvents_)  
      print "passed filters					    %.0f --- eff = %.4f" %(nPassedFilters_,nPassedFilters_/nEvents_)  
      print "found 2 jets 					    %.0f --- eff = %.4f" %(nPassedFoundJets_,nPassedFoundJets_/nEvents_) 
      print "passed Mjj  					    %.0f --- eff = %.4f" %(nPassedMjj_,nPassedMjj_/nEvents_) 
      print "passed dEta 		                                    %.0f --- eff = %.4f" %(nPassedJetsDEta_,nPassedJetsDEta_/nEvents_)
      print "passed pruend mass cut	    %.0f --- eff = %.4f" %(nPassedJetPrunedMass_,nPassedJetPrunedMass_/nEvents_) 
      print "passed tau21 cut				    %.0f --- eff = %.4f" %(nPassedTau21Cut_,nPassedTau21Cut_/nEvents_) 
      print "passed pruned mass /passed dEta 			    %.0f --- eff = %.4f" %(nPassedJetPrunedMass_,nPassedJetPrunedMass_/nPassedJetsDEta_)
      print "passed tau21 /passed dEta				    %.0f --- eff = %.4f" %(nPassedTau21Cut_,nPassedTau21Cut_/nPassedJetsDEta_) 
      print "passed pruned mass /passed Mjj			    %.0f --- eff = %.4f" %(nPassedJetPrunedMass_,nPassedJetPrunedMass_/nPassedMjj_)
      print "passed Tau21 /passed Mjj				    %.0f --- eff = %.4f" %(nPassedTau21Cut_,nPassedTau21Cut_/nPassedMjj_)

      # error1 = TMath.Sqrt(nPassedJetMass_)/nPassedJetMass_;
     #
     #  err = h.Integral()*k*error1
     #  y = h.Integral()*k
      err = 1
      y = 1
      print "Final yields: %.2f +/- %.2f" %(y,err)
   
      return [y,err]

def get_canvas():

   

   canvas = TCanvas("c2","c2",W,H)
   # canvas.SetFillColor(0)
   # canvas.SetBorderMode(0)
   # canvas.SetFrameFillStyle(0)
   # canvas.SetFrameBorderMode(0)
   # canvas.SetLeftMargin( L/W )
   # canvas.SetRightMargin( R/W )
   # canvas.SetTopMargin( T/H )
   # canvas.SetBottomMargin( B/H )
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
   ratio.SetMarkerColor(kBlack)
   ratio.SetMarkerStyle(20)
   ratio.SetMarkerSize(1.)
   ratio.SetMinimum(0.1)
   ratio.SetMaximum(1.9)
   ratio.GetYaxis().SetTitle("#frac{Data}{MC}")
   ratio.GetYaxis().SetNdivisions(504)
   ratio.GetYaxis().SetLabelSize(0.09)
   ratio.GetXaxis().SetLabelSize(0.12)
   ratio.GetYaxis().SetTitleSize(0.15)
   ratio.GetYaxis().SetTitleOffset(0.4)
   ratio.GetYaxis().CenterTitle()
   
   ratio.SetTitle("")
   ratio.SetXTitle(xAxisTitle)
   ratio.GetXaxis().SetTitleSize(0.06)
   ratio.GetXaxis().SetTitleSize(0.15)
   ratio.GetXaxis().SetTitleOffset(0.90)

   
   
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
parser.add_option("-R", "--ratio", dest="ratio", default=True, action="store_true",
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
parser.add_option("-q", "--QCDonly", dest="QCDonly", default=False, action="store_true",
                              help="plot QCD background histos for different generators")

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
sfqcd = config.getfloat('StackPlots','sfqcd')
rebin = config.getint('StackPlots','rebin')
ttbarunc = config.getfloat('StackPlots','ttbarunc')
doratio = opts.ratio
dopull = opts.pull
dolog  = opts.doLog
dosave = opts.save
dowrite = opts.write
dotime  = opts.time
doQCDonly = opts.QCDonly

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

fillStyle = [3018  , 3002,1001  ,1001,1001,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
fillColor = [1,kGray,kRed, kGreen+1,kCyan+1,kAzure+2,4,kPink-7,8,9]
fillColor = [1,kGray,kGreen+1,kRed,kAzure+2,kGreen+2,kBlack,kBlack,kBlack,kBlack]
lineWidth = [2     ,2     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2,2]
lineStyle = [1,1,1,1,1,1,1,1,1]
lineColor = [kBlack,kRed,kRed,kBlue,kBlue,kMagenta,kBlack,kBlack,kBlack,kBlack]
lineColor = [kBlack,kRed+1,kAzure+2,kGreen+2,kBlack,kBlack,kBlack,kBlack]
lineColor = [kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack,kBlack]
MarkerStyle = [23,25,26,6,7,9,10]
legendStyle = ['f','F','F','F','F','F','F','F','F','F'] 
if doQCDonly:
    lineColor = [kRed,kBlue,kCyan,kGreen,kBlack,kBlack,kBlack,kBlack]
    legendStyle = ['l','l','l','F','F','F','F','F','F','F'] 


dataevents  = 0      
for h in histos:
    
   sysunc = []
   statunc = []
   
   l = TLegend(0.6472401,0.6640212,0.8561156,0.932705,"","NDC")
   l.SetTextSize(0.038)
   l.SetLineColor(0)
   l.SetShadowColor(0)
   l.SetLineStyle(1)
   l.SetLineWidth(1)
   l.SetFillColor(0)
   l.SetFillStyle(0)
   l.SetMargin(0.35)
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
      l.AddEntry(h_data,"CMS Data","Ple")
      print "title %s" %(h_data.GetXaxis().GetTitle())
   
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
   hsum1 = TH1F("hsum1","hsum1",histolist[0].GetNbinsX()/rebin,histolist[0].GetXaxis().GetXmin(),histolist[0].GetXaxis().GetXmax())
   

   for j in range(0,len(histolist)):
      histolist[j].Scale(lumi)
      print lumi
      histolist[j].Rebin(rebin) 
      histolist[j].SetLineColor(lineColor[j+1])
      histolist[j].SetLineWidth(lineWidth[j+1])
      histolist[j].SetLineStyle(lineStyle[j+1])
      histolist[j].SetFillStyle(fillStyle[j+1])
      if doQCDonly==False:
        histolist[j].SetFillColor(fillColor[j+1])
      l.AddEntry(histolist[j],bkgname[j],legendStyle[j+1]) 
      hsum1.Add(histolist[j])
   # print 'integrating from %f to %f' %(hsum.GetBinCenter(5),hsum.GetBinCenter(6))
   # print "Non b = %f percent" %( (hsum.Integral(0,5)+hsum.Integral(7,25) )/hsum.Integral() )
   # print "b = %f percent" %(hsum.GetBinContent(6)/hsum.Integral() )
   # l.AddEntry(hsum,"MC Stat","F")
   
   # if sfqcd != 1.:
     # print "DATA/MC scalefactor = %f +- SEE ELSEWEHERE" %(sfqcd)
     # histolist[0].Scale(sfqcd)
   if data != "":  
     print "MC = %i" %hsum1.Integral()
     print "DATA = %i" %h_data.Integral()
     diff = h_data.Integral()-hsum1.Integral()
     # sf = diff/histolist[0].Integral()+1
     sf = h_data.Integral()/hsum1.Integral()
     error = sf*math.sqrt( (1./h_data.Integral()) + (1./hsum1.Integral()) )   
     print "DATA/MC scalefactor = %f +- %f" %(sf,error)
     if doQCDonly==True:
         for  i in range(0,len(histolist)):
             print  "MC = %i" %histolist[i].Integral()
             sf = h_data.Integral()/histolist[i].Integral()
             histolist[i].Scale(sf)
             error = sf*math.sqrt( (1./h_data.Integral()) + (1./histolist[i].Integral()) )   
             print  "DATA/MC scalefactor = %f +- %f" %(sf,error)
     else:
         histolist[0].Scale(sf)
     
     # diff = 1/histolist[0].Integral()*(dataevents-hsum.Integral()+histolist[0].Integral())
     # print "SF (ttbar) = %f" %diff
   
                
   for j in range(1,len(histolist)+1):   
      hs.Add( histolist[len(histolist)-j],"HIST")
      hsum.Add(histolist[len(histolist)-j])
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
      xAxisTitle = histolist[0].GetXaxis().GetTitle()
      if xAxisTitle =='':
          if h.find("Pt")!=-1:
              xAxisTitle = "p_T (GeV)"
          if h.find("Eta")!=-1:
              xAxisTitle = "#eta"
          #xAxisTitle = h
      print "xAxisTitle %s"%(xAxisTitle)
   
   yTitle = "Events / %.2f" %((xMax-xMin)/nBins)
   # yTitle = "Events"

   if xAxisTitle.find("GeV") != -1:
      yTitle+=" GeV"
   elif xAxisTitle.find("rad") != -1:
      yTitle+=" rad"
   elif xAxisTitle.find("cm") != -1:
      yTitle+=" cm"

   canv = TCanvas("c2","c2",W,H)
   canv.SetTickx()
   canv.SetTicky()  
   canv.GetWindowHeight()
   canv.GetWindowWidth()
   canv.Divide(1,2,0,0,0)
   canv.cd(1)
   
   p11_1 = canv.GetPad(1)
   p11_1.SetPad(0.01,0.26,0.99,0.98)
   p11_1.SetRightMargin(0.05)
   p11_1.SetTopMargin(0.05)
   p11_1.SetBottomMargin(0.025)
   p11_1.SetFillColor(0)
   p11_1.SetBorderMode(0)
   p11_1.SetFrameFillStyle(0)
   p11_1.SetFrameBorderMode(0)
   
   addInfo = TPaveText(0.1901109,0.6999256,0.4589097,0.7466683,"NDC")
  
   # addInfo.AddText("AK8CHSPF jets")
   addInfo.AddText("65 GeV < M_{P} < 105 GeV")
   # addInfo.AddText("|#eta| < 2.4, p_{T} > 200 GeV")
   # addInfo.AddText("M_{jj} > 1 TeV, |#Delta#eta_{jj}| < 1.3")
   addInfo.SetFillColor(0)
   addInfo.SetLineColor(0)
   addInfo.SetFillStyle(0)
   addInfo.SetBorderSize(0)
   addInfo.SetTextFont(42)
   addInfo.SetTextSize(0.040)
   addInfo.SetTextAlign(12)

   if dolog:
     p11_1.SetLogy()
     ymax = histolist[0].GetMaximum()*50 
   else:
     ymax = h_data.GetMaximum()*1.6 
   vFrame = p11_1.DrawFrame(histolist[0].GetXaxis().GetXmin(),0.05,histolist[0].GetXaxis().GetXmax(),ymax)  
   vFrame.SetTitle("")
   vFrame.SetXTitle(xAxisTitle)
   vFrame.SetYTitle(yTitle)
   vFrame.GetXaxis().SetTitleSize(0.06)
   vFrame.GetXaxis().SetTitleOffset(0.95)
   vFrame.GetXaxis().SetLabelSize(0.05)
   vFrame.GetYaxis().SetTitleSize(0.06)
   #vFrame.GetYaxis().SetTitleOffset(1.0)
   vFrame.GetYaxis().SetLabelSize(0.05)
   
   if doQCDonly==False:
    hs.Draw()
    hs.GetXaxis().SetTitle( xAxisTitle )
    hs.GetYaxis().SetTitle( yTitle )
    hs.GetXaxis().SetLabelSize(0.04)
    hs.GetYaxis().SetLabelSize(0.04)
    hs.GetYaxis().SetTitleOffset(1.2)
    hs.GetXaxis().SetTitleOffset(1.1)
   else:
       for i in range(0,len(histolist)):
           print " test "
           if i==0:
                histolist[i].Draw("HIST")
           else:
               histolist[i].Draw("sameHIST")
           #histolist[i].GetXaxis().SetTitle( xAxisTitle )
           #histolist[i].GetYaxis().SetTitle( yTitle )
           #histolist[i].GetXaxis().SetLabelSize(0.04)
           #histolist[i].GetYaxis().SetLabelSize(0.04)
           #histolist[i].GetYaxis().SetTitleOffset(1.2)
           #histolist[i].GetXaxis().SetTitleOffset(1.1)
           
   # hsum.Draw("E2same")
   if data != "":
     if doQCDonly==False:  
        if(h_data.GetMaximum()<hs.GetMaximum()):
            hs.SetMaximum(ymax)
            hs.SetMinimum(0.01)
            h_data.SetMinimum(0.01)
        else:
            hs.SetMaximum(ymax)
     else:
        if(h_data.GetMaximum()<histolist[0].GetMaximum()):
            histolist[0].SetMaximum(ymax)
            histolist[0].SetMinimum(0.01)
            h_data.SetMinimum(0.01)
        else:
            histolist[0].SetMaximum(ymax) 
   if data == "":
      hs.SetMaximum(ymax)   
   if signal != "":
      h_signal.Draw("sameHIST")
   if data != "":
      h_data.Draw("samePE")

   l.Draw("same")
   xmax = h_data.GetXaxis().GetXmax()
   x = xmax-xmax/3.
   y = ymax/2.
   if dolog:
       y = ymax/200.
   printPreSelections(1,x,y)
   # addInfo.Draw("same")
   p11_1.RedrawAxis()
   p11_1.Update()
   p11_1.GetFrame().Draw()
   CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
   canv.Update()
   
   if doratio or dopull:
      # pad1 = TPad("pad1","pad1",0.,0. ,0.99,0.24)
      # pad1.SetTopMargin(0.05)
      
      canv.cd(2)
      p11_2 = canv.GetPad(2)
      p11_2.SetPad(0.01,0.02,0.99,0.28)
      p11_2.SetBottomMargin(0.35)
      p11_2.SetRightMargin(0.05)
      p11_2.SetGridx()
      p11_2.SetGridy()
   
   if doratio:
      vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(), 0.0, p11_1.GetUxmax(), 2.0)
      # vFrame2 = p11_2.DrawFrame(fFitXmin,-3.5,fFitXmax,3.5)
      vFrame2.SetTitle("")
      vFrame2.SetXTitle(xAxisTitle)
      vFrame2.GetXaxis().SetTitleSize(0.06)
      vFrame2.SetYTitle("#frac{Data}{MC}")
      vFrame2.GetYaxis().SetTitleSize(0.15)
      vFrame2.GetYaxis().SetTitleOffset(0.40)
      vFrame2.GetYaxis().SetLabelSize(0.09)
      vFrame2.GetXaxis().SetTitleSize(0.15)
      vFrame2.GetXaxis().SetTitleOffset(0.90)
      vFrame2.GetXaxis().SetLabelSize(0.12)
      vFrame2.GetXaxis().SetNdivisions(4)
      if doQCDonly==False:
            rh = get_ratio(h_data,hsum)
            rh.Draw()
            li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),1,1)
            li.Draw()
            rh.Draw("same")
      else:
          rh = []
          for i in range(0,len(histolist)):
            rh.append(get_ratio(h_data,histolist[i]))
            rh[i].SetLineColor(lineColor[i+1])
            rh[i].SetMarkerColor(lineColor[i+1])
            rh[i].SetMarkerStyle(MarkerStyle[i])
            #rh.Draw()
            if i==0:
                rh[i].Draw()
            else:
                rh[i].Draw("same")
      li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),1,1)
      li.Draw("same")
      p11_2.RedrawAxis()
      canv.Update()
      

   if dopull:
     vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(), 0., p11_1.GetUxmax(), 2.1)
     # vFrame2 = p11_2.DrawFrame(fFitXmin,-3.5,fFitXmax,3.5)
     vFrame2.SetTitle("")
     vFrame2.SetXTitle(xAxisTitle)
     vFrame2.GetXaxis().SetTitleSize(0.06)
     vFrame2.SetYTitle("#frac{Data-MC}{#sigma}")
     vFrame2.GetYaxis().SetTitleSize(0.15)
     vFrame2.GetYaxis().SetTitleOffset(0.40)
     vFrame2.GetYaxis().SetLabelSize(0.09)
     vFrame2.GetXaxis().SetTitleSize(0.15)
     vFrame2.GetXaxis().SetTitleOffset(0.90)
     vFrame2.GetXaxis().SetLabelSize(0.12)
     ph = get_pull(h_data,hsum)
     ph.Draw()
     li = get_line(h_data.GetXaxis().GetXmin(),h_data.GetXaxis().GetXmax(),0,1)
     li.Draw()
     ph.Draw("same")
     p11_2.RedrawAxis()
                
   canv.Update()
   
   # pad0.cd()
   # CMS_lumi.CMS_lumi(pad0, 4, 0)  
   p11_1.cd()
   p11_1.Update()
   p11_1.RedrawAxis()
   frame = p11_1.GetFrame()
   frame.Draw()   
   canv.cd()
   canv.Update()
   time.sleep(10)
   
   if dosave: 
      canvasname = "plots80X/"+h+"_herwig.pdf"
      canv.Print(canvasname,"pdf")
      canv.Print(canvasname.replace("pdf","root"),"root")
      canvasname = "/mnt/t3nfs01/data01/shome/dschafer/AnalysisOutput/figures/controlplots/"+h+"_herwig.pdf"
      canv.Print(canvasname,"pdf")
      canv.Print(canvasname.replace("pdf","root"),"root")

   if dowrite:
     canvasname = h+".root"
     f = TFile(canvasname,"RECREATE")
     canv.Write()
   time.sleep(dotime)  
# data_yields = []
# if data != "":
#    print ""
#    print "================= Yields for data ================= "
#    data_yields = print_yields(file_data,1.)
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

