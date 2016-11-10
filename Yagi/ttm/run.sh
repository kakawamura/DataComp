for i in `seq 5 20`
do
    nohup python ttm.py -f baskets/baskets_per_month -d 101491 -v 226 -k $i -p 12 -i 100 &
done
