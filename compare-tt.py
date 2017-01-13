from optparse import OptionParser
import sys
from ROOT import *
import time
import CMS_lumi, tdrstyle



parser = OptionParser()
parser.add_option('-t','--time', action='store_true', dest='time', default=False, help='sleep')
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--norm', action='store_true', dest='normalize', default=False, help='Normalize')
parser.add_option('-l','--log', action='store_true', dest='log', default=False, help='Draw log')
parser.add_option('-d', '--data',  action='store_true', dest='addData', default=False, help='Add data')
parser.add_option("-s", "--save", dest="save", default=False, action="store_true", help="save canvas")
parser.add_option("-1",'--cutMin', action="store",type="float",dest="cutMin",default=0.0, help="Min Tau21 cut")
parser.add_option("-2",'--cutMax', action="store",type="float",dest="cutMax",default=1.0, help="Max Tau21 cut")
parser.add_option("-c",'--csv', action="store",type="float",dest="csv",default=1.0, help="Max CSV")
parser.add_option('-v', '--var',action="store",type="string",dest="variable",default="Whadr_pruned")
parser.add_option('--pMin',action="store",type="float",dest="prunedMin",default=0.0)
parser.add_option('--pMax',action="store",type="float",dest="prunedMax",default=500.0)
parser.add_option('--realW',  action='store_true', dest='realW', default=False, help='Is real W')
parser.add_option('--fakeW',  action='store_true', dest='fakeW', default=False, help='Is fake W')


(options, args) = parser.parse_args()


lumi = 2200
path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Wtag/PRUNED/WWTree_"
channel =["mu"]
samples =["TTbar_herwig_76X","TTbar_madgraph_76X","TTbar_powheg_76X"]

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
elif options.variable.find("jec") != -1:
  xTitle = "Pruned JEC"   
     
legends = ["t#bar{t} MC (Powheg+Herwig)","t#bar{t} MC (MadGraph+Pythia8)","t#bar{t} MC (Powheg+Pythia8)"]
colors = [ kRed,kBlue,210]
rebin = 1
doFit = False
if options.addData: addData = True
else: addData = False


if options.noX:
  gROOT.SetBatch(True)
  

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "2.2 fb^{-1}"
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
  
  
  legend = TLegend(0.3993289,0.6919643,0.8271812,0.9360119)
  legend.SetTextSize(0.033)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  # legend.SetMargin(0.35)
  
  
  
  
  if(h.find("pruned")!=-1): 
    hData = TH1F("hData","hData",36  ,20  ,200 )
  elif(h.find("tau21")!=-1): 
    hData = TH1F("hData","hData",20  ,0  ,1 )
  elif(h.find("csv")!= -1): 
    hData = TH1F("hData","hData",20  ,0.  ,1. )
  elif(h.find("nak4")!= -1): 
    hData = TH1F("hData","hData",10  ,0.  ,10. )
  elif(h.find("eta")!= -1): 
    hData = TH1F("hData","hData",30  ,-3.  ,3. )  
  elif(h.find("Whadr_pt")!= -1): 
    hData = TH1F("hData","hData",100  ,200.  ,1000. )   
  elif(h.find("lept_pt")!= -1): 
    hData = TH1F("hData","hData",100  ,0.  ,600. ) 
  elif(h.find("phi")!= -1): 
    hData = TH1F("hData","hData",20  ,-4.  ,4. )  
  elif(h.find("MET")!= -1): 
    hData = TH1F("hData","hData",100  ,0.  ,800. )  
  if(h.find("jec")!=-1): 
    hData = TH1F("hData","hData",80  ,1.0  ,1.2 )
  # else:
  #   hData = TH1F("hData","hData",100  ,-1  ,1. )
  #   hData.SetCanExtend(TH1.kAllAxes)

  # if addData:
 
  fname = path + ch + "/ExoDiBosonAnalysis.WWTree_data.root"
  file = TFile.Open(fname,"READ")
  intree = file.Get("tree")
  for i in range(intree.GetEntries()):
    intree.GetEntry(i)
    wtagger = getattr(intree,"Whadr_tau21")
    btag = getattr(intree,"Whadr_csv")
    if  wtagger < options.cutMin or wtagger > options.cutMax or btag > options.csv : continue
    if  getattr(intree,"Whadr_pruned") < options.prunedMin or getattr(intree,"Whadr_pruned") > options.prunedMax: continue
    if  options.realW and not getattr(intree,"Whadr_isW"): continue
    if  options.fakeW and getattr(intree,"Whadr_isW"): continue
    hData.Fill(getattr(intree,var),getattr(intree,"weight"))
  if addData: legend.AddEntry(hData,"Data","Ple")
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
  if options.normalize: yTitle = "A.U"
  hData.GetYaxis().SetTitle(yTitle)
  
  
  # for i in range (0,len(samples)):
    # hMC = TH1F('hMC%i'%i,'hMC%i'%i,nBins,xMin, xMax)
    # hMC = TH1F('hMC%i'%i,'hMC%i'%i,1000,0, 1000)
    # histolist.append(TH1F(hMC))
   
  ii = -1
  for sample in samples:
    ii +=1
    fname = path + ch + "/ExoDiBosonAnalysis.WWTree_" + sample + ".root"
    file = TFile.Open(fname,"READ")
    intree = file.Get("tree")
    hMC = TH1F('hMC%i'%ii,'hMC%i'%ii,nBins,xMin, xMax)
    hMC.SetDirectory(0)
    SF = 1.
    # if sample.find("TTbar")!=-1:
    #   if ch.find("mu")!=-1: SF = .85
    #   if ch.find("el")!=-1: SF = .70
    #   if ch.find("em")!=-1: SF = .80

    for i in range(intree.GetEntries()):
      intree.GetEntry(i)
      wtagger = getattr(intree,"Whadr_tau21")
      btag = getattr(intree,"Whadr_csv")
      if  wtagger < options.cutMin or wtagger > options.cutMax or btag > options.csv : continue
      if  getattr(intree,"Whadr_pruned") < options.prunedMin or getattr(intree,"Whadr_pruned") > options.prunedMax: continue
      if  options.realW and not getattr(intree,"Whadr_isW"): continue
      if  options.fakeW and getattr(intree,"Whadr_isW"): continue
      hMC.Fill(getattr(intree,var),getattr(intree,"weight"))
    hMC.Scale(lumi*SF)
    if options.normalize:hMC.Scale(1./hMC.Integral())
    hMC.SetLineColor(colors[ii])
    hMC.SetLineWidth(2)
    legend.AddEntry(hMC,legends[ii],"l")
    # legend.AddEntry(0,"Mean = %.1f RMS = %.1f"%(hMC.GetMean(),hMC.GetRMS()),"")
    histolist.append(hMC)
  
  # hsum = TH1F("hsum","hsum1",nBins,xMin,xMax)
  # for j in range(1,len(histolist)+1):
  #   hs.Add(histolist[len(histolist)-j],"HIST")
  #   hsum.Add(histolist[len(histolist)-j])
  # hsum.SetFillColor(kBlack)
  # hsum.SetFillStyle(3008)
  # hsum.SetLineColor(kWhite)
  # hsum.SetDirectory(0)
  #
         
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
  canv.SetRightMargin(0.05)
  canv.SetTopMargin(0.05)
  
  if addData:
    canv.Divide(1,2,0,0,0)
    canv.cd(1)
    p11_1 = canv.GetPad(1)
    p11_1.SetPad(0.01,0.26,0.99,0.98)
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
  if  options.realW:addInfo.AddText("#DeltaR(AK8,genW)<0.3")
  if  options.fakeW:addInfo.AddText("#DeltaR(AK8,genW)>0.3")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  max = histolist[2].GetMaximum()*1.6
  if options.log: max = histolist[2].GetMaximum()*25

  vFrame = canv .DrawFrame(histolist[0].GetXaxis().GetXmin(),0.0000001,histolist[0].GetXaxis().GetXmax(),max)
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
  histolist[0].Draw("HISTsame")
  histolist[1].Draw("HISTsame")
  histolist[2].Draw("HISTsame")
  addInfo.Draw("same")
  # hsum.Draw("E2same")
  legend.Draw("same")
  
  if addData: 
    hData.Draw("EOsame")
    addInfo.Draw("same")
    p11_1.RedrawAxis()
    p11_1.Update()
    p11_1.GetFrame().Draw()
    CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
  else: 
    # addInfo.Draw("same")
    vFrame.GetYaxis().SetNdivisions(504)
    vFrame.GetXaxis().SetNdivisions(504)
    canv.RedrawAxis()
    canv.Update()
    canv.GetFrame().Draw()
    CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  
 
    if options.save:
      addInf = ""
      if  options.realW: addInf = "_realW"
      if  options.fakeW: addInf = "_fakeW"
      Csv = "%.2f"%options.csv
      CutMin = "%.2f"%options.cutMin
      CutMax = "%.2f"%options.cutMax
      canvasname = "tt-comp/%s/tt-comp%s_%s_Tau21min%stomax%s_CSVmax%s_Pruned%ito%i.pdf"%(ch,addInf,h,CutMin.replace(".","v"),CutMax.replace(".","v"),Csv.replace(".","v"),options.prunedMin,options.prunedMax)
      if options.normalize: canvasname = "tt-comp/norm/%s/tt-comp%s_norm_%s_Tau21min%stomax%s_CSVmax%s_Pruned%ito%i.pdf"%(ch,addInf,h,CutMin.replace(".","v"),CutMax.replace(".","v"),Csv.replace(".","v"),options.prunedMin,options.prunedMax)
      canvasname = "tt-comp_%s_%s.pdf"%(ch,h)
      canv.Print(canvasname,"pdf")
      canvasname = "tt-comp_%s_%s.root"%(ch,h)
      canv.Print(canvasname,"root")
    
    file.Close()
    del intree
    
    del hMC
    # del hsum
    del histolist
    del canv
     
  if options.time: 
    time.sleep(100)
    
  
  
