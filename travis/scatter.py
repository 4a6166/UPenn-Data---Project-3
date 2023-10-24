#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, render_template, jsonify, url_for  # Lesson 10-3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import func
import pandas as pd
import json
import plotly.express as px
def get_scatter ():
    # connect to DB
    engine = create_engine("sqlite:///pa_school_district.db")
    Base = automap_base()
    Base.prepare(autoload_with=engine, reflect = True )

    # TODO: should this be moved to open and close at each route?
    session = Session(bind=engine)


    # In[2]:


    person_spend_data = []
    data = session.execute("select * from person_spend;")
    for row in data.fetchall():
        person_spend_data.append(row)


    # In[3]:


    person_df = pd.DataFrame(person_spend_data)
    person_df = person_df[["AUN","District","County",'LocalPupil','LocalNonPupil','StatePupil', 'StateNonPupil', 'FedPupil','FedNonPupil']]
    person_df['Total']= person_df['LocalPupil']+person_df['LocalNonPupil']+person_df['StatePupil']+ person_df['StateNonPupil']+ person_df['FedPupil']+person_df['FedNonPupil']
    person_df


    # In[4]:


    algebra_data = []
    data = session.execute("select * from keystone_algebra;")
    for row in data.fetchall():
        algebra_data.append(row)


    # In[18]:


    algebra_df = pd.DataFrame(algebra_data)
    algebra_df =algebra_df.groupby("AUN").mean()
    algebra_df = pd.merge(algebra_df,person_df, how='left', on="AUN")
    algebra_df.dropna(inplace=True)
    algebra_df = algebra_df[(algebra_df["Total"]<25_000)&(algebra_df["Total"]>6000)]


    # In[6]:


    bio_data = []
    data = session.execute("select * from keystone_biology;")
    for row in data.fetchall():
        bio_data.append(row)


    # In[20]:


    bio_df = pd.DataFrame(bio_data)
    bio_df =bio_df.groupby("AUN").mean()
    bio_df = pd.merge(bio_df,person_df, how='left', on="AUN")
    bio_df.dropna(inplace=True)
    bio_df = bio_df[(bio_df["Total"]<25_000)&(bio_df["Total"]>6000)]


    # In[8]:


    lit_data = []
    data = session.execute("select * from keystone_literature;")
    for row in data.fetchall():
        lit_data.append(row)


    # In[22]:


    lit_df = pd.DataFrame(lit_data)
    lit_df =lit_df.groupby("AUN").mean()
    lit_df = pd.merge(lit_df,person_df, how='left', on="AUN")
    lit_df.dropna(inplace=True)
    lit_df = lit_df[(lit_df["Total"]<25_000)&(lit_df["Total"]>6000)]


    # In[30]:


    algebra = px.scatter(x=algebra_df['Total'],y=algebra_df['Proficient'],trendline="ols", labels={'x':"total expenditure", "y":"Algebra scores"},title="Algebra scores by total expenditures")


    # In[29]:


    bio = px.scatter(x=bio_df['Total'],y=bio_df['Proficient'],trendline="ols", labels={'x':"total expenditure", "y":"Biology scores"},title="Biology scores by total expenditures")


    # In[27]:


    lit = px.scatter(x=lit_df['Total'],y=lit_df['Proficient'],trendline="ols", labels={'x':"total expenditure", "y":"literature scores"},title="literature scores by total expenditures")


    # In[ ]:

    return (algebra, bio, lit)


