import os
import sys
import shutil
import pathlib
import hashlib
import datetime
import time
import argparse


description1 = """
    - syncronization of two folders, from the source folder into the replica folder !
    - periodically in certain time intervals !
    - logging the actions into a logfile and the console !
    - reading the required pathes as command line arguments !
    - tested ONLY on linux (Arch Linux) and python 3.10 ! (2DO: testing on MS-Windows/iOS ! NOT tested yet! esp. SymLinks work??)
    - 2DOs:  more exception handlings, soft exits on errors, test routines, more modularizations , SymLinks improvements !
    - 2DOs more: 
    - BUG: could be problems with SymLinks, esp. on non-posix platforms !? 2DO !
    - requires python > 3.9
    - This is NOT the most performant way to synchronize folders, since the file-comparison is done here by their MD5-hash/size/timesamp,
      so based OS-filesystem, and not sector based (as rsync,...). So e.g. it means, a minor change to a huge file triggers the copy of
      the WHOLE file to the replica folder, which is far from perfect. But for the simple tasks could be fine !?
    - Tested ONLY on my linux! so on other platforms/OSs is to be tested ! NOT done yet !
    - I know, regarding the formatting/beautifying of this module, it is not absolutely style-guide comform.
      But I did it as a quick implementaion in my vim/linux. So you are welcome to reformat/beautify it in your favorite IDE !
      (e.g. the line lenght or one.liner-if-statements in one line, instead two! But so I can see more lines in my vim!
      of course for bigger modules using IDE and keeping to PEP 8 , ... !)
    - 2DO: also QA not done yet: so no mypy, pylint, pytype, pyre, pydantic, pytest, unittest routines yet ; for now no time, later on in August ...
    """

usage1 = """
    - help with:   -h / --help   (as:  python   ./syncFolders1.py  -h)
    - example call:   python   ./syncFolders1.py  ./source1  ./replica1  ./log1.txt   3600  --verbose  --simulation
    - positional argumenets:  <source-folder-path>  <replica-folder-path>  <logfile-path> <time-interval/seconds>
    - optional   argumenets:  [ --verbose/-v   --debug/-d   --simulation/-s ] 
    - ALL positional arguments are MANDATORY ! There are NO defaults !
    - Pathes can be relative or absolute !
    - if the replica/target folder does not already exist, it will be created!
    - if ANY permissions or ANY file creation problems, then the module will exit (NO beautiful exception handling yet! 2do)
    - terminate the programm just with the interrupt key (CTRL-C) before starting the next run of syncronization!
    """

""" functions, ... here:
    - cmdline_argsParser1() : read in user arguments and parse them
    - check_args()  :  verifying user command line arguments
    - logit() : write outputs into the log file and console
    - debugit() : debug outputs the for optional argument [-d]
    - compare_files() : if two files are identical? have sam MD5 hash? ...
    - syncFolders() : do the action of syncronization from source folder into replica folder
    - main() : main routine to call the syncronization process
"""

args = argparse.ArgumentParser()  ##--input arguments on command line

##============================ parsing command line arguments: =========================
def cmdline_argsParser1() ->  argparse.ArgumentParser:
    """  parsing command line arguments! see USAGE above for details ! """
    parser1 = argparse.ArgumentParser(usage = usage1, description=description1, exit_on_error=True)
    parser1.add_argument("src1", help="source folder path", type=str)
    parser1.add_argument("rep1", help="replica/target folder path", type=str)
    parser1.add_argument("log1", help="logfile path", type=str)
    parser1.add_argument("time1", help="time periods/intervals for synchronizations", type=int)
    parser1.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser1.add_argument("-d", "--debug", help="debug mode with much more verbosity",  action="store_true")
    parser1.add_argument("-s", "--simulation", help="simulate/dry, NO filesystem manipulations",  action="store_true")
    args1 = parser1.parse_args()
    if args1.src1[-1] != os.sep:  args1.src1 += os.sep
    if args1.rep1[-1] != os.sep:  args1.rep1 += os.sep
    return args1
##======================================================================================

##============================ command line Arguments checking : ======================
def check_args(args1:  argparse.ArgumentParser) -> bool:
    """
    - verifying the command line Arguments
    - print out a summary of user options and inputs
    - check access rights to the source/replica folders
    """
    logit ("-----------------------------------------------------------------------------")
    logit (f"your call:  {args1.src1} {args1.rep1} {args1.log1} {args1.time1}")
    logit (f"SOURCE Folder        :  {args1.src1}")
    logit (f"REPLICA/Target Folder:  {args1.rep1}")
    logit (f"LOG-FILE             :  {args1.log1}")
    logit (f"TIME-Intervals /sec. :  {args1.time1}")
    logit ("-----------------------------------------------------------------------------")
    if args1.time1 < 1 : logit("time interval must be a positive number !", exitError=3)
    if args1.simulation:
        logit ("---------- simulation/dry mode is turned on ! NO filesystem manipulations ! ----------")
    if args1.debug:
        logit ("---------- debug mode is turned on ! ----------")
        args1.verbose = True
    if args1.verbose:
        logit ("---------- verbose mode is turned on ! ----------")
    ##------- checking read/write access to folders,...:
    ##__  if not (os.path.exists(args1.src1) and os.access(args1.src1, os.F_OK) and os.access(args1.src1, os.R_OK) and os.access(args1.src1, os.X_OK)  ):
    if not (os.path.exists(args1.src1) and os.access(args1.src1, os.F_OK ^ os.R_OK ^ os.X_OK)  ):
        logit("###---ERROR: source folder problem! either it does NOT exist or permissions/acces problems !", level1="ERROR ", exitError=3)
    try:
        if not os.path.exists(args1.rep1): os.makedirs(args1.rep1)
    except:
        logit("###---ERROR: replica folder could NOT be created ! (permissions/acces problems !?)", level1="ERROR ", exitError=3)
##======================================================================================

##============================ log outputs: ============================================
def logit(msg: str, level1: str ="INFO  ", exitError: int =0):
    """
    print output messages into the logfile and console
    level1 == message label as: INFO / DEBUG / ACTIONS / ERROR / ...
    if exitError > 0, it exits the programm after printing out the message ! terminattion!
    """
    msgStr1 = datetime.datetime.now().__str__() + "  :  " + level1  + "  :  " + msg 
    with open(args.log1, "a") as f1:
        f1.write(msgStr1 + "\n")
    print (msgStr1)
    if exitError > 0 :
        print ("###--EXIT-on-Error ! the application is terminated! see previous messages !")
        os._exit(exitError)
##======================================================================================

##============================debug outputs : ==========================================
def debugit(msg1: str) -> None:
    """ debug outputs, triggered by -d/--debug """
    if args.debug : logit(msg1, "DEBUG ")
##======================================================================================

##============================ compare files: ==========================================
def compare_files(f1: str, f2:str) -> bool:
    """
    compares two regular files if they differ, based on their MD5 hash, size and modification time!
    returns true if they differ!
    """
    with open(f1, "rb") as f1_handle:
        f1_bytes = f1_handle.read()
        with open(f2, "rb") as f2_handle:
            f2_bytes = f2_handle.read()
            if (hashlib.md5(f1_bytes).hexdigest() != hashlib.md5(f2_bytes).hexdigest() or 
                os.path.getmtime(f1) != os.path.getmtime(f2) or
                os.path.getsize(f1) != os.path.getsize(f2)):
                debugit(f1 + "MODIFIED:  <->  "  + f2 + "  : differs" )
                return True
            else:
                return False
##======================================================================================

##============================ sync folders : ==========================================
def syncFolders(src1: str, rep1: str):
    """
    syncronize two folders, from sync-source-folder/src1  to  sync-replica-folder/rep1!
    procedure:
    - first creating lists/sets of all entries in source and replica folder, as objects AND strings
    - then check for: set(replica) - set(source)  , which are items to be DELETED in replica
    - then check for: set(source)  - set(replica) - , which are NEW files in source, to be COPIED
    - then check for: MODIFIED files in source by comparing their MD5 + size + timestamp
    - and in each step do the appropriate action : DELETE / COPY / OVERWRITE
    """
    logit("\n\n")
    logit ("##################  STARTING FOLDERS SYNCRONIZATION: #############################")
    srcItems = sorted(pathlib.Path(src1).rglob("*"), reverse=True)
    repItems = sorted(pathlib.Path(rep1).rglob("*"), reverse=True)
    srcItemsStr = list(ii.__str__() for ii in srcItems)
    repItemsStr = list(ii.__str__() for ii in repItems)
    srcItemsStrRelative = list(ii.__str__().replace(src1, "") for ii in srcItems)
    repItemsStrRelative = list(ii.__str__().replace(rep1, "") for ii in repItems)

    ##========= debug outputs of above kists of source and replica items : ==============
    debugit("========== source-items--reverse-sorted: =================");
    for ii in srcItemsStr: debugit (ii)
    debugit("========== replic-items-reverse-sorted: =================");
    for ii in repItemsStr: debugit (ii)
    debugit("========== source-items--reverse-sorted--relative-pathes: =================");
    for ii in srcItemsStrRelative: debugit (ii)
    debugit("========== replic-items--reverse-sorted--relative-pathes: =================");
    for ii in repItemsStrRelative: debugit (ii)

    ##========== deleting old items in replica, but not in source! so delete (replica - source) items : =============
    repItemsToDelete = set(repItemsStrRelative) - set(srcItemsStrRelative)
    logit ("---------- DELETED items in  SOURCE folder : --------------------------------", "DELETE")
    for ii in sorted(repItemsToDelete,  reverse=True):  ##--reverse !! due to removing FILES before DIRs !:
        itemFullPath1 = rep1 + ii
        logit (itemFullPath1, "DELETING")
        if not args.simulation:
            if os.path.isdir(itemFullPath1): shutil.rmtree(itemFullPath1)
            else: os.remove(itemFullPath1)

    ##========== copying new items of source, so copy (source - replica) into replica: =============
    srcItemsToAdd = set(srcItemsStrRelative) - set(repItemsStrRelative)
    logit ("---------- NEW items in SOURCE folder : -------------------------------------", "COPY  ")
    for ii in sorted(srcItemsToAdd):  ##--NOT-reverse-any-more !! due to adding DIRs before FILES !
        itemFullPath1 = src1 + ii
        repFullPath1 = rep1 +ii
        logit (itemFullPath1 + "  -->  " + repFullPath1, "COPYING")
        if not args.simulation:
            ##__  if os.path.islink(itemFullPath1): pathlib.Path(repFullPath1).unlink(missing_ok=True)
            try:
                if os.path.isdir(itemFullPath1): shutil.copytree(itemFullPath1, repFullPath1, symlinks=True, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                elif os.path.isfile(itemFullPath1): shutil.copy2(itemFullPath1, repFullPath1, follow_symlinks=False)
            except (shutil.SameFileError, shutil.Error):
                debugit ("EXCEPTIONN SameFileError, overwriting/updating symlinks is fine ! " + sys.exc_info()[1].args[0].__str__())

    ##========== modified files sync from source to replica: =======================================
    logit ("---------- MODIFIED items in SOURCE folder : --------------------------------", "MODIFY")
    for ii in srcItemsStrRelative:
        itemFullPath1 = src1 + ii
        repFullPath1  = rep1 + ii
        if os.path.isfile(itemFullPath1) and compare_files(itemFullPath1, repFullPath1):
            logit (itemFullPath1 + "  -->  " + repFullPath1, "MODIFIED")
            if not args.simulation: shutil.copy2(itemFullPath1, repFullPath1, follow_symlinks=False)

    logit (f"########__________  FINISHED SYNCHING ! next run in {args.time1} seconds __________################")
##======================================================================================


##======================================================================================
def main():
    global args
    args = cmdline_argsParser1()
    logit ("=====================================================================================")
    check_args (args)
    while True:
        syncFolders (args.src1, args.rep1)
        try:
            time.sleep(args.time1)
        except:
            logit("\nUser interruption ! OK!\n")
            os._exit(os.EX_OK)
##======================================================================================


if __name__ == "__main__":
    main()

