##version: Python 3.6.7 
import sys
import os
import datetime
import platform
import subprocess
import argparse

knownArgs = ""



def argumentReader():
    count = 1
    arr = []
    parser = argparse.ArgumentParser(description='To allow downloading of EPICS on different Systems')
    parser.add_argument('-f', '--f', action = 'store_true', help="")
    parser.add_argument('-a', '--a', action = 'store_true', help="")
    parser.add_argument('-c', '--changeconfig', nargs='?',help='Allows for you to have a unqiue config file.')
        
    #check = vars(parser.parse_args())

    check = parser.parse_known_args()



    knownArgs = vars(check[0])
    print(len(knownArgs))

    if knownArgs['changeconfig'] is not None:
      count = count + 2
      change_config = knownArgs['changeconfig']
      arr.append(str(change_config))
      print("I am going to change the config " + str(change_config))
    

    print(knownArgs)
     
    # Argument flags:
    #-f: Skip prompt to add another driver
    #-a: Skip prompt and use list of drivers "det" instead
    #-h: Display help
    DetArray = "n"
    SKIP = "n"

    if "-h" in knownArgs:
        print("Tool for creating a deployment of an "
        + "AreaDectctor IOC. \nEnsure macros are set " 
        + "correctly before running.\n \ndeploy.sh [-f] [-a] [DRIVER] [VERSION] [ARCH] "
        + "\neg. deploy.sh ADProsilica R2-4 linux-x86_64 "
        + "\n\nFlags:\n-f : Deploy only the detector given (Bypass prompt) "         
        + "\n-a : Deploy the detectors given by the ""det"" array in the script (Bypass prompt)")
        sys.exit(0)
       
    if knownArgs['f'] == True or knownArgs['a'] == True:
        if knownArgs['a'] == True:
            DetArray = "y"
            print("Using list instead of prompt:")
            count = count + 1
            for i in range(len(det)):
                print(det[i])

        else:
            count = count + 1
            SKIP = "y"
            print("Skipping Prompt.....")
        
        
        arg1 = sys.argv[count]
        arg2 = sys.argv[count+1]
        arg3 = sys.argv[count+2]
        arr.append(arg1)
        arr.append(arg2)
        arr.append(arg3)
        return arr
    else:
        print("Bad Arguments")
        sys.exit(0)


arg1 = ""
arg2 = ""
arg3 = ""


list = argumentReader()                
print(list)

change_config = list[0]
arg1 = list[1]
arg2 = list[2]
arg3 = list[3]


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Starting Script~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if len(sys.argv)-4 != 3:
    print("We ignore the python file name, we are looking for the 3 main parameters.")
    print("You need to give the following: \n1 - The name of the detector (ADProsilica, etc.) \n2 - The version number (R2-0, etc.) \n3 - The EPICS architecture (linux-x86_64, etc.)")

else:
    myCmds = [] ##I created a array that will store all my commands that i want to exectue on the command line

    ##I have to fgiure out if its a windows OS or a linux OS prior to do thing anything.

    OS = platform.system()
    
    ## This is for linux command line 
    if OS == "Linux":        
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
        


    ##Naming the tar file to be 
    NAME = "" + arg1+ "_" + arg2 + "_" + arg3 + "_" + str(OS) + str(DATE)

    ## Path to the folder that will be containing the tar
    # will be created if it does nto exists

    DESTINATION = "DEPLOYMENTS"

    

    myCmds = []

    myCmds = ["mkdir -p " + DESTINATION + "", "rm -rf temp"
    ,"mkdir temp","cp components/scripts/generateEnvPaths.sh temp",
    ]

    for i in range(len(myCmds)):
        temp = myCmds[i]
        os.system(temp)

    HOME = os.popen("pwd").read()

    myCmdHome = "cd "+ HOME + ""
    print(HOME)
    print(change_config)
    change_config = HOME + ""+ "" +change_config
    change_config = change_config.replace("\n", "")
    

    with open(change_config, "r") as configChoice:
        DetectorArrayFound = False
        ModuleArrayFound = False
        DictionaryFound = False
        detectors = []
        module = []
        filePath = {}
        for line in configChoice:
            print(line)

            if line.startswith('##Required File Start'):
                DictionaryFound = True
            elif line.startswith('##Required File End'):
                DictionaryFound = False
            if line.startswith('##Detector array start'):
                DetectorArrayFound = True
            elif line.startswith('##Detector array end'):
                DetectorArrayFound = False
            if line.startswith('##Module array start'):
                ModuleArrayFound = True
            elif line.startswith('##Module array end'):
                ModuleArrayFound = False
            
            if DictionaryFound and not line.startswith('#') and len(line) > 2:
                line = line.strip()
                l = line.split("=")
                filePath[l[0]] = l[1]
            if DetectorArrayFound and not line.startswith('#') and len(line) > 2:
                line = line.strip()
                detectors.append(line)        
            if ModuleArrayFound and not line.startswith('#') and len(line) > 2:
                print("Here ")
                line = line.strip()
                module.append(line)  



    print(detectors)
    print(filePath)
    print(module)

    myCmdSupport = "cd" + SUPPORT + ""

    SUPPORT = os.popen("pwd").read()

    os.system(HOME)

    os.system("cd " + DESTINATION)

    os.system(""+NAME+".tgz > README_"+NAME+".txt")
    os.system(">> README_"+NAME+".txt")
    os.system("Version used in the deployment >> README_"+NAME+".txt")







