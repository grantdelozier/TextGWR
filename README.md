TextGWR
=======

A Python application for doing Text Geolocation/Geo-referencing using Geographically Weighted Regression. TextGWR also includes utilities for doing geostatistics on geolocated texts.



Examples of use
=============
 

Build References Command:

GWR requires reference files to be built for the words and observation documents in a train/text/dev file. Two files are output, -rf_obs_out outputs the the observation ID and the appropriate matrix index and -rf_std_out outputs word, mean probability, and standard deviation of the words seen in the input file.

python GWRMain.py -mode build_ref_files -tf /directory/train_file.txt -rf_obs_out obs_trainset.txt -rf_std_out std_ref_trainset.txt -wordlist morans_original_%10_whitelist.txt -listuse restricted


Calculate Getis Gi* statistics:

python GWRMain.py -mode Gi_Calc -tf /directory/train_file.txt -ptbl person_table -kern Uniform_10000 -conn "dbname=someDB user=userID host='localhost' " -wordlist morans_original_%10_whitelist.txt -listuse restricted -gi_out /directory/getis_outfile.txt 

