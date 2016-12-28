
getProbByCluster <- function(file) {
  topics <- read.csv(file, header = FALSE)
  
  clusterCount <- ncol(topics)
  result <- c()
  
  # Get mean of each cluster
  for (i in 1:clusterCount) {
    result <- c(result, mean(topics[,i]))
  }
  
  return(result)
}


getProbFromMember <- function(key, value) {
  file <- '../../../data/member_analyzed.csv'
  members <- read.csv(file,header=TRUE)
  
  # 条件の行数を取得する
  count <- table(members[key] == value)[2]
  
  prob <- count / nrow(members)
  names(prob) <- NULL
  
  return(prob)
}


getProbForMemberByCluster <- function(key, value, topicFile, file) {
  file <- '../../../data/member_analyzed.csv'
  members <- read.csv(file, header=TRUE)
  tmp <- members[key] == value
  
  topics <- read.csv(topicFile, header=TRUE)
  res <- c()
  
  ## for each clusters
  for(clusIndex in 1:ncol(topics)) {
    clusRes <- c()
    
    ## for each members
    for(i in 1:nrow(topics)) {
      if(tmp[i] == TRUE) {
        # only check cluster 1
        clusRes <- c(clusRes, topics[i, clusIndex])
      }
    }
    
    res <- c(res, mean(clusRes))
    
  }
  
  return(res)
}


getResult <- function(topicDistFile, memberFile, key, value, saveDist = "~/Developer/M1/competition/DataComp/Yagi/aggregate/result/") {
  library(ggplot2)
  library(gridExtra)
  # P(男)
  var1 <- getProbFromMember(key, value)
  # P(クラスタ|男)
  var2 <- getProbForMemberByCluster(key, value, topicDistFile, memberFile)
  # P(クラスタ)
  var3  <-getProbByCluster(topicDistFile)
  
  result <- c()
  
  numOfCluters = length(var2)
  
  for(i in 1:numOfCluters) {
    
    r <- (var2[i] * var1) / var3[i]
    
    result <- c(result, r)
  }
  
  # save the graph
  df = data.frame(result)
  
  graph_1 <- ggplot(df, aes(seq_along(result), result)) + 
            geom_bar(stat='identity', fill='steelblue') +
            geom_text(aes(label=round(result, 5)), size=8, vjust=1.5, color="white") + 
            labs(title=paste(key, value, ' (overall)'), x='cluster', y='expected value of probability') +
            ylim(0,1)
  
  graph_2 <- ggplot(df, aes(seq_along(result), result)) +
            geom_bar(stat='identity', fill='steelblue') +
            geom_text(aes(label=round(result, 5)), size=8, vjust=1.5, color="white") + 
            labs(title=paste(key, value, '(focus)'), x='cluster', y='expected value of probability')

  
  chart <- arrangeGrob(graph_1, graph_2, nrow=2)
  file <- paste(saveDist, key, "_", value,".png",sep="")
  ggsave(file=file, chart)
  
  return(result)
}
