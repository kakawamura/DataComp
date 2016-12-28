source('./aggregate_enquete.R')

file <- '../../../data/enquete_analyzed.csv'
enquete <- read.csv(file,header=TRUE)
col_all <- colnames(enquete)
col_ignore <- c('answer_date', 'new_customer_id', 'customer_id', 'q3_19', 'q5', 'q6_10', 'q7_12', 'q8_32', 'q6_6')

topicsDistFile <- '../TTM/log/log_2016-12-13-16/log_2016-12-13-16-811231_K5_P13_I100/topicdist/topicdist_12.txt'


for(colm in col_all){
  if(all(colm != col_ignore)){
    tmp <- c(unique(enquete[colm])[[1]])
    choices <- tmp[!is.na(tmp)]
      for(choice in choices){
        getResult(topicsDistFile, colm, choice)
      }

  }
}
