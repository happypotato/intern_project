
import numpy as np
import pandas as pd


def gen_data(win_rate,
                oppty_growth_rate,
                cold_start_period,
                followon_periods,
                num_leads):


    mean_arrivals = np.zeros(cold_start_period).tolist() + [oppty_growth_rate**x for x in range(followon_periods)]
    actual_arrivals = [np.random.poisson(lam=x) for x in mean_arrivals]

    opptys = []

    for month,month_arrivals in enumerate(actual_arrivals):
        for a in range(month_arrivals):
            opptys.append((month,1 if np.random.random() < win_rate else 0))

    offered_leads = pd.DataFrame(opptys,columns=['MONTH','PURCH'])

    nans = [np.NAN for i in range(num_leads - len(offered_leads))]
    unoffered_leads = pd.DataFrame({'MONTH':nans,'PURCH':nans})

    leads = pd.concat({'o':offered_leads,'u':unoffered_leads}).reset_index()

    leads['CUST_ID'] = range(1,len(leads)+1)

    msk = np.random.rand(len(leads)) < win_rate

    leads['EVENTUAL_PURCH'] = np.where(leads.PURCH == 1,1,np.where(leads.PURCH == 0,0, np.where(msk,1,0)))

    leads['LOG_X1'] = leads.EVENTUAL_PURCH.map(lambda x: np.random.normal(.5,1.5) if x == 0 else np.random.normal(1.5,0.5))

    leads['X1'] = 10**leads['LOG_X1']
    leads['X2'] = [10**np.random.normal(1,1) for i in range(len(leads))]
    leads['X3'] = [10**np.random.normal(1,1) for i in range(len(leads))]


    return leads

from sklearn import metrics

def roc(yhat,y):
    fpr, tpr, thresholds = metrics.roc_curve(y, yhat)
    auc=metrics.auc(fpr, tpr)
    return auc


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(class_weight='balanced')

def freq_log_reg(train,test,FEATURES):
    result = lr.fit(np.log10(train[FEATURES]), train['PURCH'])
    #print 'Freq Coefs',result.coef_
    test['score'] = lr.predict_proba(test[FEATURES])[:,1]
    return roc(test.score,test.EVENTUAL_PURCH)

def expert_model(train,test,FEATURES):
    test['score'] = 0
    for f in FEATURES:
        test['score'] += -1*np.log10(test[f])
    return roc(test.score,test.EVENTUAL_PURCH)

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier()

def gradient_boost(train,test,FEATURES):
    result = gb.fit(log10(train[FEATURES]), train['PURCH'])
    test['score'] = gb.predict_proba(test[FEATURES])[:,1]
    return roc(test.score,test.EVENTUAL_PURCH)


import pymc3 as pm
import scipy.stats as stats

def bayes_log_reg(train,test,FEATURES):

    niter = 1000
    LOG_FEATURES = ['LOG_' + f for f in FEATURES]

    for f in FEATURES:
        train['LOG_' + f] = np.log10(train[f])
        test['LOG_' + f] = np.log10(test[f])

    with pm.Model() as model:

        priors = {}
        for f in LOG_FEATURES:
            priors[f] = pm.distributions.Normal.dist(mu=-1, sd=0.5)

        pm.glm.glm('PURCH ~ ' + ' + '.join(LOG_FEATURES), train,family=pm.glm.families.Binomial(),priors=priors)

        #This seems slow
        #start = pm.find_MAP()
        #step = pm.NUTS(scaling=start)

        step = pm.Metropolis()

        trace = pm.sample(niter, step=step,progressbar=False)
        df_trace = pm.trace_to_dataframe(trace)

        test['score'] = 0
        coefs = []
        for f in LOG_FEATURES:
            b = df_trace[f].median()
            test['score'] += b*test[f]
            coefs.append(b)
        #print '\nBayes Coefs',coefs

    return roc(test.score,test.EVENTUAL_PURCH)


def eval(month,model,train,FEATURES):
    msk = train.MONTH <= month
    local_train = train[msk].copy(True)
    local_test = train[~msk].copy(True)

    if (model.func_name in ['freq_log_reg','gradient_boost']) and         (len(local_train) == 0 or         len(np.unique(local_train.PURCH)) != 2):
        return 0.5

    auc = model(local_train,local_test,FEATURES)

    return auc

import time
def simulate():

    win_rate = 0.4
    oppty_growth_rate = 1.25
    cold_start_period = 1
    followon_periods = 30
    num_leads = 10000
    months = range(cold_start_period + followon_periods)
    #months = range(5)

    leads = gen_data(win_rate,
                    oppty_growth_rate,
                    cold_start_period,
                    followon_periods,
                    num_leads)

    FEATURES = [c for c in leads.columns.tolist() if c.startswith('X')]


    aucs = {'flr':[],'expert':[],'bayes':[]}
    for m in months:
    	print 'Progress',m,time.strftime("%H:%M:%S")
        aucs['flr'].append(eval(m,freq_log_reg,leads,FEATURES))
        aucs['expert'].append(eval(m,expert_model,leads,FEATURES))
        aucs['bayes'].append(eval(m,bayes_log_reg,leads,FEATURES))
    return aucs


import datetime
ts = str(time.time())
ts_readable = datetime.datetime.strftime(datetime.datetime.now(), '%H_%M_%S')

with open('output/results.%s.%s.csv' % (ts,ts_readable), 'a',0) as res:
    for i in range(1):
        strt = time.time()
        aucs = simulate()
        print 'Sim', time.time()-strt
        for m in aucs:
            res.write( m + ';' + time.strftime("%H:%M:%S") + ';' + ','.join([str(i) for i in aucs[m]]) + '\n' )


