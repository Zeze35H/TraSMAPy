#!/bin/bash

if [[ -z $SUMO_HOME ]]; then
    echo "Error: SUMO_HOME not set."
    exit 1
fi

argc=$#
if (( argc < 3 )) 
then
    echo "Error: missing args"
    exit 1
fi

# Set variables
in=""
out=""

############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:i:o:" option; do
   case $option in
      h)
         exit;;
      i) # summary file
         in=$OPTARG;;
      o) # output dir
         out=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# summary running vehicles
python "$SUMO_HOME/tools/visualization/plotXMLAttributes.py" $in/summary.xml -x time -y running -o ${out}/running.png;

# depart over delay time
python "$SUMO_HOME/tools/visualization/plotXMLAttributes.py" -i id -x depart -y departDelay --scatterplot\
 --xlabel "depart time [s]" --ylabel "depart delay [s]"\
 --label "depart delay over depart time" -o $out/depart_delay.png $in/tripinfo.xml