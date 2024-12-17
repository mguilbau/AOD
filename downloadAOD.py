import sys
import os
import argparse
import subprocess
import json

parser = argparse.ArgumentParser(description='Arguments to pass')
parser.add_argument('--download', help="Download AODs (have to enable the parameter to avoid downloading AODs anywhere)", action="store_true")
parser.add_argument('--merge', help="Merge AO2Ds using aod-merger", action="store_true")
parser.add_argument('--debug', help="Provide information on the code", action="store_true")
args = parser.parse_args()

# Open and read the json file
with open('datasets.json', 'r') as f:
	data = json.load(f)

datarun = '' # put run number
hylink = ''  # hyperloop link
validity = False # is the run good or bad for physics

if(args.merge):
   aodmergelist = "aodmergelist.txt" 
   command = 'touch ' + aodmergelist

#Print the json content
for runs in data['runlist']:
    #print(runs)
    datarun = runs['runnumber']
    hylink = runs['hylink']
    validity = runs['validity']

    if validity:
       command = 'alien.py find ' + hylink + ' AO2D.root'
       try:
          results = subprocess.check_output(command, shell=True, text=True).splitlines()
          print(results)
       except subprocess.CalledProcessError as e:
          print('Error executing command: {e}')
       
       ifile = 1
       for result in results:
          command = 'alien.py cp -dst file://./' + datarun + '/' + '{:03d}'.format(ifile) + ' ' + result

          if(args.debug):
            print('command to be executed: ' + command)

          if(args.download):
          	os.system(command)

          if(args.merge):
             command = 'find "$PWD" -depth 3 -name AO2D.root > ' + aodmergelist
             os.system(command)

          ifile+=1

if(args.merge):
   command = 'o2-aod-merger --input ' + aodmergelist
   os.system(command)
 
