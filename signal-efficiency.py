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

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref
# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def get_canvas():
 canvas = TCanvas("c2","c2",50,50,W,H)
 canvas.SetFillColor(0)
 canvas.SetBorderMode(0)
 canvas.SetFrameFillStyle(0)
 canvas.SetFrameBorderMode(0)
 canvas.SetLeftMargin( L/W )
 canvas.SetRightMargin( R/W )
 canvas.SetTopMargin( T/H )
 canvas.SetBottomMargin( B/H )
 canvas.SetTickx(0)
 canvas.SetTicky(0)
 return canvas
 
def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]

palette = get_palette('gv')
col = TColor()
 

prefix = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/forEfficiencies"
outdir = "plots80X/SigEff"
signalname = ["G_{Bulk}#rightarrow WW (MADGRAPH)", "G_Bulk#rightarrow ZZ(MADGRAPH)","W'#rightarrow WZ (MADGRAPH)"]

signalsVV = ["BulkWW","BulkZZ","WprimeToWZ"]
signalsVV = ["BulkWW"]
addinfo = ["High purity double V-tag","Low purity double V-tag"]
categories = [0,1] #HP=0 LP=1
channelsVVHP = [-1,2,4,6] #HP channels # channelsVV = ["VV","WW","WZ","ZZ"]
channelsVVLP = [-1,3,5,7] #LP channels # channelsVV = ["VV","WW","WZ","ZZ"]
catTitle     = ["VV","WW","WZ","ZZ"]
masspoints = [1,1.2,1.4,1.8,2.0,2.5,3.0,3.5,4.0]
# masspoints = [1]


linestyle = [1,9,2,3,4,1,1,1,1,1]
color = [kBlack,kRed,kBlue,kMagenta,kBlack,kBlack,kBlack,kBlack]

# categories = []
k=-1
for cat in categories:
  k+=1
  
  channels = channelsVVHP
  if cat == 1:
    channels = channelsVVLP
    
  mg =  TMultiGraph()
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
  
  
  i = -1
  for f in signalsVV:
    i+=1
    j=-1
    for c in channels:
      j+=1
      x=[]
      y=[]
      for m in masspoints:
        m = int(m*1000)
        filename = prefix + "/ExoDiBosonAnalysis." + f +"_13TeV_%s"%m+"GeV.VV.root"
        print "Opening " ,filename
        if not (os.path.isfile(filename)):
          print "Skipping %s"%filename
          continue 
        filetmp = TFile.Open(filename,"READ")
        intree = filetmp.Get("tree")
        
        cut = ''
        passedAcc= float(intree.GetEntries(cut))
        if passedAcc == 0:
          print "No events found!"
          continue;
        print "Total events = " ,passedAcc
        print "category " ,catTitle[j]
        cut = '(category == %i)' %(cat)
        if j > 0:
          cut = '(channel == %i)' %(c)
        passedWtag = float(intree.GetEntries(cut))
        print cut
        print " Pass = " ,passedWtag
  
        if passedWtag == 0:
          print "No events found!"
          continue;
        Efficiency = float(passedWtag/passedAcc)
        print "Efficiency = %f/%f --> %f"  %(passedWtag,passedAcc,(passedWtag/passedAcc))
        x.append(m)
        y.append(Efficiency)
      vx = array("f",x)
      vy = array("f",y)
      g = TGraphAsymmErrors(len(vx),vx,vy)
      g.SetLineColor(col.GetColor(palette[j+1]))
      g.SetName("g%i"%i)
      g.SetLineStyle(linestyle[j])
      g.SetLineWidth(2)
      if (i==0  and j<len(channels)):
        l2.AddEntry(g,"%s"%(catTitle[j]), "l" )
      if (j==0):
        l.AddEntry(g,"%s"%(signalname[i]), "l" )
      mg.Add(g)
      print ""


  canvas = get_canvas()
  mg.SetMinimum(0.001)
  mg.SetMaximum(1.1)
  mg.Draw("AL")
  # mg.GetXaxis().SetTitleSize(0.06)
  # mg.GetXaxis().SetTitleOffset(0.95)
  # mg.GetXaxis().SetLabelSize(0.05)
  # mg.GetYaxis().SetTitleSize(0.06)
  # mg.GetYaxis().SetLabelSize(0.05)
  mg.GetXaxis().SetTitle("Resonance mass (GeV)")
  mg.GetYaxis().SetTitle("Tagging efficiency")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  SetOwnership( l, 1 )
  l.Draw()
  l2.Draw()
  addInfo.Draw("same")
  # cname = outdir +"/"+ cat+"_VV_SigEff.pdf"
  # canvas.SaveAs(cname)
  time.sleep(100)

#
#
# signalsqV = ["QstarQW","QstarQZ"]
# channelsqV = ["qV","qW","qZ"]
# signalname = [ "q*#rightarrow qW (PYTHIA8)", "q*#rightarrow qZ (PYTHIA8)"]
#
# addinfo = ["High purity single V-tag","Low purity single V-tag","Untagged"]
# categories= ["HP","LP","NP"]
# addinfo = ["Untagged"]
# categories= ["NP"]
#
# k=0
# for cat in categories:
#   mg =  TMultiGraph()
#   l = TLegend(0.4630872,0.7172619,0.6744966,0.8571429)
#   l.SetTextSize(0.038)
#   l.SetLineColor(0)
#   l.SetLineStyle(0)
#   l.SetLineWidth(0)
#   l.SetFillColor(0)
#   l.SetShadowColor(0)
#   l.SetFillStyle(0)
#   l.SetMargin(0.35)
#
#   # l2 = TLegend(0.1761745,0.1696429,0.4513423,0.3467262)
#   l2 = TLegend(0.204698,0.6532738,0.4798658,0.8110119)
#   l2.SetTextSize(0.03)
#   l2.SetLineColor(0)
#   l2.SetLineStyle(0)
#   l2.SetLineWidth(0)
#   l2.SetFillColor(0)
#   l2.SetShadowColor(0)
#   l2.SetFillStyle(0)
#   l2.SetMargin(0.35)
#
#   addInfo = TPaveText(0.5201342,0.8630952,0.6895973,0.9300595,"NDC")
#   addInfo.SetFillColor(0)
#   addInfo.SetLineColor(0)
#   addInfo.SetFillStyle(0)
#   addInfo.SetBorderSize(0)
#   addInfo.SetTextFont(42)
#   addInfo.SetTextSize(0.040)
#   addInfo.SetTextAlign(12)
#
#   addInfo.AddText(addinfo[k])
#   k+=1
#   i = -1
#   for f in signalsqV:
#     i+=1
#     j=-1
#     for c in channelsqV:
#       j+=1
#       x=[]
#       y=[]
#       for m in masspoints:
#         m = int(m*1000)
#         filename = prefix + "/qV/"+cat+"/ExoDiBosonAnalysis." + f +"_%s"%m+"."+c+".root"
#         print filename
#         if (f.find("QCD")!=-1 or f.find("DATA")!=-1 ):
#           filename = prefix + "/VV/"+cat+"/ExoDiBosonAnalysis." + f +"_"+c+".root"
#         print filename
#         if not (os.path.isfile(filename)):
#           print "Skipping %s"%filename
#           continue
#         filetmp = TFile.Open(filename,"READ")
#         passedAcc= (TH1F(filetmp.Get("nPassedJetsDEta"))).GetBinContent(1)
#         if passedAcc == 0:
#           print "No events found!"
#           continue;
#         print passedAcc
#         passedWtag = (TH1F(filetmp.Get("nPassedTau21Cut"))).GetBinContent(1)
#         if passedWtag == 0:
#           print "No events found!"
#           # continue;
#         Efficiency = passedWtag/passedAcc
#         print "Efficiency = %f/%f --> %f"  %(passedWtag,passedAcc,(passedWtag/passedAcc))
#         x.append(m)
#         y.append(Efficiency)
#       vx = array("f",x)
#       vy = array("f",y)
#       g = TGraphAsymmErrors(len(vx),vx,vy)
#       g.SetLineColor(color[i])
#       g.SetName("g%i"%i)
#       g.SetLineStyle(linestyle[j])
#       g.SetLineWidth(2)
#       if (i==0  and j<len(channelsVV)):
#         l2.AddEntry(g,"%s"%(c), "l" )
#       if (j==0):
#         l.AddEntry(g,"%s"%(signalname[i]), "l" )
#       mg.Add(g)
#
#
#   canvas = TCanvas("c2","c2",W,H)
#   canvas.SetTickx()
#   canvas.SetTicky()
#   # canvas.SetLogy()
#   mg.SetMinimum(0.01)
#   mg.SetMaximum(1.0)
#   mg.Draw("ALE")
#   mg.GetXaxis().SetTitleSize(0.06)
#   mg.GetXaxis().SetTitleOffset(0.95)
#   mg.GetXaxis().SetLabelSize(0.05)
#   mg.GetYaxis().SetTitleSize(0.06)
#   mg.GetYaxis().SetLabelSize(0.05)
#   mg.GetXaxis().SetTitle("Resonance mass (GeV)")
#   mg.GetYaxis().SetTitle("Tagging efficiency")
#   CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
#   SetOwnership( l, 1 )
#   l.Draw()
#   l2.Draw()
#   addInfo.Draw("same")
#   cname = outdir +"/"+ cat+"_qV_SigEff.pdf"
#   canvas.SaveAs(cname)
#
# print "Done. Bye!!"