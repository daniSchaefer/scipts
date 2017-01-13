from ROOT import *
import time
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11

if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref
iPeriod = 0

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.13*W_ref
R = 0.04*W_ref

def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#763626','#336B87','#FF420E','#80BD9E','#336B87','#763626','#003B46','#66A5AD']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()

path = "/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/"
rebin = 1

# gROOT.SetBatch(kTRUE)
      
i =0
histolist = []

filetmp = TFile.Open(path+'ExoDiBosonAnalysis.BulkWW_13TeV_1800GeV.VV.root',"READ") 
intree = filetmp.Get("tree")

histolist=[]

nbins = 100
min = 1300
max = 2300

WWHP = TH1F('DijetMassHighPuriWW','DijetMassHighPuriWW', nbins,min,max)
WWHP_reduced = TH1F('DijetMassHighPuriWW_reduced','DijetMassHighPuriWW_reduced',nbins,min,max)



histolist.append(WWHP)
histolist.append(WWHP_reduced)

for event in intree:
  if ( event.MVV < 955.): continue
  
  if event.jet_puppi_tau2tau1_jet2 <= 0.40 and event.jet_puppi_tau2tau1_jet1 <= 0.40 :
    if (65 < event.jet_puppi_softdrop_jet1 <= 85. and 65 < event.jet_puppi_softdrop_jet2 <= 85.) :  
      WWHP.Fill(event.MVV) #WWHP
      WWHP_reduced.Fill(event.MVV_reduced) #WWHP
   
l = TLegend(0.6078894,0.5958549,0.76027638,0.8782383)
l.SetTextSize(0.034)
l.SetTextFont(42)
l.SetLineColor(0)
l.SetShadowColor(0)
l.SetLineStyle(1)
l.SetLineWidth(1)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetMargin(0.35)


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

maxbin=0
maxcontent=0
startbin = 0
for b in range(WWHP.GetXaxis().GetNbins()):
  if WWHP.GetXaxis().GetBinCenter(b+1) > startbin and WWHP.GetBinContent(b+1)>maxcontent:
    maxbin = b
    maxcontent = WWHP.GetBinContent(b+1)   
tmpmean = WWHP.GetXaxis().GetBinCenter(maxbin)  
print "tmpmean = " ,tmpmean
tmpwidth = 1800*0.3 
g1 = TF1("g1","gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
WWHP.Fit(g1, "SR")
WWHP.Fit(g1, "SR")
WWHP.Fit(g1, "SR")
mean    = g1.GetParameter(1)
meanerr = g1.GetParError(1)
sigma    = g1.GetParameter(2)
sigmaerr = g1.GetParError(2)

l.AddEntry(WWHP,"Raw M_{jj}","l")
l.AddEntry(0,"<m> = %i #pm %i GeV"%(mean,meanerr),"")
l.AddEntry(0,"#sigma = %.1f #pm %.1f GeV"%(sigma,sigmaerr),"")
l.AddEntry(0,"","")

maxbin=0
maxcontent=0
startbin = 0
for b in range(WWHP_reduced.GetXaxis().GetNbins()):
  if WWHP_reduced.GetXaxis().GetBinCenter(b+1) > startbin and WWHP_reduced.GetBinContent(b+1)>maxcontent:
    maxbin = b
    maxcontent = WWHP_reduced.GetBinContent(b+1)   
tmpmean = WWHP_reduced.GetXaxis().GetBinCenter(maxbin)  
print "tmpmean = " ,tmpmean
tmpwidth = 1800*0.15 
g2 = TF1("g2","gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
WWHP_reduced.Fit(g2, "SR")
WWHP_reduced.Fit(g2, "SR")
WWHP_reduced.Fit(g2, "SR")
mean    = g2.GetParameter(1)
meanerr = g2.GetParError(1)
sigma    = g2.GetParameter(2)
sigmaerr = g2.GetParError(2)
l.AddEntry(WWHP_reduced,"Reduced M_{jj}","l")
l.AddEntry(0,"<m> = %i #pm %i GeV"%(mean,meanerr),"")
l.AddEntry(0,"#sigma = %.1f #pm %.1f GeV"%(sigma,sigmaerr),"")


WWHP.SetLineColor(col.GetColor(palette[0]))
WWHP_reduced.SetLineColor(col.GetColor(palette[1]))
WWHP.SetLineWidth(3)
WWHP_reduced.SetLineWidth(3)
WWHP_reduced.SetLineStyle(3)
# WWHP.Scale(1./WWHP.Integral())
# WWHP_reduced.Scale(1./WWHP_reduced.Integral())
WWHP.Draw("HIST")
WWHP_reduced.Draw("HISTsame")
# g1.Draw("same")
# g2.Draw("same")
WWHP.SetMaximum(WWHP.GetMaximum()*1.5)
WWHP.GetYaxis().SetTitleOffset(1.07)
WWHP.GetXaxis().SetTitle("M_{jj} (GeV)")
WWHP.GetYaxis().SetTitle("MC events / %i GeV"%((max-min)/nbins))
WWHP.GetYaxis().SetNdivisions(403)
WWHP.GetXaxis().SetNdivisions(307)
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
SetOwnership( l, 1 )

# line = TLine(1800,0,1800,0.17)
# line.SetLineColor(kBlack)
# line.SetLineStyle(1)
# line.SetLineWidth(3)
# line.Draw("same")
canvas.RedrawAxis()

addInfo = TPaveText(0.6620603,0.3354922,0.9522613,0.4520725,"NDC")
addInfo.SetFillColor(0)
addInfo.SetLineColor(0)
addInfo.SetFillStyle(0)
addInfo.SetBorderSize(0)
addInfo.SetTextFont(42)
addInfo.SetTextSize(0.030)
addInfo.SetTextAlign(12)
addInfo.AddText("WWHP category")
addInfo.AddText("G_{Bulk}(1.8 TeV)#rightarrow WW")
addInfo.Draw("same")
canvas.Update()



l.Draw("same")
canvas.Update()  
cname = "ReducedMass.pdf"
canvas.SaveAs(cname)
canvas.SaveAs(cname.replace(".pdf",".root"))
time.sleep(500)
