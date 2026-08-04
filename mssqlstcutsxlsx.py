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
                                                           'Sales_Funnel_Process Overview',
                                                           'Maximum Revenue and Profit Unit Calculator'] )
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


      elif option=='Maximum Revenue and Profit Unit Calculator':
            import streamlit.components.v1 as components
            import streamlit as st
            from sympy import symbols, Function, solve, Eq,plot
            
            st.set_page_config(
                page_title="Ex-stream-ly Cool App",
                page_icon="🧊",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://www.extremelycoolapp.com/help',
                    'Report a bug': "https://www.extremelycoolapp.com/bug",
                    'About': "# This is a header. This is an *extremely* cool app!"
                }
            )
            
            # Number input with placeholder and no default value
            st.title("Data Entry for two Points for Calculating Max Revenue")
            col1, col2, col3 ,col4= st.columns(4, vertical_alignment="bottom")
            
            with col1:
                x_price_1 = st.number_input(
                label=":blue[Please enter the price of the product (x_price_1):]",
                placeholder="Type a number...",
                step=0.5,
                value=10.00,
                format="%0.1f",key="x_price_1"
                )
                st.write("x_price_1:", x_price_1)
            
            with col2:
                y_demand_1 = st.number_input(
                label=":blue[Please enter the quantity_sold based on price (x_price_1):]",
                placeholder="Type a number...",
                step=0.5,
                value=100.00,
                format="%0.1f",key="y_demand_1"
                )
                st.write("y_demand_1:", y_demand_1)
            
            with col3:
                x_price_2 = st.number_input(
                label=":red[Please enter the price of the product (x_price_2):]",
                placeholder="Type a number...",
                step=0.5,
                value=20.00,
                format="%0.1f",key="x_price_2"
                )
                st.write("x_price_2:", x_price_2)
            
            with col4:
                y_demand_2 = st.number_input(
                label=":red[Please enter the quantity_sold based on price (x_price_2):]",
                placeholder="Type a number...",
                step=0.5,
                value=200.00,
                format="%0.1f",key="y_demand_2"
                )
                st.write("y_demand_2:", y_demand_2)
            
            st.markdown(":red[**Slope and y-intercept formula&emsp;:**] &emsp;:blue[**$y=mx+b$  &rarr; &emsp;**] &rarr;&emsp;Revenue = Slope(m) * Price + y_intercept(b)&rarr; &emsp; :green[Slope (m)=$ \\frac{y_{demand_2}-y_{demand_1}}{x_{price_2}-x_{price_1}}$]")
            slope_prb=round((y_demand_2-y_demand_1)/(x_price_2-x_price_1),2)
            
            y_intercept=round(y_demand_1-slope_prb*x_price_1,2)   
            
            y_maxrev = symbols('y_maxrev')
            x_pricmx = symbols('x_pricmx')
            expr =y_maxrev=(slope_prb*x_pricmx+y_intercept)*x_pricmx
            
            import sympy as sympy
            df_prb=sympy.diff(expr)
            x_pricmx_solved=round(solve(df_prb)[0],2)
            
            y_maxrev=round(slope_prb*x_pricmx_solved**2+ y_intercept*x_pricmx_solved,2)
            st.write("b(y_intercept):", y_intercept , "m(slope):", slope_prb,"Price is: ", str(x_pricmx_solved), "Max Revenue is : ", str(y_maxrev))
            st.divider()
            st.title("Data Entry for Maximizing Profit:Units Sold & Revenue")
            col1, col2, col3 ,col4= st.columns(4, vertical_alignment="bottom")
            
            with col1:
                price_constant = st.number_input(
                label=":blue[Please enter the **price constant**:]",
                placeholder="Type a number...",
                step=0.5,
                value=10.00,
                format="%0.1f",key="price_constant"
                )
                st.write("price constant:", price_constant)
            
            with col2:
                coefficient_unit_x = st.number_input(
                label=":blue[Please enter the coefficient of unit x:]",
                placeholder="Type a number...",
                step=0.5,
                value=20.00,
                format="%0.1f",key="coefficient_unit_x"
                )
                st.write("coefficient_unit_x is :", coefficient_unit_x)
            
            with col3:
                cost_constant = st.number_input(
                label=":red[Please enter the cost constant:]",
                placeholder="Type a number...",
                step=0.5,
                value=100.00,
                format="%0.1f",key="cost_constant"
                )
                st.write("cost_constant:", cost_constant)
            with col4:
                coefficient_unitx_in_cost = st.number_input(
                label=":red[Please enter the coefficient of unitx in cost:]",
                placeholder="Type a number...",
                step=0.5,
                value=200.00,
                format="%0.1f",key="coefficient_unitx_in_cost"
                )
                st.write("coefficient_unitx_in_cost:", coefficient_unitx_in_cost)
            
            
            
            st.markdown(" :red[profit = Revenue - Cost &emsp; &rarr;&emsp; ] :blue[price=price_constant + coefficient_unit_x * x &emsp;|&emsp;] :green[cost= cost_constant + coefficient_unitx_in_cost * x]")
            
                        
            unitx = symbols('unitx')
            
            expr_max_prof =x_max_profit=((price_constant - coefficient_unit_x * unitx)*unitx)-(coefficient_unitx_in_cost*unitx + cost_constant)
            
            import sympy as sympy
            df_prb_max_prof=sympy.diff(expr_max_prof)
            x_pricmx_prof_solved=round(solve(df_prb_max_prof)[0],2)
            
            
            max_profit_rev=((price_constant - coefficient_unit_x * x_pricmx_prof_solved)*x_pricmx_prof_solved)-(coefficient_unitx_in_cost*x_pricmx_prof_solved + cost_constant)
            st.write(   " Profit Equation:", str(expr_max_prof), 
                        " To achieve Max Profit:unitx is:", int(x_pricmx_prof_solved),  
                        "  Total Revenue based on maximum profit unitx : ", int(max_profit_rev) )
            
            st.divider()
            # html section
            st.title("Maximizing Profit and Revenue Workflow ")
            st.subheader("Compiled by Singer")
            with open("max_profit.html", "r", encoding="utf-8") as html_file:
                html_content = html_file.read()
                components.html(html_content, height=580,width=1200)
            
            with open("max_revenue.html", "r", encoding="utf-8") as html_file:
                html_content = html_file.read()
                components.html(html_content, height=1150,width=1200)            
if __name__=="__main__":
    main()   
