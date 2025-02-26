import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL = 'visualization/density.csv'

st.title('Density Grid Visualization Tool')


@st.cache_data
def load_data_from_csv():
    return pd.read_csv(DATA_URL)


data_load_state = st.text('Loading CSV file...')
data = load_data_from_csv()
data_load_state.text('Loading CSV file... done!')

time_steps = sorted(data['timeStep'].unique())

if 'selected_time_step' not in st.session_state:
    st.session_state['selected_time_step'] = min(time_steps)

# sync slider and state
selected_time_step = st.slider('Select Time Step', min(time_steps), max(time_steps),
                               st.session_state['selected_time_step'])

st.session_state['selected_time_step'] = selected_time_step

if st.button('Increment'):
    st.session_state['selected_time_step'] = min(max(time_steps), st.session_state[
        'selected_time_step'] + 1)

st.write(st.session_state['selected_time_step'])

filtered_data = data[data['timeStep'] == st.session_state['selected_time_step']]

zmin = data['gridCount-PID7'].min()
zmax = data['gridCount-PID7'].max()

if not filtered_data.empty:
    pivot_df = filtered_data.pivot_table(index='y', columns='x', values='gridCount-PID7')

    fig = px.imshow(pivot_df,
                    labels=dict(x="x", y="y", color="Grid Count"),
                    title=f"Grid Count at Time Step {st.session_state['selected_time_step']}",
                    # add to overall compare and not just per timestep
                    zmin=zmin,
                    zmax=zmax,
                    )

    st.plotly_chart(fig)
else:
    st.write("No data available for the selected time step.")
