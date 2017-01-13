from optparse import OptionParser
import sys
from ROOT import *
import time
import CMS_lumi, tdrstyle
import math



parser = OptionParser()
parser.add_option('-t','--time', action='store_true', dest='time', default=False, help='sleep')
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('-l','--log', action='store_true', dest='log', default=False, help='Draw log')
parser.add_option('-d', '--data',  action='store_true', dest='addData', default=False, help='Add data')
parser.add_option("-s", "--save", dest="save", default=False, action="store_true", help="save canvas")
parser.add_option("-1",'--cutMin', action="store",type="float",dest="cutMin",default=0.0, help="Min Tau21 cut")
parser.add_option("-2",'--cutMax', action="store",type="float",dest="cutMax",default=1.0, help="Max Tau21 cut")
parser.add_option("-c",'--csv', action="store",type="float",dest="csv",default=1.0, help="Max CSV")
parser.add_option('-v', '--var',action="store",type="string",dest="variable",default="Whadr_puppi_softdrop")
parser.add_option('--pMin',action="store",type="float",dest="prunedMin",default=0.0)
parser.add_option('--pMax',action="store",type="float",dest="prunedMax",default=500.0)
parser.add_option('--ttsample',action="store",type="string",dest="tt",default="powheg")
parser.add_option('--out',action="store",type="string",dest="outFile",default="")
parser.add_option('--lowMass',dest="lowMass", default=False, action="store_true", help="do low mass trigger plots")
(options, args) = parser.parse_args()
  
lumi =12900.
# path = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag/PRUNED/WWTree_"
# if options.variable.find("puppi_softdrop")!= -1:
path = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag_80X/WWTree_"
channel =["em","el","mu"]
channel =["em"]
samples =["TTbar_%s"%options.tt,"STop","WJets","VV"]

h = options.variable


xTitle = options.variable

if options.variable.find("MVV") != -1:
  xTitle = "M_{VV} (GeV)"
elif options.variable.find("pruned") != -1:
  xTitle = "Pruned mass (GeV)"
elif options.variable.find("csv") != -1:
  xTitle = "CSV"    
elif options.variable.find("tau21") != -1:
  xTitle = "#tau_{21}"     
elif options.variable.find("puppi_tau2tau1") != -1:
  xTitle = "PUPPI #tau_{21}"       
elif options.variable.find("nak4")!= -1: 
  xTitle = "Number of AK4 jets"     
elif options.variable.find("eta")!= -1:  
  xTitle = "#eta"     
elif options.variable.find("Whadr_pt")!= -1:  
  xTitle = "AK8 jet p_{T}"       
elif options.variable.find("Wlept_pt")!= -1:  
  xTitle = "Leptonic W p_{T}"       
elif options.variable.find("lept_pt")!= -1:  
  xTitle = "Lepton p_{T}"  
elif options.variable.find("phi")!= -1:  
  xTitle = "#phi"     
elif options.variable.find("MET")!= -1:  
  xTitle = "Missing E_{T} (GeV)"     
elif options.variable.find("nPV")!= -1:  
  xTitle = "Number of PVs"   
elif options.variable.find("puppi_softdrop")!= -1:  
  xTitle = "PUPPI softdrop mass" 
      
label = "80X Powheg+Pythia8"
if options.tt.find("madgraph")!=-1: label = "80X Madgraph+Pythia8"
if options.tt.find("herwig")!=-1: label = "80X Powheg+Herwig"
legends = ["t#bar{t} (%s)"%label,"Single top","W+jets","WW/WZ/ZZ","QCD"]
colors = [ 210,kCyan,kRed,kBlue,kGray]
rebin = 1
doFit = False
if options.addData: addData = True
else: addData = False


if options.noX:
  gROOT.SetBatch(True)
  

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "12.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
if addData: CMS_lumi.extraText = "Preliminary"
else: CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

def get_ratio(hdata,histsum,xAxisTitle):
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
   return ratio


var = options.variable

for ch in channel:
  hs  = THStack("hs", "hs")
  histolist = []

  legend = TLegend(0.4863032,0.666088,0.7345569,0.922371)
  legend.SetTextSize(0.038)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  
  
  
  
  if(h.find("pruned")!=-1): 
    hData = TH1F("hData","hData",22  ,40  ,150 )
  elif(h.find("softdrop")!=-1): 
    hData = TH1F("hData","hData",18  ,40  ,130 )
  elif(h.find("tau21")!=-1): 
    hData = TH1F("hData","hData",20  ,0  ,1 )
  elif(h.find("tau2tau1")!=-1): 
    hData = TH1F("hData","hData",20  ,0  ,1 )
  elif(h.find("csv")!= -1): 
    hData = TH1F("hData","hData",20  ,0.  ,1. )
  elif(h.find("nak4")!= -1): 
    hData = TH1F("hData","hData",10  ,0.  ,10. )
  elif(h.find("eta")!= -1): 
    hData = TH1F("hData","hData",30  ,-3.  ,3. )  
  elif(h.find("Whadr_pt")!= -1): 
    hData = TH1F("hData","hData",100  ,200.  ,1000. )   
  elif(h.find("Wlept_pt")!= -1): 
    hData = TH1F("hData","hData",60  ,200.  ,800. )  
  elif(h.find("lept_pt")!= -1): 
    if( ch.find("mu")!=-1): hData = TH1F("hData","hData",50  ,53.  ,600. )  
    if( ch.find("el")!=-1): hData = TH1F("hData","hData",50  ,120.  ,600. ) 
    if( ch.find("em")!=-1): hData = TH1F("hData","hData",50  ,53.  ,600. )  
  elif(h.find("phi")!= -1): 
    hData = TH1F("hData","hData",20  ,-4.  ,4. )  
  elif(h.find("MET")!= -1): 
    hData = TH1F("hData","hData",60  ,0.  ,600. )
  elif(h.find("nPV")!= -1): 
    hData = TH1F("hData","hData",30  ,0.  ,30 )
  else:
    hData = TH1F("hData","hData",1000  ,-20  ,20 )
    hData.SetCanExtend(TH1.kAllAxes)

  # if addData:
 
  fname = path + ch + "/ExoDiBosonAnalysis.WWTree_data.root"
  file = TFile.Open(fname,"READ")
  print "DATA INFILE NAME = " , file.GetName()
  intree = file.Get("tree")
  for i in range(intree.GetEntries()):
    intree.GetEntry(i)
    # wtagger = getattr(intree,"Whadr_tau21")
    wtagger = getattr(intree,"Whadr_puppi_tau2tau1")
    # if options.variable.find("puppi_softdrop")!= -1: wtagger = getattr(intree,"Whadr_puppi_tau2")/getattr(intree,"Whadr_puppi_tau1")
    # wtagger = getattr(intree,"Whadr_puppi_tau2")/getattr(intree,"Whadr_puppi_tau1")+ (0.063 * math.log( (pow( getattr(intree,"Whadr_puppi_softdrop"),2))/getattr(intree,"Whadr_puppi_pt") ))
    btag = getattr(intree,"Whadr_csv")
    if  wtagger < options.cutMin or wtagger > options.cutMax: continue
    # if  getattr(intree,"Whadr_pruned") < options.prunedMin or getattr(intree,"Whadr_pruned") > options.prunedMax: continue
    hData.Fill(getattr(intree,var))
  
  hData.Rebin(rebin)
  hData.SetLineColor(kBlack)
  hData.SetMarkerColor(kBlack)
  hData.SetMarkerStyle(20)
  hData.SetMarkerSize(1.)
  hData.GetXaxis().SetTitle(xTitle)
  hData.GetXaxis().SetRangeUser(hData.GetXaxis().GetXmin(), hData.GetXaxis().GetXmax())
  hData.SetBinErrorOption(TH1.kPoisson)
  
  nBins = hData.GetNbinsX()
  xMin  = hData.GetXaxis().GetXmin()
  xMax  = hData.GetXaxis().GetXmax()
  
  addI = ""
  if xTitle.find("GeV")!=-1:
    addI = " GeV"
  yTitle = "Events / (%.2f%s)" %((xMax-xMin)/nBins, addI)
  hData.GetYaxis().SetTitle(yTitle)
   
  ii = -1
  
  totalMinoInt = 0
  ttint = 0
  for sample in samples:
    ii +=1
    fname = path + ch + "/ExoDiBosonAnalysis.WWTree_" + sample + ".root"
    file = TFile.Open(fname,"READ")
    print "MC INFILE NAME = " , file.GetName()
    intree = file.Get("tree")
    hMC = TH1F('hMC%i'%ii,'hMC%i'%ii,nBins,xMin, xMax)
    hMC.SetDirectory(0)
    SF = 1.
    if sample.find("TTbar")!=-1:
      if sample.find("herwig")!=-1:
        if ch.find("mu")!=-1: SF = 0.816482930701 #with pT weight =  0.718971907738 without pT weight =  0.681615368304
        if ch.find("el")!=-1: SF = 0.740644295699
        if ch.find("em")!=-1: SF = 0.799614355386
      if sample.find("powheg")!=-1:
        if ch.find("mu")!=-1: SF = 0.605771131375 #with pT weight =  0.718971907738 without pT weight =  0.681615368304
        if ch.find("el")!=-1: SF = 0.630992928339
        if ch.find("em")!=-1: SF = 0.667028210351#0.0.667028210351-->NoQCD    0.626419229353-->WithQCD
      if sample.find("madgraph")!=-1:
        if ch.find("mu")!=-1: SF = 0.65770501173 #with pT weight =  0.65770501173 without pT weight =  0.623046247089
        if ch.find("el")!=-1: SF = 0.57113029968
        if ch.find("em")!=-1: SF = 0.637740710524  
    if sample.find("QCD")!=-1:
       SF = 0.903018  
                #
        # if sample.find("76")!=-1:
        #   if ch.find("mu")!=-1: SF = 0.855328938647
        #   if ch.find("el")!=-1: SF = .70
        #   if ch.find("em")!=-1: SF = .80
        # if sample.find("JECv7")!=-1:
        #   if ch.find("mu")!=-1: SF = 0.847471048651
        #   if ch.find("el")!=-1: SF = 0.741619909655
        #   if ch.find("em")!=-1: SF = 0.815850898898
        # if path.find("PUPPISD")!=-1:
        #   if ch.find("mu")!=-1: SF = 0.849319276836
        #   if ch.find("el")!=-1: SF = 0.679525964292
        #   if ch.find("em")!=-1: SF = 0.79999978873
        # if path.find("PUPPISD_newcorr")!=-1:
        #   if ch.find("mu")!=-1: SF = 0.813858092835
        #   if ch.find("el")!=-1: SF = 0.671829649264
        #   if ch.find("em")!=-1: SF = 0.773493094865
    print "Using scalefactor of " , SF
    for i in range(intree.GetEntries()):
      intree.GetEntry(i)
      wtagger = getattr(intree,"Whadr_puppi_tau2tau1")
      # wtagger = getattr(intree,"Whadr_puppi_tau2tau1")
      # wtagger = getattr(intree,"Whadr_puppi_tau2")/getattr(intree,"Whadr_puppi_tau1")+ (0.063 * math.log( (pow( getattr(intree,"Whadr_puppi_softdrop"),2))/getattr(intree,"Whadr_puppi_pt") ))
      if  wtagger < options.cutMin or wtagger > options.cutMax: continue
      # if  getattr(intree,"Whadr_pruned") < options.prunedMin or getattr(intree,"Whadr_pruned") > options.prunedMax: continue
      weight = getattr(intree,"weight")
      # hMC.Fill(getattr(intree,var),getattr(intree,"weight"))
      hMC.Fill(getattr(intree,var),weight)
    hMC.Scale(lumi*SF)
    hMC.SetFillColor(colors[ii])
    legend.AddEntry(hMC,legends[ii],"f")
    histolist.append(hMC)
    if sample.find("TTbar")!=-1: ttint = hMC.Integral()
    else: totalMinoInt += hMC.Integral() 

  
  hsum = TH1F("hsum","hsum1",nBins,xMin,xMax)
  for j in range(1,len(histolist)+1):
    hs.Add(histolist[len(histolist)-j],"HIST")
    hsum.Add(histolist[len(histolist)-j]) 
  hsum.SetFillColor(kBlack)
  hsum.SetFillStyle(3008)
  hsum.SetLineColor(kWhite)
  hsum.SetDirectory(0)
  scale = hData.Integral()-totalMinoInt
  print "DATA/MC" ,scale/ttint
  
         
  W = 600
  H = 700
  H_ref = 700 
  W_ref = 600 
  T = 0.08*H_ref
  B = 0.12*H_ref
  L = 0.12*W_ref
  R = 0.04*W_ref
  canv = TCanvas("canv","canv",W,H)
  canv.cd()
  
  if addData:
    legend.AddEntry(hData,"Data","Ple")
    canv.Divide(1,2,0,0,0)
    canv.cd(1)
    p11_1 = canv.GetPad(1)
    p11_1.SetPad(0.01,0.25,0.99,0.98)
    if options.log:
      p11_1.SetLogy()
    p11_1.SetRightMargin(0.05)
    p11_1.SetTopMargin(0.05)
    p11_1.SetFillColor(0)
    p11_1.SetBorderMode(0)
    p11_1.SetFrameFillStyle(0)
    p11_1.SetFrameBorderMode(0)


  addInfo = TPaveText(0.2020956,0.8252315,0.5,0.984375,"NDC")
  txt = "W#rightarrow#mu#nu"
  if ch.find("el")!=-1: txt = "W#rightarrowe#nu"
  if ch.find("em")!=-1: txt = "W#rightarrow#mu#nu + W#rightarrowe#nu"
  addInfo.AddText(txt)
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  max = hData.GetMaximum()*1.75
  if options.log: max = hData.GetMaximum()*25

  if addData: vFrame = p11_1.DrawFrame(hData.GetXaxis().GetXmin(),0.0001,hData.GetXaxis().GetXmax(),max)
  else      : vFrame = canv .DrawFrame(hData.GetXaxis().GetXmin(),0.0000001,hData.GetXaxis().GetXmax(),max)
  vFrame.SetTitle("")
  vFrame.SetXTitle(xTitle)
  vFrame.SetYTitle(yTitle)
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)
  
  # if addData: hData.Draw("EOsame")
  hs.Draw("same")
  # hsum.Draw("E2same")
  legend.Draw("same")
  if addData: 
    hData.Draw("EOsame")
    addInfo.Draw("same")
    p11_1.RedrawAxis()
    p11_1.Update()
    p11_1.GetFrame().Draw()
    p11_1.RedrawAxis()
    CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
  else: 
    # addInfo.Draw("same")
    vFrame.GetYaxis().SetNdivisions(504)
    vFrame.GetXaxis().SetNdivisions(504)
    canv.RedrawAxis()
    canv.Update()
    canv.GetFrame().Draw()
    CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  
  if addData:
    canv.cd(2)
    p11_2 = canv.GetPad(2)
    p11_2.SetPad(0.01,0.02,0.99,0.25)
    p11_2.SetBottomMargin(0.35)
    p11_2.SetRightMargin(0.05)
    p11_2.SetGridx()
    p11_2.SetGridy()
    vFrame2 = p11_2.DrawFrame(hData.GetXaxis().GetXmin(),0.2,hData.GetXaxis().GetXmax(),1.8)
    vFrame2.SetTitle("")
    vFrame2.SetXTitle(xTitle)
    vFrame2.GetXaxis().SetTitleSize(0.06)
    vFrame2.SetYTitle("#frac{Data}{MC}")
    vFrame2.GetYaxis().SetTitleSize(0.15)
    vFrame2.GetYaxis().SetTitleOffset(0.40)
    vFrame2.GetYaxis().SetLabelSize(0.09)
    vFrame2.GetXaxis().SetTitleSize(0.15)
    vFrame2.GetXaxis().SetTitleOffset(0.90)
    vFrame2.GetXaxis().SetLabelSize(0.12)
    vFrame2.GetYaxis().CenterTitle()
  

    rh = get_ratio(hData,hsum,xTitle)
    rh.SetDirectory(0)
    line = TLine(hData.GetXaxis().GetXmin(),1,hData.GetXaxis().GetXmax(),1)
    rh.Draw("same")
    line.Draw("same")
    vFrame2.GetYaxis().SetNdivisions(504)
    vFrame2.GetXaxis().SetNdivisions(504)
    p11_2.RedrawAxis()
    p11_1.RedrawAxis()
    
    if options.save:
      canvasname = "plots_wtagSF80X/%s_%s%s.pdf"%(h,options.tt,options.outFile)
      canv.Print(canvasname,"pdf")
      canv.SaveAs(canvasname.replace(".pdf",".root"),"root")
      
    
    if doFit and var.find("pruned")!=-1:
         
      W = 600
      H = 700
      H_ref = 700 
      W_ref = 600 
      T = 0.08*H_ref
      B = 0.12*H_ref
      L = 0.12*W_ref
      R = 0.04*W_ref
      canv2 = TCanvas("canv2","canv2",W,H)
      canv2.cd()
      hsum.Fit("gaus","S","SAME",70,100)
      f = hsum.GetFunction("gaus")
      
      
      addInfo = TPaveText(0.5455198,0.7217989,0.8034242,0.883234,"NDC")
      addInfo.AddText("Cut: %.2f < #tau_{21} <%.2f" %(options.cutMin,options.cutMax))
      addInfo.AddText("<m> = %.2f #pm %.2f GeV" % ( f.GetParameter("Mean") ,f.GetParError(1) ) )
      addInfo.AddText("  #sigma   = %.2f #pm %.2f GeV" %( f.GetParameter("Sigma"),f.GetParError(2) ) )
      addInfo.SetFillColor(0)
      addInfo.SetLineColor(0)
      addInfo.SetFillStyle(0)
      addInfo.SetBorderSize(0)
      addInfo.SetTextFont(42)
      addInfo.SetTextSize(0.040)
      addInfo.SetTextAlign(12)
      
      
      
      f.SetLineWidth(2)
      hsum.SetFillStyle(0)
      hsum.SetLineColor(kBlack)
      hsum.Sumw2()
      hsum.GetXaxis().SetTitle(xTitle)
      hsum.GetYaxis().SetTitle(yTitle)
      # hsum.GetXaxis().SetTitleSize(0.06)
      # hsum.GetYaxis().SetTitleSize(0.15)
      # hsum.GetYaxis().SetTitleOffset(0.40)
      # hsum.GetYaxis().SetLabelSize(0.09)
      # hsum.GetXaxis().SetTitleSize(0.15)
      # hsum.GetXaxis().SetTitleOffset(0.90)
      # hsum.GetXaxis().SetLabelSize(0.12)
      # hsum.GetYaxis().CenterTitle()
      hsum.Draw("EO")
      f.Draw("same")
      addInfo.Draw()
      canv2.Update()
      
      if options.save:
        canvasname = "plots_wtagSF80X/%s_%s%s.pdf"%(h,options.tt,options.outFile)
        canv2.Print(canvasname,"pdf")
        canv2.SaveAs(canvasname.replace(".pdf",".root"),"root")
        
         
  
    file.Close()
    del intree
    del hData
    del hMC
    del hsum
    del histolist
    del canv
     
  if options.time: 
    time.sleep(100)
    
  
  
