#!/bin/bash
# The core of this script is created by Mark Rivers, from the AreaDetector
# repo: https://github.com/areaDetector/areaDetector/blob/master/makeADPrebuilt
# Additions and changes made by Michael Rolland

#  This script takes 3 parameters.  
# 1 - The name of the detector (ADProsilica, etc.)
# 2 - The version number (R2-0, etc.)
# 3 - The EPICS architecture (linux-x86_64, etc.)
start="$(date +%s)"

find . -name 'auto_settings.sav_*' -exec rm -fv {} \;
find . -name 'auto_settings.savB*' -exec rm -fv {} \;
find . -name 'core.*' -exec rm -fv {} \;
find . -name '*.exe.*' -exec rm -fv {} \;

AREA_DETECTOR=areaDetector
# required EPICS modules
# must be names of folders in $SUPPORT
ASYN=asyn
AUTOSAVE=autosave
BUSY=busy
CALC=calc
DEVIOCSTATS=iocStats
SEQ=seq
SSCAN=sscan
BASE_TOP=/mnt/c/epics
BASE=base
SUPPORT=/mnt/c/epics/support

declare -a det=("ADProsilica"
    "ADSimDetector"
#    "ADPluginBar"
#    "ADCompVision"
#    "ADPluginEdge"
#    "ADUVC"
    "ADAndor3"
    "ADPilatus"
    "ADMerlin"

#    "ADLambda"
    "ADPointGrey"
#    "ADEiger"
    "ADDexela"
    "ADPerkinElmer"
    "ADURL"
    )

# additional EPICS modules to be packaged
declare -a epics=(
	"modbus"
	"quadEM"
	)

DATE=`date +%Y-%m-%d`
# get OS from /etc/issue, remove trailing \n \l, remove trailing space, replace spaces with underscores
OS="$(more /etc/issue | cut -d'\' -f1 | sed -e 's/[[:space:]]*$//' | tr ' ' _)"
# remove '_GNU/Linux' from OS
OS=${OS//'_GNU/Linux'/}
echo OS: $OS

# Argument flags:
#     -f: Skip prompt to add another driver
#     -a: Skip prompt and use list of drivers "det" instead
#     -h: Display help
DetArray="n"
SKIP="n"
arg1=$1
arg2=$2
arg3=$3


if [ $1 = "-h" ]; then
    echo 'Tool for creating a deployment of an AreaDetector IOC.'
    echo 'Ensure macros are set correctly before running.'
    echo
    echo 'deploy.sh [-f] [-a] [DRIVER] [VERSION] [ARCH]'
    echo 'eg. deploy.sh ADProsilica R2-4 linux-x86_64'
    echo
    echo 'Flags:'
    echo '-f : Deploy only the detector given (Bypass prompt)'
    echo '-a : Deploy the detectors given by the "det" array in the script (Bypass prompt)'
    exit 1
fi
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo Three arguments required: Driver, version, and architecture.
    exit 1
fi
if [ $# -eq 4 ]; then
    if [ $1 = -f ] || [ $1 = -a ]; then
		if [ $1 = -a ]; then
		    DetArray="y"
		    echo Using list instead of prompt:
		    for i in "${det[@]}" 
		    do
				echo $i
	    	done
		else
	    	SKIP="y"
	    	echo Skipping prompt
		fi
		arg1=$2
		arg2=$3
		arg3=$4
	else
		echo Bad arguments
		exit 1
	fi
fi

# name of tar file
# do not include extension
NAME=${arg1}_${arg2}_${OS}_$DATE

# path to folder containing tar
# will be created if it does not exist
DESTINATION="DEPLOYMENTS"

echo "Parameter 1 = " $arg1
echo "Parameter 2 = " $arg2
echo "Parameter 3 = " $arg3

mkdir -p $DESTINATION
rm -rf temp
mkdir temp
# cp -r components/prebuilts temp
# cp -r components/scripts temp
cp components/scripts/generateEnvPaths.sh temp
# cp components/standardizeIOC.sh temp

HOME=$(pwd)
cd $SUPPORT
SUPPORT=$(pwd)
cd $HOME

cd $DESTINATION
DESTINATION=$(pwd)
echo $NAME.tgz > README_$NAME.txt
echo >> README_$NAME.txt
echo Versions used in this deployment >> README_$NAME.txt
echo [folder name] : [git tag] >> README_$NAME.txt
echo >> README_$NAME.txt
cd $HOME

# add core stuff
cd $BASE_TOP
cp --parents -r -n $BASE/bin/$arg3 $HOME/temp
cp --parents -r -n $BASE/lib/$arg3 $HOME/temp
cp --parents -r -n $BASE/lib/perl $HOME/temp
cp --parents -r -n $BASE/configure $HOME/temp
cp --parents -r -n $BASE/include   $HOME/temp
cp --parents -r -n $BASE/startup   $HOME/temp
cd $BASE
BASE_VER=$(git describe --tags)
cd $DESTINATION
echo $BASE : $BASE_VER >> README_$NAME.txt

cd $SUPPORT
cp --parents -r -n $AREA_DETECTOR/ADCore/db $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/documentation $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/ADApp/Db $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/ADApp/op $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/iocBoot $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADViewers/ImageJ $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/bin/$arg3 $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADCore/lib/$arg3 $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADSupport/bin/$arg3 $HOME/temp
cp --parents -r -n $AREA_DETECTOR/ADSupport/lib/$arg3 $HOME/temp

cp --parents -r -n $ASYN/opi $HOME/temp
cp --parents -r -n $ASYN/db $HOME/temp
cp --parents -r -n $ASYN/configure $HOME/temp
cp --parents -r -n $ASYN/include $HOME/temp
cp --parents -r -n $ASYN/bin/$arg3 $HOME/temp
cp --parents -r -n $ASYN/lib/$arg3 $HOME/temp

cp --parents -r -n $AUTOSAVE/asApp/ $HOME/temp
cp --parents -r -n $AUTOSAVE/asApp/op $HOME/temp
cp --parents -r -n $AUTOSAVE/configure $HOME/temp
cp --parents -r -n $AUTOSAVE/include $HOME/temp
cp --parents -r -n $AUTOSAVE/bin/$arg3 $HOME/temp
cp --parents -r -n $AUTOSAVE/lib/$arg3 $HOME/temp
cp --parents -r -n $AUTOSAVE/db $HOME/temp
cp --parents -r -n $AUTOSAVE/dbd $HOME/temp

cp --parents -r -n $BUSY/busyApp/Db $HOME/temp
cp --parents -r -n $BUSY/busyApp/op $HOME/temp
cp --parents -r -n $BUSY/configure $HOME/temp
cp --parents -r -n $BUSY/include $HOME/temp
cp --parents -r -n $BUSY/bin/$arg3 $HOME/temp
cp --parents -r -n $BUSY/lib/$arg3 $HOME/temp

cp --parents -r -n $CALC/calcApp/Db $HOME/temp
cp --parents -r -n $CALC/calcApp/ $HOME/temp
cp --parents -r -n $CALC/configure $HOME/temp
cp --parents -r -n $CALC/include $HOME/temp
cp --parents -r -n $CALC/bin/$arg3 $HOME/temp
cp --parents -r -n $CALC/lib/$arg3 $HOME/temp

cp --parents -r -n $DEVIOCSTATS/db $HOME/temp
cp --parents -r -n $DEVIOCSTATS/op/adl $HOME/temp
cp --parents -r -n $DEVIOCSTATS/configure $HOME/temp
cp --parents -r -n $DEVIOCSTATS/include $HOME/temp
cp --parents -r -n $DEVIOCSTATS/bin/$arg3 $HOME/temp
cp --parents -r -n $DEVIOCSTATS/lib/$arg3 $HOME/temp

cp --parents -r -n $SEQ/configure $HOME/temp
cp --parents -r -n $SEQ/include $HOME/temp
cp --parents -r -n $SEQ/bin/$arg3 $HOME/temp
cp --parents -r -n $SEQ/lib/$arg3 $HOME/temp

cp --parents -r -n $SSCAN/sscanApp/Db $HOME/temp
cp --parents -r -n $SSCAN/sscanApp/op $HOME/temp
cp --parents -r -n $SSCAN/configure $HOME/temp
cp --parents -r -n $SSCAN/include $HOME/temp
cp --parents -r -n $SSCAN/bin/$arg3 $HOME/temp
cp --parents -r -n $SSCAN/lib/$arg3 $HOME/temp

# add additional EPICs modules
for MOD in "${epics[@]}" 		
do
	EXISTS=$(ls | grep $MOD)
	if ! [ -z "$EXISTS" ]; then
		cp --parents -r -n $MOD/db $HOME/temp
		cp --parents -r -n $MOD/configure $HOME/temp
		cp --parents -r -n $MOD/include $HOME/temp
		cp --parents -r -n $MOD/bin/$arg3 $HOME/temp
		cp --parents -r -n $MOD/lib/$arg3 $HOME/temp
		cp --parents -r -n $MOD/*App/Db $HOME/temp
		cp --parents -r -n $MOD/*App/op $HOME/temp
		if [ "$MOD" == "quadEM" ]; then
			cp --parents -r -n $MOD/iocBoot $HOME/temp
		fi
		cd $MOD
		MOD_VER=$(git describe --tags)
		cd $DESTINATION
		echo $MOD : $MOD_VER >> README_$NAME.txt
		cd $SUPPORT
	else
		echo Invalid module not found: $MOD
	fi
done

# add additional areaDetector drivers
i=0
PLUGIN=$arg1
if [ "$DetArray" = y ]; then
    PLUGIN=${det[${i}]}
fi
while ! [ "$PLUGIN" = done ]; do
    EXISTS=$(ls $AREA_DETECTOR | grep $PLUGIN)
    if ! [ -z "$EXISTS" ]; then
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/configure $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/include $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/db $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/bin/$arg3 $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/lib/$arg3 $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/documentation $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/iocs/*IOC/bin/$arg3 $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/iocs/*IOC/lib/$arg3 $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/iocs/*IOC/dbd $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/iocs/*IOC/iocBoot $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/*/Db $HOME/temp
		cp --parents -r -n $AREA_DETECTOR/$PLUGIN/*/op $HOME/temp
		cd $AREA_DETECTOR/$PLUGIN
		PLUGIN_VER=$(git describe --tags)
		cd $DESTINATION
		echo $PLUGIN : $PLUGIN_VER >> README_$NAME.txt
		cd $SUPPORT
    else
		echo Invalid driver not found: $PLUGIN
    fi

    if [ "$DetArray" = y ]; then
		((i++))
		PLUGIN=${det[${i}]}
        if [ -z $PLUGIN ]; then
		    PLUGIN='done'
		fi
    else
		if [ "$SKIP" = n ]; then
		    echo Enter name of additional detector to add or \"done\" to exit:
		    read PLUGIN
		else
		    PLUGIN='done'
		fi
    fi
done

# get core versions
cd $ASYN
ASYN_VER=$(git describe --tags)
cd ../$AUTOSAVE
AUTO_VER=$(git describe --tags)
cd ../$BUSY
BUSY_VER=$(git describe --tags)
cd ../$CALC
CALC_VER=$(git describe --tags)
cd ../$DEVIOCSTATS
STAT_VER=$(git describe --tags)
cd ../$SSCAN
SCAN_VER=$(git describe --tags)
cd ../$SEQ
SEQ_VER=$(git describe --tags)
cd ../$AREA_DETECTOR
AD_VER=$(git describe --tags)

cd $DESTINATION
echo $AREA_DETECTOR : $AD_VER >> README_$NAME.txt
echo $ASYN : $ASYN_VER >> README_$NAME.txt
echo $AUTOSAVE : $AUTO_VER >> README_$NAME.txt
echo $BUSY : $BUSY_VER >> README_$NAME.txt
echo $CALC : $CALC_VER >> README_$NAME.txt
echo $DEVIOCSTATS : $STAT_VER >> README_$NAME.txt
echo $SSCAN : $SCAN_VER >> README_$NAME.txt
echo $SEQ : $SEQ_VER >> README_$NAME.txt
cp README_$NAME.txt $HOME/temp/README.txt

# tar it up
cd $HOME
#echo tarring on linux...
tar -czf $NAME.tgz -C temp .
#echo zipping on  Windows ...
#zip -r $NAME.zip temp 
echo done.

mv $NAME.tgz $DESTINATION
#mv $NAME.zip $DESTINATION
rm -rf temp

end="$(date +%s)"
time=$(($end-$start))
echo time: $time seconds
