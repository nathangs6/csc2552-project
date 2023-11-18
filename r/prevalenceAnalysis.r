library(stm)
#############################
### Initialize parameters ###
#############################
options(encoding = "UTF-8")
pdf("output/prevalenceMaterial.pdf", 8,10)
numTopics <- 8
numLabels <- 5
numThoughtExamples <- 2
numThoughtTitleExamples <- 10
thoughtLength <- 1000

########################
### Prevalence Model ###
########################
# Import data
fulldata <- read.csv("../data/output/cleanedData.csv", header = TRUE, fileEncoding = "UTF-8")
shortdata <- data.frame(fulldata)
shortdata$content <- strtrim(shortdata$content, thoughtLength)

fulldata$title <- NULL
fulldata$far_right <- NULL
fulldata$date <- fulldata$date / 86400

# process data
processed <- textProcessor(fulldata$content, metadata=fulldata)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

# Prevalence estimate
writeLines("\nConstructing prevalence model")
prevalence_formula = ~ leaning + domain + s(date)
fit <- stm(documents=docs, vocab=vocab, K=numTopics, data=meta, prevalence=prevalence_formula, init.type="Spectral", max.em.its=75, seed=238725)
saveRDS(fit, file="output/prevalenceSTM.rds")
plot(fit, type="summary")

# Use metadata
effects <- estimateEffect(1:numTopics ~ leaning + domain + s(date), fit, meta, uncertainty="Global")
summary(effects, topics=1)

# Output Visualizations
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
#par(mfrow = c(1, 1), mar = c(0.5, 0.5, 2, 0.5))
par(mfrow = c(1, 1), mar = c(3, 3, 3, 3))
for (x in 1:numTopics) {
    writeLines(paste("\nTopic ", x))
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    cloud(fit, topic=x)
    plot(effects, "date", method = "continuous", topics = x, model=z, xaxt="n", printlegend = FALSE, xlab="Month")
    dates <- as.Date(fulldata$date, origin="1970-01-01")
    years <- format(dates, "%Y")
    axis(1, at=fulldata$date, labels=years)
}

# Clean up
dev.off()
