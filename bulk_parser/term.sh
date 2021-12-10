#!/bin/bash

## $1 = PATH TO TERMOLATOR
## $2 = FOREGROUND FILE PATH
## $3 = BACKGROUND FILE PATH
## $4 = OUTPUT NAME
## $5 = BACKGROUND PICKLE FILE

./$1/run_termolator.sh $2 $3 .xml $4 True False 30000 5000 ./$1 False False False $5.pkl False