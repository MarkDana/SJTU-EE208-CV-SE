#/bin/bash

hadoop fs -copyFromLocal testinput.txt pageranktest/testinput.txt
command='hadoop jar /Users/markdana/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -files mapper.py,reducer.py -mapper mapper.py -reducer reducer.py'
mv='hadoop fs -mv '
rm='hadoop fs -rm -r '
cp2local='hadoop fs -copyToLocal '
input='pageranktest'
for ((i=1;i<$1+1;i++));
do
    echo "Processing $i"
    output="pagerankout_$i"
    eval "$command -input $input/* -output $output"
    input=$output
    eval "$rm $input/_SUCCESS"
done
mkdir /home/markdana/result
eval "$cp2local $output/* /home/markdana/result"

