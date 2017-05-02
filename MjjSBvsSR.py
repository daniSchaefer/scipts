from ROOT import *
import time
import CMS_lumi, tdrstyle
#!/usr/bin/python
from array import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--herwig',dest="herwig", default=False, action="store_true", help="Use Herwig++")
parser.add_option('--ptBinned',dest="ptBinned", default=False, action="store_true", help="Use Pythia8 pt-binned")
parser.add_option('--qV',dest="qV", default=False, action="store_true", help="do qV sideband")

(options, args) = parser.parse_args()

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

W = 800
H = 800
H_ref = 700 
W_ref = 600 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

def get_palette(mode):

 palette = {}
 palette['gv'] = [] 
 
 colors = ['#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#1b7837','#1b7837','#2166ac','#2166ac','#92c5de','#92c5de','#4393c3','#4393c3','#2166ac','#2166ac','#053061','#053061']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
 
palette = get_palette('gv')
col = TColor()
 

path = "/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/results/"

channel = "VV"
if options.qV:
    channel = "qV"

filename1 = "QCD_HTbinned_"+channel+".root"
filename2 = "QCD_HTbinned_"+channel+"_SB.root"
filename1 = "QCD_madgraph_pythia8_"+channel+"_summer16.root"
filename2 = "QCD_madgraph_pythia8_"+channel+"_summer16_SB.root"

if options.herwig:
  filename1 = "QCD_herwig_"+channel+"_summer16.root"
  filename2 = "QCD_herwig_"+channel+"_summer16_SB.root"
if options.ptBinned:
  filename1 = "QCD_pythia8_"+channel+".root"
  filename2 = "QCD_pythia8_"+channel+"_SB_test40GeV.root"
  filename1 = "QCD_pythia8_"+channel+"_summer16.root"
  filename2 = "QCD_pythia8_"+channel+"_summer16_SB.root"
  #QCD_pythia8_qV_SB_test40GeV.root
filetmpSR = TFile.Open(path+filename1,"READ")
filetmpSB = TFile.Open(path+filename2,"READ")


y = 2
if options.qV:
    y=10

markerStyle = [20,24,22,26,33,27,20]

fBins =[1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010]

# fBins = [x*200 for x in range(5, 20)]
         
mg =  []
#histos = ["DijetMassHighPuriqV","DijetMassLowPuriqV","DijetMassHighPuriWW","DijetMassLowPuriWW","DijetMassHighPuriZZ","DijetMassLowPuriZZ"]
histos = ["DijetMassHighPuriWW","DijetMassLowPuriWW","DijetMassHighPuriZZ","DijetMassLowPuriZZ"]
legend = ["WW HP","WW LP","ZZ HP","ZZ LP"]
if options.qV:
    histos = ["DijetMassHighPuriqV","DijetMassLowPuriqV"]
    legend = ["qV HP","qV LP"]

l = TLegend(0.7801508,0.7215026,0.9296482,0.9093264)
l.SetTextSize(0.033)
l.SetLineColor(0)
l.SetShadowColor(0)
l.SetLineStyle(1)
l.SetLineWidth(1)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetMargin(0.35)
# addInfo = TPaveText(0.6984925,0.5854922,0.9886935,0.7020725,"NDC")
addInfo = TPaveText(0.3969849,0.7914508,0.7072864,0.9080311,"NDC")
addInfo.SetFillColor(0)
addInfo.SetLineColor(0)
addInfo.SetFillStyle(0)
addInfo.SetBorderSize(0)
addInfo.SetTextFont(42)
addInfo.SetTextSize(0.030)
addInfo.SetTextAlign(12)
# addInfo.AddText("W-jet")
if options.herwig: addInfo.AddText("QCD, Herwig++")
elif options.ptBinned: addInfo.AddText("QCD, Pythia8")
else: addInfo.AddText("QCD, Pythia8+Madgraph")
addInfo.AddText("p_{T} > 200 GeV, |#eta| < 2.5 GeV")
addInfo.AddText("M_{jj} > 1.070 TeV")

i = -1 
for h in histos:
  fBins = [1055, 1200, 1400, 1600, 1900, 2200, 2500, 3000, 3650]
  massBins = array('d',fBins)
  if h.find("HighPuriWW") != -1 or h.find("HighPuriZZ") != -1:
    fBins = [1055, 1200, 1400, 1600, 2000, 2500, 3000, 3650]
    massBins = array('d',fBins)   
  if h.find("HighPuriqV") != -1 or h.find("LowPuriqV") != -1:
    fBins = [1055, 1200, 1400, 1600, 2000, 2500, 3000, 3650,4300,5000,6000,6500]
  massBins = array('d',fBins)
  i +=1 
  dentmp = TH1F(filetmpSB.Get(h))
  numtmp = TH1F(filetmpSR.Get(h))
  dentmp.Sumw2()
  numtmp.Sumw2()
  # dentmp.Scale(1./dentmp.Integral())
  # numtmp.Scale(1./numtmp.Integral())
  den = dentmp.Rebin(len(massBins)-1,"den_rebinned",massBins)
  num = numtmp.Rebin(len(massBins)-1,"num_rebinned",massBins)
 
  canvas = TCanvas("c","c",W,H)
  canvas.SetLogy()
  num.SetMarkerColor(col.GetColor(palette[i]))
  num.SetLineColor(col.GetColor(palette[i]))
  num.SetLineWidth(2)
  num.SetMarkerSize(2)
  num.SetMarkerStyle(markerStyle[i])
  
  den.SetMinimum(0.1)
  den.SetMaximum(den.GetMaximum()*15)
  den.Draw("E0P")
  den.SetMarkerColor(col.GetColor(palette[i+1]))
  den.SetLineColor(col.GetColor(palette[i+1]))
  den.SetLineWidth(2)
  den.SetMarkerSize(2)
  den.SetMarkerStyle(markerStyle[i+1])
  den.GetXaxis().SetTitleSize(0.06)
  den.GetXaxis().SetTitleOffset(0.95)
  den.GetXaxis().SetLabelSize(0.05)
  den.GetYaxis().SetTitleSize(0.06)
  den.GetYaxis().SetLabelSize(0.05)
  den.GetXaxis().SetTitle("M_{VV} (GeV)")
  den.GetYaxis().SetTitle("Weighted MC events")
  den.GetYaxis().SetNdivisions(304)
  den.GetXaxis().SetNdivisions(308)
  num.Draw("E0Psame")
  CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
  l2 = TLegend(0.7801508,0.7215026,0.8596482,0.87093264)
  l2.SetTextSize(0.033)
  l2.SetLineColor(0)
  l2.SetShadowColor(0)
  l2.SetLineStyle(1)
  l2.SetLineWidth(1)
  l2.SetFillColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)
  l2.AddEntry(num,"SR %s"%(legend[i]), "pl" )
  l2.AddEntry(den,"SB %s"%(legend[i]), "pl" )
  SetOwnership( l2, 1 )
  l2.Draw("same")
  addInfo.Draw("same")
  cname = "../AnalysisOutput/figures/MjjSRvsSB_MVVdist%s_pythia8Madgraph.pdf"%h
  if options.herwig:
    cname = "../AnalysisOutput/figures/MjjSRvsSB_MVVdist%s_herwig.pdf"%h
  if options.ptBinned:
    cname = "../AnalysisOutput/figures/MjjSRvsSB_MVVdist%s_pythia8.pdf"%h
  canvas.SaveAs(cname)
  
  h_efficiency = num
  h_efficiency.Divide(num,den)
  # g =  TGraphAsymmErrors()
  # num.Divide(den)
  h_efficiency.SetMarkerColor(col.GetColor(palette[i]))
  h_efficiency.SetName("g%i"%i)
  h_efficiency.SetLineColor(col.GetColor(palette[i]))
  h_efficiency.SetLineWidth(2)
  h_efficiency.SetMarkerSize(2)
  h_efficiency.SetMarkerStyle(markerStyle[i])
  mg.append(h_efficiency) 
  l.AddEntry(h_efficiency,"%s"%(legend[i]), "pl" )


      

canvas = TCanvas("c","c",W,H)
mg[0].SetMinimum(-0.5)
mg[0].SetMaximum(y)
mg[0].GetXaxis().SetLimits(1058.,6600.)
mg[0].GetXaxis().SetRangeUser(1058.,6600.)
mg[0].Draw("E0P")
mg[0].GetXaxis().SetTitleSize(0.06)
mg[0].GetXaxis().SetTitleOffset(0.95)
mg[0].GetXaxis().SetLabelSize(0.05)
mg[0].GetYaxis().SetTitleSize(0.06)
mg[0].GetYaxis().SetLabelSize(0.05)
mg[0].GetXaxis().SetTitle("M_{VV} (GeV)")
mg[0].GetYaxis().SetTitle("SR / SB")
mg[0].GetYaxis().SetNdivisions(304)
mg[0].GetXaxis().SetNdivisions(308)
for i in range(1,len(mg)):
  mg[i].Draw("E0Psame")
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
SetOwnership( l, 1 )
l.Draw()
addInfo.Draw("same")
mg[0].GetXaxis().SetLimits(1058.,6600.)
mg[0].GetXaxis().SetRangeUser(1058.,6600.)
canvas.Update()
cname = "../AnalysisOutput/figures/MjjSRvsSB_pythia8Madgraph_"+channel+".pdf"
if options.herwig:
  cname = "../AnalysisOutput/figures/MjjSRvsSB_herwig_"+channel+".pdf"
if options.ptBinned:
  cname = "../AnalysisOutput/figures/MjjSRvsSB_pythia8_"+channel+".pdf"
canvas.SaveAs(cname)
canvas.SaveAs(cname.replace("pdf","root"),"root")
canvas.SaveAs(cname.replace("pdf","C"),"C")
time.sleep(10)
