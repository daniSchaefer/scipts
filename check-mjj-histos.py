from ROOT import *
import ROOT as rt
from array import *
import time
import CMS_lumi, tdrstyle
import sys
import operator

tdrstyle.setTDRStyle()

CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

col = TColor()
colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']

rebin = 50
models = ["BulkWW","BulkZZ","ZprimeWW","WprimeWZ"]
histnames = [#'DijetMassHighPuriVV',
            'DijetMassHighPuriWW',
            'DijetMassHighPuriWZ',
            'DijetMassHighPuriZZ',
            # 'DijetMassLowPuriVV',
            'DijetMassLowPuriWW',
            'DijetMassLowPuriWZ',
            'DijetMassLowPuriZZ'
            ]

models = ["QstarQZ","QstarQW"]
models = ["QstarQW"]
histnames = ['Mjj_genMatched']

                        
for model in models:
  
  masses =[m*100 for m in range(10,45+1)]
  if model.find("Qstar") !=-1:  
    masses =[m*100 for m in range(10,60+1)]
    masses =[1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,7000]
    # masses =[1000,2000,3000,4000]
  # masses = [1000]
  bins = []
  ws = rt.RooWorkspace("ws","ws")
  
  yielddict = {}
  maxvaldict = {}
  histlist = []  
  sigfits = []
  filelist = []
  print "Length of histlist = " , len(histlist)
  for mass in masses:
    print "Working on masspoint " ,mass
    fname = "/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/ExoDiBosonAnalysis."+model+"_13TeV_%iGeV.qV.root"%mass
    print "Opening " ,fname
    infile = TFile.Open(fname,"READ")
    filelist.append(infile)
  i =-1  
  for infile in filelist: 
    i+=1
    histname = histnames[0]
    print "Getting histogram " ,histname
    hist = infile.Get(histname)
    print "With mean = %i" %hist.GetMean()
    hist.SetName(histname+"%i"%masses[i])
    # hist.Scale(1./hist.Integral())
    print "setting name to " ,hist.GetName()
    hist.Rebin(rebin)
    histlist.append(hist)

  
  # references for T, B, L, R
  T = 0.08*H_ref
  B = 0.12*H_ref 
  L = 0.12*W_ref
  R = 0.04*W_ref
  
  for cat in range(0,len(histnames)):

    l = TLegend(0.6243719,0.32241259,0.8253769,0.7880604895)
    l.SetTextSize(0.04)
    l.SetLineColor(0)
    l.SetShadowColor(0)
    l.SetLineStyle(1)
    l.SetLineWidth(1)
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetMargin(0.35)
     
    addInfo = TPaveText(0.5350754,0.7937063,0.8247739,0.9143357,"NDC")
    addInfo.SetFillColor(0)
    addInfo.SetLineColor(0)
    addInfo.SetFillStyle(0)
    addInfo.SetBorderSize(0)
    # addInfo.SetTextFont(42)
    addInfo.SetTextSize(0.045)
    addInfo.SetTextAlign(12)
    
    txt = "G_{B}#rightarrow"
    if model.find("Wprime")!=-1:  txt = "W'#rightarrow"
    if model.find("Zprime")!=-1:  txt = "Z'#rightarrow"
    if model.find("Qstar") !=-1:  txt = "q*#rightarrow"
    if model.find("WW")!=-1: txt += "WW"
    if model.find("ZZ")!=-1: txt += "ZZ"
    if model.find("WZ")!=-1: txt += "WZ"
    if model.find("QZ")!=-1: txt += "qZ"
    if model.find("QW")!=-1: txt += "qW"
    addInfo.AddText(txt)
    txt = "Pythia8 Tune CUETP8M1"
    addInfo.AddText(txt)

    canv = TCanvas("c%i"%cat,"c%i"%cat,50,50,W,H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetTickx(0)
    canv.SetTicky(0)
    canv.SetLeftMargin( L/W )
    canv.SetRightMargin( R/W )
    canv.SetTopMargin( T/H )
    canv.SetBottomMargin( B/H )

    histlist[0].Draw("hist")
    l.AddEntry( histlist[0],"M_{q*} = %i GeV"%masses[0], "l" )
    for h in range (1,len(masses)):
      histlist[h].Draw("histSAME")
      histlist[h].SetLineColor(col.GetColor(colors[h%12]))
      l.AddEntry( histlist[h],"M_{q*} = %i GeV"%masses[h], "l" )
     
    histlist[0].GetXaxis().SetRangeUser(800.,7200)
    histlist[0].SetMaximum( histlist[0].GetMaximum() *1.3)
    histlist[0].GetYaxis().SetTitle("Relative yield")
    histlist[0].GetXaxis().SetNdivisions(405)
    histlist[0].GetYaxis().SetNdivisions(905)
    histlist[0].GetXaxis().SetTitle("M_{jj}")
    histlist[0].GetYaxis().SetTitleSize(0.05)
    histlist[0].GetXaxis().SetTitleSize(0.05)
    histlist[0].GetYaxis().SetTitleOffset(1.2)
    histlist[0].GetXaxis().SetTitleOffset(1.1)
    CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
    

   
 
    l.Draw("same")
    addInfo.Draw("same")
    canv.RedrawAxis()
    canv.Update()
    cname = "plots80X/Mjj_GenMatched_%s.pdf" %(model)
    canv.SaveAs(cname)
    canv.SaveAs(cname.replace(".pdf",".root"))
    cname = "/mnt/t3nfs01/data01/shome/thaarres/Notes/notes/AN-16-235/trunk/figures/sig-interpolation/Mjj_GenMatched_%s.pdf" %(model)
    canv.SaveAs(cname)
    canv.SaveAs(cname.replace(".pdf",".root"))
  time.sleep(200)
  
     

  
              