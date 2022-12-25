import streamlit as st
import functions as f
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 

mod = {'BOT' : 'Business, Operate, Transfer', 'BOT (Toll)' : 'Business, Operate, Transfer', 'OMT' : 'Operate, Maintain and Transfer'}
na = 'Not Available'

st.set_page_config(initial_sidebar_state='collapsed', layout = 'centered')    
st.title('NHAI TOLL PLAZA')
st.markdown('_SHREY MEHRA(LCO20376)_-Also, This is all ethical I am doing, just for educational purposes, _*just to clarify*_')
    
selected = option_menu(
    menu_title = None,
    options = ['Find based of National Highway','Find based of State'] 
)

if selected == 'Find based of State':
    
    states = f.fetch_states()
    selected_state = st.selectbox('Select State', states)

    plazas = f.fetch_plazas(selected_state)
    selected_plaza = st.selectbox('Select Toll Plaza', plazas)

    highway, length, plaza_name, latitude, longitude, model, data, extra  = f.fetch_highways(selected_state,selected_plaza)
    if model in mod:
        model = mod[model] 
    st.write(f'Highway Name : {highway}')
    st.write(f'Highway Length : {length} kms')
    st.write(f'Plaza Name : {plaza_name}')
    st.write(f'Model : {model}')
    if len(data) > 2:
        data = pd.read_json(data).T
        
        st.table(data)
    else:
        st.write('TOLL DATA AVAILABLE')

    with st.expander("See Emergency Detail"):
        st.markdown('Helpline Numbers:')
        st.write('')
        st.write('')
        
        crane, ambulance, patrol = extra['Helpline No. :'].split(',')
        
        crane = crane.strip().split('-')[1] if len(crane.strip().split('-')) == 2 and crane.strip().split('-')[1] != '' else na
        ambulance = ambulance.strip().split('-')[1] if len(ambulance.strip().split('-')) == 2 and ambulance.strip().split('-')[1] != '' else na
        patrol = patrol.strip().split('-')[1] if len(patrol.strip().split('-')) == 2 and patrol.strip().split('-')[1] != '' else na
        
        st.write('Crane : ', crane)
        st.write('Ambulance : ', ambulance)
        st.write('Route Patrol : ', patrol)

        st.write('')
        emergency = extra['Emergency Services :']
        emergency = emergency if emergency is not None else 'Sorry! ' + na

        st.markdown(f'Call for Urgency at : {patrol}')

        police = extra["Nearest Police Station:"]
        if police == '/':
            st.write(f'Police Station  ::  {na} neither Phone Number  ::  {na}')
            st.write('')
        else:
            if len(police.split(' / ')) == 2:
                ps = police.split(' / ')[0]
                num = police.split(' / ')[1]

                ps, num = ps.split(','), num.split(',')
                
                if len(ps) == len(num):
                    for i in range(len(ps)):
                        st.write(f'Police Station  ::  _*{ps[i].strip()}*_ and Phone Number  ::  _*{num[i].strip()}*_')
                        st.write('')
                else:
                    for i in range(min(len(ps), len(num))):
                        st.write(f'Police Station  ::  _*{ps[i].strip()}*_ and Phone Number  ::  _*{num[i].strip()}*_')
                        st.write('')
            else:
                if isinstance(police.split(' / ')[0], int):
                    num = police.split(' / ')[0]
                    st.write(f'Police Station  ::  _*{na}*_ and Phone Number  ::  _*{num.strip()}*_')
                    st.write('')  
                else:
                    ps = police.split(' / ')[0]
                    st.write(f'Police Station  ::  _*{ps.strip()}*_ and Phone Number  ::  _*{na}*_')
                    st.write('')

        
        hospital = extra['Nearest Hospital(s):']
        
        if hospital != None:
            st.markdown('_LIST OF HOSPITAL ON THE NATIONAL HIGHWAY_')
            hospital = hospital.split(')')
            st.write(hospital[1].rsplit(',', 1)[0].strip())
            
            if len(hospital) == 3:
                st.write(hospital[2])
            
            if len(hospital) > 3:
                for i in range(3, len(hospital), 2):
                    st.write(hospital[i].rsplit(',', 1)[0].strip())            
        else:
            st.markdown('_No Data or Hospital Available_')


    fig = px.scatter_mapbox(
        lat = [latitude], 
        lon = [longitude],
        color_continuous_scale=px.colors.sequential.Rainbow,
        hover_name = [f'{plaza_name}, {selected_state}'],
        height = 700,
        width = 1000,
        zoom = 4,
        center=dict( lat=22.065773, lon=76.040497 ),   
    )

    fig.update_layout(
        showlegend = False,
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig.update_traces(marker={'size': 30})
    
    if st.button('Show on Map', key = 11):
        st.plotly_chart(fig)
    
if selected == 'Find based of National Highway':
    
    highways = f.fetch_highway_wise()
    selected_highway = st.selectbox('Select State', highways)

    state_list = f.fetch_highway_state(selected_highway)
    temp_lat, temp_long, hover_whole, id_whole = [], [], [], []
    for i in range(len(state_list)):
        state = list(state_list.keys())[i]
        count = list(state_list.values())[i]
        
        st.write(f'State Name : {state}')
        st.write(f'Number of Tolls : {count}')
        st.write('')
        
        with st.expander("See in detail"):
            
            length, id, plaza_name, latitude, longitude, model, details, extra = f.fetch_toll_state(selected_highway, state)
            hover_data = [[plaza]+[i]+[state] for plaza,i  in zip(plaza_name, id)]
            
            temp_lat += latitude
            temp_long += longitude
            hover_whole += hover_data
            id_whole += id

            for i in range(len(length)):
                st.write(f'Plaza Name : {plaza_name[i]}, Plaza ID : {id[i]}')
                st.write(f'Length of Stretch : {length[i]}')
                st.write(f'Model : {model[i]}')
                st.write(f'Latitude : {latitude[i]}, Longitude : {longitude[i]}')
                if len(details[i]) > 2:
                    data = pd.read_json(details[i]).T
                    st.table(data)
                else:
                    st.write('TOLL DATA AVAILABLE')
                try:
                    if st.button('Emergency Services', key = str(latitude[i])+plaza_name[i]+str(id[i])):    
                        st.markdown('Helpline Numbers:')
                        st.write('')
                        st.write('')
                        
                        crane, ambulance, patrol = extra[i]['Helpline No. :'].split(',')
                        
                        crane = crane.strip().split('-')[1] if len(crane.strip().split('-')) == 2 and crane.strip().split('-')[1] != '' else na
                        ambulance = ambulance.strip().split('-')[1] if len(ambulance.strip().split('-')) == 2 and ambulance.strip().split('-')[1] != '' else na
                        patrol = patrol.strip().split('-')[1] if len(patrol.strip().split('-')) == 2 and patrol.strip().split('-')[1] != '' else na
                        
                        st.write('Crane : ', crane)
                        st.write('Ambulance : ', ambulance)
                        st.write('Route Patrol : ', patrol)

                        st.write('')
                        emergency = extra[i]['Emergency Services :']
                        emergency = emergency if emergency is not None else 'Sorry! ' + na

                        st.markdown(f'Call for Urgency at : {patrol}')

                        police = extra[i]["Nearest Police Station:"]
                        if police == '/':
                            st.write(f'Police Station  ::  {na} neither Phone Number  ::  {na}')
                            st.write('')
                        else:
                            if len(police.split(' / ')) == 2:
                                ps = police.split(' / ')[0]
                                num = police.split(' / ')[1]

                                ps, num = ps.split(','), num.split(',')
                                
                                if len(ps) == len(num):
                                    for i in range(len(ps)):
                                        st.write(f'Police Station  ::  _*{ps[i].strip()}*_ and Phone Number  ::  _*{num[i].strip()}*_')
                                        st.write('')
                                else:
                                    for i in range(min(len(ps), len(num))):
                                        st.write(f'Police Station  ::  _*{ps[i].strip()}*_ and Phone Number  ::  _*{num[i].strip()}*_')
                                        st.write('')
                            else:
                                if isinstance(police.split(' / ')[0], int):
                                    num = police.split(' / ')[0]
                                    st.write(f'Police Station  ::  _*{na}*_ and Phone Number  ::  _*{num.strip()}*_')
                                    st.write('')  
                                else:
                                    ps = police.split(' / ')[0]
                                    st.write(f'Police Station  ::  _*{ps.strip()}*_ and Phone Number  ::  _*{na}*_')
                                    st.write('')

                        
                        hospital = extra[i]['Nearest Hospital(s):']
                        
                        if hospital != None:
                            st.markdown('_LIST OF HOSPITAL ON THE NATIONAL HIGHWAY_')
                            hospital = hospital.split(')')
                            st.write(hospital[1].rsplit(',', 1)[0].strip())
                            
                            if len(hospital) == 3:
                                st.write(hospital[2])
                            
                            if len(hospital) > 3:
                                for i in range(3, len(hospital), 2):
                                    st.write(hospital[i].rsplit(',', 1)[0].strip())            
                        else:
                            st.markdown('_No Data or Hospital Available_')
                except:
                    continue

                st.write(''); st.write(''); st.write(''); st.write(''); 
                st.write('')
            
            fig = px.scatter_mapbox(
                lat = latitude, 
                lon = longitude,
                color_continuous_scale=px.colors.sequential.Rainbow,
                hover_name = hover_data,
                color = id,
                height = 700,
                width = 1000,
                zoom = 4,
                center=dict( lat=22.065773, lon=76.040497 ),   
            )

            fig.update_layout(
                showlegend = False,
                mapbox_style="open-street-map",
                margin={"r":0,"t":0,"l":0,"b":0}
            )
            fig.update_traces(marker={'size': 30})
            
            st.plotly_chart(fig)
    
    fig = px.scatter_mapbox(
        lat = temp_lat, 
        lon = temp_long,
        color_continuous_scale=px.colors.sequential.Rainbow,
        hover_name = hover_whole,
        color = id_whole,
        height = 500,
        width = 800,
        zoom = 3.2,
        center=dict( lat=22.065773, lon=76.040497 ),   
    )

    fig.update_layout(
        showlegend = False,
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    fig.update_traces(marker={'size': 30})
    
    st.plotly_chart(fig)
     