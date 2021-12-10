#!/bin/bash

## $1 = PATH TO TERMOLATOR
## $2 = BASE FILE
## $3 = LEVEL 1 FILE
## $4 = LEVEL 2 FILE
## $5 = LEVEL 3 FILE
## $6 = LEVEL 4 FILE
## $3 = BACKGROUND FILE PATH
## $4 = OUTPUT NAME
## $5 = BACKGROUND PICKLE FILE

# We need to start 4 processes for each foreground corpus since
# we are testing 4 different breadths for each. 

bash ./term $1 $6 $5 "l4_l3"    "l3"    &
bash ./term $1 $6 $4 "l4_l2"    "l2"    &
bash ./term $1 $6 $3 "l4_l1"    "l1"    &
bash ./term $1 $6 $2 "l4_base"  "base"  &
wait