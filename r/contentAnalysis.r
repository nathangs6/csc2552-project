########################
### Import Libraries ###
########################
library(stm)

#############################
### Initialize Parameters ###
#############################
options(encoding = "UTF-8")
pdf("output/contentMaterial.pdf", 8,10)
numTopics <- 16
numLabels <- 5
numThoughtExamples <- 2
numThoughtTitleExamples <- 10
thoughtLength <- 1000

###################
### Import Data ###
###################
fulldata <- read.csv("../data/output/farData.csv", header = TRUE, fileEncoding = "UTF-8")
# shortdata will be used for visualization of results at end
shortdata <- data.frame(fulldata)
shortdata$content <- strtrim(shortdata$content, thoughtLength)
# Remove variables that aren't needed for stm
fulldata$title <- NULL
fulldata$domain <- NULL
fulldata$leaning <- NULL
fulldata$date <- NULL
fulldata$url <- NULL

#####################
### Get STM Model ###
#####################
constructModel <- FALSE
if (constructModel == TRUE) {
    # Process data
    processed <- textProcessor(fulldata$content, metadata=fulldata)
    out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
    docs <- out$documents
    vocab <- out$vocab
    meta <- out$meta
    
    # Construct model
    fit <- stm(documents=docs, vocab=vocab, K=numTopics, data=meta, prevalence=~far, content=~far, init.type="Spectral", max.em.its=75, seed=238725)

    # Get metadata effects
    effects <- estimateEffect(1:numTopics ~ far, fit, meta, uncertainty="Global")
    data_to_save = list(out=out, stm=fit, effects=effects)
    saveRDS(data_to_save, "output/contentSTM.rds")
} else {
    # Load model
    loaded_data <- readRDS("output/contentSTM.rds")
    out <- loaded_data$out
    docs <- out$documents
    vocab <- out$vocab
    meta <- out$meta
    fit <- loaded_data$stm
    effects <- loaded_data$effects
}

#######################
### Export Findings ###
#######################
# Get global topic summary
plot(fit, type="summary")
# Get per topic summary
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
par(mfrow = c(1, 1), mar = c(3, 3, 3, 3))
for (x in 1:numTopics) {
    writeLines(paste("\nTopic ", x))
    # Get highly related article introductions
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$topics[x,])))
    # Get highly related article titles
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$topics[x,])))
    # Get highly related titles from left-leaning domains
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x, meta=meta, where=far=="left")
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": Far Left"))
    # Get highly related urls from left-leaning domains
    thoughts <- findThoughts(fit, texts=shortdata$url, n=numThoughtTitleExamples, topics=x, meta=meta, where=far=="left")
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": Far Left URLs"))
    # Get highly related titles from right-leaning domains
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x, meta=meta, where=far=="right")
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": Far Right"))
    # Get highly related urls from right-leaning domains
    thoughts <- findThoughts(fit, texts=shortdata$url, n=numThoughtTitleExamples, topics=x, meta=meta, where=far=="right")
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": Far Right URLs"))
    # Get word cloud
    cloud(fit, topic=x, main=paste("Topic ", x, ": Word Cloud"))
    # Get leaning-contrasted words
    plot(fit, type="perspectives", topics=x, main=paste("Topic ", x, ": Content Breakdown"))
}

# Clean up
dev.off()
