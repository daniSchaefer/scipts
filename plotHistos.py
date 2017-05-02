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
 colors = ['#40004b','#a6dba0','#de77ae','#9970ab','#762a83','#00441b','#de77ae','#a6dba0','#5aae61','#1b7837','#92c5de','#4393c3','#2166ac','#053061']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]


def plotTH1(filenames, histoname, xlabel, ylabel,maximum,legendEntries,palette,linestyle,name,rebin=1.):
    col = TColor() 
    if len(filenames) != len(legendEntries):
        return -1
    l = TLegend(0.4630872,0.7172619,0.6744966,0.8571429)
    l.SetTextSize(0.038)
    l.SetLineColor(0)
    l.SetLineStyle(0)
    l.SetLineWidth(0)
    l.SetFillColor(0)
    l.SetShadowColor(0)
    l.SetFillStyle(0)
    l.SetMargin(0.35)
    
    canvas = get_canvas()
    h = [];
    files = [];
    #for f in filenames:
        #h.append(TH1())
    j=-1
    for f in filenames:
        j+=1
        if not (os.path.isfile(f)):
          print "Skipping %s"%f
          continue 
        files.append( TFile.Open(f,"READ"))
        print files
        h.append((files[j].Get(histoname)).Clone("htmp"+str(j)))
        print f
        print h
        h[j].SetLineColor(col.GetColor(palette[j+1]))
        h[j].SetLineStyle(linestyle[j])
        h[j].SetLineWidth(2)
    print h
    for i in range(0,len(legendEntries)):
        l.AddEntry(h[i],legendEntries[i], "lp" )
    h[0].SetMaximum(maximum)
    h[0].GetXaxis().SetTitle(xlabel)
    h[0].GetYaxis().SetTitle(ylabel)
    h[0].Rebin(rebin)
    h[0].Draw()
    print h[0].Integral()
    for i in range(1,len(h)):
        h[i].Rebin(rebin)
        h[i].Draw("same")
        print h[i].Integral()
    l.Draw()
    canvas.SaveAs(name)
    time.sleep(10)
    return 0
    



if __name__=='__main__':
    
    
    palette = get_palette('gv')
    linestyle = [1,2,3,4,1,1,1,1,1]
    
    ############################## plot cos(theta1) (sensitive to polarisation) ############################################
    #filenames=["/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/test/ExoDiBosonAnalysis.BulkWW_13TeV_1200GeV.PDF.root" , "/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/test/ExoDiBosonAnalysis.ZprimeWW_13TeV_1200GeV.VV.root","/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/test/ExoDiBosonAnalysis.WprimeWZ_13TeV_1200GeV.VV.root",'/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/test/ExoDiBosonAnalysis.QstarQW_13TeV_1200GeV.PDF.root', '/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/test/ExoDiBosonAnalysis.QstarQZ_13TeV_1200GeV.PDF.root']
    #legendEntries=["Bulk Graviton","Zprime","Wprime","QstarQW","QstarQZ"]
    #histoname="gen_COS_Theta1"

    #plotTH1(filenames,histoname,"cos(#theta_{1})","events",legendEntries,palette,linestyle)
    
    ############################## plot W+jets and QCD after all selections   ##############################################
    
    filenames=["/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/results/QCD_pythia8_qV_summer16.root", "/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/results/Wjets_qV.root"]
    legendEntries=["QCD","Wjets"]
    histoname="DijetMassHighPuriqW"
    maximum = 800
    rebin=100
    plotTH1(filenames,histoname,"m_{jj}","events",maximum,legendEntries,palette,linestyle,"plotBkg_qWHP.pdf",rebin)



