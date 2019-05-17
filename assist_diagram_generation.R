rm(list=ls())
library(circlize)
colors1 = c("#d73027","#f46d43","#fdae61","#fee090","#ffffbf","#e0f3f8","#abd9e9","#74add1","#4575b4")
width = 1800
height = width/1.5


teamTotal = c("Mavericks","Warriors","Lakers","Rockets","Heat","Celtics","Bucks","Spurs")
for(index in 1:length(teamTotal)){
  team = teamTotal[index]
  for(year in c(2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016)){
    nameTeamYear = paste(c(team, " ", year), collapse ="")
    nameTeamYearTally = paste(c(team, " ", year, " tally.csv"), collapse ="")
    address = paste(c('~/Desktop/Classes/NBA/thesis/code/real/scrapingDone/',team,"/",nameTeamYear),collapse="")
    setwd(address)
    df <- read.csv(nameTeamYearTally, header = TRUE)
    total_players <- length(df)-1
    counter_row <- 1
    counter_column <- 1
    
    assignedColor = colors1
    address = paste(c('~/Desktop/Classes/NBA/thesis/code/real/scrapingDone/',team),collapse="")
    setwd(address)
    
    #saves assist diagram generated as a png 
    png(file=paste(c(nameTeamYear, ".png"), collapse =""), width, height)
    
    # creates assist diagrams
    circos.par(start.degree = 90, clock.wise = TRUE)
    chordDiagram(df, grid.col = assignedColor, transparency=0, directional = 1, 
                 direction.type = c("arrows"), link.arr.type = "big.arrow",
                 link.sort = TRUE, link.decreasing = TRUE, link.rank = rank(df[[3]]),
                 annotationTrack = c("grid"), annotationTrackHeight = uh(15, "mm"))
    
    # creates axis around diagram
    for (sector in unique(df$passer)) {
      circos.axis(labels = TRUE, major.tick = TRUE, 
                  major.tick.percentage = 0.5, labels.away.percentage = major.tick.percentage/2,
                  lwd = par("lwd"), col = par("col"), labels.col = par("col"),
                  labels.cex = convert_y(25,"mm"), major.tick.length = convert_y(5,"mm"),
                  sector.index=sector)
    }
    
    # fixes orientation of names
    for(si in get.all.sector.index()) {
      xlim = get.cell.meta.data("xlim", sector.index = si, track.index = 1)
      ylim = get.cell.meta.data("ylim", sector.index = si, track.index = 1)
      circos.text(mean(xlim), mean(ylim), si, sector.index = si, track.index = 1, cex=2,
                  facing = "bending.inside", niceFacing = TRUE, col = "black")
    }

    # capitablizes title
    simpleCap <- function(x) {
      s <- strsplit(x, " ")[[1]]
      paste(toupper(substring(s, 1,1)), substring(s, 2),
            sep="", collapse=" ")
    }
    # nameTeamYear = simpleCap(team)
    par(adj=.78)
    title(main=simpleCap(team), cex.main=5, line=-4, outer=FALSE)
    par(adj=.8)
    title(main=year, cex.main=5, line=-8, outer=FALSE)
    print(nameTeamYear)
    dev.off()
    circos.clear()
  }
}
