#!/bin/sh
for i in $PWD/*; do
    if [[ -d $i ]]; then
        cd $i
        if [[ -e month_macd.csv ]]; then
                sed -i {} -e "/2015-12-14/d" -e "/2015-12-15/d" -e "/2015-12-16/d" -e "/2015-12-17/d" month_macd.csv
                echo "update month.csv in $i"
        fi
        if [[ -e week_macd.csv ]]; then
                sed -i {} -e "/2015-12-14/d" -e "/2015-12-15/d" -e "/2015-12-16/d" -e "/2015-12-17/d" week_macd.csv
                echo "update week.csv in $i"
        fi
        cd ..
    fi
done
