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
--measures entered,entered --xlabel [m] --ylabel [m] \
--default-width 1 -i $in \
--xlim -500,2500 --ylim -1250,500 \
--default-color "#606060" \
--min-color-value -100 --max-color-value 100 \
--max-width-value 1000 --min-width-value -1000 \
--colormap "viridis" --blind -o $out/edge_dense_%s.png --dpi 120 --size 15,10
