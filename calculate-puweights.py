import ROOT
from ROOT import *
import time
import CMS_lumi, tdrstyle
from optparse import OptionParser

def get_canvas(cname,lumi):

   CMS_lumi.lumi_13TeV = "%.1f pb^{-1},#sqrt{s} = " %(lumi)
   CMS_lumi.writeExtraText = 0
   CMS_lumi.extraText = "Preliminary"

   iPos = 0
   if( iPos==0 ): CMS_lumi.relPosX = 0.15

   H_ref = 600; 
   W_ref = 800; 
   W = W_ref
   H  = H_ref

   T = 0.08*H_ref
   B = 0.12*H_ref 
   L = 0.12*W_ref
   R = 0.06*W_ref

   canvas = ROOT.TCanvas(cname,cname,W,H)
   canvas.SetFillColor(0)
   canvas.SetBorderMode(0)
   canvas.SetFrameFillStyle(0)
   canvas.SetFrameBorderMode(0)
   canvas.SetLeftMargin( L/W+0.01 )
   canvas.SetRightMargin( R/W )
   canvas.SetTopMargin( T/H )
   canvas.SetBottomMargin( B/H+0.03 )
   canvas.SetTickx()
   canvas.SetTicky()
   
   return canvas

parser = OptionParser()
parser.add_option('--data', '--data',action="store",type="string",dest="data",default="/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned/VV/HP/ExoDiBosonAnalysis.DATA_VV.root")
parser.add_option('--mc', '--mc',action="store",type="string",dest="mc",default="/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/Pruned/VV/HP/ExoDiBosonAnalysis.QCD_VV_forPUdistribution.root")
parser.add_option('--rebin', '--rebin',action="store",type="int",dest="rebin",default=1)
(options, args) = parser.parse_args()

tdrstyle.setTDRStyle()

lumi = 2600. 

rebin = options.rebin

fdata = TFile.Open(options.data,'READ')
fmc = TFile.Open(options.mc,'READ')

pudata = ROOT.TH1F(fdata.Get('nVertices'))
pudata.SetName('pudata')
pumc   = ROOT.TH1F(fmc.Get('nVertices'))
pumc.SetName('pumc')

pudata.Rebin(rebin)
pumc.Rebin(rebin)
# pudata.Scale(1./pudata.GetEntries())
# pumc.Scale(1./pumc.GetEntries())
pudata.Scale(1./pudata.Integral())
pumc.Scale(1./pumc.Integral())

l = ROOT.TLegend(0.5574713,0.729021,0.7571839,0.8653846,"","NDC")
l.SetLineWidth(2)
l.SetBorderSize(0)
l.SetFillColor(0)
l.SetTextFont(42)
l.SetTextSize(0.035)
l.SetTextAlign(12)

pumc.SetLineColor(kRed)
pudata.SetLineColor(kBlack)
pudata.SetMarkerStyle(20)
pudata.SetLineStyle(2)
pudata.GetXaxis().SetTitle('Number of Vertices')
pudata.GetYaxis().SetTitle('Normalized')
pudata.GetYaxis().SetTitleOffset(1.1)
pudata.GetYaxis().SetNdivisions(505)
pudata.SetMaximum(pudata.GetMaximum()*1.3)

l.AddEntry(pudata,'JetHT Run 2015D','PL')
l.AddEntry(pumc,'QCD MC','L')

canv = get_canvas('c',lumi)
canv.cd()

pudata.Draw('PC')
pumc.Draw('HISTsame')
l.Draw()

CMS_lumi.CMS_lumi(canv, 4, 0)	
canv.cd()
canv.Update()
canv.RedrawAxis()
frame = canv.GetFrame()
frame.Draw()
canv.cd()
canv.Update()   
canv.SaveAs('nVertices.png','png')

hweights = ROOT.TH1F('puweights','puweights',pudata.GetNbinsX(),pudata.GetXaxis().GetXmin(),pudata.GetXaxis().GetXmax())
for b in range(1,pudata.GetNbinsX()+1):
   if pumc.GetBinContent(b) !=0:
      hweights.SetBinContent(b,pudata.GetBinContent(b)/pumc.GetBinContent(b))
      #print "%.2f" %(pudata.GetBinContent(b)/pumc.GetBinContent(b))
   else: hweights.SetBinContent(b,0.) 

c = get_canvas('c2',1.)
c.cd()
hweights.GetXaxis().SetTitle('Number of Vertices')
hweights.GetYaxis().SetTitle('PU weight')
hweights.GetYaxis().SetTitleOffset(0.9)
hweights.SetFillColor(kBlack-2)
hweights.SetLineColor(kBlack)
hweights.SetLineWidth(2)
hweights.SetFillStyle(3018)
hweights.Draw('hist')
c.Update()   
c.SaveAs('puweights.pdf','pdf')
hweights.SaveAs('../ExoDiBosonAnalysis/data/PUweights_2016_JetHT.root')
   
time.sleep(100)    
