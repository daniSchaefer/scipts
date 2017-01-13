from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
import array

gStyle.SetGridColor(kGray)
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTopMargin(0.07)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.14)
gStyle.SetPadRightMargin(0.06)
gROOT.ForceStyle()

def print_yields(f,h,k):

   nEvents_ = ( TH1F(f.Get("nEvents"))).GetBinContent(1);
   
   if nEvents_ == 0:
      print "No events found!"

   error1 = 0
   
   if nEvents_ != 0:      
      nPassedTrigger_	      = ( TH1F(f.Get("nPassedTrigger"))).GetBinContent(1)
      nPassedFoundJets_       = ( TH1F(f.Get("nPassedFoundJets"))).GetBinContent(1)
      nPassedJetsDEta_        = ( TH1F(f.Get("nPassedJetsDEta"))).GetBinContent(1)
      nPassedMjj_             = ( TH1F(f.Get("nPassedMjj"))).GetBinContent(1)
      nPassedTau21Cut_        = ( TH1F(f.Get("nPassedTau21Cut"))).GetBinContent(1)
      nPassedPrunedJetMass_   = ( TH1F(f.Get("nPassedPrunedJetMass"))).GetBinContent(1)
    

      print "############ Cut flow: ############"      
      print "number of events					    %.0f" %nEvents_ 
      print "passed trigger					    %.0f --- eff = %.4f" %(nPassedTrigger_,nPassedTrigger_/nEvents_)  
      

      error1 =  TMath.Sqrt(nPassedPrunedJetMass_)/nPassedPrunedJetMass_;

      err = h.Integral()*k*error1
      y = h.Integral()*k
      print "Final yields: %.2f +/- %.2f" %(y,err)
   
      return [y,err]


def get_ratio(hdata,histsum):

   ratio =  TH1F("ratio","ratio",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         r = hdata.GetBinContent(b)/nbkg
         ratio.SetBinContent(b,r)
         err = r* TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b)/(ndata*ndata) + histsum.GetBinError(b)*histsum.GetBinError(b)/(nbkg*nbkg) )
         ratio.SetBinError(b,err)   
    
   ratio.SetLineColor( TColor.kBlack)      
   ratio.SetLineColor( TColor.kBlack)
   ratio.SetMarkerColor( TColor.kBlack)
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
   
   pull =  TH1F("pull","pull",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
   for b in xrange(1,hdata.GetNbinsX()+1):
      nbkg = histsum.GetBinContent(b)
      ndata = hdata.GetBinContent(b)
      if nbkg != 0 and ndata != 0:
         err =  TMath.Sqrt( hdata.GetBinError(b)*hdata.GetBinError(b) + histsum.GetBinError(b)*histsum.GetBinError(b) )
         p = (hdata.GetBinContent(b)-nbkg)/err
         pull.SetBinContent(b,p)
         pull.SetBinError(b,1) 
	 #print "bin %i center %.2f pull %.2f" %(b,hdata.GetBinCenter(b),p)  
    
   pull.SetLineColor( TColor.kBlack)      
   pull.SetLineColor( TColor.kBlack)
   pull.SetMarkerColor( TColor.kBlack)
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

   pt =  TPaveText(0.71,0.34,0.92,0.51,"NDC")
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

   line =  TLine(xmin,y,xmax,y)
   line.SetLineColor( TColor.kRed)
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
parser.add_option("-n", "--norm", dest="norm", default=False, action="store_true",
                              help="normalize histos")                              
parser.add_option("-t", "--time", dest="time", default=10, action="store", type="float",
                              help="time sleep")
parser.add_option("-l", "--logy", dest="logy", default=False, action="store_true",
                              help="draw log y")
                              			      			      			      			      
(opts, args) = parser.parse_args(argv)
print opts.config

config = ConfigParser.ConfigParser()
config.read(opts.config)

prefix = config.get('StackPlots','prefix')
files = eval(config.get('StackPlots','filelist'))
lumi = config.getfloat('StackPlots','lumi')
data = config.get('StackPlots','data')
bkg = config.get('StackPlots','background')
histos = eval(config.get('StackPlots','histos'))
signame = eval(config.get('StackPlots','signame'))
bkgname = config.get('StackPlots','bkgname')
scalesignal = config.getfloat('StackPlots','scalesignal')
sfwjets = config.getfloat('StackPlots','sfwjets')
rebin = config.getint('StackPlots','rebin')
ttbarunc = config.getfloat('StackPlots','ttbarunc')
doratio = opts.ratio
dopull = opts.pull

print "------------------------------------"
print "Lumi = %.1f" %lumi
print "------------------------------------"
print "Input files directory: %s" %prefix
print "------------------------------------"
print "data file : %s" %data
print "background file : %s" %bkg
print "signal : "
print files  
print "------------------------------------"
print "Histos : "
print histos

filelist = []

for f in files:
   filename = prefix + "/" + f
   filetmp =  TFile.Open(filename,"READ") 
   filelist.append(filetmp)
      
if bkg != "":
   file_bkg =  TFile.Open(prefix+"/"+bkg,"READ")

if data != "":
   file_data =  TFile.Open(prefix+"/"+data,"READ")

fillStyle = [3018  ,1001  ,1001     ,1001   ,1001 ,1001    ]
fillColor = [1,2,210,4, TColor.kCyan, TColor.kAzure+8, TColor.kPink-7]
lineWidth = [3     ,3     ,2        ,2      ,2    ,2       , 2,2,2,2,2,2]
# lineStyle = [2,1,1,1,1,1,1]
lineStyle = [2,3,2,2,1,1,1,1,1,1,1]
lineColor = [ TColor.kGreen+2, TColor.kRed, TColor.kBlack, TColor.kBlue, TColor.kMagenta, TColor.kBlack, TColor.kBlack, TColor.kAzure, TColor.kOrange]
# lineColor = [ TColor.kBlack, TColor.kBlack, TColor.kBlack, TColor.kBlack, TColor.kBlack, TColor.kBlack, TColor.kBlack]
# legendStyle = ['F','F','F','F','F','F','F']   
legendStyle = ['l','l','l','l','l','l','l','l','l','l','l','l']
for h in histos:
    
   sysunc = []
   statunc = []
   
   l = TLegend(.18,.72,.38,.9)
   l.SetBorderSize(0)
   l.SetFillColor(0)
   l.SetFillStyle(0)
   l.SetTextFont(42)
   l.SetTextSize(0.021)
             
   if data != "":  
      h_data =  TH1F(file_data.Get(h)) 
      h_data.Rebin(rebin)   
      h_data.SetLineColor( TColor.kBlack)
      h_data.SetLineColor( TColor.kBlack);
      h_data.SetMarkerColor( TColor.kBlack);
      h_data.SetMarkerStyle(20);
      h_data.SetMarkerSize(1.);
      l.AddEntry(h_data,"CMS Data","LEP")
   
   if bkg != "":
      h_QCD =  TH1F(file_bkg.Get(h))
      h_QCD.SetLineColor(lineColor[0])
      h_QCD.SetLineWidth(lineWidth[0])
      h_QCD.SetLineStyle(lineStyle[0])
      # h_QCD.SetFillStyle(fillStyle[0])
      # h_QCD.SetFillColor(fillColor[0])
      h_QCD.Scale(lumi)
      # h_QCD.Scale(1./h_QCD.Integral())
      h_QCD.Rebin(rebin)
      l.AddEntry(h_QCD,bkgname,legendStyle[0])
   
   histolist = []
   hs =  THStack("hs", h)
   
   for f in xrange(0,len(filelist)):
      histolist.append( TH1F(filelist[f].Get(h)))
         
   for j in range(0,len(histolist)):  
      histolist[j].Scale(scalesignal*lumi)
      # histolist[j].Scale(1./histolist[j].Integral())
      histolist[j].Rebin(rebin) 
      histolist[j].SetLineColor(lineColor[j+1])
      histolist[j].SetLineWidth(lineWidth[j+1])
      histolist[j].SetLineStyle(lineStyle[j+1])
      l.AddEntry(histolist[j],signame[j],legendStyle[j+1])
      xMin  = h_QCD.GetXaxis().GetXmin()
      xMax  = h_QCD.GetXaxis().GetXmax()
      nBins = h_QCD.GetXaxis().GetNbins()
      xAxisTitle = h_QCD.GetXaxis().GetTitle()
   
   print (xMax-xMin)
   print nBins
   yTitle = "Events / %.02f" %((xMax-xMin)/nBins)
   
   
   if xAxisTitle.find("GeV") != -1:
      yTitle+=" GeV"
   elif xAxisTitle.find("rad") != -1:
      yTitle+=" rad"
   elif xAxisTitle.find("cm") != -1:
      yTitle+=" cm"
   elif xAxisTitle.find("") != -1:
      yTitle+=" "
   # yTitle = "A.U"
   tdrstyle.setTDRStyle()   
   canv = TCanvas("c", "",800,800)
   canv.cd()

   pad0 =  TPad("pad0","pad0",0.,0.,0.99,1.)
   pad0.SetBottomMargin(0.15)
   pad0.SetTopMargin(0.08)
   pad0.SetRightMargin(0.05)
   pad0.Draw()
   pad0.cd()
   
   h_QCD.Draw("hist")
   h_QCD.GetXaxis().SetTitle("|#Delta#eta_{jj}|" )
   h_QCD.GetYaxis().SetTitle( yTitle )
   h_QCD.GetXaxis().SetLabelSize(0.04)
   h_QCD.GetYaxis().SetLabelSize(0.04)
   h_QCD.GetYaxis().SetTitleOffset(1.9)
   h_QCD.GetXaxis().SetTitleOffset(1.2)
   
   for j in range(0,len(histolist)):
     histolist[j].Draw("HISTsame")
     hs = histolist[0]

   # h_QCD.GetXaxis().SetRangeUser(-2.5,2.5)
   # if data != "":
  #     hs.SetMaximum(h_data.GetMaximum()+10)
  #  if data == "":
  #     hs.SetMaximum(histolist[0].GetMaximum()+120)
   if bkg != "":
      # h_QCD.Smooth(1,"")
      h_QCD.Draw("histsame")
      h_QCD.SetMaximum(h_QCD.GetMaximum()*4.5)
  #  if data != "":
  #     h_data.Draw("samePE")

   l.Draw()
   
   l1 = TLatex()
   l1.SetNDC()
   l1.SetTextAlign(12)
   l1.SetTextFont(42)
   l1.SetTextSize(0.025)
  
   l1.DrawLatex(0.62,0.85, "p_{T} > 200 GeV, |#eta| < 2.4")
   # l1.DrawLatex(0.62,0.81, "|#Delta#eta_{jj}| < 1.3, M_{jj} > 1040 GeV")#, M_{jj} > 1040 GeV
   # l1.DrawLatex(0.62,0.77, "60 GeV < M_{p} < 100 GeV, #tau_{21}<0.5")
   l1.DrawLatex(0.62,0.81, "M_{jj} > 1040 GeV")
   
   canv.Update()
   canv.cd()
   
   if doratio or dopull:
      pad1 =  TPad("pad1","pad1",0.,0. ,0.99,0.24) 
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
   if opts.logy:
      pad0.SetLogy()
   CMS_lumi.CMS_lumi(pad0, 4, 0)
   pad0.cd()
   pad0.Update()
   pad0.RedrawAxis()
   frame = pad0.GetFrame()
   frame.Draw()   
   canv.cd()
   canv.Update()


   if opts.save: 
      canvasname = "/shome/thaarres/EXOVVAnalysisRunII/EANote/notes/AN-15-037/trunk/figures/dijetchannel/"+h+".png"
      canv.Print(canvasname,"png")

   time.sleep(opts.time)