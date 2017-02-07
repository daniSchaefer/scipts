# see: https://arxiv.org/pdf/physics/0308063v2.pdf for explanation of punzi significance
# use a confidence level for exclusion limits of 95% i.e. ~2 sigma


import sys
from array import *
  
from ROOT import *
import time
import math
import numpy as np

import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()
gStyle.SetOptFit(0) 
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
# gROOT.SetBatch(True)
fillStyle = [3018  ,3002  ,3005, 3003,1001 ,1001,1001,1001 ,1001,1001,1001 ,1001    ]
lineColor = [1,210,2,4,kPink,kAzure+8,kPink-7,8,9]
lineStyle = [1,1,1,1,2,2,2,2]
markerStyles = [20,22,26,31,32,33,34,35,36]
lumi = 36814.

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4
def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#762a83','#de77ae','#a6dba0','#4393c3','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 #colors = ['#762a83','#de77ae','#a6dba0','#4393c3','#4393c3']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
 

def getSigFileList(masses,prefix):
        
    sigfiles = []
    for m in masses:
        if Signal=="Wprime":
            sigfiles.append('ExoDiBosonAnalysis.'+Signal+'WZ_13TeV_'+str(int(1000*m))+'GeV.VV.root')
        else:
            sigfiles.append('ExoDiBosonAnalysis.'+Signal+'WW_13TeV_'+str(int(1000*m))+'GeV.VV.root')

    sigfilelist = []  
    for sigf in sigfiles:
        filename = prefix+sigf
        print filename
        print sigMass(filename)
        filetmp = TFile.Open(filename,"READ") 
        sigfilelist.append(filetmp)
    result = [sigfilelist,sigfiles]
    return result


def sigMass(filename):
    s = filename.split("_")
    s2 = s[2].split("GeV")
    return s2[0]



def getPunzi2(fsig,fbkg,massup,massdown,category):
    testcuts =[]
    c = 0
    testcuts.append(100)
    for i in range(1,100):
        c = 0 + i/100.
        testcuts.append(c*100)
    punzi=[]
    #print testcuts
    ressig = getNevents(fsig, testcuts, massup, massdown,category)
    resbkg = getNevents(fbkg, testcuts, massup, massdown,category)
    denBKG = resbkg[0]
    denSIG = ressig[0]
    es = []
    for s in range(1,len(ressig)):
        es = ressig[s]/denSIG
        eb = resbkg[s]/denBKG
        ps = es/(1+math.sqrt(resbkg[s]*lumi))
        punzi.append(ps)
        #print "cut : "+str(testcuts[s])+" punzi: "+str(ps)
    
        
    apunzi = array('d',punzi)
    atestcuts = array('d',testcuts)
    
    c = TCanvas("c","c",400,400)
    g = TGraph(len(apunzi),atestcuts, apunzi)
    g.Draw("ALP")
    c.SaveAs("PunziOverCut_M"+str(int(massup*(1/1.2)))+"_"+cat+".pdf")
    #time.sleep(20)
    
    max_value = max(punzi)
    max_index = punzi.index(max_value)
    max_cut = testcuts[max_index]*0.01
    
    dict_res = {}
    for index in range(1,len(testcuts)):
        dict_res[int(testcuts[index])] = punzi[index-1]
        #print int(testcuts[index])
    dict_res['maxcut'] = max_cut
    dict_res['maxvalue']= max_value
    #print max_index
    #print max_value
    #print max_cut
    result =[max_value,max_cut]
    return dict_res
    
        

def getPunziGraphs(category, masses,sigfilelist,filenames , lumi, fbkg,outdir,rebin):
    histos = []
    ii = 0
    maxmass = array('d',[])
    maxpunzi = array('d',[])
    maxcuts = array('d',[])
    maxcutsup = array('d',[])
    maxcutsdown = array('d',[])
    maxes = array('d',[])
    maxB = array('d',[])

    cut075punzi = array('d',[])
    cut075 = array('d',[])

    cut06punzi = array('d',[])
    cut06 = array('d',[])

    cut05punzi = array('d',[])
    cut05 = array('d',[])

    cut055punzi = array('d',[])
    cut055 = array('d',[])

    cut045  = array('d',[])
    cut045punzi = array('d',[])
    
    cut040  = array('d',[])
    cut040punzi = array('d',[])
    
    cut030  = array('d',[])
    cut030punzi = array('d',[])
    
    cut035  = array('d',[])
    cut035punzi = array('d',[])

    for file in sigfilelist:
        m = masses[ii]
        mass = m*1000
        print 'Mass set to %i' %mass
        punzi = array('d',[])
        cuts = array('d',[])
        ES = array('d',[])
        B = array('d',[])
        i = 0
        
        r = getPunzi2(file,fbkg,mass*1.2,mass*0.8,category)
        maxpunzi.append(r['maxvalue'])
        maxcuts.append(r['maxcut'])
        maxcutsup.append(r['maxcut']*1.1)
        maxcutsdown.append(r['maxcut']*0.9)
        maxmass.append(mass)
        
        ListOfAllcuts = [100,75,60,50,55,45,40,35,30]
        
        
        
        #denBKG = resBkg[0]
        #denSIG = resSig[0]
        #print "ALL BKG = %f" %(denBKG*lumi)
        #print "ALL SIG = %f" %denSIG
        print "====================="
        print maxcuts
        print maxmass
        print "====================="
        ii+=1
        ListOfcuts = [75,60,50,55,45,40,35,30]
        ind = 0
        for x in ListOfcuts:
            ind +=1
            #numBKG = resBkg[ind]
            #numSIG = resSig[ind]
            ps = r[x]
            cut = x/100.
            #eb = numBKG/denBKG   
            #es = numSIG/denSIG
            #ps = es/(1+math.sqrt(numBKG))
            #punzi.append(ps)
            #cuts.append(cut)
            #ES.append(es)
            #B.append(numBKG)
            if (x==75):
                cut075punzi.append(ps)  
                cut075.append(cut)
            if (x==60):
                cut06punzi.append(ps)  
                cut06.append(cut)  
            if (x==55):
                cut055punzi.append(ps)  
                cut055.append(cut)
            if (x==50):
                cut05punzi.append(ps)  
                cut05.append(cut)    
            if (x==45):
                cut045punzi.append(ps)  
                cut045.append(cut)  
            if (x==40):
                cut040punzi.append(ps)  
                cut040.append(cut)  
            if (x==30):
                cut030punzi.append(ps)  
                cut030.append(cut)  
            if (x==35):
                cut035punzi.append(ps)  
                cut035.append(cut)  
            #print " Cut = %0.2f"%cut
            #print "Signal numerator: %i" %(numSIG*lumi)
            #print "Signal denominator: %i" %(denSIG*lumi)
            #print "Signal efficiency: %0.3f" %(es)
            #print "Total background: %i" %(numBKG*lumi)
            #print "PUNZI: %f" %(ps)
            #print "---------------------------"

        del punzi[:]
        del cuts[:]
        del ES[:]
        del B[:]
    
    
    
    l2 = TLegend(.2,.68,.65,.75)
    l2.SetBorderSize(0)
    l2.SetFillColor(0)
    l2.SetTextFont(42)
    l2.SetTextSize(0.035)

    cut030punziRatio = array('d',[])
    cut035punziRatio = array('d',[])
    cut040punziRatio = array('d',[])
    cut045punziRatio = array('d',[])
    cut05punziRatio = array('d',[])
    cut055punziRatio = array('d',[])
    cut06punziRatio = array('d',[])
    cut075punziRatio = array('d',[])
    for i in range (0,len(maxpunzi)):
        cut040punziRatio.append(cut040punzi[i]/maxpunzi[i])
        cut045punziRatio.append(cut045punzi[i]/maxpunzi[i])
        cut05punziRatio.append(cut05punzi[i]/maxpunzi[i])
        cut055punziRatio.append(cut055punzi[i]/maxpunzi[i])
        cut06punziRatio.append(cut06punzi[i]/maxpunzi[i])
        cut075punziRatio.append(cut075punzi[i]/maxpunzi[i])
        cut030punziRatio.append(cut030punzi[i]/maxpunzi[i])
        cut035punziRatio.append(cut035punzi[i]/maxpunzi[i])
  
  
    print "maxpunzi: ===================================================="
    print maxpunzi
    print "============================================================="

    l1 = TLatex()
    l1.SetNDC()
    l1.SetTextAlign(12)

    c2 = TCanvas("c2", "",800,800)
    c2.cd()
    #c2.SetGridx()
    #c2.SetGridy()
    
    n = len(maxcuts)
    gr10perBand = TGraph(2*n)
    for i in range(0,n):
        gr10perBand.SetPoint(i,maxmass[i],maxcutsup[i])
        gr10perBand.SetPoint(n+i,maxmass[n-i-1],maxcutsdown[n-i-1])

    
    g = TGraph(len(maxcuts), maxmass,maxcuts)
    gup = TGraph(len(maxcuts), maxmass,maxcutsup)
    gdown = TGraph(len(maxcuts), maxmass,maxcutsdown)
    g.SetLineWidth(2)
    g.GetXaxis().SetTitle('M_{X} (TeV)')
    g.GetYaxis().SetTitle("Optimal cut")
    g.SetMarkerStyle(22)
    g.SetMarkerSize(3)
    g.SetMarkerColor(kRed-3)
    g.GetYaxis().SetRangeUser(0.,1.)
    l2.SetFillColor(0)
    if not Signal=="Wprime":l2.AddEntry(g,"G_{%s}: Optimal #tau_{21} cut"%Signal,"p")
    if Signal=="Wprime":l2.AddEntry(g,"W': Optimal #tau_{21} cut","p")
    # l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
    # l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
    # l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
    # l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
    # l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")
    
    gr10perBand.SetFillColor(kGreen+1)
    gr10perBand.SetLineColor(kGreen+1)
    gr10perBand.SetFillStyle(1001)
    gr10perBand.Draw("AF")
    g.Draw("PL")
    
    l2.Draw()

    l1.SetTextFont(42)
    l1.SetTextSize(0.031)
    l1.DrawLatex(0.6,0.81, "0.8 #times M_{X} < M_{jj} < 1.2 #times M_{X}")
    l1.DrawLatex(0.6,0.77, "65 GeV < M_{p} < 105 GeV")
    CMS_lumi.CMS_lumi(c2, iPeriod, iPos)
    c2.Update()

    # l3 = TLegend(.2,.6,.4,.8)
    l3 = TLegend(.2,.7,.4,.9)
    l3.SetBorderSize(0)
    l3.SetFillColor(0)
    l3.SetTextFont(42)
    l3.SetTextSize(0.035)
    c3 = TCanvas("c3", "",800,800)
    c3.cd()
    c3.SetGridx()
    c3.SetGridy()

    g2 = TGraph(len(cut05), maxmass,cut05punziRatio)
    g3 = TGraph(len(cut055),maxmass,cut055punziRatio)
    g4 = TGraph(len(cut06), maxmass,cut06punziRatio)
    g5 = TGraph(len(cut075), maxmass,cut075punziRatio)
    g6 = TGraph(len(cut045), maxmass,cut045punziRatio)
    g7 = TGraph(len(cut040), maxmass,cut040punziRatio)
    g8 = TGraph(len(cut035), maxmass,cut035punziRatio)
    g9 = TGraph(len(cut030), maxmass,cut030punziRatio)
    
    g2.SetLineWidth(2)
    g3.SetLineWidth(2)
    g4.SetLineWidth(2)
    g5.SetLineWidth(2)
    g6.SetLineWidth(2)
    g7.SetLineWidth(2)
    g8.SetLineWidth(2)
    g9.SetLineWidth(2)
    
    
    g2.GetXaxis().SetTitle('M_{X} (TeV)')
    # g2.GetYaxis().SetTitle("#epsilon_{S}/(1+#sqrt{B})")
    g2.GetYaxis().SetTitle("Sign / Sign_{Opt. cut}")
    g2.GetYaxis().SetRangeUser(0.0,1.5)
    #g2.SetNdivisions(4)
    g2.SetMarkerColor(col.GetColor(palette[0]))
    g3.SetMarkerColor(col.GetColor(palette[1]))
    g4.SetMarkerColor(col.GetColor(palette[2]))
    g5.SetMarkerColor(col.GetColor(palette[3]))
    g7.SetMarkerColor(col.GetColor(palette[4]))
    g8.SetMarkerColor(col.GetColor(palette[5]))
    g9.SetMarkerColor(col.GetColor(palette[6]))
    
    g2.SetLineColor(col.GetColor(palette[0]))
    g3.SetLineColor(col.GetColor(palette[1]))
    g4.SetLineColor(col.GetColor(palette[2]))
    g5.SetLineColor(col.GetColor(palette[3]))
    g7.SetLineColor(col.GetColor(palette[4]))
    g8.SetLineColor(col.GetColor(palette[5]))
    g9.SetLineColor(col.GetColor(palette[6]))
    g2.SetMarkerStyle(markerStyles[0])
    g3.SetMarkerStyle(markerStyles[1])
    g4.SetMarkerStyle(markerStyles[2])
    g5.SetMarkerStyle(markerStyles[3])
    g7.SetMarkerStyle(markerStyles[4])
    g8.SetMarkerStyle(markerStyles[5])
    g9.SetMarkerStyle(markerStyles[6])
    l3.AddEntry(g9,"#tau_{21} < 0.30","p")
    l3.AddEntry(g8,"#tau_{21} < 0.35","p")
    l3.AddEntry(g7,"#tau_{21} < 0.40","p")
    l3.AddEntry(g6,"#tau_{21} < 0.45","p")
    l3.AddEntry(g2,"#tau_{21} < 0.50","p")
    l3.AddEntry(g3,"#tau_{21} < 0.55","p")
    l3.AddEntry(g4,"#tau_{21} < 0.60","p")
    l3.AddEntry(g5,"#tau_{21} < 0.75","p")
    # l2.AddEntry(0,"[1] Bulk G#rightarrow WW: %.1f" %(maxcuts[0]),"")
    # l2.AddEntry(0,"[2] RS1 G#rightarrow WW: %.1f" %(maxcuts[1]),"")
    # l2.AddEntry(0,"[3] RS1 G#rightarrow ZZ: %.1f" %(maxcuts[2]),"")
    # l2.AddEntry(0,"[4] q*#rightarrow qZ: %.1f" %(maxcuts[3]),"")
    # l2.AddEntry(0,"[5] q*#rightarrow qW: %.1f" %(maxcuts[4]),"")

    g2.Draw("APL")
    g3.Draw("PLsame")
    g4.Draw("PLsame")
    g5.Draw("PLsame")
    g6.Draw("PLsame")
    g7.Draw("PLsame")
    g8.Draw("PLsame")
    g9.Draw("PLsame")
    l3.Draw()
    CMS_lumi.CMS_lumi(c3, iPeriod, iPos)
    c3.Update()
    time.sleep(10)





    l = TLegend(.59,.62,.80,.9)
    l.SetBorderSize(0)
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.035)


   
    canvasname =outdir+Signal+"WWPunzi_"+category+".pdf"
    c2.Print(canvasname,"pdf")
    c2.Print(canvasname.replace("pdf","root"),"root")
    canvasname =outdir+Signal+"WWSignvsM_"+category+".pdf"
    c3.Print(canvasname,"pdf")
    c3.Print(canvasname.replace("pdf","root"),"root")
    #sys.stdout = orig_stdout

    time.sleep(10)
    return maxpunzi
    
def plotMaxPunzi(maxpunzi, masses):
    m = array('d',masses)
    g = TGraph(len(masses), m,maxpunzi)
    c2 = TCanvas("c2", "",800,800)
    c2.cd()
    c2.SetGridx()
    c2.SetGridy()
    g.GetXaxis().SetTitle('M_{X} (TeV)')
    g.GetYaxis().SetTitle("min cross section")
    g.SetMarkerStyle(22)
    g.SetMarkerSize(3)
    g.SetMarkerColor(kRed-3)
    g.GetYaxis().SetRangeUser(0.,0.01)

    g.Draw("A*L")
    l1 = TLatex()
    l1.SetNDC()
    l1.SetFillColor(0)
    l1.SetTextAlign(12)
    l1.SetTextFont(42)
    l1.SetTextSize(0.031)
    l1.DrawLatex(0.6,0.81, "0.8 #times M_{X} < M_{jj} < 1.2 #times M_{X}")
    l1.DrawLatex(0.6,0.77, "65 GeV < M_{p} < 105 GeV")
    CMS_lumi.CMS_lumi(c2, iPeriod, iPos)
    c2.Update()

    time.sleep(10)
    
    
def getNevents(tfile, cutup, massup, massdown, category):
    tree = tfile.Get('tree')
    n = []
    LPcut =0.75
    for cut in cutup:
        n.append(0)
    groomedmassdown = 65.
    groomedmassup   = 105.
    if category.find("WW")!=-1:
        groomedmassup   = 85.
    for event in tree:
        if (event.MVV < massdown) or (event.MVV > massup):
            continue;
        if(category.find("q") == -1):
            if (event.jet_puppi_softdrop_jet2 < groomedmassdown) or (event.jet_puppi_softdrop_jet2 > groomedmassup):
                continue;
            if (event.jet_puppi_softdrop_jet1 < groomedmassdown) or (event.jet_puppi_softdrop_jet1 > groomedmassup):
                continue;
            #if event.jet_puppi_tau2tau1_jet2 > cutup or event.jet_puppi_tau2tau1_jet2 < cutdown:
                #continue
            #if event.jet_puppi_tau2tau1_jet1 > cutup or event.jet_puppi_tau2tau1_jet1 < cutdown:
                #continue
            i=0
            for cut in cutup:
                #print cut*0.01
                x = cut*0.01
                if category.find("HP")!=-1:
                    if (event.jet_puppi_tau2tau1_jet2 <= x) and (event.jet_puppi_tau2tau1_jet1 <= x):
                        n[i]+= event.weight
                        #print event.jet_puppi_tau2tau1_jet1
                        #print event.jet_puppi_tau2tau1_jet2
                else:
                    if x >= 0.75:
                       if x == 1.:
                           n[i]+=event.weight
                       else:
                           continue
                    else:
                        if ((event.jet_puppi_tau2tau1_jet2 <= x) and (x < event.jet_puppi_tau2tau1_jet1 <= LPcut)) or ((event.jet_puppi_tau2tau1_jet1 <= x) and (x < event.jet_puppi_tau2tau1_jet2 <= LPcut)):
                            n[i]+= event.weight
                    
                i+=1

    return n


if __name__=='__main__':
    palette = get_palette('gv')
    col = TColor()
    Signal="Bulk"
    outdir="/shome/dschafer/AnalysisOutput/figures/testTau21Cut/"
    prefix="/shome/dschafer/AnalysisOutput/80X/SignalMC/Summer16/"
    rebin = 5
    lumi = 2500.#36814.
    bfname = '/shome/dschafer/AnalysisOutput/80X/Bkg/Summer16/QCD_pythia8_VVdijet_SR.root'

    fbkg = TFile.Open(bfname,"READ")
    dhnamesb = {'1000' : 'Tau21_punzi1TeV', '1200' : 'Tau21_punzi1v2TeV', '1600' : 'Tau21_punzi1v6TeV', '1800' : 'Tau21_punzi1v8TeV', '2000' : 'Tau21_punzi2TeV', '2500' : 'Tau21_punzi2v5TeV','3000' : 'Tau21_punzi3TeV', '4000' : 'Tau21_punzi4TeV'}
    #orig_stdout = sys.stdout
    #f = file(outdir+Signal+'WW.txt', 'w')
    #sys.stdout = f

    #masses= [1.2]
    #filelist = getSigFileList(masses,prefix)
    #bkgfile  = TFile.Open(bfname,"READ") 
    #for file in filelist:
        #sigh = file[0].Get('Tau21_punzi1v2TeV')
        #bkgh = bkgfile.Get('Tau21_punzi1v2TeV')
        #denSig = sigh.Integral()
        #denBKG = bkgh.Integral()
        #getMaxPunzi(sigh,bkgh,denSig,denBKG)
        #time.sleep(20)



    masses = [1,1.2,2,2.5,3]
    cat = "VVLP"
    filelist = getSigFileList(masses,prefix)
    maxpunzi = getPunziGraphs(cat, masses, filelist[0],filelist[1] , lumi, fbkg,outdir,rebin)
    
    
    
    #Signal="Zprime"
    #masses = [1,1.2,1.4,1.8,2,3,3.5,4]
    #filelist = getSigFileList(masses,prefix)
    #maxpunzi = getPunziGraphs(masses,filelist[0],filelist[1] , lumi, fbkg,outdir,rebin)
    
    #Signal="Wprime"
    #masses = [1,1.2,1.4,1.8,2,3,3.5,4]
    #filelist = getSigFileList(masses,prefix)
    #maxpunzi = getPunziGraphs(masses,filelist, hnameb, hnames, lumi, fbkg,outdir,rebin)
    
