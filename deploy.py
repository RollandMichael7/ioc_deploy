##version: Python 3.6.7 
import sys
import os
import datetime
import platform
import subprocess
import argparse
import shutil
import distutils.dir_util 
import stat
import tarfile
import zipfile

knownArgs = ""



def argumentReader():
    
    arr = []
    parser = argparse.ArgumentParser(description='To allow downloading of EPICS on different Systems')
    parser.add_argument('-c', '--changeconfig', nargs='?',help='Allows for you to have a unqiue config file.')
        
    check = parser.parse_known_args()
    knownArgs = vars(check[0])
    
    if knownArgs['changeconfig'] is not None:
      change_config = knownArgs['changeconfig']
      arr.append(str(change_config))
      print("I am going to change the config " + str(change_config))
      
    else:
        change_config = "configure"
        arr.append(change_config)
        
        return arr
    

list = argumentReader()                


change_config = list[0]
arg3 = ""

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Starting Script~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

myCmds = [] ##I created a array that will store all my commands that i want to exectue on the command line

##I have to fgiure out if its a windows OS or a linux OS prior to do thing anything.

OS = platform.system()
    
    ## This is for linux command line 
         
myCmds.append('find -name auto_settings.sav_* -exec rm -fv {} \\;')
myCmds.append('find -name auto_settings.savB* -exec rm -fv {} \\;')
myCmds.append('find -name core.* -exec rm -fv {} \\;')
myCmds.append('find -name *.exe.* -exec rm -fv {} \\;')
## The exectution of my commands that I have placed in my array 
os.system(myCmds[0])
os.system(myCmds[1])
os.system(myCmds[2])
os.system(myCmds[3])

        

DATE = datetime.datetime.now()
checkMyOS = "more /etc/issue | cut -d '\\' -f1 | tr ' ' _"

OS = os.popen(checkMyOS).read()

if OS.startswith("Invalid"):
    OS = platform.system()

##Naming the tar file to be 
NAME = arg3 + "_" + str(OS) + str(DATE) 
NAME = NAME.replace("\n","")
NAME = NAME.replace("'","")
NAME = NAME.replace("$","")
NAME = NAME.replace(" ","_")
NAME = NAME.replace(":","-")
## Path to the folder that will be containing the tar
# will be created if it does nto exists

DESTINATION = "DEPLOYMENTS"

    

myCmds = []

myCmds = ["mkdir " + DESTINATION + "", "rm -rf temp"
,"mkdir temp","cp components/scripts/generateEnvPaths.sh temp",
]

for i in range(len(myCmds)):
    temp = myCmds[i]
    os.system(temp)

os.chmod("temp/",0o777)
HOME = os.popen("pwd").read()

myCmdHome = "cd "+ HOME + ""
change_config = change_config
change_config = change_config.replace("\n", "")
HOME = HOME.replace("\n","")
AREA_DETECTOR= "areaDetector/"

os.system(HOME)

readMe = "README_"+NAME+".txt"

file = open(DESTINATION+"/"+readMe, "w")
tarFile = NAME + ".tgz"
file.write(tarFile)
file.write("\n")
file.write("Version used in this deployment " + OS)
file.write("\n")
file.write("##   FOLDER NAME           :    GIT TAG          COMMIT MESSAGE    ##")
##I try to open the file and read in information
try:   
    with open(change_config, "r") as configChoice:
        DetectorArrayFound = False
        ModuleArrayFound = False
        DictionaryFound = False
        detectors = []
        module = []
        install_path =""
        original_path = ""
        ##for loop for each line in the configure file
        for line in configChoice:
            line= line.strip()
            ##I determine which arch they are using
            if line.startswith('##EPIC_ARCH'):
                t = line.split("=")
                arg3 = t[1]
            if line.startswith('##Required File Start'):
                DictionaryFound = True
            elif line.startswith('##Required File End'):
                DictionaryFound = False
                
            elif line.startswith('##Detector array start'):
                DetectorArrayFound = True
                print(install_path)
                ##Force them to add ADSupport and ADCore
                os.makedirs("temp/support/areaDetector/ADSupport")
                print("Adding ADSupport")
                distutils.dir_util.copy_tree(install_path+AREA_DETECTOR+"ADSupport" ,"temp/support/areaDetector/ADSupport")
                os.makedirs("temp/support/areaDetector/ADCore")
                print("Adding ADCore")
                distutils.dir_util.copy_tree(install_path+AREA_DETECTOR+"ADCore" ,"temp/support/areaDetector/ADCore")
                print("Finished here")
            elif line.startswith('##Detector array end'):
                DetectorArrayFound = False
                
            elif line.startswith('##Modules start'): 
                ModuleArrayFound = True
            elif line.startswith('##Modules end'):
                ModuleArrayFound = False
                
            if DictionaryFound and not line.startswith('#') and len(line) > 2:
                if line.startswith("INSTALL_PATH"):
                    ##I figure out the install path they have
                    line = line.strip()
                    r = line.split("=")
                    install_path = str(r[1])
                    original_path = install_path
                elif line.startswith("?"):
                    ##I figure out what they want downloaed
                    install_path = original_path
                    line = line.strip()
                    line = line.replace("?","")
                    line = line.replace("[INSTALL_PATH]","")
                    k = line.split("=")
                    install_path = install_path + str(k[1])
                    print(install_path)
                    
                    os.makedirs("temp/"+str(k[1]))
                else:
                    if line.startswith("BIN") or line.startswith("LIB"):
                        line = line.strip()
                        l = line.split("=")
                        ##I copy the files here and make dirs
                        partOfInstall = str(l[1])
                        temp = "temp/" + str(k[1]) +str(l[1]) + "/"+ arg3
                        os.makedirs(temp)
                        print("Adding...... " + temp)
                        distutils.dir_util.copy_tree(install_path+partOfInstall+"/"+arg3,temp)
                            
                        path = os.popen("pwd").read()
                        git = os.popen("git -C "+install_path+partOfInstall+" branch").read()
                        start = git.find("R")
                        end = git.find(")")
                        version = git[start:end]
                        commit_msg = os.popen("git -C "+install_path+partOfInstall+" log").read()
                        msg = commit_msg.split('\n',1)[0]
                        msg =msg.replace("commit ", "")
                        file.write("\n")
                        file.write(install_path + partOfInstall + "/" + arg3 + " : " + version + " " + msg)
                            
                    else:
                        line = line.strip()
                        l = line.split("=")
                        ##I copy the files here and make dirs
                        partOfInstall = str(l[1])
                        temp = "temp/" + str(k[1])+str(l[1])
                        os.makedirs(temp)
                        print("Adding....... "+temp)
                        distutils.dir_util.copy_tree(install_path+partOfInstall, temp)  
                            
                        path = os.popen("pwd").read()
                        git = os.popen("git -C "+install_path+partOfInstall+" branch").read()
                        start = git.find("R")
                        end = git.find(")")
                        version = git[start:end]
                        commit_msg = os.popen("git -C "+install_path+partOfInstall+" log").read()
                        msg = commit_msg.split('\n',1)[0]
                        msg =msg.replace("commit ", "")
                        file.write("\n")
                        file.write(install_path + partOfInstall + " : " + version + " "+ msg)
                            
            if DetectorArrayFound and not line.startswith('#') and len(line) > 2:
                if line.startswith("INSTALL_PATH"):
                    line = line.strip()
                    r = line.split("=")
                    install_path = str(r[1])
                elif line.startswith("?"):
                    install_path = original_path
                    line = line.strip()
                    line = line.replace("?","")
                    line = line.replace("[INSTALL_PATH]","")
                    k = line.split("=")
                    install_path = install_path + str(k[1])
                    print(install_path)
                    try:
                        os.makedirs("temp/"+str(k[1]))
                    except:
                        print("")
                else:
                    line = line.strip()
                    detectors.append(line) 
                    ##I copy the files here and make dirs
                    partOfInstall = line
                    temp = "temp/support/areaDetector/" +line
                    print("Adding...... "+temp)
                    os.makedirs(temp)
                    distutils.dir_util.copy_tree(install_path+AREA_DETECTOR+partOfInstall, temp)  
                    
                    path = os.popen("pwd").read()
                    git = os.popen("git -C "+install_path+AREA_DETECTOR+partOfInstall+" branch").read()
                    start = git.find("R")
                    end = git.find(")")
                    version = git[start:end]
                    git = os.popen("git -C "+install_path+AREA_DETECTOR+partOfInstall+" log").read()
                    msg = commit_msg.split('\n',1)[0]
                    msg =msg.replace("commit ", "")
                    file.write("\n")
                    file.write(install_path + AREA_DETECTOR +partOfInstall + " : " + version + " "+ msg)

            if ModuleArrayFound == True and not line.startswith('#') and len(line) > 2:
                line = line.strip()
                module.append(line)  
                if line.startswith("INSTALL_PATH"):
                    line = line.strip()
                    r = line.split("=")
                    install_path = str(r[1])
                elif line.startswith("?"):
                    install_path = original_path
                    line = line.strip()
                    line = line.replace("?","")
                    line = line.replace("[INSTALL_PATH]","")
                    k = line.split("=")
                    install_path = install_path + str(k[1])
                    print(install_path)
                    try:
                        os.makedirs("temp/"+str(k[1]))
                    except:
                        print("")
                else:
                    line = line.strip()
                    detectors.append(line) 
                    ##I copy the files here and make dirs
                    partOfInstall = line
                    print(str(k[1]))
                    temp = "temp/" + str(k[1]) +line
                    os.makedirs(temp)
                    print("Adding........ "+temp)
                    distutils.dir_util.copy_tree(install_path+partOfInstall, temp)  

                    path = os.popen("pwd").read()
                    git = os.popen("git -C "+install_path+partOfInstall+" branch").read()
                    start = git.find("R")
                    end = git.find(")")
                    version = git[start:end]
                    git = os.popen("git -C "+install_path+partOfInstall+" log").read()
                    msg = commit_msg.split('\n',1)[0]
                    msg =msg.replace("commit ", "")
                    file.write("\n")
                    file.write(install_path +partOfInstall + " : " + version + " "+ msg)
    file.close()
    print("")
    print("TARRING IN PROGRESS")
    subprocess.call(["tar", "-czf",DESTINATION+"/"+tarFile,"temp"])
    print("TARRING COMPLETED!")
    print("Moved Tar into DEPLOYMENT")

except:
    print("Make sure your packages are correct!")
    print("Crashed at: " +install_path + partOfInstall)
    print("Make sure that what's above is correct")
    ##Error handling 