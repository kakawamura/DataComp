for i in `seq 5 20`
do
    nohup python lda.py -f basket.txt -k $i -i 200 &
done
