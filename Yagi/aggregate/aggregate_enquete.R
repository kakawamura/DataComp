#a = cluster1
#b = answer enquete
#c = answer 1
#P(c|a,b) = p(a|b,c)p(b,c)/p(a,b) = p(a|b,c)p(c|b)p(b) / p(b|a)p(a) = p(a|b,c)p(c|b) / p(a|b)


getProb_a_bc <- function(topicFile, key, value){
  topics <- read.csv(topicFile, header = FALSE)
  file <- '../../../data/enquete_analyzed.csv'
  enquete <- read.csv(file,header=TRUE)
  enquete[is.na(enquete)] <- -999
  
  tmp <- enquete[key] == value
  
  res <- c()
  
  ## for each clusters
  for(clusIndex in 1:ncol(topics)) {
    clusRes <- c()
    
    ## for each members
    for(i in 1:nrow(enquete)) {
      if(tmp[i] == TRUE) {
        # only check cluster 1
        clusRes <- c(clusRes, topics[i, clusIndex])
      }
    }
    
    res <- c(res, mean(clusRes))
    
  }
  
  return(res)
  
}


getProb_c_b <- function(key, value) {
  file <- '../../../data/enquete_analyzed.csv'
  enquete <- read.csv(file,header=TRUE)
  enquete[is.na(enquete)] <- -999
  
  # 条件の行数を取得する  <--- ここまずいきがする！
  count <- table(enquete[key] == value)[2]
  
  prob <- count / 497
  names(prob) <- NULL
  
  return(prob)
}

getProb_a_b <- function(key, value, topicFile) {
  topics <- read.csv(topicFile, header=TRUE)
  res <- c()
  
  ## for each clusters
  for(clusIndex in 1:ncol(topics)) {
    clusRes <- c()
    
    ## for each members
    for(i in 1:497) {
      clusRes <- c(clusRes, topics[i, clusIndex])
    }
    
    res <- c(res, mean(clusRes))
    
  }
  
  return(res)
}


#a = cluster1
#b = answer enquete
#c = answer 1
#P(c|a,b) = p(a|b,c)p(c|b) / p(a|b)
getResult <- function(topicDistFile, key, value, saveDist = "~/Developer/M1/competition/DataComp/Yagi/aggregate/result/") {
  library(ggplot2)
  library(gridExtra)
  
  var1 <- getProb_a_bc(topicDistFile, key, value)
  var2 <- getProb_c_b(key, value)
  var3  <-getProb_a_b(key, value, topicDistFile )
  
  result <- c()
  
  numOfCluters = length(var1)
  
  for(i in 1:numOfCluters) {
    
    r <- (var1[i] * var2) / var3[i]
    
    result <- c(result, r)
  }
  
  # save the graph
  df = data.frame(result)
  
  graph_1 <- ggplot(df, aes(seq_along(result), result)) + 
            geom_bar(stat='identity', fill='steelblue') +
            geom_text(aes(label=round(result, 5)), size=6, vjust=1.5, color="white") + 
            labs(title=paste(key, value, ' (overall)'), x='cluster', y='expected value of probability') +
            ylim(0,1)
  
  graph_2 <- ggplot(df, aes(seq_along(result), result)) +
            geom_bar(stat='identity', fill='steelblue') +
            geom_text(aes(label=round(result, 5)), size=6, vjust=1.5, color="white") + 
            labs(title=paste(key, value, '(focus)'), x='cluster', y='expected value of probability')

  
  chart <- arrangeGrob(graph_1, graph_2, nrow=2)
  file <- paste(saveDist, key, "_", value,".png",sep="")
  ggsave(file=file, chart)
  
  return(result)
}
