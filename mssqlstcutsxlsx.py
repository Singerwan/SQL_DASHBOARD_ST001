import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
import folium
import mapclassify
from shapely.geometry import Point ,Polygon

st.set_page_config(layout="wide")






def main():
      st.title('Customer Overview')
      option =st.sidebar.selectbox('Select an Operation', ["Existing Customers Table",'Upload CSV Files & Summary Review','Map Overview'] )
      if option=='Existing Customers Table':
         st.subheader('Existing Customers Table Overview')
         
         dfConvProQty=pd.read_excel('cust1.xlsx')
         st.dataframe(dfConvProQty)
         
      elif option=='Upload CSV Files & Summary Review':
            uploaded_files = st.file_uploader("Upload data(CSV Only! And Ignore the ERROR )", accept_multiple_files=True, type="csv")
            df_csv_readin = None # assign to none to avoid initial error 
            dfConvProQty=pd.read_excel('cust1.xlsx')
            
            if uploaded_files is not None:
               for uploaded_file in uploaded_files:
                  df_csv_readin = pd.read_csv(uploaded_file)

                  
               with st.expander("dataframe in mysql",icon="💼", expanded=True):
                  st.dataframe(dfConvProQty)
               with st.expander("dataframe in uploaded csv file", icon="⌨",expanded=True):      
                  st.dataframe(df_csv_readin)
               with st.expander("concatenated dataframes from both mysql and uploaded files",icon="➕", expanded=True):
                  newdf=pd.concat([dfConvProQty,df_csv_readin],ignore_index=True)
                  st.dataframe(newdf)
               with st.expander("DataFrame's DataTypes", expanded=True):
                  dfConvProQty['Revenue']=dfConvProQty['Revenue'].fillna(0).astype('int')
             
                  st.dataframe(dfConvProQty.dtypes)   
               st.title('Summary Overview')
               st.header('Revenue Summary')
               revenue_type=st.selectbox(' chart type dropdown box :' ,[   'Revenue in Grand Total',
                                                                           'Revenue in Total by|(per) Province',
                                                                           'Revenue in Total by|(per) City',
                                                                           'Revenue in Total by|per| Sales_Employee',
                                                                           'Revenue in Total by|per| Product_catagory',
                                                                           'Revenue in Brief Statistical & Heirarchical Order'
                                                                           ] ,key='revenue_type')

               if revenue_type =="Revenue in Grand Total":
                     rgt=dfConvProQty['Revenue'].sum()               
                     st.write(f'The total revenue is {rgt} K $ ')
               elif revenue_type=="Revenue in Total by|(per) Province":
                     st.dataframe(dfConvProQty.groupby('Province')['Revenue'].sum())    
                     revenueprov =pd.DataFrame(newdf.groupby('Province')['Revenue'].sum())
                     # ----------------------------------------------.re
                     fig = px.pie( revenueprov,
                                    names=revenueprov.index,    # label|legend
                                    values=revenueprov['Revenue'],
                                    color=revenueprov.index,
                                    hole=True,
                                    title='Revenue in Total by|(per) Province')
                     st.plotly_chart(fig)
    
               elif revenue_type=='Revenue in Total by|(per) City':                  
                     st.dataframe(newdf.groupby('City')['Revenue'].sum())    
                     revenuecity =pd.DataFrame(newdf.groupby('City')['Revenue'].sum())
                     fig = px.bar(revenuecity, 
                                 x=revenuecity.index,
                                 y=revenuecity['Revenue'],
                                 color=revenuecity.index,
                                 title='Revenue in Total by|(per) City')
                     st.plotly_chart(fig)         
                                     
               elif revenue_type=="Revenue in Total by|per| Sales_Employee":  
                     st.dataframe(newdf.groupby('Sales')['Revenue'].sum())   
                     revenuesale =pd.DataFrame(newdf.groupby('Sales')['Revenue'].sum())
                     fig = px.bar(  revenuesale, 
                                    x=revenuesale.index,
                                    y=revenuesale['Revenue'],
                                    color=revenuesale.index,
                                    title='Revenue in Total by|(per) Sales_Employee ')
                     st.plotly_chart(fig) 
                                                      
               elif revenue_type=="Revenue in Total by|per| Product_catagory":  
                     st.dataframe(newdf.groupby('Product_Category')['Revenue'].sum())        
                     revenuecatg =pd.DataFrame(newdf.groupby('Product_Category')['Revenue'].sum())
                     fig = px.pie(revenuecatg, 
                                 names=revenuecatg.index,
                                 values=revenuecatg['Revenue'],
                                 color=revenuecatg.index,
                                 title='Revenue in Total by|(per) Product_catagory' )
                     st.plotly_chart(fig)            
               elif revenue_type=="Revenue in Brief Statistical & Heirarchical Order":  
                     st.dataframe(newdf.groupby(['Company_Name','City','Province']).agg( {'Revenue':['min','mean','max','sum'],'visits_per_year':['min','mean','max','sum']} ))  
                     
                     fig = px.scatter(newdf, 
                                       x=newdf['Revenue'],
                                       y=newdf['visits_per_year'],
                                       color='Province',
                                       title='Revenue VS Visit Frequency')
                     st.plotly_chart(fig)                               
               st.header('Number of Customers')
               numberofcust=st.selectbox(' chart type dropdown box :' ,[   'How many customers do we have in every Province?',
                                                                           'How many customers do we have in every city?',
                                                                           'How many customers do each sales_employee have ?'] ,key='numofcust1')              
               if numberofcust=="How many customers do we have in every Province?":
                     nofc_prov=pd.DataFrame(newdf.groupby('Province')['Company_Name'].count())
                     nofc_prov.columns=['Number of customers']
                     st.dataframe(nofc_prov)

                     fig = px.pie(nofc_prov, 
                                 names=nofc_prov.index,
                                 values=nofc_prov['Number of customers'],
                                 color=nofc_prov.index,
                                 title='Number of customer per province' )
                     st.plotly_chart(fig)     
                                          
               elif  numberofcust=="How many customers do we have in every city?" :  
                     nofc_city=pd.DataFrame(newdf.groupby('City')['Company_Name'].count())
                     nofc_city.columns=['Number of customers']
                     
                     fig = px.bar(  nofc_city, 
                                    x=nofc_city.index,
                                    y=nofc_city['Number of customers'],
                                    color=nofc_city.index,
                                    title='Number of customer per city')
                     st.plotly_chart(fig) 
                     

               elif  numberofcust=="How many customers do each sales_employee have ?":                     
                     nofc_emp=pd.DataFrame(newdf.groupby('Sales')['Company_Name'].count())
                     nofc_emp.columns=['Number of customers']
                     st.dataframe(nofc_emp)      

                     fig = px.pie(nofc_emp, 
                                 names=nofc_emp.index,
                                 values=nofc_emp['Number of customers'],
                                 color=nofc_emp.index,
                                 title='Number of customer per employee' )
                     st.plotly_chart(fig)          
         
      elif option=='Map Overview':
            worldcities_lonlat=None

            worldcities_lonlat=pd.read_csv('worldcities_lonlat.csv')
            points_long_lati_w1=worldcities_lonlat.apply( lambda row: Point( row.lng,row.lat)   ,axis=1)
            powerplantgdf_w1=gpd.GeoDataFrame(worldcities_lonlat,geometry=points_long_lati_w1)
            powerplantgdf_w1.crs={'init':'epsg:4326'}
            chinalon_lat_1=None
            chinalon_lat_1=powerplantgdf_w1[(worldcities_lonlat['id'].isin([1156237133,1156158707,1156478242,1156738403,1156579621,1156457499,1156203268,1156073548,1156117184,
                                                                        1410836482,1156936556,1356872604,1887433410,1704988146,1800495740,1800000051,1800972565,1800770335,]))]

            chinalon_lat_1['latitude'] = chinalon_lat_1.lat
            chinalon_lat_1['longitude'] = chinalon_lat_1.lng          
                  
            st.map(chinalon_lat_1[['latitude','longitude']],size="population",color=[1.0, 0.1,0.2,0.5])     

           gpdmap1=chinalon_lat_1.explore( cmap='jet',
                                            column='city',
                                            marker_kwds={'radius':5},
                                            tooltip=["population","country",'city','id'])
            
            st_folium(gpdmap1,width=1200,height=300)            
            

            # Create a Folium map
            m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
            # Add a marker to the map
            folium.Marker([39.949610, -75.150282], popup="Marker Example").add_to(m)
            # Render the map in Streamlit
            st_folium(m, height=200, width=1200)
if __name__=="__main__":
    main()   
