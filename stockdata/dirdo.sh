#!/bin/sh
for i in $PWD/*; do
    if [[ -d $i ]]; then
        cd $i
        if [[ -e week.csv ]]; then
            if [[ `grep "2015-12-08" week.csv` ]]; then
                sed -i {} "/2015-12-08/d" week.csv
                echo "update week.csv in $i"
            fi
            if [[ `grep "2015-12-08" month.csv` ]]; then
                sed -i {} "/2015-12-08/d" month.csv
                echo "update month.csv in $i"
            fi
        fi
        cd ..
    fi
done
