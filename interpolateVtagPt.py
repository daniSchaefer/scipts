#python do-jes.py -s JES -c VV --signal BulkWW
import xml.etree.ElementTree as ET
import os,commands
import sys
#from optparse import OptionParser
import ROOT
from ROOT import *
import math
from array import array
import time
ptBins = [200,400,600,800,1200,2000]

def getFitFunc():
    fa = TF1("fa","[0]*log(x/2./200.)/100.",590,4500)
    return fa




def getEfficiencyVV(tfile, category,tau21):
    
    cuts_jet1 = []
    cuts_jet2 = []
    ptcuts_jet1=[]
    ptcuts_jet2=[]
    debugs = []
    results = {}
    if category.find("HP")!=-1:
        #cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && jet_puppi_tau2tau1_jet1 < "+tau21+" && jet_puppi_tau2tau1_jet2 < "+tau21
        cut_jet1 =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_tau2tau1_jet1 < "+tau21
        cut_jet2 =  "jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && jet_puppi_tau2tau1_jet2 < "+tau21
    else:
        #cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && ((jet_puppi_tau2tau1_jet1 < "+tau21+" && jet_puppi_tau2tau1_jet2 > "+tau21+" && jet_puppi_tau2tau1_jet2 < 0.75) || (jet_puppi_tau2tau1_jet2 < "+tau21+" && jet_puppi_tau2tau1_jet1 > "+tau21+" && jet_puppi_tau2tau1_jet1 < 0.75))"
        cut_jet1 = "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_tau2tau1_jet1 < 0.75 && jet_puppi_tau2tau1_jet1 > "+tau21
        cut_jet2 = "jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && jet_puppi_tau2tau1_jet2 < 0.75 && jet_puppi_tau2tau1_jet2 > "+tau21
    for i in range(0,len(ptBins)-1):
        pmin = ptBins[i]
        pmax = ptBins[i+1]
        debugs.append(category+"_"+str(pmin)+'-'+str(pmax))
        ptcuts_jet1.append("jet_pt_jet1 < "+str(pmax)+" && jet_pt_jet1 >= "+str(pmin))
        ptcuts_jet2.append("jet_pt_jet2 < "+str(pmax)+" && jet_pt_jet2 >= "+str(pmin))
        cuts_jet1.append(cut_jet1+" && jet_pt_jet1 < "+str(pmax)+" && jet_pt_jet1 >= "+str(pmin))
        cuts_jet2.append(cut_jet2+" && jet_pt_jet2 < "+str(pmax)+" && jet_pt_jet2 >= "+str(pmin))
        #print cuts_jet1[i]
    
    tree = tfile.Get("tree")

    for i in range(0,len(cuts_jet1)):
       #print tree.GetEntries(cut)
       #print tree.GetEntries()
       num1 = tree.GetEntries(cuts_jet1[i])
       num2 = tree.GetEntries(cuts_jet2[i])
       denom1 = tree.GetEntries(ptcuts_jet1[i])
       denom2 = tree.GetEntries(ptcuts_jet2[i])
       num = (num1+num2)
       denom = (denom1+denom2)
       #print num 
       #print denom
       if denom != 0:
            results[debugs[i]] = float(num/float(denom))
            results[debugs[i]+"err"] = TMath.Sqrt( num/float(pow(denom,2)) + pow( num/float(denom*denom),2)*denom ) 
       else:
           results[debugs[i]] = 0
           results[debugs[i]+"err"] = 0
       
       
    return results


def getEfficiencyOverPt(massesMad,cat, gen,tau21):
    ldirMad=[]
    for m in massesMad:
        filename = "ExoDiBosonAnalysis.BulkWW_13TeV_"+str(m)+"GeV"+gen+".CV.root"
        tfile = TFile.Open(inputdir+filename,"READ")
        ldirMad.append(getEfficiencyVV(tfile,cat,tau21))
        #print ldirMad
    effMad = array("f",[])
    for i in range(0,len(ptBins)-1):
        index = -10
        pmin = ptBins[i]
        pmax = ptBins[i+1]
        key = cat+"_"+str(pmin)+'-'+str(pmax)
        if key== cat+"_200-400": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 600:
                    index = i
        if key== cat+"_400-600": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 1000:
                    index = i
        if key== cat+"_800-1200": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 2000:
                    index = i
        if key== cat+"_1200-2000": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 3000:
                    index = i
        if index >=0:
            print key
            print index
            print ldirMad[index][key] 
            effMad.append(ldirMad[index][key])
    return effMad
    
def getEfficiencyOverPtError(massesMad,cat, gen,tau21):
    ldirMad=[]
    for m in massesMad:
        filename = "ExoDiBosonAnalysis.BulkWW_13TeV_"+str(m)+"GeV"+gen+".CV.root"
        tfile = TFile.Open(inputdir+filename,"READ")
        ldirMad.append(getEfficiencyVV(tfile,cat,tau21))
    effMad = array("f",[])
    for i in range(0,len(ptBins)-1):
        index = -10
        pmin = ptBins[i]
        pmax = ptBins[i+1]
        key = cat+"_"+str(pmin)+'-'+str(pmax)+"err"
        if key== cat+"_200-400err": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 600:
                    index = i
        if key== cat+"_400-600err": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 1000:
                    index = i
        if key== cat+"_800-1200err": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 2000:
                    index = i
        if key== cat+"_1200-2000err": 
            for i in range(0,len(massesMad)):
                if massesMad[i] == 3000:
                    index = i
        if index >=0:
            effMad.append(ldirMad[index][key])
    return effMad
    
    
    


if __name__=="__main__":
    inputdir = "../AnalysisOutput/80X/SignalMC/Summer16/wtagPt/"
    outdir  = inputdir
    tau21 = "0.35"
    categories = ["VV HP category","VV LP category"]
    for category in categories:
        cat = "VVHP"
        if category.find("LP")!=-1:
            cat = "VVLP"
        masses = [600, 1000, 2000, 3000, 4000]
        masseserr = array('f',[0,0,0,0,0])
        eff = getEfficiencyOverPt(masses,cat,"_herwig",tau21)
        efferr = getEfficiencyOverPtError(masses,cat,"_herwig",tau21)
        
        massesMad = [600, 1000, 2000, 3000, 4000]
        massesMaderr = array('f', [0,0,0,0])
        
        effMad =  getEfficiencyOverPt(massesMad,cat, "",tau21)
        effMaderr = getEfficiencyOverPtError(masses,cat,"",tau21)
        print eff
        print effMad
        masses = array('f',massesMad)
       
        diff =array('f',[])
        for i in range(0,len(eff)):
            print str(effMad[i]) + "   "+str(eff[i])
            num = (effMad[i]-eff[i])
            denom = (effMad[0]-eff[0])
            print num 
            print denom
            diff.append(TMath.Abs(((effMad[i]-eff[i])/(effMad[0]-eff[0]) -1 )*100))
            print diff[i]
        
        pt = array('f',[300,500,1000,1600])
        g = TGraph(len(diff),pt,diff)
        g.SetMarkerStyle(32)
        g.SetMarkerColor(kBlue)
        
        g.SetMarkerStyle(23)
        g.SetMarkerColor(kRed)
        g.GetXaxis().SetTitle("dijet mass [GeV]")
        g.GetYaxis().SetTitle("eff. mad. - eff.herwig, norm.")
        g.GetYaxis().SetTitleOffset(1.5)
        c = TCanvas("c","c",400,400)
        c.SetLeftMargin(0.15)
        

               
        g.Draw("AP")
        c.SaveAs(outdir+"VtagPt_"+cat+"_"+tau21+".pdf")
        time.sleep(10)
        
        #cdiff = TCanvas("c","c",400,400)
        #cdiff.SetLeftMargin(0.15)
        #effdiff= array("f")
        ##errdiff = array("f")
        ##print len(eff)
        ##massesdiff = array("f",[1000,2000,4000])
        ##massesdifferr = array("f",[0,0,0])
        #x0 = eff[0]
        #y0 = effMad[0]
        #for i in range(0,len(ptBins)-1):
            #x = eff[i]
            #y = effMad[i]
            #effdiff.append(TMath.Abs((y-x)/(y0-x0)))
            ##error = TMath.Sqrt(gMad.)
            ##errdiff.append(error)
        #aptBins = array("f",[200,500,1000,2000])
        #gdiff = TGraph(len(aptBins),aptBins,effdiff)
        #gdiff.SetMarkerStyle(24)
        #gdiff.Draw("AP")
        #cdiff.SaveAs(outdir+"difference_madgraph_herwig_"+cat+".pdf")
        #time.sleep(10)
        print category
        print "========================================================="
        print "pT range     200-400    400-600    800-1200    1200-2000"
        print "madgraph "+str(round(effMad[0],4))+" +- "+str(round(effMaderr[0],4))+"  "+str(round(effMad[1],4)) +" +- "+str(round(effMaderr[1],4))+ "   "+str(round(effMad[2],4))+" +- "+str(round(effMaderr[2],4))+"   "+str(round(effMad[3],4))+ " +- "+str(round(effMaderr[3],4))
        print "herwig   "+str(round(eff[0],4))+" +- "+str(round(efferr[0],4))+"  "+str(round(eff[1],4)) +" +- "+str(round(efferr[1],4))+ "   "+str(round(eff[2],4))+" +- "+str(round(efferr[2],4))+"   "+str(round(eff[3],4))+ " +- "+str(round(efferr[3],4))
        print "========================================================="
        print "rel. diff "+str(round(diff[0],2))+"      " +str(round(diff[1],2))+"      "+str(round(diff[1],2))+"      " +str(round(diff[3],2))
        print "========================================================="
        
       
