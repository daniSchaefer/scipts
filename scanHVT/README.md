programm to make exclusion contour in HVT coupling parameter space:


code copied from:  https://github.com/jngadiub/ExoDiBosonCombination/tree/master/scanHVT-EXO-15-002-paper
also the root-file parameter scans were done by jennifer using the tools found on: http://rtorre.web.cern.ch/rtorre/Riccardotorre/vector_triplet_t.html
to make scans yourself go to the website and download CDF player. than follow instructions on site

   scans contain: 
   the scans are in the root files that you find in the folder called for instance “scanHVT-M3500.root”
   yes, so basically for each combination of parameters gV, cF, cH you have a theoretical cross section
   the root files in fact contain the cross section for each combination of parameters
   

to make the scans modify https://github.com/jngadiub/ExoDiBosonCombination/blob/master/scanHVT-EXO-15-002-paper/contourPlot.py
then in the code you have to write your limit on the xsec*BR here: https://github.com/jngadiub/ExoDiBosonCombination/blob/master/scanHVT-EXO-15-002-paper/contourPlot.py#L170

here you also set the max width for the narrow width approximation
the grey shaded area that you see in the plots of EXO-14-010 or B2G-16-004
https://github.com/jngadiub/ExoDiBosonCombination/blob/master/scanHVT-EXO-15-002-paper/contourPlot.py#L171
in this case is 6%, but usually we exclude 5%

and then here I do actually fill the histos for the contours
https://github.com/jngadiub/ExoDiBosonCombination/blob/master/scanHVT-EXO-15-002-paper/contourPlot.py#L81-L87
so you fill the histo if the xsec*BR predicted for a certain combination of parameter is smaller than your limit
and like this you get the region of the parameter space that you do not exclude

