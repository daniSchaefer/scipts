import ROOT
import sys
from ROOT import *
import CMS_lumi, tdrstyle
import time
from array import array

##################################################################################
def get_canvas(cname):

  #CMS_lumi.lumi_8TeV = "19.7 fb^{-1}"
  CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
  CMS_lumi.writeExtraText = 0
  CMS_lumi.extraText = "Preliminary"

  iPos = 11
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  iPeriod=4
  
  H_ref = 700; 
  W_ref = 700; 
  W = W_ref
  H  = H_ref

  T = 0.08*H_ref
  B = 0.12*H_ref 
  L = 0.12*W_ref
  R = 0.04*W_ref

  canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)
  canvas.SetLeftMargin( L/W )
  canvas.SetRightMargin( R/W )
  canvas.SetTopMargin( T/H )
  canvas.SetBottomMargin( B/H )
  #canvas.SetLeftMargin( 0.18 )
  #canvas.SetRightMargin( 0.06 )
  #canvas.SetTopMargin( 0.05 )
  #canvas.SetBottomMargin( 0.12 )
  canvas.SetTickx()
  canvas.SetTicky()
  canvas.SetGrid()
  
  return canvas

##################################################################################
def fill_histos_for_contour(mass,limit,max_width):
 
  hname = ['h_M'+str(mass)+'_xsec','h_M'+str(mass)+'_width']
  h_list = []
  h_list.append(ROOT.TH2F(hname[0], hname[0], 60,  0., 4., 60,  0., 2.)) #20,-4.,0.,20,0,2.
  h_list.append(ROOT.TH2F(hname[1], hname[1], 60,  0., 4., 60,  0., 2.))
      
  fname13 = 'scanHVT-M%s.root'%mass
  f13 = TFile.Open(fname13,"READ")
  t13 = f13.Get("hvtM%s"%mass)

  gV = array('f',[0])
  cH = array('f',[0])
  cF = array('f',[0])
  g = array('f',[0])
  br_ratio_WW = array('f',[0])
  br_ratio_WZ = array('f',[0])
  brvv13 = array('f',[0])
  brvv8 = array('f',[0])
  brvh13 = array('f',[0])
  brvh8 = array('f',[0])
  w = array('f',[0])

  t13.SetBranchAddress('gV', gV)
  t13.SetBranchAddress('cH', cH)
  t13.SetBranchAddress('cF', cF)
  t13.SetBranchAddress('g', g)
  t13.SetBranchAddress('br_WW_13TeV', br_ratio_WW)
  t13.SetBranchAddress('br_WZ_13TeV', br_ratio_WZ)
  t13.SetBranchAddress('xsecTot_WV_13TeV', brvv13)
  t13.SetBranchAddress('xsecTot_WV_8TeV', brvv8)
  t13.SetBranchAddress('xsecTot_VH_13TeV', brvh13)
  t13.SetBranchAddress('xsecTot_VH_8TeV', brvh8)
  t13.SetBranchAddress('width_Wp_13TeV', w)
       
  for e in range(t13.GetEntries()):
   t13.GetEntry(e)
   #br = brvv8[0]+brvh8[0]+brvv13[0]+brvh13[0] -> combination of 8 and 14 TeV as well as WV and VH analysis
   br = brvv13[0]#*br_ratio_WZ[0]
   if br < limit:
     h_list[0].Fill(gV[0]*cH[0],g[0]*g[0]*cF[0]/gV[0])
   #print max_width
   if (w[0]/float(mass) - max_width) < 0.00019 :
     h_list[1].Fill(gV[0]*cH[0],g[0]*g[0]*cF[0]/gV[0])
	  
  for h in h_list:
   for bx in xrange(1,h.GetNbinsX()+1):
    for by in xrange(1,h.GetNbinsY()+1):
     ne = h.GetBinContent(bx,by)
     if ne != 0:
        h.SetBinContent(bx,by,1)
  
  return h_list

##################################################################################
def plot_graphs_for_contour(histo,opt):

   c = ROOT.TCanvas()
   c.cd()

   histo.Smooth()
   histo.SetContour(2)
   #histo.Draw("COLZ")
   histo.Draw("CONT Z LIST")
   #time.sleep(1000)

   c.Update()

   curves = []
   
   conts = ROOT.TObjArray(gROOT.GetListOfSpecials().FindObject("contours"))
   
   gs = ROOT.TGraphSmooth("normal")
   gin = ROOT.TGraph(conts.At(0).At(0))
   gout = gs.SmoothSuper(gin,"",3)

   x_m = array('d',[])
   x_p = array('d',[])
   y_m = array('d',[])
   y_p = array('d',[])
   npoints = gout.GetN()
   for p in xrange(0,npoints):
    gr_x = ROOT.Double(0.)
    gr_y = ROOT.Double(0.)
    gout.GetPoint(p,gr_x,gr_y)
    x_m.append(-gr_x)
    y_m.append(-gr_y)
    x_p.append(gr_x)
    y_p.append(gr_y)

   if opt == 'w':
    x_p[0] = 0.
    x_m[0] = 0.
      
   curves.append(ROOT.TGraph(len(x_p),x_p,y_p))
   curves.append(ROOT.TGraph(len(x_m),x_m,y_m))
   curves.append(ROOT.TGraph(len(x_p),x_p,y_m))
   curves.append(ROOT.TGraph(len(x_m),x_m,y_p))
   
   c.Close()  

   return curves

##################################################################################
def write_extra_text(text,textpos,col,opts):

   ptext = ROOT.TPaveText(textpos[0],textpos[1],textpos[2],textpos[3],"NDC")
   ptext.SetTextFont(42)
   ptext.SetTextSize(0.036)
   ptext.SetTextAlign(12)
   ptext.SetFillStyle(0)
   ptext.SetFillColor(0)
   ptext.SetBorderSize(0)
   ptext.SetTextColor(col)
   ptext.AddText(text)
   
   if opts == 'w':
      ptext.SetFillStyle(0)
      ptext.SetTextSize(0.03)
      ptext.SetFillColor(kWhite)

   return ptext

##################################################################################
gROOT.SetBatch(ROOT.kTRUE)
#obs_lim = {'1500': 0.0402,'2000': 0.0282,'3000': 0.0241, '3500':0.00570} #8+13 TeV runB  WV+VH combo

# cross section*BR_fraction limits for Wprime to WZ model
 #observed limit for M=1500 GeV 0.0131596165727
 #observed limit for M=2000 GeV 0.0119851681581
 #observed limit for M=3000 GeV 0.00201076705332
 #observed limit for M=3500 GeV 0.000661402835783
obs_lim_Wprime = {'1500': 0.0132 , '2000': 0.0120  , '3000': 0.0020 , '3500': 0.0007  } #observed limit x branching_ratio  for full 13 TeV dataset
# branching_ratio = (0.6991*0.6760) since W' is an exclusive sample
obs_lim_Wprime = {'1500': 0.0132 , '2000': 0.0120  , '3500': 0.0007  } 


# cross section*BR_fraction limits for Zprime to WW model
  #observed limit for M=1500 GeV 0.00976174019721
  #observed limit for M=2000 GeV 0.00917084383571
  #observed limit for M=3000 GeV 0.00142709199701
  #observed limit for M=3500 GeV 0.00080688451398
obs_lim_Zprime = {'1500': 0.0098 , '2000': 0.0092  , '3000': 0.0014 , '3500': 0.0008  } #observed limit x branching-ratio for full 13 TeV dataset
# branching_ratio = 1. since Z' is an inclusive sample

obs_lim = obs_lim_Wprime

max_width = 0.050
#models = ['A1','B']
models = ['B']

print ""

histos = {}

for m,l in obs_lim.iteritems():

   print "M %s : preparing 2D histos for width and xsec contours" %(m)
   histos[m] = fill_histos_for_contour(m,l,max_width)

print ""

g_xsec = {}
g_width = {}

for m in histos.keys():

   print "M %s : preparing graphs for width and xsec contours" %(m)
   g_width[m] = plot_graphs_for_contour(histos[m][1],'w')
   g_xsec[m] = plot_graphs_for_contour(histos[m][0],'')

##################################################################################   
colors = {'1000':kAzure+1,'1500':kBlack,'2000':kViolet+7, '3000': kTeal-8, '3500':kGreen+2}
linestyle = {'1000':1,'1500':8,'2000':1,'3000':7,'3500':1}
lim_text_pos = {'1000':[0.5138191,0.4825175,0.5942211,0.5629371],'1500':[0.4468391,0.485119,0.5948276,0.5550595],
                '2000':[0.6206897,0.2752976,0.6925287,0.3452381],'3000':[0.6609195,0.7276786,0.7284483,0.797619],'3500':[0.6896552,0.5803571,0.7571839,0.6502976]}
lim_extra_text = {'1000':'1 TeV','1500':'1.5 TeV','2000':'2 TeV','3000':'3 TeV','3500':'3.5 TeV'}
#models_text_pos = {'A1':[0.34,0.41,0.40,0.48],'A2':[0.33,0.65,0.39,0.72],'A3':[0.51,0.54,0.57,0.61],'A4':[0.14,0.65,0.20,0.72],'A5':[0.14,0.49,0.20,0.56],'B':[0.1508621,0.54,0.2025862,0.62]}
#models_point = {'B':[-2.928729,0.13883712988411501],'A1':[-0.9,-0.154917],'A2':[-1,0.4225],'A3':[-0.3,0.14083],'A4':[-3,0.4225],'A5':[-3,0.014083]}
#models_extra_text = {'A1':'A(g_{V}=1)','A3':'A(g_{V}=3)','B':'B'}
models_text_pos = {'A1':[0.43,0.30,0.49,0.37],'A2':[0.33,0.65,0.39,0.72],'A3':[0.51,0.54,0.57,0.61],'A4':[0.14,0.65,0.20,0.72],'A5':[0.14,0.49,0.20,0.56],'B':[0.1508621,0.54,0.2025862,0.62]}
models_point = {'B':[-2.928729,0.13883712988411501],'A1':[-0.555969,-0.5326010579364125],'A2':[-1,0.4225],'A3':[-0.3,0.14083],'A4':[-3,0.4225],'A5':[-3,0.014083]}
models_extra_text = {'A1':'A','A3':'A(g_{V}=3)','B':'B'}
width_extra_text = ['#frac{#Gamma_{th}}{M} > 5% #approx #frac{#sigma_{exp}}{M}']
width_text_pos = [0.13,0.14,0.33,0.21]

tdrstyle.setTDRStyle()

canv = get_canvas("canv")
canv.cd()

mg = ROOT.TMultiGraph("mg","mg")

leg = ROOT.TLegend(0.7083333,0.6517857,0.9181034,0.7827381)
leg.SetBorderSize(0)
leg.SetShadowColor(0)
leg.SetFillColor(0)
#leg.SetFillStyle(0)
leg.SetTextSize(0.036)
leg.SetTextFont(42)
leg.SetMargin(0.35)

linewidth = [3502,3502,-3502,-3502]

idx = 0
for g in g_width['2000']:

   g.SetLineColor(kGray)
   g.SetLineStyle(7)
   g.SetFillColor(kGray)
   g.SetFillStyle(1001)
   g.SetLineWidth(linewidth[idx])
   g.RemovePoint(3)
   mg.Add(g)
   idx = idx+1
      
for m in obs_lim.keys():
 i = 0
 for g in g_xsec[m]: 
  g.SetName("gr%i_M%s"%(i,m))
  g.SetLineWidth(2)
  if m == '3000': g.SetLineWidth(3)
  g.SetLineColor(colors[m])
  g.SetLineStyle(linestyle[m])
  mg.Add(g)
  i+=1
 leg.AddEntry(g,lim_extra_text[m],"L")
     
mg.Draw("AL")   
mg.GetXaxis().SetTitle("g_{V}c_{H}") 
mg.GetXaxis().SetRangeUser(-3,3)
mg.GetXaxis().SetTitleSize(0.05) 
mg.GetXaxis().SetTitleOffset(1.1)
mg.GetYaxis().SetTitle("g^{2}c_{F}/g_{V}")
mg.GetYaxis().SetTitleSize(0.05)  
mg.GetYaxis().SetTitleOffset(1.1)
mg.GetYaxis().SetRangeUser(-1.,1.)
mg.GetYaxis().SetNdivisions(505)

add_text = []
#for m in lim_text_pos.keys():
for m in obs_lim.keys():
  add_text.append(write_extra_text(lim_extra_text[m],lim_text_pos[m],colors[m],''))

g_models = []
mcols = {'B':kMagenta,'A1':kMagenta,'A2':kBlue,'A3':kOrange,'A4':kAzure+8,'A5':kRed}
for m in models:
 x = array('d',[models_point[m][0]])
 y = array('d',[models_point[m][1]])
 g_models.append(ROOT.TGraph(1,x,y))
 add_text.append(write_extra_text(models_extra_text[m],models_text_pos[m],mcols[m],''))
 
for g in range(len(g_models)):
 g_models[g].SetMarkerStyle(21)
 g_models[g].SetMarkerColor(mcols[models[g]])
 g_models[g].Draw("Psame")

add_text.append(write_extra_text(width_extra_text[0],width_text_pos,kBlack,'w'))

for t in add_text:
   t.Draw()

#leg.Draw()

       
#--------------------------------
canv.Update()
canv.cd()

CMS_lumi.CMS_lumi(canv, 4, 11)
		
canv.cd()
canv.Update()
canv.RedrawAxis()
canv.RedrawAxis("g")
frame = canv.GetFrame()
frame.Draw()   
canv.cd()
canv.Update()

canv.SaveAs("hvt-couplings.pdf")
canv.SaveAs("hvt-couplings.png")
canv.SaveAs("hvt-couplings.eps")
canv.SaveAs("hvt-couplings.root")
