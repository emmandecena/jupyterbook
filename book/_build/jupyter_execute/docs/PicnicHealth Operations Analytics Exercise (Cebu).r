library(dplyr)
library(ggplot2)
library(ggridges)
library(ggsci)
library(lubridate)
library(tidyverse)
options(repr.plot.width=12, repr.plot.height=8)
options(warn=0)

tasks = read_csv("/Volumes/data/work/picnichealth/tasks.csv", col_types = "cTTccccc")
tasks_group = read_csv("/Volumes/data/work/picnichealth/task_group.csv")
records = read_csv("/Volumes/data/work/picnichealth/records.csv")
timesheet = read_csv("/Volumes/data/work/picnichealth/timesheet_entries.csv")

#renaming cols for join match
tasks <- tasks %>% rename(task_id = id)
records <- records %>% rename(record_id = id)
#join tasks table with records info; pages, uploaded date
tasks_records = left_join(tasks,records,by = c("record_id" = "record_id"))
#join tasks table with created tasks group - simplified task grouping
tasks_records = left_join(tasks_records,tasks_group,by = c("task_type" = "task_type"))
#tables for joining previous task type from prev task id
prev = tasks_records %>% select(previous_task_task_id)
curr = tasks_records %>% select(task_id,task_type)
#join info for previous tasks
previous_task = left_join(prev,curr,by = c("previous_task_task_id" = "task_id")) %>% rename(previous_task_type = task_type) %>% select(previous_task_type)
previous_task = left_join(previous_task,tasks_group, by = c("previous_task_type" = "task_type")) %>% rename(previous_task_group = task_group)
#binding
tasks_records = bind_cols(tasks_records,previous_task)

backlogs = filter(tasks_records, is.na(completed_at))
glimpse(backlogs)

tasks %>%
    arrange((completed_at)) 

backlogs = backlogs %>% group_by(task_type, previous_task_type, task_group, previous_task_group) %>% summarise(no = n()) %>% ungroup()
backlogs = mutate(backlogs, 
       task_transition = paste(previous_task_type,"to ",task_type),
       task_group_transition = paste(previous_task_group,"to ",task_group)
      )

#arrange(backlogs, desc(no))

p1 = ggplot(data=filter(backlogs,!is.na(previous_task_type), no > 250), aes(x=reorder(task_type, no, max), y=no, fill=task_group)) +
  geom_bar(stat="identity") + coord_flip() + theme(text = element_text(size = 18)) +
  theme(axis.title=element_blank()) + geom_text(aes(label=no), hjust=2, color="black", size=5) +
    ggtitle("Stand-alone backlog tasks according to task group")



p2 = ggplot(data=filter(backlogs, no > 250), aes(x=reorder(task_type, no, sum), y=no, fill=task_group)) +
  geom_bar(stat="identity") + coord_flip() + theme(text = element_text(size = 18))+
  theme(axis.title=element_blank()) + geom_text(aes(label=no), hjust=2, color="black", size=5)+
    ggtitle("Transition backlog tasks according to task group")

p1

p2

#head(backlogs)

p3 = ggplot(data=filter(backlogs, is.na(previous_task_type),no > 250), aes(x=reorder(task_transition, no, max), y=no, fill=task_group_transition)) +
  geom_bar(stat="identity") + coord_flip() + scale_fill_ucscgb() + 
    theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank()) + 
    geom_text(aes(label=no), hjust=1, color="black", size=5)+
    ggtitle("Stand-alone backlog tasks according to transition")

p4 = ggplot(data=filter(backlogs, !is.na(previous_task_type),no > 250), aes(x=reorder(task_transition, no, max), y=no, fill=task_group_transition)) +
  geom_bar(stat="identity") + coord_flip() + scale_fill_ucscgb() + theme(text = element_text(size = 18))+
  theme(axis.title=element_blank()) + geom_text(aes(label=no), hjust=1, color="black", size=5)+
    ggtitle("Transition backlog tasks according to transition")

p3

p4

write_csv(backlogs, "processed-backlogs.csv")

#tasks_records

#selecting only completed task
turnaround = filter(tasks_records, !is.na(completed_at)) %>% 
    mutate(task_duration = completed_at-created_at) %>% 
    mutate(task_duration_hrs=as.numeric((task_duration/3600))) %>%
    mutate(stand_alone = is.na(previous_task_type))

#turnaround

#plot duration distribution between transistion and standalone tasks
p5 = ggplot(turnaround, aes(x=reorder(task_group, task_duration_hrs, mean), y=task_duration_hrs, fill=task_group))+
    geom_boxplot() + 
    stat_summary(fun=weighted.mean, colour="black", size = 5, geom="text", vjust=0, aes(label=round(..y.., digits=1)))+
    theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank()) +
    ggtitle("Average task duration according to task group")

p5

#weighted mean tell different story
wmean_task_group = turnaround%>% 
   group_by(task_group)%>% 
   summarize(count = n(),mean = mean(task_duration_hrs), wmean = round((count*mean)/11473, digits=2))
wmean_task_group


p6 = ggplot(data=wmean_task_group, aes(x=reorder(task_group, wmean, max), y=wmean, fill=task_group)) +
  geom_bar(stat="identity") + theme(text = element_text(size = 18)) +
  theme(axis.title=element_blank()) + geom_text(aes(label=wmean), vjust=0, color="black", size=5) +
    ggtitle("Count-weighted average task duration according to task group")


p6

#turnaround

p7 = ggplot(turnaround, aes(x = task_duration_hrs, y = task_type, fill = task_type)) +
  geom_density_ridges() +
  theme_ridges() + 
  theme(legend.position = "none") +
    theme(text = element_text(size = 18)) +
  theme(axis.title=element_blank()) +
    ggtitle("Distribution of task duration per specific task")

p7

p8 = ggplot(turnaround, aes(x = task_duration_hrs, y = task_group, fill = task_type)) +
  geom_density_ridges() +
  theme_ridges() + 
  theme(legend.position = "none")+
theme(text = element_text(size = 18)) +
  theme(axis.title=element_blank()) +
    ggtitle("Distribution of task duration per task group")

p8

p9 = ggplot(turnaround, aes(x=reorder(stand_alone, task_duration_hrs, mean), y=task_duration_hrs, fill=stand_alone))+
  geom_boxplot()+ theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank()) +
    ggtitle("Apparent lack of duration difference between Stand-alone/Transition tasks")


p9

p7 = ggplot(turnaround, aes(x=reorder(task_group, task_duration_hrs, mean), y=task_duration_hrs, fill=stand_alone))+
  geom_boxplot()+ theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank()) +
    ggtitle("Difference evident when plotted by task group")

p7

#filter(turnaround,!is.na(num_pages))

p8 = qplot(num_pages, task_duration_hrs, data = filter(turnaround,!is.na(num_pages)), colour = task_type) + 
facet_grid(. ~ task_group)+
theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank()) +
    ggtitle("Task duration versus number of pages per task type")

p8

#interesting to see that num pages is irrelevant to the time it takes to complete the task
p9 = qplot(num_pages, task_duration_hrs, data = filter(turnaround,!is.na(num_pages)), colour = task_group) + 
facet_grid(. ~ task_group)+
theme(text = element_text(size = 18)) +
    theme(axis.title=element_blank())+
    ggtitle("Task duration versus number of pages per task group")

p9

write_csv(turnaround, "processed-turnaround.csv")

#dropping id column since no relevant info found 
timesheet = timesheet %>% select(-id)


#joined task with timesheet entries; tasks without timesheet entries are discared
timesheet_task = left_join(timesheet,tasks,by = c("task_id" = "task_id"))

#join tasks table with created tasks group - simplified task grouping
timesheet_task = left_join(timesheet_task,tasks_group,by = c("task_type" = "task_type"))

timesheet_task = timesheet_task %>% mutate(timesheet_duration = end-start)

timesheet_task = left_join(timesheet_task, select(turnaround, task_id,task_duration),by = c("task_id" = "task_id"))

#looking at tasks completed by same employee
filter(timesheet_task,employee_user_id==completer_user_id)

#completer is not the employee who started
#filter(timesheet_task,employee_user_id!=completer_user_id)

notcompleter = filter(timesheet_task,employee_user_id!=completer_user_id) %>% select(employee_user_id) %>% distinct()

completer = filter(timesheet_task,employee_user_id==completer_user_id) %>% select(employee_user_id) %>% distinct()

setdiff(notcompleter,completer)

#total of 87 employees
timesheet_task %>% select(employee_user_id) %>% n_distinct()

timesheet_task %>% select(task_id) %>% n_distinct()

#filter(timesheet_task, is.na(completed_at))

#groupby task id, then sum total timesheet duration
totals_all = timesheet_task %>% group_by(employee_user_id) %>% 
summarise(backlog = sum(is.na(completed_at)),
          tot_complete = sum(!is.na(completed_at)),
          self_complete = sum(!is.na(completed_at)&employee_user_id==completer_user_id),
          net_complete = tot_complete-backlog,
          .groups = 'drop') %>%
arrange(desc(net_complete),backlog)

(totals_all)

totals_all %>% arrange(desc(backlog)) %>% head()


totals_per_task = timesheet_task %>% group_by(task_group,employee_user_id) %>% 
summarise(backlog = sum(is.na(completed_at)),
          tot_complete = sum(!is.na(completed_at)),
          self_complete = sum(!is.na(completed_at)&employee_user_id==completer_user_id),
          net_complete = tot_complete-backlog,
          .groups = 'drop') %>%
arrange(task_group,desc(net_complete))

filter(totals_per_task, task_group=="PROCESS") %>% head()

filter(totals_per_task, task_group=="CHECK") %>% head()

filter(totals_per_task, task_group=="REVIEW") %>% head()

filter(totals_per_task, task_group=="CALL") %>% head()

write_csv(totals_per_task,"processed-timesheet.csv")

#facet by selected type group_by
target <- c("PROCESS", "OCR", "QUALITY", "CHECK")
performance = totals_per_task %>% filter(task_group %in% task_group)
performance

forfacet = gather(performance, variable, value, -employee_user_id,-task_group)
forfacet

ggplot(forfacet, aes(x=reorder(employee_user_id, value, max), y=value, fill=variable))+
  geom_bar(position="stack", stat="identity")+
  coord_flip()+
theme(text = element_text(size = 18)) +
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
    theme(axis.title=element_blank())+
    ggtitle("Task totals leaderboard")

forfacet %>% filter(variable!="backlog" & value>5)

#task_group %in% target

forteams = forfacet %>% filter(variable!="backlog" & value>5 & task_group %in% target) %>% group_by(task_group, variable)  %>%
    arrange(desc(value), .by_group = TRUE) %>%
   top_n(3, employee_user_id)

forteams



ggplot(forteams, aes(x=employee_user_id, y=log(value), fill=variable, label = task_group))+
  geom_bar(position="stack", stat="identity")+coord_flip() +facet_wrap(~task_group)+
theme(text = element_text(size = 18)) +
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
    theme(axis.title=element_blank())+
    ggtitle("Task Team Leaderboard")

timesheet_task
