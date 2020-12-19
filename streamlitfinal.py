# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:57:19 2020

@author: Brian
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:48:54 2020
@author: Brian Peterson
TO RUN: 
    streamlit run streamlitfinal.py
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time


@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('Medicare — Expenses - NY')



    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.1)
     my_bar.progress(percent_complete + 1)
  

st.write('Hello, *World!* :sunglasses:') 
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()







hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']


#Bar Chart
st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')


st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)



st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#Timeliness of Care
st.subheader('NY Hospitals - Timelieness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')



#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )





##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Hospital - ")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)







# BEGIN HOMEWORK ASSIGNMENT: FURTHER EXPLORATION! Will first briefly look at other states, such as California
st.header('BEGIN HOMEWORK ASSIGNMENT, FIRST ANALYZING ONE STATE, THEN MORE CLOSELY ANALYZING NEW YORK HOSPITALS')
st.header('Hospital Type - CA')

##California Hospital Types

hospitals_ca = df_hospital_2[df_hospital_2['state'] == 'CA']

bar4 = hospitals_ca['hospital_type'].value_counts().reset_index()
st.dataframe(bar4)


st.markdown('Most hospitals in California are acute care, closely followed by Psychiatric')

st.header('Hospital Type Ownership in CA')
hos_ownership_ca = hospitals_ca['hospital_ownership'].value_counts().reset_index()
st.dataframe(hos_ownership_ca)

## The following function will provide a pie chart on the types of hospitals in california.
##We will first break down the hospital types visually using a pie chart

st.subheader('Hospital Type Breakdown in CA')
fig = px.pie(bar4, values='hospital_type', names='index')
st.plotly_chart(fig)
st.markdown('The pie chart visually displays the data in the table above.')

st.subheader('Hospital Ownership Breakdown in CA')
figca = px.pie(hos_ownership_ca, values = 'hospital_ownership', names='index')
st.plotly_chart(figca)
st.markdown('The pie chart above visually displays the data in the prior table.')

##Hospital Ownership Types in NY analysis. We will now begin to hone in on New York hospitals..
##we will first create dataframe for NY hospital, then look at ownerships


st.header('Hospital Types in NY')

hospitals_ny2 = df_hospital_2[df_hospital_2['state'] == 'NY']

hos_types_ny = hospitals_ny2['hospital_type'].value_counts().reset_index()
st.dataframe(hos_types_ny)
st.markdown('Most hospital types in New York are Acute care, followed by Psychiatric')

##now hospital ownership type analysis
st.header('Hospital Type Ownership in NY')
hos_ownership_ny = hospitals_ny2['hospital_ownership'].value_counts().reset_index()
st.dataframe(hos_ownership_ny)

st.markdown('Most hospitals in New York have a private ownership, followed by state government owned.')

## simple pie chart display of hospital types and ownership types in NY, now being hospital types.

st.subheader('Hospital Type Breakdown in NY')
hos_type_ny = hospitals_ny2['hospital_type'].value_counts().reset_index()
fighosny = px.pie(hos_type_ny, values = 'hospital_type', names = 'index')
st.plotly_chart(fighosny)

##now to use a pie chart for hospital ownership breakdown in NY

st.subheader('Hospital Ownership Breakdown in NY')
figa = px.pie(hos_ownership_ny, values='hospital_ownership', names='index')
st.plotly_chart(figa)

##now using a bar chart for hospital breakdown in NY
st.subheader('Hospital Ownership NY Chart Breakdown')
bara = hospitals_ny2['hospital_ownership'].value_counts().reset_index()
figb = px.bar(bara, x='index', y='hospital_ownership')
st.plotly_chart(figb)

st.markdown('The chart above is another display of the types of ownership in NY.')


##Analysis of Stony Brook Hospital using hospital data, brief information

stony_brook_hospital_data = df_hospital_2[df_hospital_2['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']

st.subheader('Brief data of some variables for Stony Brook Hospital')
st.markdown('Basic Information about Stony Brook Hospital looking at the hospital excel dataset')
st.dataframe(stony_brook_hospital_data)


## Overall Description of Stony Brook Hospital using some outpatient data such as outpatient services, apcs, submitted charges, and total payments..

st.subheader('We will now take a look at some data involving apcs at Stony Brook University Hospital')
stonybrook_ny_outpatient_data = df_outpatient_2[df_outpatient_2['provider_name'] == 'University Hospital ( Stony Brook )']

costs_stony = stonybrook_ny_outpatient_data.groupby(['apc', 'outpatient_services', 'average_estimated_submitted_charges'])['average_total_payments'].sum().reset_index()
st.dataframe(costs_stony)
st.markdown('Outpatient services, average estimated submitted charges and average total payments for differing APCs at Stony Brook Hospital. As can be seen, the most expensive APC is level IV Endoscopy upper airway.')
     
##Overall description of NYU Lagone as a comparison using the same outpatient data..

NYU_Lagone_medical_outpatient = df_outpatient_2[df_outpatient_2['provider_name'] == 'Nyu Hospitals Center']

st.subheader('As a comparison, we will now look at the same data as previously, but looking at NYU lagone instead')
costs_nyu_lagone = NYU_Lagone_medical_outpatient.groupby(['apc', 'outpatient_services', 'average_estimated_submitted_charges'])['average_total_payments'].sum().reset_index()
st.dataframe(costs_nyu_lagone)
st.markdown('Outpatient services, average estimated submitted charges and average total payments for differing APCs at NYU Lagone Hospital. As can be seen, the most expensive APC is level IV Endoscopy upper airway as well.')

NYU_Lagone_medical = df_hospital_2[df_hospital_2['hospital_name']== 'NEW YORK UNIVERSITY LANGONE MEDICAL CENTER']
st.subheader('Brief data of some variables for NYU Lagone Medical Center')
st.markdown('Basic information via the hospital dataset')
st.dataframe(NYU_Lagone_medical)


##Now, we will use the .describe function to help give us an overall view and comparison of NYU/Stony for select variables gives statistics..
statistics_lagone = costs_nyu_lagone.describe()
statistics_stony = costs_stony.describe()

st.subheader('We will now display a summary statistic set for NYU Lagone hospital for the previous variables')
st.dataframe(statistics_lagone)

st.subheader('Now, as a comparison, we will now display the same set of statistics but for Stony Brook Hospital..')
st.dataframe(statistics_stony)
st.markdown('If we compare Stony with NYU, theres a number of differences. NYU seems like a much larger facility, with much more outpatient services and submitted charges. When looking at the average total payments, interestingly it seems Stony Brook is a cheaper hospital, with a smaller mean value for payments.')

##Common discharges for NYU Lagone and Stony Brook DATA for medicare, drg, and payments
##NYU First

NYU_Lagone_medical_inpatient = df_inpatient_2[df_inpatient_2['provider_name'] == 'NYU HOSPITALS CENTER']

st.subheader('We will now show the most common DRG definitions along with total discharges per the conditions and average medicare/total payments. This dataset is for NYU.')
common_discharges_NYU = NYU_Lagone_medical_inpatient.groupby('drg_definition')['total_discharges', 'average_medicare_payments', 'average_total_payments'].sum().reset_index()
st.dataframe(common_discharges_NYU)
st.markdown('It appears that the most common discharges were for a DRG 470, which is major joint replacement. The most expensive medicare and total payments were for a DRG 003, which stands for: ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R.')

##Now Stony same data
st.subheader('We will now show the same data as previously with most common DRG definitions, total discharges, and medicare/total payments but for Stony Brook')
stony_brook_inpatient_data = df_inpatient_2[df_inpatient_2['provider_name'] == 'UNIVERSITY HOSPITAL ( STONY BROOK )']
common_discharges_stony = stony_brook_inpatient_data.groupby('drg_definition')['total_discharges', 'average_medicare_payments', 'average_total_payments'].sum().reset_index()
st.dataframe(common_discharges_stony)
st.markdown('Unlike NYU, the most common DRG definition at Stony Brook is for a DRG of 871, or sepsis. The most expensive medicare and total payments were for the same DRG 003. However, Stony Brooks average medicare payment is about 12k less than NYUs for the same DRG, meanwhile Stony Brooks total payment for that DRG is roughly 24k more expensive. Overall, Stony Brook costs a lot more to treat DRG 003, with medicare paying less to the providers. For many other DRGs, Stony brook also appears more expensive overall.')


## we want to get the top 5 and bottom 5 drgs for both NYU and stony
##new dataframe using only drg and total discharges for NYU first

common_discharges_NYU2 = NYU_Lagone_medical_inpatient.groupby('drg_definition')['total_discharges'].sum().reset_index()

top5nyu = common_discharges_NYU2.head(5)
bottom5nyu = common_discharges_NYU2.tail(5)

##now new dataframe for drg and total discharges for stony brook
common_discharges_stony2 = stony_brook_inpatient_data.groupby('drg_definition')['total_discharges'].sum().reset_index()

top5stony = common_discharges_stony2.head(5)
bottom5stony = common_discharges_stony2.tail(5)

##Now to create side by side columns comparing top DRGs in stony and NYU
st.header('DRGs for Stony Brook and NYU per Total Discharges')

col1, col2 = st.beta_columns(2)

col1.header('Top 5 DRGS for Stony')
col1.dataframe(top5stony)

col2.header('Top 5 DRGs for NYU')
col2.dataframe(top5nyu)

col1a, col2a = st.beta_columns(2)

col1a.header('Bottom 5 DRGS for Stony')
col1a.dataframe(bottom5stony)

col2a.header('Bottom 5 DRGS for NYU')
col2a.dataframe(bottom5nyu)
st.markdown('As can be observed in the DRG tables, Stony Brook and NYU have differing top and bottom 5 DRGs. Although Stony Brook and NYU share the same top DRG 025 - CRANIOTOMY & ENDOVASCULAR INTRACRANIAL PROCEDURES W MCC, they have differing DRGs in general. Stony Brooks bottom DRG is DRG 981 meanwhile for NYU the DRG is 948. These charts just help illustrate some further differences between Stony and NYU in a basic sense.')

## now we will create two pie charts that help to visually display the prior information, but for only bottom 5 drgs.

st.subheader('Bottom 5 DRGs in Stony Brook')
figbotstony = px.pie(bottom5stony, values='total_discharges', names='drg_definition')
st.plotly_chart(figbotstony)

st.subheader('Bottom 5 DRGs in NYU')
bot5nyu = px.pie(bottom5nyu, values='total_discharges', names='drg_definition')
st.plotly_chart(bot5nyu)
st.markdown('The two pie charts above help visually display the DRG data for NYU/STONY data in prior tables, showing pie charts for only the bottom 5 DRGS. (Side note- may need to press the expand option on top right of chart to see it properly. For some reason, the legend is blocking the table. When you expand it with the option, you can see everything fine).')

## lets take a look at the hospital information for NYU Lagone first. will look at overall ratings and other comparisons
## now to make a side by side chart, with NYU lagone first

NYU_Lagone_hospital_data = df_hospital_2[df_hospital_2['hospital_name'] == 'NEW YORK UNIVERSITY LANGONE MEDICAL CENTER']
NYU_Lagone_quality_data = NYU_Lagone_hospital_data.groupby(['hospital_overall_rating', 'mortality_national_comparison', 'safety_of_care_national_comparison', 'readmission_national_comparison'])['patient_experience_national_comparison'].sum().reset_index()
stony_quality_data = stony_brook_hospital_data.groupby(['hospital_overall_rating', 'mortality_national_comparison', 'safety_of_care_national_comparison', 'readmission_national_comparison'])['patient_experience_national_comparison'].sum().reset_index()


col1astony, col2anyu = st.beta_columns(2)

col1astony.header('Stony Basic Quality Information')
col1astony.dataframe(stony_quality_data)

col2anyu.header('NYU Basic Quality Information')
col2anyu.dataframe(NYU_Lagone_quality_data)
st.markdown('As can be observed in the side-by side quality comparison between NYU and Stony Brook, few differences are noted. First, NYU has a 5 for an overall rating compared to Stony Brook, with a 4. In terms of the safety of care, Stony brook is above the national average, while NYU is below, which is troublesome. NYU also has more readmissions it seems since NYUs readmissions compared to national average is above, while for Stony Brook the value is below. Interestingly, most patients at Stony Brook have an experience sub par compared to average, meanwhile patients at NYU have an average hospital experience compared to national.')

## Comparison for NYU hospital using inpatient data for finances more..

NYU_Lagone_finances = NYU_Lagone_medical_inpatient.groupby(['average_covered_charges', 'average_total_payments', 'average_medicare_payments']).sum().reset_index()
NYU_finances = NYU_Lagone_finances.describe()
st.subheader('Will now display some summary statistics for the main finances involved for NYU')
st.dataframe(NYU_finances)

##Comparison for Stony brook hospital using inpatient data for finances..

Stony_brook_finances = stony_brook_inpatient_data.groupby(['average_covered_charges', 'average_total_payments', 'average_medicare_payments']).sum().reset_index()

Stony_finances = Stony_brook_finances.describe()
st.subheader('Will now display the same financial information but for Stony Brook')
st.dataframe(Stony_finances)
st.markdown('As can be observed, the two tables above show relevant financial information for both institutions. NYU has a higher average covered charges, total payments, and medicare payments. Both hospitals have very similar numbers of average discharges. Also, relevant data looking at the quartiles, minimum or maximum values for the financial indiactors can be observed.')

##we will now create a bar chart showing average payments for select drgs at NYU..
common_discharges_NYU3 = NYU_Lagone_medical_inpatient.groupby('drg_definition')['average_total_payments'].sum().reset_index()

top5nyu2 = common_discharges_NYU3.head(5)

st.subheader('Average total payments for a select few DRGs at NYU hospital')
fignyuprices = px.bar(top5nyu2, x='drg_definition', y='average_total_payments')
st.plotly_chart(fignyuprices)

##We will now do the same but for Stony..

common_discharges_stony3 = stony_brook_inpatient_data.groupby('drg_definition')['average_total_payments'].sum().reset_index()

top5stony2 = common_discharges_stony3.head(5)

st.subheader('Average total payments for a select few DRGs at Stony Brook hospital')
figstonyprices = px.bar(top5stony2, x='drg_definition', y='average_total_payments')
st.plotly_chart(figstonyprices)
st.markdown('As can be observed, the two hospitals have different average total payments corresponding to the same DRGs.')

##we will now make visualizations for DRG definition and total discharges using top 5.. first for NYU bar charts

drgdischargesNYU = NYU_Lagone_medical_inpatient.groupby('drg_definition')['total_discharges'].sum().reset_index()

top5nyu3 = drgdischargesNYU.head(5)

st.subheader('Visualization for total discharges per top DRGs for NYU Hospital')
figtopnyu3 = px.bar(top5nyu3, x='drg_definition', y='total_discharges')
st.plotly_chart(figtopnyu3)
st.markdown('As can be observed, the visualization above shows the top 5 DRGs and their respective discharges for NYU.')

##Now make the same visualization but for Stony

stony_discharges_drg = stony_brook_inpatient_data.groupby('drg_definition')['total_discharges'].sum().reset_index()

top5stony3 = stony_discharges_drg.head(5)

st.subheader('Visualization for total discharges per top DRGs for Stony Brook Hospital')
figtopstony3 = px.bar(top5stony3, x='drg_definition', y='total_discharges')
st.plotly_chart(figtopstony3)
st.markdown('As can be observed, the visualization above shows the top 5 DRGs and their respective discharges for Stony brook hospital.')

## APCs for NYU

apcs_NYU = NYU_Lagone_medical_outpatient.groupby('apc')['average_total_payments'].sum().reset_index()

top_apcs_NYU = apcs_NYU.head(5)

st.subheader('Pie Chart for APCs used in NYU along with the Total Payments')
apcstopnyu = px.pie(top_apcs_NYU, values='average_total_payments', names='apc')
st.plotly_chart(apcstopnyu)

##now the same APCs but for Stony
apcs_stony = stonybrook_ny_outpatient_data.groupby('apc')['average_total_payments'].sum().reset_index()
top_apcs_stony = apcs_stony.head(5)

st.subheader('Pie Chart for APCs used in Stony Brook along with the Total Payments')
apcstopstony = px.pie(top_apcs_stony, values='average_total_payments', names='apc')
st.plotly_chart(apcstopstony)
st.markdown('The two pie charts above show some similar APCs between Stony Brook and NYU along with their relative cost. As can be observed, APC 074 is very similar in total payments between the two hospitals. DRG 20 is also fairly similar in total payments. However in both cases, although marginally, stony brook is more expensive for the same APCs.')

## Nice bar chart for NYU..
st.subheader('Overall Look at More APC costs at NYU Hospital')
barnyubig = px.bar(apcs_NYU, x='apc', y='average_total_payments')
st.plotly_chart(barnyubig)

##Nice bar chart for Stony..
st.subheader('Overall look at more APC costs at Stony Hospital')
barstonybig = px.bar(apcs_stony, x='apc', y='average_total_payments')
st.plotly_chart(barstonybig)
st.markdown('The two charts above just illustrate more APCs for each hospital, helping to give a more broad overview. Would help to press the expand option above to better see the chart.')

##covered charges per DRG for NYU

covered_drgNYU = NYU_Lagone_medical_inpatient.groupby('drg_definition')['average_covered_charges'].sum().reset_index()

top10_NYU = covered_drgNYU.head(10)
st.subheader('Overall chart of top ten DRGs and their respected covered charges for NYU')
barnyucovered = px.bar(top10_NYU, x='drg_definition', y='average_covered_charges')
st.plotly_chart(barnyucovered)

##covered charges for Stony

covered_stony = stony_brook_inpatient_data.groupby('drg_definition')['average_covered_charges'].sum().reset_index()

top10_stony = covered_stony.head(10)
st.subheader('Overall chart of top ten DRGs and their respected covered charges for Stony')
barstonycovered = px.bar(top10_stony, x='drg_definition', y='average_covered_charges') 
st.plotly_chart(barstonycovered)
st.markdown('As can see in the two charts above, a general overview of the top ten DRGs along with their covered charges were included for Stony and NYU; Some differences were noted. For DRG 003, Stony brook has a higher covered charges, by about 60k. However for other DRGs such as DRG 004, NYU Appears to cover more. These charts just help to visually display some data with covered charges since it was not touched on previously.')


st.subheader('END PROJECT')
st.write('This now marks the end of my project for statistics, as I have covered a lot of different data points between NYU, Stony Brook and other hospitals.')

st.write('I hope you have a good holiday break Professor Hants, I learned a lot in this class! :sunglasses:') 
