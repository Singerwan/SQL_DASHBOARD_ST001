import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import matplotlib
import folium
import mapclassify
from shapely.geometry import Point ,Polygon
from folium.plugins import HeatMap
from folium.plugins import AntPath

st.set_page_config(layout="wide")






def main():
      st.title('Customer Overview')
      option =st.sidebar.selectbox('Select an Operation', ['Existing Customers Table Overview',
                                                           'Summary with Updatable Feature via CSV Upload',
                                                           'Sales_Revenue_Customer_Distribution Map Overview',
                                                           'Vlookup_For_Quick_On_The_Go_CR',
                                                           'Sales_Funnel_Process Overview'] )
      if option=='Existing Customers Table Overview':
         st.subheader('Existing Customers Table Overview')

         vidfile=open("sql.mp4","rb").read()
         st.video(vidfile,loop=True, autoplay=True, muted=True )
         dfConvProQty=pd.read_excel('cust1.xlsx')
         st.dataframe(dfConvProQty)
         
      elif option=='Summary with Updatable Feature via CSV Upload':
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
         
      elif option=='Sales_Revenue_Customer_Distribution Map Overview':
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
                  
            st.map(chinalon_lat_1[['latitude','longitude']],size="Revenue",color=[1.0, 0.1,0.2,0.5])     

            gpdmap1=chinalon_lat_1.explore( cmap='jet',
                                            column='city',
                                            marker_kwds={'radius':5},
                                            tooltip=["Revenue","country",'city','id'])
            
            st_folium(gpdmap1,width=1200,height=300)            
            iconlist=['star','th','times','gear','inbox','list-alt','volume-down','tags','font','align-left','dedent','image','tint','arrows','pause','eject','times-circle',
                  'arrow-up','compress','gift','warning','comment','shopping-cart','key',
                  'thumb-tack','upload','phone-square','unlock','bullhorn','arrow-circle-down','briefcase','link','copy',
                  'square','list-ol','truck','columns','sort-up','undo','umbrella','cloud-download','h-square','angle-double-down','desktop','circle-o','mail-reply','reply-all','crop','info','puzzle-piece','fire-extinguisher','chevron-circle-up','unlock-alt','play-circle','leveldown','compass','dollar','rmb','rub','file','sort-amount-desc','long-arrow-up','vimeo-square','bank','google','paw','car','binoculars','at','pie-chart','toggle-on','cart-arrow-down','street-view','venus-mars','genderless','user-plus','train','battery-3','battery-quarter','object-group',
                  'hourglass-start','hourglass','trademark','tv','map-pin','pause-circle','shopping-basket','wheelchair-alt','braille','hard-of-hearing','sign-language','music','th-list','search-plus','cog','road','lock','volume-up','book','bold','align-center','outdent','edit','step-backward','stop','chevron-left','check-circle','arrow-down','plus','leaf','exclamation-triangle','magnet','folder','bar-chart','gears','star-half','external-link','credit-card']

            colors=['red','blue','green','orange','purple','darkred','lightred','beige','darkblue','darkgreen','cadetblue','darkpurple','white','pink','lightblue','lightgreen','gray','black']


            xx=pd.read_excel('x.xlsx')

            mapmarker1=folium.Map(location=[21.168247129485962, 79.93652343750001],
                      zoom_start=4,
                      tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 
                      attr='default')

            for i in range(len(xx['lat'])):
                      folium.Marker( location=[xx['lat'][i],xx['lng'][i]],
                         tooltip=xx['city'][i],
                         icon=folium.Icon(icon=iconlist[i+50], prefix='fa', color=colors[i]),
                         popup=xx['population'][i]).add_to(mapmarker1)     
    

            st_folium(mapmarker1, width=1200, height=700)
            google_m = folium.Map(  location=[24.547836328731947, 112.47906862329836], zoom_start=5,
                        tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', attr='default')
            salesworkb001=pd.read_excel('bubbleantheatmap - Copy.xlsx')
            
            rad=salesworkb001['Revenue']
            lat=salesworkb001['latitude']
            lng=salesworkb001['longitude']
            colors=salesworkb001['colors']
            city_tooltip=salesworkb001['city']
            prov_hover=salesworkb001['admin_name']
            
            
            heatmapdata=pd.DataFrame({    'lat':lat,
                                          'lng':lng,
                                          'rad':rad})

            heatmapdata['rad']=heatmapdata['rad'].apply(lambda x:(x-heatmapdata['rad'].min())/(heatmapdata['rad'].max()-heatmapdata['rad'].min()))
            HeatMap(heatmapdata).add_to(google_m)
            st_folium(google_m,width=1200,height=300)
 

            google_m_b1 = folium.Map(  location=[24.547836328731947, 112.47906862329836], zoom_start=5,
                        tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', attr='default')

            legendHtml = '''
            <div style="position: fixed; 
            bottom: 50px; left: 50px; width: 150px; height: 85px; 
            border:2px solid grey; z-index:9999; font-size:14px;background-color:gray
            ">&nbsp; Fuel Types <br>
            &nbsp; <i class="fa fa-circle"
                              style="color:yellow"></i> &nbsp;minor<br>
            &nbsp; <i class="fa fa-circle"
                              style="color:red"></i> &nbsp;primary<br>
            &nbsp; <i class="fa fa-circle"
                              style="color:blue"></i> &nbsp; admin<br>
                  </div>
            '''
            google_m_b1.get_root().html.add_child(folium.Element(legendHtml))
            folium.LayerControl().add_to(google_m_b1)
            
            for i in range(len(lng)):
                  folium.Circle( location=[lat[i], lng[i]],radius=rad[i]/1000, 
                              popup=prov_hover[i],tooltip=city_tooltip[i], 
                              fill=True,fill_color=colors[i], fill_opacity=0.8).add_to(google_m_b1)
            pathLatLngs = [(lat[0],lng[0]), 
               (lat[1],lng[1]),
               (lat[2],lng[2]),
               (lat[3],lng[3]), 
               (lat[4],lng[4])]

            AntPath(pathLatLngs, delay=200, dash_array=[10,50], color="blue", 
                  pulse_color="orange", weight=5, opacity=1).add_to(google_m_b1)

            st_folium(google_m_b1,width=1200,height=300)

      elif option=='Vlookup_For_Quick_On_The_Go_CR':
      
            st.title('Vlookup Online')
            st.write('Please Upload Source FIle and Entry Data File')
            st.link_button("Click to launch the application","https://vlookupexcelwebapp-sd22cj8apf9ud2zoehaalz.streamlit.app")
      elif option=='Sales_Funnel_Process Overview':      
          funnel_s_all=pd.read_excel('funnelchartdata.xlsx')
          fig_funnel=px.funnel(data_frame=funnel_s_all,
                              x=funnel_s_all['Values'],
                              y=funnel_s_all['stage'],
                              color="Sales",
                              color_discrete_sequence=["red", "blue", "green", "orange","cyan","indigo"])        
          st.plotly_chart(fig_funnel)  
          st.dataframe(funnel_s_all)
                  
if __name__=="__main__":
    main()   
