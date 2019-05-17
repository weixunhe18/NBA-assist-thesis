library(plotly)
library(plyr)

summary <- "summaryByEra.csv"
address <- '~/Desktop/Classes/NBA/thesis/code/real/scrapingDone/zdata processing'
# address <- '~/Desktop'
setwd(address)
df <- read.csv(summary)
str(df)

# DAL,GSW,LAL,HOU,MIA,BOS,MIL,SAS
pal <- c("blue", "orange", "purple", "yellow2","black", "red", "green", "magenta", "darkgray")
# pal <- setNames(pal, c("Mavericks","Warriors","Lakers","Rockets","Heat","Celtics","Bucks","Spurs"))
# "DAL","GSW","LAL","HOU","MIA","BOS","MIL","SAS"
# "Mavericks","Warriors","Lakers","Rockets","Heat","Celtics","Bucks","Spurs"
pal <- setNames(pal, c("Mavericks (2005-2011)","Warriors (2013-2015)","Lakers (2005-2011)","Rockets (2012-2015)","Rockets (2006-2011)","Heat (2010-2013)","Celtics (2007-2011)","Bucks","Spurs (2005-2015)"))
result <- c(23,16,1)
result <- setNames(result, c("champ","playoff", "missed"))

# aggregate data
df_agg <- ddply(df, .(Team), summarise, 
    Out2in.Variance_M = mean(Out2in.Variance, na.rm = TRUE),
    Out2in.Variance_SD = sd(Out2in.Variance, na.rm = TRUE),
    Contribution.Variance_M = mean(Contribution.Variance, na.rm = TRUE),
    Contribution.Variance_SD = sd(Contribution.Variance, na.rm = TRUE),
    Offensive.Rating_M = mean(Offensive.Rating, na.rm = TRUE),
    Offensive.Rating_SD = sd(Offensive.Rating, na.rm = TRUE))

# ortg v out2in var
plot_ly(df_agg, type="scatter", mode="markers", x=~Contribution.Variance_M, y=~Offensive.Rating_M, 
        error_x = ~list(array = Contribution.Variance_SD), error_y = ~list(array = Offensive.Rating_SD),
        color=~Team, colors=pal
)
