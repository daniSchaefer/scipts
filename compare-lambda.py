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

rebin = 30

setmax = 0.39
prefix = '80X/'
addBKG = True
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
 
 colors = ['#336B87','#336B87','#763626','#763626','#a6dba0','#92c5de','#4393c3','#2166ac','#053061']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
palette = get_palette('gv')

col = TColor()
  
files = [ 
  'ExoDiBosonAnalysis.lambda1TeV_QstarQW_13TeV_1000GeV.qV.root',
  'ExoDiBosonAnalysis.lambdaM_QstarQW_13TeV_1000GeV.qV.root',
  'ExoDiBosonAnalysis.lambda1TeV_QstarQW_13TeV_4000GeV.qV.root',
  'ExoDiBosonAnalysis.lambdaM_QstarQW_13TeV_4000GeV.qV.root'
          ]


legendname = [ "M_{q*}=1 TeV, #Lambda=1 TeV (old)",
               "M_{q*}=1 TeV, #Lambda=M_{q*} (new)",       
               "M_{q*}=4 TeV, #Lambda=1 TeV (old)",
               "M_{q*}=4 TeV, #Lambda=M_{q*} (new)",     
             ]
                

histonames = ['Mjj_genMatched']
titles     = ['M_{jj}']
lineStyle = [3,1,3,1]



ii = -1
for hname in histonames:
  print "Working on histogram " ,hname
  ii += 1
  
  min = 0
  max = 5600
  
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


  filelist = []
  histos = []

  for f in files:
    filename = prefix + f
    filetmp = TFile.Open(filename,"READ") 
    filelist.append(filetmp)
    
  for f in filelist:
      histtmp = TH1F(f.Get(hname))
      histtmp.SetName(f.GetName())
      histos.append(histtmp)

  for j in xrange(0,len(histos)):
    histos[j].SetLineColor(col.GetColor(palette[j]))
    histos[j].SetLineStyle(lineStyle[j])
    histos[j].SetLineWidth(3)
    histos[j].Rebin(rebin)
    histos[j].Scale(1./histos[j].Integral())
    legend = legendname[j]
    l.AddEntry(histos[j],legend,"l")
  
  fits = []
  for h in histos:
    fittmp = TGraph(h)
    fits.append(fittmp)
  

  yTitle = "Arbitrary scale"
   
  canv = getCanvas()
  canv.cd()
  setmax = histos[0].GetMaximum()*1.5
  vFrame = canv.DrawFrame(min,0.000005,max,setmax)  
  vFrame.SetXTitle(titles[ii])
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
    for h in histos: h.Draw("sameHIST")

  


  l1 = TLatex()
  l1.SetNDC()
  l1.SetTextAlign(12)
  l1.SetTextFont(42)
  l1.SetTextSize(0.025)
  l1.DrawLatex(0.20,0.83, "AK, R= 0.8")
  l1.DrawLatex(0.20,0.86, "q*#rightarrowqW")
  l1.DrawLatex(0.20,0.80, "p_{T} > 200 GeV, |#eta| #leq 2.5")  
 
  # l1.DrawLatex(0.7,0.42,"65 GeV < M_{p} < 105 GeV")
  

   
  l.Draw("same")
  CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  canv.Update()
  canvname = "plots80X/lambdaCompare_%s.pdf"%hname
  canv.SaveAs(canvname,"pdf")
  canv.SaveAs(canvname.replace("pdf","root"),"pdf")
  time.sleep(200)
