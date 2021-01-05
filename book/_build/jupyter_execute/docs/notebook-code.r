packages <- c("ggplot2", 
              "dplyr", 
              "parallel", 
              "mlr3", 
              "DBI", 
              "bigrquery", 
              "tidyverse",
              "data.table",
              "ggmap",
              "mlr3learners",
              "mlr3filters",
              "mlr3viz",
              "mlr3pipelines",
               "mlr3tuning",
              "glmnet",
              "paradox",
              "ranger",
              "kknn",
             "ggExtra"
             ,"GGally")
install.packages(setdiff(packages, rownames(installed.packages())))
lapply(packages, require, character.only = TRUE, quietly = TRUE)


# billing <- "ml-vm-290912" #project ID 

# con <- dbConnect(
#   bigrquery::bigquery(),
#   project = "properati-data-public",
#   dataset = "properties_br",
#   billing = billing
# )
# options(scipen=20) #prevent integer error in R


# ptm <- proc.time()
# datalist = list()
#     sqlstr1 = "SELECT id, 
#                 created_on, 
#                 operation, 
#                 property_type, 
#                 place_name, 
#                 state_name, 
#                 lat, 
#                 lon, 
#                 price_aprox_usd, 
#                 surface_total_in_m2, 
#                 surface_covered_in_m2, 
#                 price_usd_per_m2, 
#                 floor, 
#                 rooms 
#                 FROM `properati-data-public.properties_br."
#     sqlstr2 = "` WHERE NOT (lat IS NULL OR 
#                             lon IS NULL OR
#                             place_name IS NULL OR
#                             state_name IS NULL OR
#                             price_aprox_usd IS NULL)"
# paster <- function(i) {  
#             sql <- paste0(sqlstr1,dbListTables(con)[i],sqlstr2)
#             tb <- bq_project_query(billing, sql)
#             dat = bq_table_download(tb)
#             return(dat)  
# }
# numCores <- detectCores()
# numTbl <- length(dbListTables(con))
# datalist <- mclapply(1:numTbl, paster, mc.cores=numCores)
# df <- bind_rows(datalist)
# proc.time() - ptm
# write.csv(df,"brazil.csv", row.names = FALSE)


df = fread("brazil.csv",drop = 1)
df = as_tibble(df)
df_orig = df

head(df, n=5)

df %>% count(id) %>% ggplot(aes(x=n)) + geom_histogram(binwidth=1,color="black", fill="green")

df %>% count(id) %>% filter(n==6) %>% head(n=2)

df %>% filter(id=="000059ce72528af3a35e956b9217f444c3a67a8f") %>% head()

dim(df)
df <- df %>% distinct()
dim(df)

#select only columns predictors and drop with nas
df <- df %>%  select(-(price_aprox_usd:surface_covered_in_m2)) %>%  
        select(-(floor:rooms))
dim(df)
df <- df %>% drop_na()
dim(df)


df %>% count(id) %>% ggplot(aes(x=n)) + geom_histogram(binwidth=1,color="black", fill="green")

df %>% count(id) %>% filter(n==6) %>% head(n=2)

df %>% filter(id=="0000800755b8cda73539b32ad25cfd9c96adacc8")

df <- df %>% 
        group_by(id) %>%
        filter(price_usd_per_m2 == min(price_usd_per_m2)) %>% 
        ungroup()


df %>% filter(id=="0000800755b8cda73539b32ad25cfd9c96adacc8")

df %>% count(id) %>% ggplot(aes(x=n)) + geom_histogram(binwidth=1,color="black", fill="green")


df %>% count(state_name) %>% arrange(desc(n))

df %>% count(state_name) %>% arrange(desc(n)) %>% ggplot(aes(x=state_name, y=n)) +
geom_bar(stat="identity", fill="steelblue") + 
coord_flip()


df = df %>% filter(state_name =="São Paulo")

df %>% count(place_name) %>% arrange(desc(n)) %>% select(place_name) %>% head(n=20)


places = df %>% count(place_name) %>% arrange(desc(n)) %>% select(place_name) %>% head(n=10)
places[[1]]

df = df %>% filter(place_name %in% places[[1]])

df <- df %>% 
    select(-c(id,state_name)) %>%  
    mutate(across(where(is.character), as.factor))
head(df, n=3)

 ggplot(df, aes(x = price_usd_per_m2)) + geom_density()


ggplot(df %>% 
       filter(price_usd_per_m2 < 10000 & price_usd_per_m2 > 40) %>% 
       select(price_usd_per_m2), aes(x = price_usd_per_m2)) + 
    geom_density()


plot_density1 = ggplot(df %>% filter(operation=="rent") %>% 
       filter(price_usd_per_m2 < 100 & price_usd_per_m2 > 40) %>% 
       select(price_usd_per_m2,property_type), aes(x = log(price_usd_per_m2), fill=property_type)) + 
    geom_density(alpha=0.3)


plot_density1

plot_density2 = ggplot(df %>% filter(operation=="sell") %>% 
       filter(price_usd_per_m2 < 10000 & price_usd_per_m2 > 40) %>% 
       select(price_usd_per_m2,property_type), aes(x = log(price_usd_per_m2), fill=property_type)) + 
    geom_density(alpha=0.3)


plot_density2

table(df$operation,df$property_type)

plot_bar1 = ggplot(data=df %>% filter(price_usd_per_m2 < 10000 & price_usd_per_m2 > 40) %>% 
       select(price_usd_per_m2,property_type, operation), aes(x=operation, y=price_usd_per_m2, fill=property_type)) +
geom_bar(stat="identity", position=position_dodge())

plot_bar1

dim(df)
df = df %>% filter(price_usd_per_m2 < 10000 & price_usd_per_m2 > 40) %>% arrange(-desc(price_usd_per_m2))
dim(df)

p =  ggplot(df, aes(x=lat, y=lon)) + 
  geom_point(aes(color=log(price_usd_per_m2))) +
theme(legend.position="none")
p1 = ggMarginal(p,type="histogram")
      

p1

df_border = df %>% filter(between(lon, -53.2,-44.01) & 
                              between(lat, -25.45,-19.67))

p =  ggplot(df_border, aes(x=lat, y=lon)) + 
  geom_point(aes(color=log(price_usd_per_m2))) +
theme(legend.position="none")
p1 = ggMarginal(p,type="histogram")
p1


df = df_border

plot_viz1 = ggpairs(df %>% select(-c(created_on,operation,place_name,property_type)), title="Correlogram") 

plot_viz1

#date
plot_viz2 = ggplot(df, aes(x=created_on, y=log(price_usd_per_m2))) + 
  geom_point()+geom_smooth(method=lm)+ 
  facet_grid(property_type ~ operation) 

plot_viz2

#operation
plot_viz3 = qplot(x=operation, y=log(price_usd_per_m2),data=df, geom=c("boxplot"))+ 
  facet_grid(. ~ property_type) 

plot_viz3

#states
plot_viz4 = qplot(x=place_name, y=log(price_usd_per_m2),data=df, geom=c("boxplot"))+
theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

plot_viz4

df_task = df %>% select(-c(created_on))

#write.csv(df_task,"df_task.csv", row.names = FALSE)

#df_task = as_tibble(read.csv("df_task.csv"))

head(df_task)

price_predict = TaskRegr$new("price_predict", backend = df_task, target = "price_usd_per_m2")

#factor encoder
fencoder = po("encode", method = "treatment",
  affect_columns = selector_type("factor"))
fencoder$train(list(price_predict))
print(price_predict)

tuner_grid = mlr3tuning::tnr("grid_search", resolution = 2L)

term_evals = trm("evals", n_evals = 2L)

resampling_cv = rsmp("cv", folds = 2L)
resampling_outer = rsmp("cv", folds = 3L)

measure = msr("regr.rmse")

rpart_learner = lrn("regr.rpart")

rpart_learner$param_set

# hyperparameter
param_set_cart = ParamSet$new(
  params = list(
    ParamInt$new("minsplit", lower = 1L, upper = 5L),
    ParamDbl$new("cp", lower = 0.01, upper = 0.1)
  )
)

set.seed(123456)
at_rpart = AutoTuner$new(rpart_learner,
  resampling = resampling_cv,
  measure = measure,
  search_space = param_set_cart,
  terminator = term_evals,
  tuner = tuner_grid
)

at_rpart$train(price_predict)
archive_rpart = at_rpart$archive$data()[, c("regr.rmse",
                                            "minsplit",
                                            "cp")]

print(archive_rpart)

lm_learner = lrn("regr.lm")


pipe_xgb = fencoder %>>% lrn("regr.xgboost")
xgb_learner = GraphLearner$new(pipe_xgb)

xgb_learner$param_set

param_set_xgb = ParamSet$new(
  params = list(
    ParamInt$new("regr.xgboost.eta", lower = 0L, upper = 1L)
  )
)

set.seed(123456)
at_xgb = AutoTuner$new(xgb_learner,
  resampling = resampling_cv,
  measure = measure,
  search_space = param_set_xgb,
  terminator = term_evals,
  tuner = tuner_grid
)

at_xgb$train(price_predict)

archive_at_xgb = at_xgb$archive$data()[, c("regr.rmse",
                                          "regr.xgboost.eta")]
print(archive_at_xgb)

#pipe_ranger = fencoder %>>% lrn("regr.ranger", importance = "impurity")
#ranger_learner_encoded = GraphLearner$new(pipe_ranger)


ranger_learner = lrn("regr.ranger", importance = "impurity")

filter_ranger = flt("importance", learner = ranger_learner)
filter_ranger$calculate(price_predict)
feature_importance = as.data.table(filter_ranger)

feature_importance

ranger_learner$param_set
#ranger_learner_encoded$param_set

param_set_ranger = ParamSet$new(
  params = list(
    ParamInt$new("regr.ranger.mtry", lower = 1L, upper = 5L),
    ParamInt$new("importance.filter.nfeat", lower = 1L, upper = 5L)
  )
)

po_flt = po("filter", filter_ranger, param_vals = list(filter.nfeat = 5L)) %>>%
  po("learner", ranger_learner$clone())

grid = generate_design_grid(param_set_ranger, resolution = 5)
grid$data = grid$data[regr.ranger.mtry <= importance.filter.nfeat]
grid$data = grid$data[importance.filter.nfeat %in% c(1, 2, 3, 5)]

set.seed(123456)

ranger_learner_graph = GraphLearner$new(po_flt)

at_ranger = AutoTuner$new(ranger_learner_graph,
  resampling = resampling_cv,
  measure = measure,
  search_space = param_set_ranger,
  terminator = term_evals,
  tuner = mlr3tuning::tnr("design_points", design = grid$data)
)

# at_ranger$store_tuning_instance = FALSE
at_ranger$train(price_predict)

archive_ranger = at_ranger$archive$data()[, c("regr.rmse","importance.filter.nfeat","regr.ranger.mtry")]
print(archive_ranger)

lrns = list(rpart_learner,
            lm_learner,
            xgb_learner,
            ranger_learner,
            at_rpart,
            at_xgb,
            at_ranger
)
design = benchmark_grid(
  tasks = price_predict,
  learners = lrns,
  resamplings = resampling_outer
)
set.seed(123456)
bmr = benchmark(design)
bmr_table = bmr$aggregate(msr("regr.rmse")) %>%
  select(-c(nr, resample_result, task_id))

plot_bmr = autoplot(bmr, measure = msr("regr.rmse")) +
  theme_bw() +
  labs(y = "RMSE") +
  coord_flip() +
  theme(axis.title = element_text(size = 9))

plot_bmr

bmr_table = bmr$aggregate(msr("regr.rmse")) %>%
  select(-c(nr, resample_result, task_id))

bmr_table

trained = ranger_learner$train(price_predict)

prediction = trained$predict(price_predict)

dt_prediction = as.data.table(prediction)
dt_prediction[, differences := truth - response]
dt_prediction[, model_valuation := ifelse(differences < 0, "under", "over")]
dt_prediction[, model_valuation := as.factor(model_valuation)]
setnames(dt_prediction, "response", "predict_price")

dt_prediction[, c("row_id","truth") := NULL]

tb_prediction = as_tibble(dt_prediction)
head(tb_prediction)

df_final = df_task
df_final = bind_cols(df_final, tb_prediction)

head(df_final %>% filter(operation=="sell" & property_type=="apartment"))


p =  ggplot(df_final %>% filter(operation=="sell" & property_type=="apartment"), aes(x=price_usd_per_m2, y=predict_price)) + 
  geom_point(aes(color=differences)) +
theme(legend.position="none")
p1 = ggMarginal(p,type="histogram")

p1

# for comparison
trained2 = at_xgb$train(price_predict)
prediction2 = trained2$predict(price_predict)

dt_prediction2 = as.data.table(prediction2)
dt_prediction2[, differences := truth - response]
dt_prediction2[, model_valuation := ifelse(differences < 0, "under", "over")]
dt_prediction2[, model_valuation := as.factor(model_valuation)]
setnames(dt_prediction2, "response", "predict_price")
dt_prediction2[, c("row_id","truth") := NULL]
tb_prediction2 = as_tibble(dt_prediction2)

df_final2 = df_task
df_final2 = bind_cols(df_final2, tb_prediction2)

q =  ggplot(df_final2 %>% filter(operation=="sell" & property_type=="apartment"), aes(x=price_usd_per_m2, y=predict_price)) + 
  geom_point(aes(color=differences)) +
theme(legend.position="none")



q1 = ggMarginal(q,type="histogram")
q1

trained3 = lm_learner$train(price_predict)
prediction3 = trained3$predict(price_predict)

dt_prediction3 = as.data.table(prediction3)
dt_prediction3[, differences := truth - response]
dt_prediction3[, model_valuation := ifelse(differences < 0, "under", "over")]
dt_prediction3[, model_valuation := as.factor(model_valuation)]
setnames(dt_prediction3, "response", "predict_price")
dt_prediction3[, c("row_id","truth") := NULL]
tb_prediction3 = as_tibble(dt_prediction3)

df_final3 = df_task
df_final3 = bind_cols(df_final3, tb_prediction3)

r =  ggplot(df_final3 %>% filter(operation=="sell" & property_type=="apartment"), aes(x=price_usd_per_m2, y=predict_price)) + 
  geom_point(aes(color=differences)) +
theme(legend.position="none")
r1 = ggMarginal(r,type="histogram")

r1

head(df_final)

#plot_model1 = 
ggplot(df_final, aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()+facet_wrap(.~property_type)

plot_model = ggplot(df_final %>% filter(operation=="sell"), aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()

plot_model

plot_centro = ggplot(df_final %>% filter(operation=="rent"), aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()

plot_centro


 map_centro = qmplot(lon, lat, maptype = "watercolor", color = differences,size = 2,
   data = df_final %>% filter(operation=="rent" & place_name=="Centro" & 
                              between(lon, -47.1555,-46.54756) & 
                              between(lat, -23.71091,-23.14523))) + 
                            scale_colour_gradient(low = "red", high = "green")
 

map_centro

#plot_model1 = 
ggplot(df_final %>% filter(property_type=="PH"), aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()

plot_model2 = ggplot(df_final %>% filter(property_type=="apartment"), aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()

plot_model2

map_cotia = qmplot(lon, lat, maptype = "watercolor", color = differences, size = 2,
   data = df_final %>% filter(place_name=="Cotia" & property_type=="apartment")) + 
                            scale_colour_gradient(low = "red", high = "green")

map_cotia

map_moema = qmplot(lon, lat, maptype = "watercolor", color = differences, size = 2,
   data = df_final %>% filter(place_name=="Moema" & property_type=="apartment"& 
                              between(lon, -46.67848,-46.64879) & 
                              between(lat, -23.65011,-23.6021))) + 
                            scale_colour_gradient(low = "red", high = "green")


map_moema

plot_model3 = ggplot(df_final %>% filter(property_type=="store"), aes(x=place_name, y=differences, fill=model_valuation))+
  geom_bar(stat="identity")+coord_flip()

plot_model3


plot_praia = qmplot(lon, lat, maptype = "watercolor", color = log(price_usd_per_m2),size=1,
  data = df_final %>% filter(place_name=="Praia Grande" & between(lon, -46.47359,-46.41666))) + 
scale_colour_gradient(low = "red", high = "green")

plot_praia
