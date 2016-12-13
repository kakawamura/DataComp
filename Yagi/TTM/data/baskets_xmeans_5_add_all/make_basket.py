
def main():
    import optparse
    import os
    parser = optparse.OptionParser()
    parser.add_option("-d", dest="D", type="int", help="number of customers")
    (options, args) = parser.parse_args()

    if not options.D:
        parser.error("need number of customers(-d)")

    basket = [[] for d in range(options.D)]

    filenames = os.listdir('./baskets_per_month')
    for filename in filenames:
        f = open('./baskets_per_month/'+filename, 'r')
        for line in f:
            tmp = line.replace('\n', '').split(" ")
            basket[int(tmp[0])] += tmp[1:]
        f.close()

    output = open('./baskets_per_month/basket.txt', 'w')
    for (i, items) in enumerate(basket):
        output.write(str(i)+' ')
        output.write(' '.join(items)+'\n')
    output.flush()
    output.close()


if __name__ == "__main__":
    main()



