########################
### Import Libraries ###
########################
library(stm)

#############################
### Initialize Parameters ###
#############################
# initialize parameters
options(encoding = "UTF-8")
pdf("output/eliminatedMaterial.pdf", 8,10)
numTopics <- 12
numLabels <- 5
numThoughtExamples <- 2
numThoughtTitleExamples <- 10
thoughtLength <- 1000

###################
### Import Data ###
###################
fulldata <- read.csv("../data/output/eliminatedData.csv", header = TRUE, fileEncoding = "UTF-8")
# shortdata will be used for visualization of results at end
shortdata <- data.frame(fulldata)
shortdata$content <- strtrim(shortdata$content, thoughtLength)
# Remove variables that aren't needed for stm
fulldata$title <- NULL

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
    fit <- stm(documents=docs, vocab=vocab, K=numTopics, data=meta, init.type="Spectral", max.em.its=75, seed=238725)
    data_to_save = list(out=out, stm=fit)
    saveRDS(data_to_save, "output/eliminatedSTM.rds")
} else {
    # Load model
    loaded_data <- readRDS("output/eliminatedSTM.rds")
    out <- loaded_data$out
    fit <- loaded_data$stm
}

#######################
### Export Findings ###
#######################
# Get global topic summary
plot(fit, type="summary")
# Get per topic summary
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
par(mfrow = c(1, 1), mar = c(0.5, 0.5, 2, 0.5))
for (x in 1:numTopics) {
    print(paste("Topic", x, ": ", toString(topicLabels$frex[x,])))
    # Get highly related article introductions
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    # Get highly related article titles
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
}
# Clean up
dev.off()
