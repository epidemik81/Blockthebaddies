# Blockthebaddies
majorbbs add script kids to hostdeny.txt

- reads the wgsaudit.adt file and and creates a dump of all the IP Addresses listed in "output.xlsx"
- checks the output.xlsx file for ips that show up consecutively in the column and puts them in a "matched.xlsx"(default is 10 matches = matches.xlsx, change this with the consecutive_threshold variable)
- compares matched.xlsx with current hostdeny.txt file and adds any ip address that do not already exist in hostdeny.txt and will let you know how many ip's it blocked
- excludes any matches it finds on the 192.168(change this to your ipschema i.e. 10.1 etc) because of some router forwarding

1. install python on your system(python.org)
2. make sure to install the environment variable path, depending on your version of windows you may need to open a cmd prompt and type "python" to take you to the windows store to install
3. from a cmd prompt type pip install pandas this is the module dependency needed to run this
4. Download blockthebaddies from git repo https://github.com/epidemik81/Blockthebaddies.git and place the file in your MBBS dir
5. add this line to your wgsclean.bat
@echo off
python blockthebaddies.py
timeout /t 10 >nul
6. you may also add this to a single bat if you want to run it manually
7. enjoy

Note: This all could have been buffered into memory and read but I wanted traceability, that said keep an eye on your "matched and output.xlsx" files to make sure they aren't getting to big
