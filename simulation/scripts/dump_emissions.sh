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
in_net=""
in=""
out=""

############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:i:o:n:" option; do
   case $option in
      h)
         exit;;
      i) # dump file
         in=$OPTARG;;
      o) # output dir
         out=$OPTARG;;
      n)
         # network input
         in_net=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# net dump density
python "$SUMO_HOME/tools/visualization/plot_net_dump.py" -v -n $in_net \
 --measures CO2_normed,CO2_normed --xlabel [m] --ylabel [m] \
 --default-width 2 -i $in \
 --xlim -500,2500 --ylim -1250,500 \
 --default-color "#606060" \
 --min-color-value -10000 --max-color-value 100000 \
 --max-width-value 1000 --min-width-value -1000 \
 --colormap "summer" --blind -o $out/edge_emission_%s.png --dpi 120 --size 15,10
