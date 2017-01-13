# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=1.00 -b &
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.60 -b &
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.45 -b &
# python macros/wtag-cp.py -s -d --cutMin=0.45 --cutMax=1.00 -b &
# python macros/wtag-cp.py -s -d --cutMin=0.60 --cutMax=1.00 -b &
#
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=1.00 -b -c 0.46&
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.60 -b -c 0.46&
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.45 -b -c 0.46&
# python macros/wtag-cp.py -s -d --cutMin=0.45 --cutMax=1.00 -b -c 0.46&
# python macros/wtag-cp.py -s -d --cutMin=0.60 --cutMax=1.00 -b -c 0.46&
#
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=1.00 -b -v "Whadr_csv"&
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.60 -b -v "Whadr_csv" &
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.45 -b -v "Whadr_csv" &
# python macros/wtag-cp.py -s -d --cutMin=0.45 --cutMax=1.00 -b -v "Whadr_csv" &
# python macros/wtag-cp.py -s -d --cutMin=0.60 --cutMax=1.00 -b -v "Whadr_csv"

# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=1.00 -b --lowMass&
# python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.45 -b --lowMass&
# python macros/wtag-cp.py -s -d --cutMin=0.45 --cutMax=1.00 -b --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 65. --pMax 105. --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 40. --pMax 65. --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 105. --pMax 150. --lowMass&
#
# python macros/wtag-cp.py -s -d -b -v "pfMET" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "lept_pt" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_pt" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "Whadr_eta" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "lept_eta" --lowMass&
# python macros/wtag-cp.py -s -d -b -v "nak4jets" --lowMass&


python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=1.00 -b &
python macros/wtag-cp.py -s -d --cutMin=0.00 --cutMax=0.45 -b &
python macros/wtag-cp.py -s -d --cutMin=0.45 --cutMax=1.00 -b &
python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" &
python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 65. --pMax 105. &
python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 40. --pMax 65. &
python macros/wtag-cp.py -s -d -b -v "Whadr_tau21" --pMin 105. --pMax 150. & 

python macros/wtag-cp.py -s -d -b -v "nPV" &
python macros/wtag-cp.py -s -d -b -v "pfMET" &
python macros/wtag-cp.py -s -d -b -v "lept_pt" &
python macros/wtag-cp.py -s -d -b -v "Whadr_pt" &
python macros/wtag-cp.py -s -d -b -v "Whadr_eta" &
python macros/wtag-cp.py -s -d -b -v "lept_eta" &
python macros/wtag-cp.py -s -d -b -v "nak4jets" &
python macros/wtag-cp.py -s -d -b -v "Whadr_puppi_softdrop" &