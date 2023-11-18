library(stm)
#############################
### Initialize parameters ###
#############################
options(encoding = "UTF-8")
pdf("output/contentMaterial.pdf", 8,10)
numTopics <- 8
numLabels <- 5
numThoughtExamples <- 2
numThoughtTitleExamples <- 10
thoughtLength <- 1000

#####################
### Content Model ###
#####################
# Import data
fulldata <- read.csv("../data/output/farData.csv", header = TRUE, fileEncoding = "UTF-8")
shortdata <- data.frame(fulldata)
shortdata$content <- strtrim(shortdata$content, thoughtLength)

fulldata$title <- NULL

attributes(fulldata)

# process data
processed <- textProcessor(fulldata$content, metadata=fulldata)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Prevalence estimate
writeLines("\nConstructing prevalence model")
fit <- stm(documents=docs, vocab=vocab, K=numTopics, data=meta, prevalence=~far, content=~far, init.type="Spectral", max.em.its=75, seed=238725)
saveRDS(fit, file="output/contentSTM.rds")
plot(fit, type="summary")

# Output Visualizations
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
#par(mfrow = c(1, 1), mar = c(0.5, 0.5, 2, 0.5))
par(mfrow = c(1, 1), mar = c(3, 3, 3, 3))
for (x in 1:numTopics) {
    writeLines(paste("\nTopic ", x))
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$topics[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$topics[x,])))
    cloud(fit, topic=x)
    plot(fit, type="perspectives", topics=x)
}

# Clean up
dev.off()
