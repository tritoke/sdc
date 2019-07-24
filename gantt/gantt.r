#!/usr/bin/env Rscript

# this code is all adapted from this blog post:
# https://www.molecularecologist.com/2019/01/simple-gantt-charts-in-r-with-ggplot2-and-the-tidyverse/

require("tidyverse")

gantt <- read.csv("data.csv")
tasks <- as.vector(gantt$task)
depts <- as.vector(gantt$department)
gantt$item <- 1:length(gantt$task)

head(gantt)

g.gantt <- gather(gantt, "state", "date", 3:4) %>% mutate(date = as.Date(date, "%d/%m/%Y"), task=factor(task, tasks[length(tasks):1]), department=factor(department, unique(depts)))

head(g.gantt)

plot <- ggplot(g.gantt, aes(date, task, color = department, group=item)) +
  geom_line(size = 10) +
  labs(x="Year", y=NULL, title="Project timeline")

svg("gantt.svg")
print(plot)
dev.off()

ggsave("gantt.png", plot=plot)
