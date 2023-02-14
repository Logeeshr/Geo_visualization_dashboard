import pandas as pd
import plotly.express as px
import streamlit as st 
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie

Data_Aggregated_Transaction_df = pd.read_csv(r'D:/spyder/dash/Data_Aggregated_Transaction_Table.csv')

Data_Aggregated_User_df= pd.read_csv(r'D:/spyder/dash/Data_Aggregated_User_Table.csv')

#page layout
st.set_page_config(page_title='Phonepe Dashboard', page_icon=':moneybag:', layout='wide')

#Animations 
def load_lottieur(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()  
lottie_coding = load_lottieur("https://assets5.lottiefiles.com/private_files/lf30_poez9ped.json")  


#title 
with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(":violet[_PHONEPE DASHBOARD_]")
    with right_column:
        st_lottie(lottie_coding,height=150, key='codings')

#barchart-1
st.title(":violet[_Analysis of Phonepe Transaction_]")

Data_Aggregated_Transaction=Data_Aggregated_Transaction_df.copy()
State_PaymentMode=Data_Aggregated_Transaction.copy()
mode = st.selectbox(
    'select the Payment Mode',
    ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')
state = st.selectbox(
    'select the State',
    ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
       'haryana', 'himachal-pradesh', 'jammu-&-kashmir','jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram','nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
       'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh','uttarakhand', 'west-bengal'),key='b')
State= state
Year_List=[2018,2019,2020,2021,2022]
Mode=mode


State_PaymentMode=State_PaymentMode.loc[(State_PaymentMode['State'] == State ) & (State_PaymentMode['Year'].isin(Year_List)) & 
                        (State_PaymentMode['Payment_Mode']==Mode )]
State_PaymentMode = State_PaymentMode.sort_values(by=['Year'])
State_PaymentMode["Quarter"] = "Q"+State_PaymentMode['Quarter'].astype(str)
State_PaymentMode["Year_Quarter"] = State_PaymentMode['Year'].astype(str) +"-"+ State_PaymentMode["Quarter"].astype(str)
import plotly.express as px
fig = px.bar(State_PaymentMode, x='Year_Quarter', y='Total_Transactions_count',color="Total_Transactions_count",
            title='Transaction pattern of '+Mode+' in '+State, color_continuous_scale="Plasma")
st.plotly_chart(fig,theme="streamlit", use_container_width=True)

#Geo visualization
df1 = Data_Aggregated_Transaction_df.copy()

df1['State'] = df1['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunachal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana', 'tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})

with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        
        df2 = df1.groupby('State')['Total_Transactions_count'].sum().reset_index()

        fig8 = go.Figure(data=go.Choropleth(
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locationmode='geojson-id',
            locations=df2['State'],
            z=df2['Total_Transactions_count'],

            

            autocolorscale=False,
            colorscale='Agsunset',
            marker_line_color='peachpuff',

            
        ))
        fig8.update_geos(
            visible=False,
            projection=dict(
                type='conic conformal',
                parallels=[12.472944444, 35.172805555556],
                rotation={'lat': 24, 'lon': 80}
            ),
            lonaxis={'range': [68, 98]},
            lataxis={'range': [6, 38]}
        )

        fig8.update_layout(
            title=dict(
                text="Number of Transaction statewise",
                xanchor='center',
                x=0.5,
                yref='paper',
                yanchor='bottom',
                y=1,
                pad={'b': 10}
            ),
            margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
            height=550,
            width=550
        )

        st.plotly_chart(fig8,theme="streamlit", use_container_width=True) 
    with right_column:
       
        df3 = df1.groupby('State')['Total_amount'].sum().reset_index()
         
        fig9 = go.Figure(data=go.Choropleth(
             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
             featureidkey='properties.ST_NM',
             locationmode='geojson-id',
             locations=df3['State'],
             z=df3['Total_amount'],
         
             
         
             autocolorscale=False,
             colorscale='Magenta',
             marker_line_color='peachpuff',
         
             
         ))
        fig9.update_geos(
             visible=False,
             projection=dict(
                 type='conic conformal',
                 parallels=[12.472944444, 35.172805555556],
                 rotation={'lat': 24, 'lon': 80}
             ),
             lonaxis={'range': [68, 98]},
             lataxis={'range': [6, 38]}
         )
         
        fig9.update_layout(
             title=dict(
                 text="Maximum Transacted amount statewise",
                 xanchor='center',
                 x=0.5,
                 yref='paper',
                 yanchor='bottom',
                 y=1,
                 pad={'b': 10}
             ),
             margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
             height=550,
             width=550
         )
         
        st.plotly_chart(fig9)

#barchart2 and pie chart 1
with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        st.write('### :violet[_Analysis by Payment Mode_]')
        M = st.selectbox(
            'Select Mode',
            ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='D')
        Y = st.selectbox(
            'Select Year',
            ('2018', '2019', '2020','2021','2022'),key='F')
        Year_PaymentMode=Data_Aggregated_Transaction.copy()
        Year=int(Y)
        Mode=M
        Year_PaymentMode=Year_PaymentMode.loc[(Year_PaymentMode['Year']==Year) & 
                                (Year_PaymentMode['Payment_Mode']==Mode )]
        States_List=Year_PaymentMode['State'].unique()
        State_groupby_YP=Year_PaymentMode.groupby('State')
        Year_PaymentMode_Table=State_groupby_YP.sum()
        Year_PaymentMode_Table['states']=States_List
        del Year_PaymentMode_Table['Quarter']
        del Year_PaymentMode_Table['Year']
        Year_PaymentMode_Table = Year_PaymentMode_Table.sort_values(by=['Total_Transactions_count'])
        fig2= px.bar(Year_PaymentMode_Table, x='states', y='Total_Transactions_count',color="Total_Transactions_count",
                    title='In the Year '+str(Year)+' the '+Mode+" pattern in all states ",color_continuous_scale="plotly3",)
        st.plotly_chart(fig2,theme="streamlit", use_container_width=True)
    
    with right_column:  
        st.write('### :violet[_Transaction Share_]')
        years=Data_Aggregated_Transaction.groupby('Year')
        years_List=Data_Aggregated_Transaction['Year'].unique()
        years_Table=years.sum()
        del years_Table['Quarter']
        years_Table['year']=years_List
        total_trans=years_Table['Total_Transactions_count'].sum()
        fig1 = px.pie(years_Table, values='Total_Transactions_count', names='year')
        st.plotly_chart(fig1)
        
#barchart3 and pie chart 2
with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        st.write('# :violet[User Brand Analysis ]')
        state = st.selectbox(
            'Please select the State',
            ('india','andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
               'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir',
               'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
               'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram','nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
               'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh','uttarakhand', 'west-bengal'),key='Z')
        Y = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'),key='X')
        y=int(Y)
        s=state
        brand=Data_Aggregated_User_df[Data_Aggregated_User_df['Year']==y] 
        brand=Data_Aggregated_User_df.loc[(Data_Aggregated_User_df['Year'] == y) & (Data_Aggregated_User_df['State'] ==s)]
        myb= brand['Brand_Name'].unique()
        x = sorted(myb)
        b=brand.groupby('Brand_Name').sum()
        b['brand']=x
        br=b['Registered_Users_Count'].sum()
        labels = b['brand']
        values = b['Registered_Users_Count']
        fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.2,customdata=labels,textinfo='label+percent',texttemplate='%{label}<br>%{percent:1%f}',insidetextorientation='horizontal',textfont=dict(color='#F5AEEE'),marker_colors=px.colors.qualitative.Vivid)])
        st.plotly_chart(fig3)
    with right_column:
        b = b.sort_values(by=['Registered_Users_Count'])
        fig4= px.bar(b, x='brand', y='Registered_Users_Count',color="Registered_Users_Count",
                    title='In '+state+' the Brand Share distribution in '+str(y),
                    color_continuous_scale="Plasma",)
        st.plotly_chart(fig4,theme="streamlit", use_container_width=True) 
        

 

































