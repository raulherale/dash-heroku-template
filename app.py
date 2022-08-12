%%capture

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


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


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Gender Wage Gap study using \n the 2019 General Social Survey"),
        
        html.H1("Summary"),
        dcc.Graph(figure=table),
        
        html.H2("Survey responses on if males are breadwinners or not"),
        dcc.Graph(figure=fig2),
        
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

if __name__ == '__main__':
    app.run_server(debug=True)
