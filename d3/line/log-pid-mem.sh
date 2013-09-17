echo -e "date\tpid\t%mem\tvsz\trss" > test.tsv
# echo -e "date\trss" > test.tsv
while true; do
(echo -en `date +"%D %H:%M:%S\t"`; ps --pid 19520 -o "pid=,%mem=,vsz=,rss="| tr -s "[:blank:]" "[\t]") >> test.tsv
# (echo -en `date +"%D %H:%M:%S:%N\t"`; ps --pid 1997 -o "rss="| tr -s "[:blank:]" "[\t]") >> test.tsv
sleep 1
done