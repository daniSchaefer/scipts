from optparse import OptionParser
from ROOT import *
import sys
import ConfigParser
import time
import gc
import math
import CMS_lumi, tdrstyle
from array import *
import os.path
import copy


tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = "1.26 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

W = 600
H = 700
H_ref = 700 
W_ref = 600 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

rebin=500

bins1 = range (1000,3400,200)
bins2 = range (3400,4000,300)
bins3 = range (4000,5500,500)
bins = []
bins = bins1
# bins += bins2
# bins += bins3
print bins
runArray = array('d',bins)
binnum = len(bins)-1

prefix = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned"
outdir = "/shome/thaarres/Notes/notes/AN-15-211/trunk/figures/"
signalname = ["G_{Bulk}#rightarrow WW (MADGRAPH)","G_{RS1}#rightarrow WW (PYTHIA8)",
              "G_{RS1}#rightarrow ZZ(PYTHIA8)","W'#rightarrow WZ (PYTHIA8)","q*#rightarrow qW (PYTHIA8)", "q*#rightarrow qZ (PYTHIA8)"]

bkgVV = ["QCD"]
addinfo = ["High purity double V-tag","Low purity double V-tag","Untagged"]
categories= ["HP","LP","NP"]
# categories= ["HP"]
channelsVV = ["VV","WW","WZ","ZZ"]
# channelsVV = ["qV","qW","qZ"]
#
#
# signalname = [ "q*#rightarrow qW (PYTHIA8)", "q*#rightarrow qZ (PYTHIA8)"]
#
# addinfo = ["High purity single V-tag","Low purity single V-tag","Untagged"]
# categories= ["HP","LP","NP"]


linestyle = [1,9,2,3,4,1,1,1,1,1]
color = [kBlack,kRed,kBlue,kMagenta,kBlack,kRed,kBlue,kMagenta,]

# categories = []
k=0
for cat in categories:
  mg =  TMultiGraph()
  histolist=[]
  mg_data =  TMultiGraph()
  # l = TLegend(0.4513423,0.1741071,0.6627517,0.3139881)
  l = TLegend(0.6879195,0.702381,0.9630872,0.8422619)
  l.SetTextSize(0.038)
  l.SetLineColor(0)
  l.SetLineStyle(0)
  l.SetLineWidth(0)
  l.SetFillColor(0)
  l.SetShadowColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)

  # l2 = TLegend(0.1761745,0.1696429,0.4513423,0.3467262)
  l2 = TLegend(0.6879195,0.702381,0.9630872,0.8422619)
  l2.SetTextSize(0.03)
  l2.SetLineColor(0)
  l2.SetLineStyle(0)
  l2.SetLineWidth(0)
  l2.SetFillColor(0)
  l2.SetShadowColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)

  addInfo = TPaveText(0.5201342,0.8630952,0.6895973,0.9300595,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)

  addInfo.AddText(addinfo[k])
  k+=1
  i = -1
  for f in bkgVV:
    i+=1
    j=-1
    for c in channelsVV:
      x=[]
      y=[]
      j+=1
      if (not c.find("q")!=-1):
        filename = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
        if (f.find("QCD")!=-1 or f.find("DATA")!=-1 ):
          filename = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
      if (c.find("q")!=-1):
        filename = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
        if (f.find("QCD")!=-1 or f.find("DATA")!=-1 ):
          filename = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
      
      print filename
      if not (os.path.isfile(filename)):
        print "Skipping %s"%filename
        continue
      filetmp = TFile.Open(filename,"READ")
      nPassedJetsDEta_= (TH1F(filetmp.Get("Mjj_fine")))
      nPassedTau21Cut_ = (TH1F(filetmp.Get("DiBosonInvMass")))
      nPassedJetsDEta_.GetXaxis().SetRangeUser(1000.,3200.)
      nPassedTau21Cut_.GetXaxis().SetRangeUser(1000.,3200.)
      nPassedTau21Cut_ = nPassedTau21Cut_.Rebin(binnum,"nPassedTau21Cut_",runArray)
      nPassedJetsDEta_ = nPassedJetsDEta_.Rebin(binnum,"nPassedJetsDEta_",runArray)
      if( not f.find("DATA")!=-1):
        g=copy.copy(nPassedTau21Cut_)
        g.Divide(g,nPassedJetsDEta_,1.0,1.0,"B")
        g.SetLineColor(color[j])
        g.SetName("g%i"%i)
        g.SetLineStyle(linestyle[j])
        g.SetLineWidth(2)
        # l2.AddEntry(g,"%s"%(c), "l" )
        # mg.Add(g)
        histolist.append(g)
#         # for ii in range(0,nPassedJetsDEta_.GetNbinsX()):
#   #         if(nPassedJetsDEta_.GetBinContent(ii+1)==0):continue
#   #         if(nPassedJetsDEta_.GetBinCenter(ii+1)>5000.):break
#   #         n    = nPassedTau21Cut_.GetBinContent(ii+1)/nPassedJetsDEta_.GetBinContent(ii+1)
#   #         mass = nPassedJetsDEta_.GetBinCenter(ii+1)
#   #         print mass
#   #         x.append(mass)
#   #         y.append(n)
#   #       vx = array("f",x)
#   #       vy = array("f",y)
#   #       g = TGraphAsymmErrors(len(vx),vx,vy)
#       if(f.find("DATA")!=-1):
      g = TGraphAsymmErrors()
      g.Divide(nPassedTau21Cut_,nPassedJetsDEta_)
      # histolist.append(g)
      data = copy.copy(g)
      data.SetMarkerSize(0.9)
      data.SetMarkerStyle(20)
      data.SetMarkerColor(color[j])
      data.GetXaxis().SetNdivisions(405)
      l2.AddEntry(data,"%s"%(c), "lp" )
      mg_data.Add(data)
        # g.Draw("pe0 same")
        

 
  canvas = TCanvas("c%i"%k,"c%i"%k,W,H)
  canvas.SetTickx()
  canvas.SetTicky()
  # canvas.SetLogy()
  # histolist[0].SetMinimum(0.0)
 #  histolist[0].SetMaximum(histolist[0].GetMaximum()*2.0)
  mg_data.Draw("Ape0")
  # histolist[0].Draw("HIST E")
 #  for h in histolist:
 #    h.Draw("HIST E same)")
  # if(histolist[0]):histolist[0].Draw("pe0")
  mg_data.SetMaximum(histolist[0].GetMaximum()*1.3)
  mg_data.GetXaxis().SetNdivisions(405)
  mg_data.GetXaxis().SetTitleSize(0.06)
  mg_data.GetXaxis().SetTitleOffset(0.95)
  mg_data.GetYaxis().SetTitleOffset(1.3)
  mg_data.GetXaxis().SetLabelSize(0.05)
  mg_data.GetYaxis().SetTitleSize(0.06)
  mg_data.GetYaxis().SetLabelSize(0.04)
  mg_data.GetXaxis().SetTitle("Diboson invariant mass [GeV]")
  mg_data.GetYaxis().SetTitle("Mistagging rate")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  SetOwnership( l, 1 )
  # l.Draw()
  l2.Draw()
  addInfo.Draw("same")

  cname =" all-hadronic-plots/BkgEff/QCD_" +cat+"_VV_MistaggingRateEff.pdf"
  print "saving canvas %s" %cname
  canvas.SaveAs(cname)
  cname =outdir +"/QCD_" +cat+"_VV_MistaggingRateEff.pdf"
  print "saving canvas %s" %cname
  canvas.SaveAs(cname)
  
  cname =" all-hadronic-plots/BkgEff/QCD_" +cat+"_VV_MistaggingRateEff.C"
  print "saving canvas %s" %cname
  canvas.SaveAs(cname)
  # time.sleep(100)



signalsqV = ["QstarQW","QstarQZ"]
channelsqV = ["qV","qW","qZ"]
signalname = [ "q*#rightarrow qW (PYTHIA8)", "q*#rightarrow qZ (PYTHIA8)"]

addinfo = ["High purity single V-tag","Low purity single V-tag","Untagged"]
categories= ["HP","LP"]
categories=[]

k=0
for cat in categories:
  mg =  TMultiGraph()
  l = TLegend(0.4630872,0.7172619,0.6744966,0.8571429)
  l.SetTextSize(0.038)
  l.SetLineColor(0)
  l.SetLineStyle(0)
  l.SetLineWidth(0)
  l.SetFillColor(0)
  l.SetShadowColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)

  # l2 = TLegend(0.1761745,0.1696429,0.4513423,0.3467262)
  l2 = TLegend(0.204698,0.6532738,0.4798658,0.8110119)
  l2.SetTextSize(0.03)
  l2.SetLineColor(0)
  l2.SetLineStyle(0)
  l2.SetLineWidth(0)
  l2.SetFillColor(0)
  l2.SetShadowColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)

  addInfo = TPaveText(0.5201342,0.8630952,0.6895973,0.9300595,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)

  addInfo.AddText(addinfo[k])
  k+=1
  i = -1
  for f in signalsqV:
    i+=1
    j=-1
    for c in channelsqV:
      j+=1
      x=[]
      y=[]
      for m in masspoints:
        m = int(m*1000)
        filename = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_%s"%m+"."+c+".root"
        if (f.find("QCD")!=-1 or f.find("DATA")!=-1 ):
          filename = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
        print filename
        if not (os.path.isfile(filename)):
          print "Skipping %s"%filename
          continue
        filetmp = TFile.Open(filename,"READ")
        nPassedJetsDEta_= (TH1F(filetmp.Get("nPassedJetsDEta"))).GetBinContent(1)
        if nPassedJetsDEta_ == 0:
          print "No events found!"
          continue;
        print nPassedJetsDEta_
        nPassedTau21Cut_ = (TH1F(filetmp.Get("nPassedTau21Cut"))).GetBinContent(1)
        if nPassedTau21Cut_ == 0:
          print "No events found!"
          # continue;
        Efficiency = nPassedTau21Cut_/nPassedJetsDEta_
        print "Efficiency = %f/%f --> %f"  %(nPassedTau21Cut_,nPassedJetsDEta_,(nPassedTau21Cut_/nPassedJetsDEta_))
        x.append(m)
        y.append(Efficiency)
      vx = array("f",x)
      vy = array("f",y)
      g = TGraphAsymmErrors(len(vx),vx,vy)
      g.SetLineColor(color[i])
      g.SetName("g%i"%i)
      g.SetLineStyle(linestyle[j])
      g.SetLineWidth(2)
      if (i==0  and j<len(channelsVV)):
        l2.AddEntry(g,"%s"%(c), "l" )
      if (j==0):
        l.AddEntry(g,"%s"%(signalname[i]), "l" )
      mg.Add(g)


  canvas = TCanvas("c2","c2",W,H)
  canvas.SetTickx()
  canvas.SetTicky()
  # canvas.SetLogy()
  mg.SetMinimum(0.01)
  mg.SetMaximum(0.57)
  mg.Draw("AL")
  mg.GetXaxis().SetTitleSize(0.06)
  mg.GetXaxis().SetTitleOffset(0.95)
  mg.GetXaxis().SetLabelSize(0.05)
  mg.GetYaxis().SetTitleSize(0.06)
  mg.GetYaxis().SetLabelSize(0.05)
  mg.GetXaxis().SetTitle("Resonance mass [GeV]")
  mg.GetYaxis().SetTitle("Tagging efficiency")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  SetOwnership( l, 1 )
  l.Draw()
  l2.Draw()
  addInfo.Draw("same")
  cname = cat+"_qV_SigEff.pdf"
  canvas.SaveAs(cname)


bins1 = range (1000,3000,500)
bins2 = range (3000,6000,1000)
bins = []
bins = bins1
bins += bins2
print bins
runArray = array('d',bins)
binnum = len(bins)-1


linestyle = [1,19,2,3,4,1,5,6,1,1,1,1]
color = [kBlack,kRed,kBlue,kMagenta,kGreen,kCyan,kBlack,kRed,kBlue,kMagenta,]

print 'Doing stability for double tag categories!'
bkgVV = ["QCD"]
addinfo = ["Low purity double V-tag"]
categories= ["LP"]
# categories= ["NP"]
channelsVV = ["WW","WZ","ZZ"]
categories =[]
k=0
for cat in categories:
  mg =  TMultiGraph()
  mg_data =  TMultiGraph()
  # l = TLegend(0.4513423,0.1741071,0.6627517,0.3139881)
  l = TLegend(0.4630872,0.7172619,0.6744966,0.8571429)
  l.SetTextSize(0.038)
  l.SetLineColor(0)
  l.SetLineStyle(0)
  l.SetLineWidth(0)
  l.SetFillColor(0)
  l.SetShadowColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)

  # l2 = TLegend(0.1761745,0.1696429,0.4513423,0.3467262)
  l2 = TLegend(0.7214765,0.6741071,0.9966443,0.8318452)
  l2.SetTextSize(0.03)
  l2.SetLineColor(0)
  l2.SetLineStyle(0)
  l2.SetLineWidth(0)
  l2.SetFillColor(0)
  l2.SetShadowColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)

  addInfo = TPaveText(0.5201342,0.8630952,0.6895973,0.9300595,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  addInfo.AddText(addinfo[k])
  k+=1
  i = -1
  for f in bkgVV:
    i+=1
    j=-1
    for c in channelsVV:
      x=[]
      y=[]
      j+=1  
      if (c.find("q")!=-1):
        filename   = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"  
        filenameNP = prefix + "/qV/NP/ExoDiBosonAnalysis." + f +"_qV.root"
      else:
        filename   = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
        filenameNP = prefix + "/VV/NP/ExoDiBosonAnalysis." + f +"_VV.root"        
      print filename
      print filenameNP
      if not (os.path.isfile(filename)):
        print "Skipping %s"%filename
        continue 
      filetmp = TFile.Open(filename,"READ")
      filetmpNP = TFile.Open(filenameNP,"READ")
      TagCat= (TH1F(filetmp.Get("DiBosonInvMass")))
      TagCat.SetName("SubCat%i"%j)
      print TagCat.GetName()
      NP = (TH1F(filetmpNP.Get("DiBosonInvMass")))
      NP.SetName("All%i"%j)
      print NP.GetName()
      # TagCat.GetXaxis().SetRangeUser(1000.,5000.)
      # NP.GetXaxis().SetRangeUser(1000.,5000.)
      TagCat = TagCat.Rebin(binnum,"TagCat",runArray)
      NP = NP.Rebin(binnum,"NP",runArray)
      for ii in range(0,NP.GetNbinsX()):
        if(NP.GetBinContent(ii+1)==0):continue
        if(NP.GetBinCenter(ii+1)>5000.):break
        # if( NP.GetBinCenter(ii+1)>3000. and not (c.find("q")!=-1)):break
        n    = TagCat.GetBinContent(ii+1)/NP.GetBinContent(ii+1)
        mass = TagCat.GetBinCenter(ii+1)
        x.append(mass)
        y.append(n)
      vx = array("f",x)
      vy = array("f",y)
      g = TGraphAsymmErrors(len(vx),vx,vy)
      g =  TGraphAsymmErrors()
      g.Divide(TagCat,NP)
      if(f.find("DATA")!=-1):
        data = copy.copy(g)
        data.SetMarkerSize(0.9)
        data.SetMarkerStyle(20)
        data.SetMarkerColor(color[j])
        data.GetXaxis().SetNdivisions(405)
        l2.AddEntry(data,"%s"%(c), "lp" )
        mg_data.Add(data)
        # g.Draw("pe0 same")
      else: 
        g.SetMarkerSize(0.9)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(color[j])
        g.SetLineColor(color[j])
        g.SetName("g%i"%i)
        g.SetLineStyle(0)
        g.SetLineWidth(2)
        l2.AddEntry(g,"%s"%(c), "l" )
        mg.Add(g)     

  canvas = TCanvas("c%i"%k,"c%i"%k,W,H)
  canvas.SetTickx()
  canvas.SetTicky()
  # canvas.SetLogy()
  if (cat.find("LP")!=-1):
    mg.SetMinimum(0.0)
    mg.SetMaximum(.25000)
  if (cat.find("HP")!=-1):
    mg.SetMinimum(0.0)
    mg.SetMaximum(.05000)
  mg.Draw("ALpe0")
  if(mg_data):mg_data.Draw("pe0")
  mg.GetXaxis().SetNdivisions(405)
  mg.GetXaxis().SetTitleSize(0.06)
  mg.GetXaxis().SetTitleOffset(0.95)
  mg.GetXaxis().SetLabelSize(0.05)
  mg.GetYaxis().SetTitleSize(0.06)
  mg.GetYaxis().SetLabelSize(0.05)
  if (cat.find("HP")!=-1):mg.GetYaxis().SetLabelSize(0.04)
  mg.GetXaxis().SetTitle("Dijet invariant mass [GeV]")
  mg.GetYaxis().SetTitle("Dijet mass/ Dijet mass (NP VV)")
  if (c.find("q")!=-1): mg.GetYaxis().SetTitle("Dijet mass/ Dijet mass (NP qV)")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  # SetOwnership( l, 1 )
  l.Draw("same")
  l2.Draw("same")
  addInfo.Draw("same")
  cname =" all-hadronic-plots/BkgEff/NPVVeff-vs-categories_" +cat+".pdf"
  print "saving canvas %s" %cname
  canvas.SaveAs(cname)


# print "Done. Bye!!"

print 'Doing stability for single tag categories!'
bins1 = range (1000,3000,500)
bins2 = range (3000,6000,1000)
bins = []
bins = bins1
bins += bins2
print bins
runArray = array('d',bins)
binnum = len(bins)-1


linestyle = [1,19,2,3,4,1,5,6,1,1,1,1]
color = [kBlack,kRed,kBlue,kMagenta,kGreen,kCyan,kBlack,kRed,kBlue,kMagenta,]

bkgVV = ["QCD"]
addinfo = ["Low purity single V-tag"]
categories= ["LP"]
# categories= ["NP"]
channelsVV = ["qW","qZ"]
k=0
for cat in categories:
  mg =  TMultiGraph()
  mg_data =  TMultiGraph()
  # l = TLegend(0.4513423,0.1741071,0.6627517,0.3139881)
  l = TLegend(0.4630872,0.7172619,0.6744966,0.8571429)
  l.SetTextSize(0.038)
  l.SetLineColor(0)
  l.SetLineStyle(0)
  l.SetLineWidth(0)
  l.SetFillColor(0)
  l.SetShadowColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)

  # l2 = TLegend(0.1761745,0.1696429,0.4513423,0.3467262)
  l2 = TLegend(0.7214765,0.6741071,0.9966443,0.8318452)
  l2.SetTextSize(0.03)
  l2.SetLineColor(0)
  l2.SetLineStyle(0)
  l2.SetLineWidth(0)
  l2.SetFillColor(0)
  l2.SetShadowColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)

  addInfo = TPaveText(0.5201342,0.8630952,0.6895973,0.9300595,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  
  addInfo.AddText(addinfo[k])
  k+=1
  i = -1
  for f in bkgVV:
    i+=1
    j=-1
    for c in channelsVV:
      x=[]
      y=[]
      j+=1  
      if (c.find("q")!=-1):
        filename   = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"  
        filenameNP = prefix + "/qV/NP/ExoDiBosonAnalysis." + f +"_qV.root"
      else:
        filename   = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
        filenameNP = prefix + "/VV/NP/ExoDiBosonAnalysis." + f +"_VV.root"        
      print filename
      print filenameNP
      if not (os.path.isfile(filename)):
        print "Skipping %s"%filename
        continue 
      filetmp = TFile.Open(filename,"READ")
      filetmpNP = TFile.Open(filenameNP,"READ")
      TagCat= (TH1F(filetmp.Get("DiBosonInvMass")))
      TagCat.SetName("SubCat%i"%j)
      print TagCat.GetName()
      NP = (TH1F(filetmpNP.Get("DiBosonInvMass")))
      NP.SetName("All%i"%j)
      print NP.GetName()
      # TagCat.GetXaxis().SetRangeUser(1000.,5000.)
      # NP.GetXaxis().SetRangeUser(1000.,5000.)
      TagCat = TagCat.Rebin(binnum,"TagCat",runArray)
      NP = NP.Rebin(binnum,"NP",runArray)
      for ii in range(0,NP.GetNbinsX()):
        if(NP.GetBinContent(ii+1)==0):continue
        if(NP.GetBinCenter(ii+1)>5000.):break
        # if( NP.GetBinCenter(ii+1)>3000. and not (c.find("q")!=-1)):break
        n    = TagCat.GetBinContent(ii+1)/NP.GetBinContent(ii+1)
        mass = TagCat.GetBinCenter(ii+1)
        x.append(mass)
        y.append(n)
      vx = array("f",x)
      vy = array("f",y)
      g = TGraphAsymmErrors(len(vx),vx,vy)
      g =  TGraphAsymmErrors()
      g.Divide(TagCat,NP)
      if(f.find("DATA")!=-1):
        data = copy.copy(g)
        data.SetMarkerSize(0.9)
        data.SetMarkerStyle(20)
        data.SetMarkerColor(color[j])
        data.GetXaxis().SetNdivisions(405)
        l2.AddEntry(data,"%s"%(c), "lp" )
        mg_data.Add(data)
        # g.Draw("pe0 same")
      else: 
        g.SetMarkerSize(0.9)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(color[j])
        g.SetLineColor(color[j])
        g.SetName("g%i"%i)
        g.SetLineStyle(0)
        g.SetLineWidth(2)
        l2.AddEntry(g,"%s"%(c), "l" )
        mg.Add(g)     

  canvas = TCanvas("c%i"%k,"c%i"%k,W,H)
  canvas.SetTickx()
  canvas.SetTicky()
  # canvas.SetLogy()
  if (cat.find("LP")!=-1):
    mg.SetMinimum(0.0)
    mg.SetMaximum(.8000)
  if (cat.find("HP")!=-1):
    mg.SetMinimum(0.0)
    mg.SetMaximum(.3000)
  mg.Draw("ALpe0")
  if(mg_data):mg_data.Draw("pe0")
  mg.GetXaxis().SetNdivisions(405)
  mg.GetXaxis().SetTitleSize(0.06)
  mg.GetXaxis().SetTitleOffset(0.95)
  mg.GetXaxis().SetLabelSize(0.05)
  mg.GetYaxis().SetTitleSize(0.06)
  mg.GetYaxis().SetLabelSize(0.05)
  if (cat.find("HP")!=-1):mg.GetYaxis().SetLabelSize(0.04)
  mg.GetXaxis().SetTitle("Dijet invariant mass [GeV]")
  mg.GetYaxis().SetTitle("Dijet mass/ Dijet mass (NP qV)")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  # SetOwnership( l, 1 )
  l.Draw("same")
  l2.Draw("same")
  addInfo.Draw("same")
  cname =" all-hadronic-plots/BkgEff/NPVVeff-vs-categories_" +cat+".pdf"
  print "saving canvas %s" %cname
  canvas.SaveAs(cname)
  time.sleep(100)