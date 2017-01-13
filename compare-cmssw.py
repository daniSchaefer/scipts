from optparse import OptionParser
import sys
from ROOT import *
import time
import CMS_lumi, tdrstyle



parser = OptionParser()
parser.add_option('-t','--time', action='store_true', dest='time', default=False, help='sleep')
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--norm', action='store_true', dest='normalize', default=True, help='Normalize')
parser.add_option('-l','--log', action='store_true', dest='log', default=False, help='Draw log')
parser.add_option("-s", "--save", dest="save", default=False, action="store_true", help="save canvas")
parser.add_option("-1",'--cutMin', action="store",type="float",dest="cutMin",default=0.0, help="Min Tau21 cut")
parser.add_option("-2",'--cutMax', action="store",type="float",dest="cutMax",default=1.0, help="Max Tau21 cut")
parser.add_option("-c",'--csv', action="store",type="float",dest="csv",default=1.0, help="Max CSV")
parser.add_option('-v', '--var',action="store",type="string",dest="variable",default="Whadr_jec")
parser.add_option('--pMin',action="store",type="float",dest="prunedMin",default=0.0)
parser.add_option('--pMax',action="store",type="float",dest="prunedMax",default=500.0)
parser.add_option('--realW',  action='store_true', dest='realW', default=False, help='Is real W')
parser.add_option('--fakeW',  action='store_true', dest='fakeW', default=False, help='Is fake W')
parser.add_option('--usePuppiSD',  action='store_true', dest='usePuppiSD', default=False, help='Use PUPPI+SD')
parser.add_option('--fit',  action='store_true', dest='doFit', default=False, help='Fit mass peak')
(options, args) = parser.parse_args()

if options.variable.find("_puppi_") != -1: options.usePuppiSD= True



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

def getMean(histolist,legends,yieldlist):
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
  addInfo2 = TPaveText(0.1761745,0.1407143,0.4379195,0.2547024,"NDC")
  for i in range(0,len(histolist)):
    # if options.normalize:
    #   histolist[i].Scale(yieldlist[i]) 
    xmin = histolist[i].GetMean()*0.8
    xmax = histolist[i].GetMean()*1.2
    histolist[i].Fit("gaus","S","SAME",xmin,xmax)
    f = histolist[i].GetFunction("gaus")
    myString = "%s: <m> = %.2f GeV   #sigma = %.2f GeV" % (legends[i],f.GetParameter("Mean"),f.GetParameter("Sigma"))
    myStrings = []
    myStrings.append(myString)
    # addInfo.AddText("<m> = %.2f #pm %.2f GeV   #sigma   = %.2f #pm %.2f GeV" % ( f.GetParameter("Mean") ,f.GetParError(1),f.GetParameter("Sigma"),f.GetParError(2) ) ) )
    addInfo2.AddText("%s: <m> = %.2f GeV   #sigma = %.2f GeV" % (legends[i],f.GetParameter("Mean"),f.GetParameter("Sigma")) )
    addInfo2.SetFillColor(0)
    addInfo2.SetLineColor(0)
    addInfo2.SetFillStyle(0)
    addInfo2.SetBorderSize(0)
    addInfo2.SetTextFont(42)
    addInfo2.SetTextSize(0.030)
    addInfo2.SetTextAlign(12)
    f.SetLineWidth(2)
    # histolist[i].SetFillStyle(0)
  #   histolist[i].SetLineColor(kBlack)
  #   histolist[i].Sumw2()
  #   histolist[i].GetXaxis().SetTitle(xTitle)
  #   histolist[i].GetYaxis().SetTitle(yTitle)
    histolist[i].Draw("EO")
    f.Draw("same")
    addInfo2.Draw()
    canv2.Update()
  if options.save:
      CutMin = "%.2f"%options.cutMin
      CutMax = "%.2f"%options.cutMax
      canvasname = "tt-comp/%s/FIT_cmssw-comp%s_Tau21min%stomax%s_Pruned%ito%i.pdf"%(ch,h,CutMin.replace(".","v"),CutMax.replace(".","v"),options.prunedMin,options.prunedMax)
      if options.normalize: canvasname = "tt-comp/norm/%s/FIT_cmssw-comp%s_norm_Tau21min%stomax%s_Pruned%ito%i.pdf"%(ch,h,CutMin.replace(".","v"),CutMax.replace(".","v"),options.prunedMin,options.prunedMax)
      canv2.Print(canvasname,"pdf")
  # SetOwnership( addInfo2, 1 )
  # SetOwnership( myStrings, 1 )
  # if options.normalize:
  #   histolist[i].Scale(1./histolist[i].Integral())
  return addInfo2
  

lumi = 2200
path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Wtag/WWTree_"
channel =["mu"]
samples =["TTbar_powheg_76X","TTbar_JECv7","TTbar","data_76X","data_JECv7","data"]
samples =["TTbar_powheg_76X","TTbar_JECv7","data_76X","data_JECv7"]
if options.usePuppiSD: 
  samples =["TTbar_powheg_76X_PUPPISD","data_76X_PUPPISD"]
h = options.variable


xTitle = options.variable

if options.variable.find("MVV") != -1:
  xTitle = "M_{VV} (GeV)"
if options.variable.find("pruned") != -1:
  xTitle = "Pruned mass (GeV)"
if options.variable.find("csv") != -1:
  xTitle = "CSV"    
if options.variable.find("tau21") != -1:
  xTitle = "#tau_{21}"     
if options.variable.find("jec") != -1:
  xTitle = "JEC"  
if options.variable.find("pruned_jec") != -1:
    xTitle = "Pruned JEC" 
if options.variable.find("puppi_softdrop") != -1:
    xTitle = "Puppi softdrop mass"  
        
legends = ["76X t#bar{t} MC JEC = Fall15_25nsV2","74X t#bar{t} MC JEC = Summer15_25nsV7","74X t#bar{t} MC JEC = Summer15_25nsV2",
           "76X DATA JEC = Fall15_25nsV2","74X DATA JEC = Summer15_25nsV7","74X DATA JEC = Summer15_25nsV5"]

legends = ["76X t#bar{t} MC JEC = Fall15_25nsV2","74X t#bar{t} MC JEC = Summer15_25nsV7",
           "76X DATA JEC = Fall15_25nsV2","74X DATA JEC = Summer15_25nsV7"]
legends = ["76X t#bar{t} MC","74X t#bar{t} MC",
           "76X DATA","74X DATA"]           
if options.usePuppiSD: legends = ["76X t#bar{t} MC", "76X DATA"]

colors = [ kBlack,kRed,kBlue,kBlack,kRed,kBlue]
style = [2,2,2, 1,1,1]
colors = [ kBlack,kRed,kBlack,kRed]
style = [2,2,1,1]



if options.noX:
  gROOT.SetBatch(True)
  

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

var = options.variable

    

for ch in channel:
  hs  = THStack("hs", "hs")
  histolist = []
  yieldlist = []
  
  legend = TLegend(0.3093289,0.6419643,0.8271812,0.9360119)
  legend.SetTextSize(0.030)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)

  if(h.find("jec")!= -1): 
      hData = TH1F("hData","hData",40  ,0.90  ,1.2 )
  elif(h.find("pruned")!=-1): 
    hData = TH1F("hData","hData",22  ,40  ,150 )
  elif(h.find("softdrop")!=-1): 
    hData = TH1F("hData","hData",22  ,40  ,150 )
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
  else:
    hData = TH1F("hData","hData",100  ,-1  ,1. )
    hData.SetCanExtend(TH1.kAllAxes)

  nBins = hData.GetNbinsX()
  xMin  = hData.GetXaxis().GetXmin()
  xMax  = hData.GetXaxis().GetXmax()
  
  addI = ""
  if xTitle.find("GeV")!=-1:
    addI = " GeV"
  yTitle = "Events / (%.2f%s)" %((xMax-xMin)/nBins, addI)
  if options.normalize: yTitle = "A.U"
  hData.GetYaxis().SetTitle(yTitle)
   
  ii = -1
  for sample in samples:
    ii +=1
    fname = path + ch + "/ExoDiBosonAnalysis.WWTree_" + sample + ".root"
    file = TFile.Open(fname,"READ")
    print file.GetName()
    intree = file.Get("tree")
    hMC = TH1F('hMC%i'%ii,'hMC%i'%ii,nBins,xMin, xMax)
    hMC.SetDirectory(0)
    hMC.SetName(sample)
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
      weight = getattr(intree,"weight")
      if (var.find("jec")!=-1): weight = 1.
      hMC.Fill(getattr(intree,var),weight)
    hMC.Scale(lumi*SF)
    yieldlist.append(hMC.Integral())
    if options.normalize:hMC.Scale(1./hMC.Integral())
    hMC.SetLineColor(colors[ii])
    hMC.SetLineStyle(style[ii])
    hMC.SetLineWidth(2)
    legend.AddEntry(hMC,legends[ii],"l")
    # legend.AddEntry(0,"Mean = %.3f RMS = %.3f"%(hMC.GetMean(),hMC.GetRMS()),"")
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
  
  
  if options.doFit:
    addInfo = getMean(histolist,legends,yieldlist)
           
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


  # addInfo = TPaveText(0.1644295,0.1860119,0.4211409,0.3467262,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.030)  
  addInfo.SetTextAlign(12)
  
  

  # f ch.find("el")!=-1: txt = "W#rightarrowe#nu"
#   if ch.find("em")!=-1: txt = "W#rightarrow#mu#nu + W#rightarrowe#nu"
#   addInfo.AddText(txt)
#   if  options.realW:addInfo.AddText("#DeltaR(AK8,genW)<0.3")
#   if  options.fakeW:addInfo.AddText("#DeltaR(AK8,genW)>0.3")
  
  max = histolist[0].GetMaximum()*1.8
  if options.log: max = histolist[0].GetMaximum()*25

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
  vFrame.GetYaxis().SetNdivisions(504)
  vFrame.GetXaxis().SetNdivisions(504)
  
  
  for i in range(0,len(histolist)):
    SetOwnership( histolist[i], 1 )
    histolist[i].Draw("HISTsame")
  addInfo.Draw("same")
  legend.Draw("same")
  
  vFrame.GetYaxis().SetNdivisions(806)
  vFrame.GetXaxis().SetNdivisions(806)
  canv.RedrawAxis()
  canv.Update()
  canv.GetFrame().Draw()
  CMS_lumi.CMS_lumi(canv, iPeriod, iPos)

  if options.save:
      addInf = ""
      if  options.realW: addInf = "_realW"
      if  options.fakeW: addInf = "_fakeW"
      CutMin = "%.2f"%options.cutMin
      CutMax = "%.2f"%options.cutMax
      canvasname = "tt-comp/%s/cmssw-comp%s_%s_Tau21min%stomax%s_Pruned%ito%i.pdf"%(ch,addInf,h,CutMin.replace(".","v"),CutMax.replace(".","v"),options.prunedMin,options.prunedMax)
      if options.normalize: canvasname = "tt-comp/norm/%s/cmssw-comp%s_norm_%s_Tau21min%stomax%s_Pruned%ito%i.pdf"%(ch,addInf,h,CutMin.replace(".","v"),CutMax.replace(".","v"),options.prunedMin,options.prunedMax)
      canv.Print(canvasname,"pdf")
      
  file.Close()
  del intree
  del hMC
  # del hsum
  del histolist
  del canv
     
  if options.time: time.sleep(100)
    
  
  
