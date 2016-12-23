
# coding: utf-8

# In[1]:

get_ipython().magic(u'pylab inline')


# In[2]:

get_ipython().magic(u'load_ext rpy2.ipython')


# In[3]:

get_ipython().run_cell_magic(u'R', u'', u'Temp <- read.table("temporal_behaviors.tsv", sep ="\\t",header=TRUE)')


# In[4]:

get_ipython().run_cell_magic(u'R', u'', u'tail(Temp)\ndim(Temp)')


# In[5]:

get_ipython().run_cell_magic(u'R', u'', u'Acct_Purchase <- read.table("acct_purchases_long.tsv", sep ="\\t",header=TRUE)')


# In[6]:

get_ipython().run_cell_magic(u'R', u'', u'tail(Acct_Purchase)\ndim(Acct_Purchase)')


# In[7]:

get_ipython().run_cell_magic(u'R', u'', u'Acct_Purchase_Test <- read.table("acct_purchases_long_test.tsv", sep ="\\t",header=TRUE)')


# In[8]:

get_ipython().run_cell_magic(u'R', u'', u'Acct_Purchase_long <- rbind(Acct_Purchase, Acct_Purchase_Test)\nhead(Acct_Purchase_long)')


# In[9]:

get_ipython().run_cell_magic(u'R', u'', u'unique(Acct_Purchase_long$PROD_NM)')


# In[10]:

get_ipython().run_cell_magic(u'R', u'', u'Acct_Purchase_long$DATE <- as.Date(Acct_Purchase_long$CLSD_DATE, format = "%Y-%m-%d")\nmax(Acct_Purchase_long$DATE)')


# In[11]:

get_ipython().run_cell_magic(u'R', u'', u"# Delete the dataset with invalid account_id\nnew <- Temp[ ! Temp$ACCOUNT_ID %in% c('0','000000000000000'), ] \ndim(new)")


# In[ ]:




# In[12]:

get_ipython().run_cell_magic(u'R', u'', u"# Take the features at '2014-10-01 00:00:00' as base features\nbase = new[new$QRY_DATE == '2014-05-01 00:00:00',]\ndim(base)")


# In[13]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \nAC <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Analytics Cloud" ,]\ndim(AC)')


# In[14]:

get_ipython().run_cell_magic(u'R', u'', u'AC$DATE <- as.Date(AC$CLSD_DATE, format = "%Y-%m-%d")\nmin(AC$DATE) ')


# In[15]:

get_ipython().run_cell_magic(u'R', u'', u'a <- as.Date("2016-05-1", format = "%Y-%m-%d")')


# In[16]:

get_ipython().run_cell_magic(u'R', u'', u'Temp$DATE <- as.Date(Temp$QRY_DATE, format = "%Y-%m-%d")\nmin(Temp$DATE)  #\'2014-10-01\'\nDate <- unique(Temp$DATE)   \nDate <- Date[order(Date)]\n#length(Date)')


# In[17]:

get_ipython().run_cell_magic(u'R', u'', u'Date <- c(Date, a)\nDate ')


# In[18]:

get_ipython().run_cell_magic(u'R', u'', u'# Get labels\n# Baseline\n# Initialze two vectors of lists of length 24\nac_date_list <- vector("list", 25)\nlabel_list <- vector("list", 25)\nm <- vector("list", 25)\nfor (i in 1:25){\n    ac_date_list[[i]] <- AC[AC$DATE <= Date[i],] # Get dataframe for accounts which made a purchase before certain dates\n    label_list[[i]] <- rep(0,dim(base)[1]) # Initialize the label vector at 0 for each account\n    m[[i]] = merge(base, ac_date_list[[i]] , by.x = "ACCOUNT_ID", by.y = "ACCT_ID") \n    label_list[[i]][base$ACCOUNT_ID %in% m[[i]]$ACCOUNT_ID]=1\n}')


# In[19]:

get_ipython().run_cell_magic(u'R', u'', u'table(label_list[[25]])')


# In[20]:

get_ipython().run_cell_magic(u'R', u'', u'save(label_list, file = "Label2.RData")')


# In[22]:

get_ipython().run_cell_magic(u'R', u'', u'write.csv( file = "df1.csv",base)')


# In[ ]:




# In[ ]:




# In[37]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \npd <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Data.com Premium Clean" ,]#pardot #analytic\ndim(pd)')


# In[ ]:




# In[21]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \npd <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Pardot" ,]#pardot #analytic\ndim(pd)')


# In[22]:

get_ipython().run_cell_magic(u'R', u'', u'pd$DATE <- as.Date(pd$CLSD_DATE, format = "%Y-%m-%d")\nmin(pd$DATE) ')


# In[23]:

get_ipython().run_cell_magic(u'R', u'', u'# Get labels\n# Baseline\n# Initialze two vectors of lists of length 24\nac_date_list <- vector("list", 25)\nlabel_list_pc <- vector("list", 25)\nm <- vector("list", 25)\nfor (i in 1:25){\n    ac_date_list[[i]] <- pd[pd$DATE <= Date[i],] # Get dataframe for accounts which made a purchase before certain dates\n    label_list_pc[[i]] <- rep(0,dim(base)[1]) # Initialize the label vector at 0 for each account\n    m[[i]] = merge(base, ac_date_list[[i]] , by.x = "ACCOUNT_ID", by.y = "ACCT_ID") \n    label_list_pc[[i]][base$ACCOUNT_ID %in% m[[i]]$ACCOUNT_ID]=1\n}')


# In[24]:

get_ipython().run_cell_magic(u'R', u'', u'table(label_list_pc[[25]])')


# In[25]:

get_ipython().run_cell_magic(u'R', u'', u'save(label_list_pc, file = "Label4.RData")')


# In[ ]:




# In[26]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \npd <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Sandbox" ,]#pardot #analytic\ndim(pd)')


# In[27]:

get_ipython().run_cell_magic(u'R', u'', u'pd$DATE <- as.Date(pd$CLSD_DATE, format = "%Y-%m-%d")\nmin(pd$DATE) ')


# In[28]:

get_ipython().run_cell_magic(u'R', u'', u'# Get labels\n# Baseline\n# Initialze two vectors of lists of length 24\nac_date_list <- vector("list", 25)\nlabel_list_pc <- vector("list", 25)\nm <- vector("list", 25)\nfor (i in 1:25){\n    ac_date_list[[i]] <- pd[pd$DATE <= Date[i],] # Get dataframe for accounts which made a purchase before certain dates\n    label_list_pc[[i]] <- rep(0,dim(base)[1]) # Initialize the label vector at 0 for each account\n    m[[i]] = merge(base, ac_date_list[[i]] , by.x = "ACCOUNT_ID", by.y = "ACCT_ID") \n    label_list_pc[[i]][base$ACCOUNT_ID %in% m[[i]]$ACCOUNT_ID]=1\n}')


# In[29]:

get_ipython().run_cell_magic(u'R', u'', u'table(label_list_pc[[25]])')


# In[30]:

get_ipython().run_cell_magic(u'R', u'', u'save(label_list_pc, file = "Label5.RData")')


# In[ ]:




# In[35]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \npd <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Customer Community" ,]#pardot #analytic\ndim(pd)')


# In[36]:

get_ipython().run_cell_magic(u'R', u'', u'pd$DATE <- as.Date(pd$CLSD_DATE, format = "%Y-%m-%d")\nmin(pd$DATE) ')


# In[37]:

get_ipython().run_cell_magic(u'R', u'', u'# Get labels\n# Baseline\n# Initialze two vectors of lists of length 24\nac_date_list <- vector("list", 25)\nlabel_list_pc <- vector("list", 25)\nm <- vector("list", 25)\nfor (i in 1:25){\n    ac_date_list[[i]] <- pd[pd$DATE <= Date[i],] # Get dataframe for accounts which made a purchase before certain dates\n    label_list_pc[[i]] <- rep(0,dim(base)[1]) # Initialize the label vector at 0 for each account\n    m[[i]] = merge(base, ac_date_list[[i]] , by.x = "ACCOUNT_ID", by.y = "ACCT_ID") \n    label_list_pc[[i]][base$ACCOUNT_ID %in% m[[i]]$ACCOUNT_ID]=1\n}')


# In[38]:

get_ipython().run_cell_magic(u'R', u'', u'table(label_list_pc[[25]])')


# In[39]:

get_ipython().run_cell_magic(u'R', u'', u'save(label_list_pc, file = "Label6.RData")')


# In[ ]:




# In[ ]:




# In[40]:

get_ipython().run_cell_magic(u'R', u'', u'# Take the subset of purchase history of when the \npd <- Acct_Purchase_long[Acct_Purchase_long$PROD_NM=="Data.com Premium Clean" ,]#pardot #analytic\ndim(pd)')


# In[41]:

get_ipython().run_cell_magic(u'R', u'', u'pd$DATE <- as.Date(pd$CLSD_DATE, format = "%Y-%m-%d")\nmin(pd$DATE) ')


# In[42]:

get_ipython().run_cell_magic(u'R', u'', u'pd$DATE <- as.Date(pd$CLSD_DATE, format = "%Y-%m-%d")\nmin(pd$DATE) ')


# In[43]:

get_ipython().run_cell_magic(u'R', u'', u'# Get labels\n# Baseline\n# Initialze two vectors of lists of length 24\nac_date_list <- vector("list", 25)\nlabel_list_pc <- vector("list", 25)\nm <- vector("list", 25)\nfor (i in 1:25){\n    ac_date_list[[i]] <- pd[pd$DATE <= Date[i],] # Get dataframe for accounts which made a purchase before certain dates\n    label_list_pc[[i]] <- rep(0,dim(base)[1]) # Initialize the label vector at 0 for each account\n    m[[i]] = merge(base, ac_date_list[[i]] , by.x = "ACCOUNT_ID", by.y = "ACCT_ID") \n    label_list_pc[[i]][base$ACCOUNT_ID %in% m[[i]]$ACCOUNT_ID]=1\n}')


# In[44]:

get_ipython().run_cell_magic(u'R', u'', u'table(label_list_pc[[25]])')


# In[45]:

get_ipython().run_cell_magic(u'R', u'', u'save(label_list_pc, file = "Label7.RData")')


# In[2]:

get_ipython().run_cell_magic(u'R', u'', u'for (i in 1:10){\n    print(i)\n}')


# In[ ]:



