library(stm)
# initialize parameters
options(encoding = "UTF-8")
pdf("output/eliminatedMaterial.pdf", 8,10)
numTopics <- 8
numLabels <- 5
numThoughtExamples <- 2
numThoughtTitleExamples <- 10
thoughtLength <- 1000

# import data
fulldata <- read.csv("../data/output/eliminatedData.csv", header = TRUE, fileEncoding = "UTF-8")
shortdata <- data.frame(fulldata)
shortdata$content <- strtrim(shortdata$content, thoughtLength)

fulldata$title <- NULL

# process data
processed <- textProcessor(fulldata$content, metadata=fulldata)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta


# estimate
fit <- stm(documents=docs, vocab=vocab, K=numTopics, data=meta, init.type="Spectral", max.em.its=75, seed=238725)
saveRDS(fit, file="output/eliminatedSTM.rds")
plot(fit, type="summary")

# analyze topics themselves
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
par(mfrow = c(1, 1), mar = c(0.5, 0.5, 2, 0.5))
for (x in 1:numTopics) {
    print(paste("Topic", x, ": ", toString(topicLabels$frex[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    cloud(fit, topic=x)
}

# Clean up
dev.off()
