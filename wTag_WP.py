import sys
from ROOT import *
import time
import math
import CMS_lumi, tdrstyle

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4


wp = 0.60
sname1 = "$HOME/EXOVVAnalysisRunII/ExoDiBosonAnalysis/ExoDiBosonAnalysis.M-2000.BulkWW.root"
sfile1 = TFile.Open(sname1,"READ")
intreeS1 = sfile1.Get("tree")
cutstring = "jet_tau2tau1_jet1 <= %.2f" %wp
num = float(intreeS1.GetEntries(cutstring))
den = float(intreeS1.GetEntries())
eff = float(num/den)
print "----------------"
print "For normal Tau21:"
print "Efficiency = %.1f %% (%i/%i)" %(eff*100,num,den)
print "For WP <= %.2f" %wp

cutmax = [x*0.01 for x in range(0,100)]

sname = "$HOME/EXOVVAnalysisRunII/ExoDiBosonAnalysis/ExoDiBosonAnalysis.M-2000-puppiSD.BulkWW.root"
sfile = TFile.Open(sname,"READ")
intreeS = sfile.Get("tree")
den = intreeS.GetEntries()


rebin = 4

W = 800
H = 800
H_ref = 700 
W_ref = 600 
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref
canv = TCanvas("canv","canv",W,H)
canv.cd()
intreeS1.Draw("jet_tau2tau1_jet1","","hist")
intreeS.Draw("jet_puppi_tau2tau1_jet1","","histSAME")
intreeS.Draw("jet_ddt_jet1","","histSAME")

hTAU21 = gPad.GetListOfPrimitives().At(0)
hPUPPITAU21 = gPad.GetListOfPrimitives().At(1)
hDDT = gPad.GetListOfPrimitives().At(2)

hTAU21.GetXaxis().SetTitle("W-tag working point") 
hTAU21.GetYaxis().SetTitle("A.U") 
hTAU21.SetLineColor(kTeal-5) 
hPUPPITAU21.SetLineColor(kMagenta-2) 
hDDT.SetLineColor(kRed+1) 
hTAU21.Rebin(rebin) 
hPUPPITAU21.Rebin(rebin) 
hDDT.Rebin(rebin) 
hTAU21.SetLineStyle(1) 
hPUPPITAU21.SetLineStyle(2) 
hDDT.SetLineStyle(9) 
hTAU21.SetLineWidth(3) 
hPUPPITAU21.SetLineWidth(3) 
hDDT.SetLineWidth(3) 
hTAU21.Scale(1./hTAU21.Integral()) 
hPUPPITAU21.Scale(1./hPUPPITAU21.Integral()) 
hDDT.Scale(1./hDDT.Integral()) 


hTAU21.SetMaximum(hTAU21.GetMaximum()*1.6) 

legend = TLegend(0.5863032,0.706088,0.7345569,0.852371)
legend.SetTextSize(0.038)
legend.SetLineColor(0)
legend.SetShadowColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetMargin(0.35)
legend.AddEntry(hTAU21,"#tau_{21}","l")
legend.AddEntry(hPUPPITAU21,"PUPPI #tau_{21}","l")
legend.AddEntry(hDDT,"DDT","l")
legend.Draw("same")

addInfo = TPaveText(0.1863032,0.86088,0.2345569,0.892371,"NDC")
addInfo.AddText("G_{Bulk}(2 TeV)#rightarrowWW")
addInfo.SetFillColor(0)
addInfo.SetLineColor(0)
addInfo.SetFillStyle(0)
addInfo.SetBorderSize(0)
addInfo.SetTextFont(42)
addInfo.SetTextSize(0.040)
addInfo.SetTextAlign(12)
addInfo.Draw("same")
CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
canvasname = "wTaggers%.2f.pdf" %wp
canv.Print(canvasname,"pdf")
time.sleep(20)


ddt = True
puppi = True
for cut in cutmax:
  cutPUPPI = '(jet_puppi_tau2tau1_jet1 <= %f)' %(cut)
  cutDDT   = '(jet_ddt_jet1 <= %f )' %(cut) 
  nsigPUPPI = float(intreeS.GetEntries(cutPUPPI))
  nsigDDT = float(intreeS.GetEntries(cutDDT))
  
  esPUPPI = nsigPUPPI/den
  esDDT   = nsigDDT/den
  
  if puppi and esPUPPI >= eff:
    puppi = False
    print "----------------"
    print "For PUPPI Tau21:"
    print "Efficiency = %.1f %% (%i/%i)" %(esPUPPI*100,nsigPUPPI,den)
    print "For WP <= %.2f" %cut

  if ddt and esDDT >= eff:
    ddt = False
    print "----------------"
    print "For DDT:"
    print "Efficiency = %.1f %% (%i/%i)" %(esDDT*100,nsigDDT,den)
    print "For WP <= %.2f" %cut  

  if not ddt and not puppi:
    print "----------------"
    print "DONE!"
    break
