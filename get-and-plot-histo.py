import time
import CMS_lumi, tdrstyle
from ROOT import *

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

rebin = 1

setYmax = 1.3
setYmin = 0.9
prefix = '/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/GEN/'
doFit = False


def getCanvas():
  c = TCanvas("c","c",800,800)
  c.GetWindowHeight()
  c.GetWindowWidth()
  c.SetTitle("")
  return c
  
  
def get_palette(mode):

 palette = {}
 palette['gv'] = [] 
 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#de77ae','#a6dba0','#92c5de','#4393c3','#2166ac','#053061']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
palette = get_palette('gv')

col = TColor()
  
file = 'ExoDiBosonAnalysis.W_all.root'



histonames = ['puppiJECvsPT','puppiJECvsPT_eta1v3','prunedJECvsPT']
legendname = ['PUPPI L2L3','PUPPI L2L3 (|#eta|<1.3)','CHS L2L3']
titles     = ['p_{T}','p_{T}','p_{T}']
lineStyle = [1,1,1,1,3,3,3,3]
markerStyle = [20,24,22,26,33]

filelist = []
histos = []


filename = prefix + file
filetmp = TFile.Open(filename,"READ") 
    
ii = -1
for hname in histonames:
  ii += 1
  
  min = 200
  max = 2200
  
  if hname.find("gen_Mass") != -1:
    min = 0
    max = 305
  
  if hname.find("Tau21") != -1 or hname.find("DDT") != -1 :
    min = 0
    max = 1  

  #l = TLegend(.16,.7,.4,.9)
  l = TLegend(0.4861809,0.7020725,0.6859296,0.9209845)
  l.SetTextSize(0.035)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  

  histtmp = TProfile(filetmp.Get(hname))
  histtmp.SetName(filetmp.GetName())
  histos.append(histtmp)

for j in xrange(0,len(histos)):
  # histos[j].SetLineColor(col.GetColor(palette[j %4]))
  # histos[j].SetLineStyle(lineStyle[j])
  # histos[j].SetLineWidth(3)
  histos[j].Rebin(rebin)
  histos[j].SetMarkerStyle(markerStyle[j])
  histos[j].SetMarkerColor(col.GetColor(palette[j %4]))
  legend = legendname[j]
  l.AddEntry(histos[j],legend,"p")

  
fits = []
for h in histos:
  fittmp = TGraph(h)
  fits.append(fittmp)
  

yTitle = "Arbitrary scale"
 
canv = getCanvas()
canv.cd()
vFrame = canv.DrawFrame(min,setYmin,max,setYmax)  
vFrame.SetXTitle(titles[0])
vFrame.SetYTitle(yTitle)
vFrame.GetXaxis().SetTitleSize(0.06)
vFrame.GetXaxis().SetTitleOffset(0.95)
vFrame.GetXaxis().SetLabelSize(0.05)
vFrame.GetYaxis().SetTitleSize(0.06)
#vFrame.GetYaxis().SetTitleOffset(1.0)
vFrame.GetYaxis().SetLabelSize(0.05)
vFrame.GetXaxis().SetNdivisions(408)
vFrame.GetYaxis().SetNdivisions(404)


if doFit:
  for f in fits: f.Draw("Csame")      
else:
  for h in histos: h.Draw("sameEMP")



l1 = TLatex()
l1.SetNDC()
l1.SetTextAlign(12)
l1.SetTextFont(42)
l1.SetTextSize(0.025)
l1.DrawLatex(0.20,0.86, "AK, R= 0.8")
# if hname.find("Mass") != -1 and not hname.find("UnCorr") != -1: l1.DrawLatex(0.20,0.83, "L2L3 corrected")
l1.DrawLatex(0.20,0.80, "p_{T} > 200 GeV, |#eta| < 2.5")
# if not hname.find("Mass") != -1: l1.DrawLatex(0.20,0.76, "65 GeV < M_{G} < 105 GeV")

# l1.DrawLatex(0.7,0.42,"65 GeV < M_{p} < 105 GeV")

l.Draw("same")
CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
canv.Update()
canvname = "plots80X/%s.pdf"%hname
canv.SaveAs(canvname,"pdf")
canv.SaveAs(canvname.replace("pdf","root"),"pdf")
time.sleep(100)
