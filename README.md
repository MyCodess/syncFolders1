
syncronization of two folders with python
===================================================

DESCRIPTION :
-------------------------
- syncronization of two folders, from the source folder to the replica folder !
- periodically running in certain time intervals !
- logging the actions into a logfile and to the console !
- reading the required pathes as command line arguments !
- NOT using any external Libs ... ! ONLY standard python packages !
- requires python > 3.9
- tested ONLY on linux (Arch Linux) and python 3.10 ! (2DO: testing on MS-Windows/iOS ! NOT tested yet! esp. SymLinks work??)

Notes:
--------------------------
- 2DO:  more exception handlings, soft exits on errors, test routines, more modularizations , SymLinks improvements ! QA routines ! Testing on other OS/platforms !
- BUG:  could be problems with SymLinks, esp. on non-posix platforms !? 2DO !
- This is NOT the most performant way to synchronize folders, since the file-comparison is done here by their MD5-hash/size/timesamp, so based on OS-filesystem and not sector based (as rsync,...).
  So it means e.g. a minor change to a huge file triggers the copy of the WHOLE file to the replica folder, which is far from performant. But for the simple tasks or smaller files could be fine !?
- I know, regarding the formatting/beautifying of this module, it is not absolutely style-guide comform.
  But I did it as a quick implementaion with my vim/linux. So you are welcome to reformat/beautify it in your favorite IDE !
  (e.g. the line lenght or one.liner-if-statements in one line, instead two! But so I can see more lines in my vim!
  of course for bigger modules using IDE and keeping to PEP 8 , ... !)
- 2DO: also QA not done yet: so no mypy, pylint, pytype, pyre, pydantic, pytest, unittest routines yet ; for now no time, later on in August ...

USAGE:
-------------------------
- help with:   -h / --help   (as:  python   ./syncFolders1.py  -h)
- example call:   python   ./syncFolders1.py  ./source1  ./replica1  ./log1.txt   3600  --verbose  --simulation
- positional argumenets:  <source-folder-path>  <replica-folder-path>  <logfile-path> <time-interval/seconds>
- optional   argumenets:  [ --verbose/-v   --debug/-d   --simulation/-s ] 
- ALL positional arguments are MANDATORY ! There are NO defaults !
- Pathes can be relative or absolute !
- if the replica/target folder does not already exist, it will be created!
- if ANY permissions or ANY file creation problems, then the module will exit (NO beautiful exception handling yet! 2do)
- terminate the programm just with the interrupt key (CTRL-C) before starting the next run of syncronization!

functions defined :
-------------------------
- cmdline_argsParser1() : read in user arguments and parse them
- check_args()  :  verifying user command line arguments
- logit() : write outputs into the log file and console
- debugit() : debug outputs the for optional argument [-d]
- compare_files() : if two files are identical? have sam MD5 hash? ...
- syncFolders() : do the action of syncronization from source folder into replica folder
- main() : main routine to call the syncronization process
______________________________________________________________________


