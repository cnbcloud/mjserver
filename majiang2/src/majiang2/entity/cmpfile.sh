#!/bin/sh  
targetdir=$1
for afile in `find ${basedir}  -type f  -name "*.py"`; do  
        #echo ${afile};
	#echo ${afile:2};  
        targetfile=/home/gamedev/majiang2_xj/majiang2/${targetdir}/${afile:2}
	#echo ${targetfile};
        if [ -f "${afile}" ]; then  
                cmp $afile ${targetfile};  
        fi  
done  
