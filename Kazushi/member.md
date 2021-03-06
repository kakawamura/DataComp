### \[About Data\]

#### About age column

-   1 = 10 ~ 19
-   2 = 20 ~ 24
-   3 = 25 ~ 29
-   4 = 30 ~ 34
-   5 = 35 ~ 39
-   6 = 40 ~

#### About gender column

-   1 = male
-   2 = female

### \[Start Analyzing\]

#### Importing member.csv

    member <- read.csv("data/member.csv", header = TRUE)

#### Creating a Pie chart of gender ratio

    genderRatio <- table(member["gender"] == 1)
    genderHeader <- c(
      paste("(female)", genderRatio[1]),
      paste("(male)", genderRatio[2])
    )
    names(genderRatio) <- genderHeader
    pie(genderRatio, col = rainbow(2))

![](member_files/figure-markdown_strict/unnamed-chunk-2-1.png)

#### Creating a Pie chart of age ratio

    ages <- member["age"]
    agesRatio <- c(
      table(ages == 1)[2],
      table(ages == 2)[2],
      table(ages == 3)[2],
      table(ages == 4)[2],
      table(ages == 5)[2],
      table(ages == 6)[2]
    )

    agesHeader <- c(
      paste("(10 ~ 19)"),
      paste("(20 ~ 24)"),
      paste("(25 ~ 30)"),
      paste("(30 ~ 34)"),
      paste("(35 ~ 40)"),
      paste("(40 ~ )")
    )
    names(agesRatio) <- agesHeader

    par(mfrow=c(1, 2))
    pie(agesRatio, col = rainbow(20))
    barplot(agesRatio, col = rainbow(20))

![](member_files/figure-markdown_strict/unnamed-chunk-3-1.png)
