# Installation Instructions

1. Clone the repository to your computer
```
git clone https://github.com/lilloukas/tx_tracker.git
cd tx_tracker
```

2. Update the permissions of the files (not necessary, but is nice for convenience)
```
chmod +x add_hashes.py
chmod +x tx_tracker.py
```
3. Download all required installs
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
4. Add accounts of interest using add_hashes.py
```
./add_hashes.py
```
If you didn't update the permissions on the files, do the following instead
```
python3 add_hashes.py
```
5. Run tx_tracker
```
./tx_tracker
```
If you didn't update the permissions on the files, do the following instead
```
python3 tx_tracker.py
```

The default is to check each address for new updates with a 1 second buffer between the next api request. 

