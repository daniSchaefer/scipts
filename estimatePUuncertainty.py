import xml.etree.ElementTree as ET
import os,commands
import sys
from optparse import OptionParser
import ROOT
from ROOT import *
import math
import multiprocessing

argv = sys.argv
parser = OptionParser()

parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="VV")    #VV qV
parser.add_option('-S', '--signal',action="store",type="string",dest="signal",default="BulkWW")  #VBulkWW BulkZZ WprimeWZ ZprimeWW QstarQW QstarQZ
(opts, args) = parser.parse_args(argv)


unc_yield_minBiasXsec_up = []
unc_yield_minBiasXsec_down = []

yield_minBiasXsec_up   = []
yield_minBiasXsec_down = []
yield_minBiasXsec      = []
masses = [1200,1400,1800,2000,3000,3500,4000,4500]
  
def calculateYields(sys):
  
  outpath = '/mnt/t3nfs01/data01/shome/dschafer/ExoDiBosonAnalysis/forSystematics/'
  inpath  = '/mnt/t3nfs01/data01/shome/dschafer//AnalysisOutput/80X/SignalMC/Summer16/Sys/'
  
  status,ls_la = commands.getstatusoutput( 'ls -l %s' %sys )													      
  if status:																				      
    os.system('mkdir %s/%s' %(outpath,sys))
  
  signals = ['%s'%opts.signal]
  if opts.signal == 'ALL':
    signals = ['BulkWW','BulkZZ','WprimeWZ',"ZprimeWW"]
  
  for signal in signals:
  
    fout = ['%s/%s/%ssys_HPVV_%s.txt'%(outpath,sys,sys,signal),'%s/%s/%ssys_LPVV_%s.txt'%(outpath,sys,sys,signal),
            '%s/%s/%ssys_HPWW_%s.txt'%(outpath,sys,sys,signal),'%s/%s/%ssys_LPWW_%s.txt'%(outpath,sys,sys,signal),
            '%s/%s/%ssys_HPWZ_%s.txt'%(outpath,sys,sys,signal),'%s/%s/%ssys_LPWZ_%s.txt'%(outpath,sys,sys,signal),
            '%s/%s/%ssys_HPZZ_%s.txt'%(outpath,sys,sys,signal),'%s/%s/%ssys_LPZZ_%s.txt'%(outpath,sys,sys,signal)]

    cuts = []
    debugs = []

    debugs.append("VV HP category")
    cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 < 0.4"
    cuts.append(cut)

    debugs.append("VV LP category")
    cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 105 && ((jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 > 0.4 && jet_puppi_tau2tau1_jet2 < 0.75) || (jet_puppi_tau2tau1_jet2 < 0.4 && jet_puppi_tau2tau1_jet1 > 0.4 && jet_puppi_tau2tau1_jet1 < 0.75))"
    cuts.append(cut)

    debugs.append("WW HP category")
    cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 85 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 85 && jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 < 0.4"
    cuts.append(cut)

    debugs.append("WW LP category")
    cut =  "jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 85 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 85 &&  ((jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 > 0.4 && jet_puppi_tau2tau1_jet2 < 0.75) || (jet_puppi_tau2tau1_jet2 < 0.4 && jet_puppi_tau2tau1_jet1 > 0.4 && jet_puppi_tau2tau1_jet1 < 0.75))"
    cuts.append(cut)

    debugs.append("WZ HP category")
    cut =  "((jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 85 && jet_puppi_softdrop_jet2 > 85 && jet_puppi_softdrop_jet2 < 105) || (jet_puppi_softdrop_jet1 > 85 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 85)) && jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 < 0.4"
    cuts.append(cut)

    debugs.append("WZ LP category")
    cut =  "((jet_puppi_softdrop_jet1 > 65 && jet_puppi_softdrop_jet1 < 85 && jet_puppi_softdrop_jet2 > 85 && jet_puppi_softdrop_jet2 < 105) || (jet_puppi_softdrop_jet1 > 85 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 65 && jet_puppi_softdrop_jet2 < 85)) &&  ((jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 > 0.4 && jet_puppi_tau2tau1_jet2 < 0.75) || (jet_puppi_tau2tau1_jet2 < 0.4 && jet_puppi_tau2tau1_jet1 > 0.4 && jet_puppi_tau2tau1_jet1 < 0.75))"
    cuts.append(cut)

    debugs.append("ZZ HP category")
    cut =  "jet_puppi_softdrop_jet1 > 85 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 85 && jet_puppi_softdrop_jet2 < 105 && jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 < 0.4"
    cuts.append(cut)

    debugs.append("ZZ LP category")
    cut =  "jet_puppi_softdrop_jet1 > 85 && jet_puppi_softdrop_jet1 < 105 && jet_puppi_softdrop_jet2 > 85 && jet_puppi_softdrop_jet2 < 105 && ((jet_puppi_tau2tau1_jet1 < 0.4 && jet_puppi_tau2tau1_jet2 > 0.4 && jet_puppi_tau2tau1_jet2 < 0.75) || (jet_puppi_tau2tau1_jet2 < 0.4 && jet_puppi_tau2tau1_jet1 > 0.4 && jet_puppi_tau2tau1_jet1 < 0.75))"
    cuts.append(cut)
    
    for f in range(len(fout)):
      
      print "Writing to file: " ,fout[f]
      outfile = open(fout[f],'w')
      outfile.write('signal yield %sUp %sDown (in percent)\n'%(sys,sys))
      outfile.write('\n')
      
      print ""
      print debugs[f]
      print cuts[f]
      print ""

      for mass in masses:
       
       #Central value
       print "######## Mass = %i #########" %mass
       fname = inpath + 'ExoDiBosonAnalysis.%s_13TeV_%sGeV.CV.root' %(signal,mass)
       tfile = ROOT.TFile.Open(fname,'READ')
       tree = tfile.Get("tree")
       cv = float(tree.GetEntries(cuts[f]))
       print "Central value = %.3f" %(cv)
       tfile.Close()
       tfile.Delete()
       
       #Scale up value
       fname = inpath + 'ExoDiBosonAnalysis.%s_13TeV_%sGeV.%sUp.root' %(signal,mass,sys)
       tfile = ROOT.TFile.Open(fname,'READ')
       tree = tfile.Get("tree")
       up = float(tree.GetEntries(cuts[f]))
       print "Sys up = %.3f" %(up)
       tfile.Close()
       tfile.Delete()
       
       #Scale down value
       fname = inpath + 'ExoDiBosonAnalysis.%s_13TeV_%sGeV.%sDown.root' %(signal,mass,sys)
       tfile = ROOT.TFile.Open(fname,'READ')
       tree = tfile.Get("tree")
       down = float(tree.GetEntries(cuts[f]))
       print "Sys down = %.3f" %(down)
       tfile.Close()
       tfile.Delete()
       
       sup = up-cv
       sdown = down-cv
       if sup < 0 and sdown < 0: sdown = -sdown
       unc_yield_minBiasXsec_up.append(math.fabs(sup*100/cv))
       unc_yield_minBiasXsec_down.append(math.fabs(sdown*100/cv))
       yield_minBiasXsec.append(cv)
       yield_minBiasXsec_down.append(down)
       yield_minBiasXsec_up.append(up)
           
           
       print '%s_M%i %.3f %.3f\n' %(signal,mass,sup*100/cv,sdown*100/cv)
       outfile.write('%s_M%i %.3f %.3f\n' %(signal,mass,sup*100/cv,sdown*100/cv))
     
      outfile.close()
  
       
### Start  main
if __name__ == '__main__':
  
  # Define which systematics to run
  doSys = []
  
  #======================= Calculate yields ========================================================================================================
  
  calculateYields("minBiasXsec")

  unc_yield_minBiasXsec_down.sort();    
  unc_yield_minBiasXsec_up.sort();    
    

  print "                  UP            DOWN"
  print "               min/max        min/max"
  print "yield_minBiasXsec    %.6f/%.6f      %.6f/%.6f" %(unc_yield_minBiasXsec_up[0],unc_yield_minBiasXsec_up[-1], unc_yield_minBiasXsec_down[0], unc_yield_minBiasXsec_down[-1])
  
  s= " VV HP"
  print "mass     :     yield    :    yield up   : yield down"
  for i in range(0,len(yield_minBiasXsec)):
      x=0
      if i>= len(masses):
          x = len(masses)
          s = "VV LP"
      if i>= len(masses)*2:
          x =len(masses)*2
          s = "WW HP"
      if i>= len(masses)*3:
          x =len(masses)*3
          s = "WW LP"
      if i>= len(masses)*4:
          x =len(masses)*4
          s = "WZ HP"
      if i>= len(masses)*5:
          x =len(masses)*5
          s = "WZ LP"
      if i>= len(masses)*6:
          x =len(masses)*6
          s = "ZZ HP"
      if i>= len(masses)*7:
          x =len(masses)*7
          s = "ZZ LP"
      if i>= len(masses)*8:
          x =len(masses)*8
      if i-x == 0:
          print s
      print str(masses[i-x])+"    "+str(round(yield_minBiasXsec[i],2))+"     "+str(round(yield_minBiasXsec_up[i],2))+"    "+str(round(yield_minBiasXsec_down[i],2))
