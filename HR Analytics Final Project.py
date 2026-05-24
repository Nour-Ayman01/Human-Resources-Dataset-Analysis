#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df=pd.read_csv('HR_Analytics.csv')


# In[3]:


df=df.dropna(axis=1,how='all')


# In[4]:


df


# In[5]:


df.isnull().sum()


# In[6]:


df.columns


# In[7]:


df.describe()


# ## Attrition Percentage:

# In[11]:


Attrition_dist=(df['Attrition'].value_counts(normalize=True)*100).round(2)


# In[12]:


colors=['green','red']
Attrition_dist.plot(kind='pie',autopct='%1.2f%%',figsize=(4,3),colors=colors)
plt.title('Attrition Percentage')
plt.ylabel('');


# ### distribution of employees according to gender,age,joblevel and department:

# In[15]:


#department distribution
(df['Department'].value_counts(normalize=True)*100).round(2)


# In[13]:


#gender distribuion
(df['Gender'].value_counts(normalize=True)*100).round(2)


# In[89]:


#Job Level in company
df['JobLevel'].value_counts()


# # Which gender left the company more?

# In[16]:


#gender at each department
df.groupby('Department')['Gender'].value_counts().unstack()


# In[60]:


#Attrition by gender
ATT_BY_GENDER=df.groupby('Gender')['Attrition'].value_counts(normalize=True).unstack().round(2)*100


# In[63]:


plt.style.use('ggplot')
colors=['green','red']
ax=ATT_BY_GENDER.plot(kind='bar',stacked=False,color=colors)
plt.title('Attrition PERCENTAGE by Gender',fontsize=16)
for container in ax.containers:
    ax.bar_label(container)
    plt.xticks(rotation=45)


# In[19]:


#Attrition by Agegroup
df.groupby('AgeGroup')['Attrition'].value_counts().unstack()


# In[20]:


plt.style.use('ggplot')
colors=['green','red']
df.groupby('AgeGroup')['Attrition'].value_counts().unstack().plot(kind ='bar',figsize=(8,5),color=colors)
plt.title('Attrition byAge Group',fontsize=16)
plt.xticks(rotation=45)


# ## What are the departments that have the high rate of attrition?

# In[21]:


#Attrition by each department
ATTrition_by_DEP = df.groupby('Department')['Attrition'].value_counts(normalize=True).round(2)*100


# In[22]:


plt.style.use('ggplot')
colors=['green','red']
ax=ATTrition_by_DEP.unstack().plot(kind='barh',color=colors)
for container in ax.containers:
    ax.bar_label(container)
plt.title('Attrition percentage by Department')
plt.legend()


# ## what is the impact of monthlyincome on Attrition??

# In[23]:


#monthlyincome analysis
df.groupby('Department')['MonthlyIncome'].mean().sort_values(ascending=False)


# In[24]:


df.groupby('JobRole')['MonthlyIncome'].mean().sort_values(ascending=False).round(2)


# In[25]:


df.groupby('Attrition')['MonthlyIncome'].mean().sort_values().round(2)


# In[27]:


plt.style.use('ggplot')

sns.boxplot(x='Attrition',y='MonthlyIncome',data=df, color = 'red')

plt.title('Attrition by monthlyincome',fontsize=16)


# ## what is the impact of PercentSalaryHike on Attrition?

# In[29]:


df.groupby("Department")["PercentSalaryHike"].mean()


# In[28]:


df.groupby("Attrition")["PercentSalaryHike"].mean()


# In[70]:


plt.style.use('ggplot')
sns.boxplot(x="Attrition", y="PercentSalaryHike", data=df,color='red')
plt.title('Attrition byPercentSalaryHike ',fontsize=16)


# In[31]:


#Attrition by salary slab:
df["SalarySlab"].value_counts()


# In[74]:


plt.style.use('ggplot')
colors=['#2ecc71','#e74c3c','#27ae60','#c0392b']
ax=sns.countplot(x="SalarySlab",data=df,palette=colors)
for container in ax.containers:
    ax.bar_label(container)
    plt.xticks(rotation=45)


# In[102]:


#ATTRITION BY SALARY SLAB:
ATT_BY_salaryslab =df.groupby("SalarySlab")["Attrition"].value_counts(normalize=True).unstack().round(2)*100


# In[105]:


plt.style.use('ggplot')
colors=['#2ecc71','#e74c3c','#27ae60','#c0392b']
ax=ATT_BY_salaryslab.plot(kind='barh',color=colors)
for container in ax.containers:
    ax.bar_label(container)
plt.title('Attrition percentage by salaryslab')
plt.legend()


# In[36]:


#Attrition by joblevel:
ATTRITION_BY_JOBLEVEl=df.groupby("JobLevel")['Attrition'].value_counts(normalize=True).unstack().round(2)*100


# In[66]:


plt.style.use('ggplot')
colors=['green','red']
ax=ATTRITION_BY_JOBLEVEl.plot(kind='barh',color=colors)
for container in ax.containers:
    ax.bar_label(container)
plt.title('Atrrition by JobLevel',fontsize=16)
plt.legend()
plt.ylabel('Job Level')
plt.xlabel('count')


# ## when the employees left the company??

# In[83]:


#Attrition by Yearsatcompany
df.groupby('Attrition')['YearsAtCompany'].mean()


# In[94]:


plt.style.use('ggplot')
fig,axes=plt.subplots(1,2,figsize=(9,5))
attrtion_yes=df[df['Attrition']=='Yes']
sns.boxplot(y='YearsAtCompany',x='Attrition',color='red',data=df,ax=axes[0])
sns.histplot(attrtion_yes['YearsAtCompany'],bins=8,kde=True,ax=axes[1])


# ###  what are the the factors that contribute in attrition??

# In[40]:


# Attrition by over time
AO=df.groupby('OverTime')['Attrition'].value_counts(normalize=True).unstack().round(2)*100


# In[41]:


plt.style.use('ggplot')
colors=['green','red']
ay=AO.plot(kind='bar',stacked=False,figsize=(7,4),color=colors)
for container in ay.containers:
    ay.bar_label(container)
plt.title('Attrition by OverTime',fontsize=16)
plt.show()


# ## impact of promotion on attrition:
# 

# In[44]:


df['YearsSinceLastPromotion'].value_counts()


# In[45]:


sns.histplot(df['YearsSinceLastPromotion'],bins=20,kde=True)


# In[42]:


#Attrition by business travel
df.groupby('BusinessTravel')['Attrition'].value_counts().unstack()


# In[43]:


plt.style.use('ggplot')
colors=['green','red']

ay=df.groupby('BusinessTravel')['Attrition'].value_counts().unstack().plot(kind ='barh',figsize=(8,5),color=colors)
for container in ay.containers:
    ay.bar_label(container)
plt.title('Attrition by BusinessTravel',fontsize=16)


# ### impact of distance on Attrition

# In[46]:


df.loc[:,'DistanceCategory']= pd.cut(df['DistanceFromHome'],
                                    bins=[1,10,20,30],
                                    labels=['short distance','long distance','very long distance'])


# In[47]:


plt.style.use('ggplot')
colors=['green','red']

az=pd.crosstab(df['DistanceCategory'],df['Attrition']).plot(kind='barh',color=colors,stacked=False)
plt.xticks(rotation=45)
plt.title('Attrition byDistanceFromHome',fontsize=16)
for container in az.containers:
    az.bar_label(container)


# ### impact of environment satisfaction,work life balance,job satisfaction ,performance rating on Attrition

# In[48]:


mapping={1:'LOW',2:'MEDIUM',3:'HIGH',4:'VERY HIGH'}
df.loc[:,'EnvironmentSatisfactionRATE']=df['EnvironmentSatisfaction'].map(mapping)
df.loc[:,'JobSatisfactionRATE']=df['JobSatisfaction'].map(mapping)
df.loc[:,'WorkLifeBalanceRATE']=df['WorkLifeBalance'].map(mapping)
df.loc[:,'PerformanceRatingLABEL']=df['PerformanceRating'].map(mapping)


# In[52]:


plt.style.use('ggplot')
colors=['green','red']

fig,axes=plt.subplots(2,2,figsize=(12,8))
pd.crosstab(df['EnvironmentSatisfactionRATE'],df['Attrition']).plot(kind='barh',color=colors,stacked=False,ax=axes[0,0])
pd.crosstab(df['JobSatisfactionRATE'],df['Attrition']).plot(kind='barh',color=colors,stacked=False,ax=axes[0,1])
pd.crosstab(df['WorkLifeBalanceRATE'],df['Attrition']).plot(kind='barh',color=colors,stacked=False,ax=axes[1,0])
pd.crosstab(df['PerformanceRatingLABEL'],df['Attrition']).plot(kind='barh',color=colors,stacked=False,ax=axes[1,1])
plt.tight_layout()


# In[ ]:




