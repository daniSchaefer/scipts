python macros/compare-tt.py -s --cutMin=0.00 --cutMax=1.00 -b &
python macros/compare-tt.py -s --cutMin=0.00 --cutMax=0.45 -b &
python macros/compare-tt.py -s --cutMin=0.45 --cutMax=1.00 -b &
python macros/compare-tt.py -s -b -v "Whadr_tau21" &
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 65. --pMax 105. &
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 40. --pMax 65. &
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 105. --pMax 150.

python macros/compare-tt.py -s --cutMin=0.00 --cutMax=1.00 -b --norm&
python macros/compare-tt.py -s --cutMin=0.00 --cutMax=0.45 -b --norm &
python macros/compare-tt.py -s --cutMin=0.45 --cutMax=1.00 -b --norm &
python macros/compare-tt.py -s -b -v "Whadr_tau21"  --norm&
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 65. --pMax 105.  --norm&
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 40. --pMax 65.  --norm&
python macros/compare-tt.py -s -b -v "Whadr_tau21" --pMin 105. --pMax 150. --norm

python macros/compare-tt.py -s -b -v "Whadr_pt"  --norm&
python macros/compare-tt.py -s -b -v "Whadr_pt"  &

python macros/compare-tt.py -s -b -v "Whadr_eta"  --norm&
python macros/compare-tt.py -s -b -v "Whadr_eta"  &

python macros/compare-tt.py -s -b -v "Whadr_phi"  --norm&
python macros/compare-tt.py -s -b -v "Whadr_phi"  &

python macros/compare-tt.py -s -b -v "lept_pt"  --norm&
python macros/compare-tt.py -s -b -v "lept_pt"  &
python macros/compare-tt.py -s -b -v "lept_eta"  --norm&
python macros/compare-tt.py -s -b -v "lept_eta"  &
python macros/compare-tt.py -s -b -v "lept_phi"  --norm&
python macros/compare-tt.py -s -b -v "lept_phi"  &

python macros/compare-tt.py -s -b -v "nak4jets"  --norm&
python macros/compare-tt.py -s -b -v "nak4jets"  &


python macros/compare-tt.py -s -b -v "pfMET"  --norm&
python macros/compare-tt.py -s -b -v "pfMET"  &

python macros/compare-tt.py -s --cutMin=0.00 --cutMax=1.00 -b --realW --norm&
python macros/compare-tt.py -s --cutMin=0.00 --cutMax=0.45 -b --realW --norm&
python macros/compare-tt.py -s --cutMin=0.45 --cutMax=1.00 -b --realW --norm&

python macros/compare-tt.py -s --cutMin=0.00 --cutMax=1.00 -b --fakeW --norm&
python macros/compare-tt.py -s --cutMin=0.00 --cutMax=0.45 -b --fakeW --norm&
python macros/compare-tt.py -s --cutMin=0.45 --cutMax=1.00 -b --fakeW --norm&