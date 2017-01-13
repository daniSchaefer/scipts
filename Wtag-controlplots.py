from optparse import OptionParser
import sys
from ROOT import *
import math
import time
from array import *
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "2.2 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

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
    ratio.SetMinimum(0.4)
    ratio.SetMaximum(1.6)
    ratio.GetYaxis().SetTitle("#frac{Data}{MC}")
    ratio.GetYaxis().SetNdivisions(504)
    ratio.GetYaxis().SetLabelSize(0.09)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetTitleSize(0.15)
    ratio.GetYaxis().SetTitleOffset(0.4)
    ratio.GetYaxis().CenterTitle()

    ratio.SetTitle("")
    ratio.GetXaxis().SetTitleSize(0.06)
    ratio.GetXaxis().SetTitleSize(0.15)
    ratio.GetXaxis().SetTitleOffset(0.90)
   
# gROOT.SetBatch( True )

lumi = 2200
path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Wtag/lowMass/WWTree_"
channel =["mu"]
samples =["data","TTbar","STop","VV","WJets"]
histolist =[]
legends = ["Data","t#bar{t}","Single top","W+jets","WW/WZ/ZZ"]
colors = [kBlack,kGreen-1,kCyan,kRed,kBlue]


legend = TLegend(0.74164991,0.70,0.8603575,0.89)
legend.SetTextSize(0.038)
legend.SetLineColor(0)
legend.SetShadowColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetMargin(0.35)

for ch in channel:
  stacks = []

  mvvs = THStack("mvv", "mvv")
  mps  = THStack("mps", "mps")
  
  stacks.append(mvvs)
  stacks.append(mps)
  
  datas = []
  histos = []
  
  
  hsums = []
  hsummvvs       = TH1F('MVV'      ,'MVV'      ,100  ,0  ,2000 )
  hsumpms        = TH1F('hpm'      ,'hpm'      ,40  ,0  ,200  )
  hsumhl_pts     = TH1F('hl_pt'    ,'hl_pt'    ,300  ,0  ,3000 )
  hsumhl_etas    = TH1F('hl_eta'   ,'hl_eta'   ,100  ,-3 ,3    )
  
  i=-1
  for sample in samples:
    i+=1
    var_histos = []
    hmvv      = TH1F('MVV_%s'%sample      ,'MVV_%s'%sample      ,100  ,0  ,2000 )
    hpm       = TH1F('hpm_%s'%sample      ,'hpm_%s'%sample      ,40  ,0  ,200  )
    hl_pt     = TH1F('hl_pt_%s'%sample    ,'hl_pt_%s'%sample    ,300  ,0  ,3000 )
    hl_eta    = TH1F('hl_eta_%s'%sample   ,'hl_eta_%s'%sample   ,100  ,-3 ,3    )
  
    var_histos.append(hmvv)
    var_histos.append(hpm)
    var_histos.append(hl_pt)
    var_histos.append(hl_eta)
    
    for h in var_histos:
      if not sample.find("data")!=-1: 
        h.SetFillColor(colors[i]) 
      else:
        h.SetMarkerColor(kBlack) 
        h.SetMarkerStyle(20) 
        h.SetMarkerSize(1.) 
    h.SetLineColor(kBlack) 
    histos.append(var_histos)
  
  ii=-1    
  for sample in samples: 
    ii+=1
    
    fname = path + ch + "/ExoDiBosonAnalysis.WWTree_" + sample + ".root"
    file = TFile.Open(fname,"READ")
    intree = file.Get("tree")
  
    for event in intree:
      histos[ii][0].Fill(event.MWW,event.weight)
      histos[ii][1].Fill(event.Mjpruned,event.weight)
    if not sample.find("data")!=-1:
      legend.AddEntry(histos[ii][0], legends[ii],"f")
      for i in range (0,2): histos[ii][i].Scale(lumi)
      hsummvvs.Add(histos[ii][0])
      hsumpms.Add(histos[ii][1])
    else:
      legend.AddEntry(histos[ii][0], legends[ii],"lpe")
      datas.append(histos[ii][0]) 
      datas.append(histos[ii][1]) 
  
  for j in range(1,len(samples)+1):  
    if not samples[len(samples)-j].find("data")!=-1: 
      mvvs.Add(histos[len(samples)-j][0],"HIST")
      mps.Add(histos[len(samples)-j][1],"HIST")
  
  hsums.append(hsummvvs)
  hsums.append(hsumpms)
  
  W = 600
  H = 700
  H_ref = 700 
  W_ref = 600 
  T = 0.08*H_ref
  B = 0.12*H_ref
  L = 0.12*W_ref
  R = 0.04*W_ref
  
  
  canvases = []
  for i in range(0,len(datas)): 
    canv = TCanvas("canv_%i"%i,"canv_%i"%i,W,H)
    canv.GetWindowHeight()
    canv.GetWindowWidth()
    # canv.SetLogy()
    canv.Divide(1,2,0,0,0)

    canv.cd(1)
    p11_1 = canv.GetPad(1)
    p11_1.SetPad(0.01,0.26,0.99,0.98)
    # p11_1.SetLogy()
    p11_1.SetRightMargin(0.05)
    p11_1.SetTopMargin(0.05)
    p11_1.SetFillColor(0)
    p11_1.SetBorderMode(0)
    p11_1.SetFrameFillStyle(0)
    p11_1.SetFrameBorderMode(0)


    addInfo = TPaveText(0.2055198,0.01917989,0.5034242,0.1783234,"NDC")
    addInfo.AddText("Muon channel")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.040)
    addInfo.SetTextAlign(12)

    vFrame = p11_1.DrawFrame(histos[0][i].GetXaxis().GetXmin(),0.0001,histos[0][i].GetXaxis().GetXmax(),histos[0][i].GetMaximum()*2.0)
    vFrame.SetTitle("")
    vFrame.SetXTitle("Dijet invariant mass [GeV]")
    vFrame.SetYTitle("Events")
    vFrame.GetXaxis().SetTitleSize(0.06)
    vFrame.GetXaxis().SetTitleOffset(0.95)
    vFrame.GetXaxis().SetLabelSize(0.05)
    vFrame.GetYaxis().SetTitleSize(0.06)
    #vFrame.GetYaxis().SetTitleOffset(1.0)
    vFrame.GetYaxis().SetLabelSize(0.05)
  
    stacks[i].Draw("HISTsame")
    datas[i].Draw("pe0same")
    hsums[i].Draw("E2same")
    legend.Draw("same")
    # addInfo.Draw("same")
    p11_1.RedrawAxis()
    p11_1.Update()
    p11_1.GetFrame().Draw()
    CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)

    canv.cd(2)
    p11_2 = canv.GetPad(2)
    p11_2.SetPad(0.01,0.02,0.99,0.27)
    p11_2.SetBottomMargin(0.35)
    p11_2.SetRightMargin(0.05)
    p11_2.SetGridx()
    p11_2.SetGridy()
    vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(), -2.8, p11_1.GetUxmax(), 2.8)
    vFrame2.SetTitle("")
    vFrame2.SetXTitle("Dijet invariant mass [GeV]")
    vFrame2.GetXaxis().SetTitleSize(0.06)
    vFrame2.SetYTitle("#frac{Data-Fit}{#sigma}")
    vFrame2.GetYaxis().SetTitleSize(0.15)
    vFrame2.GetYaxis().SetTitleOffset(0.40)
    vFrame2.GetYaxis().SetLabelSize(0.09)
    vFrame2.GetXaxis().SetTitleSize(0.15)
    vFrame2.GetXaxis().SetTitleOffset(0.90)
    vFrame2.GetXaxis().SetLabelSize(0.12)
    vFrame2.GetXaxis().SetNdivisions(405)

    styles = [20,22,32,25,32]
    i =0
    rh = get_ratio(datas[i],hsums[i])
    line = TLine(histos[0][i].GetXaxis().GetXmin(),0,histos[0][i].GetXaxis().GetXmax(),0)
    rh.Draw()
    line.Draw("same")
    p11_2.RedrawAxis()
    line2=TLine()
    line2.DrawLine(p11_2.GetUxmin(), p11_2.GetUymax(), p11_2.GetUxmax(), p11_2.GetUymax())
    line2.DrawLine(p11_2.GetUxmax(), p11_2.GetUymin(), p11_2.GetUxmax(), p11_2.GetUymax())
    time.sleep(100)
    






  # # for h in histolist:
  # #    print "Scaling histogram to %f pb"%lumi
  # #    print "Saving histogram %s" %h.GetName()
  # #    h.Scale(lumi)
  # #  write(name,histolist)
  # #  filetmp.Close()
  # #  del intree
  # #  del histolist
  #
