# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # TASK 1: Add a Launch Site Drop-down Input Component
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a Range Slider to Select Payload
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function for the Pie Chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # For ALL sites, show the total success counts (Class=1) by site
        fig = px.pie(filtered_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        # For a specific site, filter and show Success vs. Failure counts
        # Filter the dataframe for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Get the counts of success (1) and failure (0)
        site_counts = site_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(site_counts, values='count', 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TASK 4: Callback function for the Scatter Plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    # Filter data based on payload range slider
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    range_df = spacex_df[mask]

    if entered_site == 'ALL':
        # Render scatter plot for all sites
        fig = px.scatter(range_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Filter based on specific site
        site_df = range_df[range_df['Launch Site'] == entered_site]
        # Render scatter plot for selected site
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)