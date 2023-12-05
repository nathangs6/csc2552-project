library(stm)
#############################
### Initialize parameters ###
#############################
options(encoding = "UTF-8")
pdf("output/prevalenceMaterial.pdf", 8,10)
numTopics <- 16
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
    
constructModel <- FALSE
if (constructModel == TRUE) {
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
    
    # Use metadata
    effects <- estimateEffect(1:numTopics ~ leaning + domain + s(date), fit, meta, uncertainty="Global")
    data_to_save = list(out=out, stm=fit, effects=effects)
    saveRDS(data_to_save, file="output/prevalenceSTM.rds")
} else {
    loaded_data <- readRDS("output/prevalenceSTM.rds")
    out <- loaded_data$out
    fit <- loaded_data$stm
    effects <- loaded_data$effects
}

# Basic output
plot(fit, type="summary")
summary(effects, topics=1)
plot(effects, "date", method = "continuous", topics = 1:numTopics, main="Time Variance Across All Topics", xaxt="n")
dates <- as.Date(fulldata$date, origin="1970-01-01")
start <- format(min(dates), "%Y")
end <- format(max(dates), "%Y")
years <- seq(as.numeric(start), as.numeric(end), by=1)
axis(1,
    at=as.Date(paste0(years, "-01-01")),
    labels=years)
# Output Visualizations
topicLabels <- labelTopics(fit, n = numLabels, frexweight = 0.5)
par(mfrow = c(1, 1), mar = c(3, 3, 3, 3))
for (x in 1:numTopics) {
    writeLines(paste("\nTopic ", x, toString(topicLabels$prob[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$content, n=numThoughtExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$prob[x,])))
    thoughts <- findThoughts(fit, texts=shortdata$title, n=numThoughtTitleExamples, topics=x)
    plotQuote(thoughts$docs[[1]], width=80, main = paste("Topic ", x, ": ", toString(topicLabels$frex[x,])))
    cloud(fit, topic=x)
    plot(effects, "leaning", topics=x, method="difference", cov.value1="right", cov.value2="left", xlab="Left ... Right", xlim=c(-1,1), main="Left vs. Right")
    thoughts <- findThoughts(fit, texts=shortdata$date, n=200, topics=x)
    thought_years <- as.numeric(format(as.Date(as.POSIXct(thoughts$docs[[1]], origin = "1970-01-01")), "%Y"))
    year_counts <- aggregate(thought_years, by=list(thought_years), FUN=length)
    barplot(year_counts$x, names.arg=year_counts$Group.1, las=2, xlab="Year", ylab="Number of Documents", space=0, main=paste("Topic ", x, ": ", "Highly Associated Document Counts by Year"))
    axis(1, at=2008:2021, labels=2008:2021)
    plot(effects, "date", method = "continuous", topics = x, main=paste("Topic ", x, ": Change Over Time"), model=z, xaxt="n", printlegend = FALSE, xlab="Month", linecol=rgb(0.09345636, 0.48744329, 0.71430988), axes=FALSE)
    dates <- as.Date(fulldata$date, origin="1970-01-01")
    start <- format(min(dates), "%Y")
    end <- format(max(dates), "%Y")
    years <- seq(as.numeric(start), as.numeric(end), by=1)
    axis(1,
         at=as.Date(paste0(years, "-01-01")),
         labels=years,
         col="#2f4f4f",
         col.ticks="#2f4f4f",
         col.axis="#2f4f4f")
    axis(2,
         col="#2f4f4f",
         col.ticks="#2f4f4f",
         col.axis="#2f4f4f")
}

for (x in 1:numTopics) {
    thoughts <- findThoughts(fit, texts=shortdata$date, n=200, topics=x)
    thought_years <- as.numeric(format(as.Date(as.POSIXct(thoughts$docs[[1]], origin = "1970-01-01")), "%Y"))
    year_counts <- aggregate(thought_years, by=list(thought_years), FUN=length)
    barplot(year_counts$x, names.arg=year_counts$Group.1, las=2, xlab="Year", ylab="Number of Documents", space=0, main=paste("Topic ", x, ": ", "Highly Associated Document Counts by Year"))
    axis(1, at=2008:2021, labels=2008:2021)
    plot(effects, "date", method = "continuous", topics = x, main=paste("Topic ", x, ": Change Over Time"), model=z, xaxt="n", printlegend = FALSE, xlab="Month", linecol=rgb(0.09345636, 0.48744329, 0.71430988), axes=FALSE)
    dates <- as.Date(fulldata$date, origin="1970-01-01")
    start <- format(min(dates), "%Y")
    end <- format(max(dates), "%Y")
    years <- seq(as.numeric(start), as.numeric(end), by=1)
    axis(1,
         at=as.Date(paste0(years, "-01-01")),
         labels=years,
         col="#2f4f4f",
         col.ticks="#2f4f4f",
         col.axis="#2f4f4f")
    axis(2,
         col="#2f4f4f",
         col.ticks="#2f4f4f",
         col.axis="#2f4f4f")
}
# Clean up
dev.off()

prevalence_out <- out
prevalence_stm <- fit
prevalence_effects <- effects
