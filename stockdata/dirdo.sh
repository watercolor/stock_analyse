#!/bin/sh
for i in $PWD/*; do
    if [[ -d $i ]]; then
        cd $i
        if [[ -e month.csv -a -e month_new.csv ]]; then
            rm -f month.csv
            mv month_new.csv month.csv
            echo "rename $i month.csv "
        fi
        if [[ -e week.csv -a -e week_new.csv ]]; then
            rm -f week.csv
            mv week_new.csv week.csv
            echo "rename $i week.csv "
        fi
        cd ..
    fi
done
