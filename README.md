# ioc_deploy #


Author: Michael Rolland  
Corresponding Authors: Kazimierz Gofron, Jakud Wlodek, Michael Posada  
Created: July 18, 2018  
Last Updated: June 17, 2019   
Copyright (c): 2018-2019 Brookhaven National Laboratory  

## Online manual can be found [here](https://rollandmichael7.github.io/ioc-manual/) ##

**This script is a modified version of Mark Rivers's makeADPrebuilt script, which can be found at 
https://github.com/areaDetector/areaDetector/blob/master/makeADPrebuilt**

This script creates a portable deployment of an areaDetector plugin that was previously compiled locally. The script creates a tarball archive of all the necessary files for an IOC in a target directory. The tarball also contains a generateEnvPaths bash script which can create a usable envPaths file for any external IOC that needs to use this deployment. In the same folder as the tarball will be a README file which documents the version for each component that was used in the deployment.

## Requirements ##
- ADSupport, ADCore, and any detectors to be copied must be compiled already.
- The EPICS modules that these plugins depend on must be compiled already.
  - asyn, autosave, busy, calc, seq, sscan, (dev)iocStats
- EPICS base must be compiled already
- Note: Any envPaths files generated use absolute paths; thus, moving the deployment will break the IOC unless the envPaths file is 
modified or re-generated.

## Usage ##
Before using the script, it is necessary to define the macros which define the folder names for area detector and EPICS modules, the path to the support folder which contains them, and the location of the EPICS base installation. Additionally, the destination macro must be defined to tell the script where to put the tarball. The script takes three arguments: (1) The areaDetector driver to add, (2) the version of the driver, and (3) the EPICS_HOST_ARCH architecture. The script will ask for additional drivers to add, if you want to deploy multiple drivers in one tarball; to bypass this prompt, use the -f flag prior to the arguments. Examples:

```
bash deploy.sh ADProsilica R2-2 linux_x86-64

bash deploy.sh -f aravisGigE R1-0 linux-x86_64
```

To deploy multiple drivers at once, define the array "det" in deploy.sh to include the names of all drivers you want to add. Then run the script with the -a flag. (Note: the first two command line arguments are arbitrary when deploying this way, and there is no prompt to add additional drivers)

```
bash deploy.sh -a NSLS2 master linux_x86-64
```
