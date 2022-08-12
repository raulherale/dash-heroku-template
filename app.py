#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:48:48 2022

@author: apple
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output



mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 



gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')



# https://www.americanprogress.org/article/quick-facts-gender-wage-gap/

Text = '''The gender wage gap refers to the difference in earnings between women and men. According to the 
census data, women from all races, on average, earned 82 cents for every dollar earned by men.The gender wage gap is more 
skewed in minority demographics such as Hispanic and Black women populations. The main reasons for
gender wage gap are - 

1. Differences in industries women and men work in
2. Differences in years of average experience beween men and women in the workforce
3. Differences in the hours worked by men and women
4. Discrimination against women at workplaces in terms of growth and pay

About GSS Data 

The General Social Survey (GSS) is a nationally representative survey of adults in the United States. The GSS collects data on contemporary American society in order to monitor and explain trends in opinions, attitudes and behaviors. GSS also conducts surveys on special topics such as civil liberties, crime and violence etc. 
The GSS is a best resource for sociological and attitudinal trend data. It enables easy access to high quality data to scholars, students, policy-makers with minimal cost. 

'''


gss_display = gss_clean.groupby('sex').agg({'income':'mean',
                                        'job_prestige':'mean',
                             'socioeconomic_index':'mean',
                                           'education':'mean'}).reset_index()
gss_display = gss_display.rename({'income':'Mean income',
                                  'sex':'Gender',
                                   'job_prestige':'Mean Occupational prestige',
                                   'socioeconomic_index':'Mean socioeconomic index',
                                   'education':'Mean years of education'}, axis=1)
gss_display = round(gss_display, 2)

table = ff.create_table(gss_display)

gss_clean['income'] = round(gss_clean['income'],2)

gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly agree', 
                                                            'agree', 
                                                            'disagree', 
                                                            'strongly disagree'])

gss_groupbar = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index().rename({0:'Count'}, axis=1)

fig2 = px.bar(gss_groupbar, x='sex', y='Count', color='male_breadwinner',
            labels={'male_breadwinner':'Male breadwinner', 'Count':'Count','sex':'Gender'},
            hover_data = ['male_breadwinner', 'Count'],
            text='Count',
            barmode = 'group')
fig2.update_layout(showlegend=True)
fig2.update(layout=dict(title=dict(x=0.5)))




fig3 = px.scatter(gss_clean, x='job_prestige', y='income', color = 'sex',
                  trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income',
                        'sex':'Gender',
                        'socioeconomic_index':'Socioeconomic Index',
                        'education':'Years of Education'},
                 hover_data=['education', 'socioeconomic_index'])
fig3.update(layout=dict(title=dict(x=0.5)))

fig4 = px.box(gss_clean, x='sex', y = 'income', color = 'sex',
                   labels={'sex':'', 'income':'Income'},
            height=600, width=600)
fig4.update(layout=dict(title=dict(x=0.5)))
fig4.update_layout(showlegend=False)

fig5 = px.box(gss_clean, x='sex', y = 'job_prestige',color ='sex',
                   labels={'sex':'', 'job_prestige':'Occupational Prestige'},
            height=600, width=600)
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.update_layout(showlegend=False)


gss2 = gss_clean[['income','sex','job_prestige']]

gss2['job_prestige_bucket'] = pd.cut(gss2.job_prestige , bins = [-1,25,35,45,55,65,1000],
                                   labels = ('<=25','25-35','35-45','45-55','55-65',
                                             '65+'))
gss2.dropna(inplace=True)

fig6 = px.box(gss2, x='sex', y = 'income', color = 'sex',
                   labels={'sex':'', 'income':'Income',
                           'job_prestige_bucket': 'Occupation Prestige' },
              facet_col= 'job_prestige_bucket',
              facet_col_wrap= 2,
              color_discrete_map = {'male':'blue', 'female':'red'},
            height=1000, width=800)
fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(showlegend=False)

col_options = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 
               'child_suffer', 'men_overwork']

group_options = ['sex','region','education']





externa_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets= externa_stylesheets)


app.layout = html.Div(
    [
        html.H1("Gender Wage Gap study using \n the 2019 General Social Survey"),
        
        dcc.Markdown(children = Text),

        html.H1("Summary"),
        dcc.Graph(figure=table),
        
        html.Div([
            
            html.H3("Category"),
            
            dcc.Dropdown(id='category',
                            options=[{'label': i, 'value': i} for i in col_options],
                            value='male_breadwinner'),
            
            html.H3("Grouped By"),
            
            dcc.Dropdown(id='group',
                            options=[{'label': i, 'value': i} for i in group_options],
                            value='region'),
        
        ], style={'width': '25%', 'float': 'left'}),


        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),
        
        html.H2("Income vs Occupational Prestige by Gender"),
        dcc.Graph(figure=fig3),
        
        #html.H2("Income distribution by Gender"),
        #dcc.Graph(figure=fig4),
        
        #html.H2("Occupational Prestige distribution by Gender"),
        #dcc.Graph(figure=fig5),
    
        html.Div([
            
        html.H2("Income distribution by Gender"),
        dcc.Graph(figure=fig4)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
        html.H2("Occupational Prestige distribution by Gender"),
        dcc.Graph(figure=fig5),
            
        ], style = {'width':'48%', 'float':'right'}),
    
        html.H2("Income distribution by \n Gender and Occupational Prestige"),
        dcc.Graph(figure=fig6)
        
    ]
)

@app.callback(Output(component_id="graph",component_property="figure"), 
             [Input(component_id='category',component_property="value"),
              Input(component_id='group',component_property="value")])

def make_figure(x, y):
    gss_group = gss_clean.groupby([y,x]).size().reset_index().rename({0:'Count'}, axis=1)

    return px.bar(
        gss_group,
        x=y,
        y='Count',
        color=x,
        hover_data=[x,'Count'],
        barmode = 'group')



if __name__ =='__main__':
    app.run_server(debug = True )     
