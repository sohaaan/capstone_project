# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import no_update

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

div_data = spacex_df[spacex_df['class'] != 0]
div_data1 = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
div_data2 = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
div_data3 = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
div_data4 = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                dcc.Dropdown(id='site_dropdown', 
                                        options=[
                                        {'label': 'All Sites', 'value': 'SITE'},
                                        {'label': 'CCAFS LC-40', 'value': 'SITE1'},
                                        {'label': 'CCAFS SLC-40', 'value': 'SITE2'},
                                        {'label': 'KSC LC-39A', 'value': 'SITE3'},
                                        {'label': 'VAFB SLC-4E', 'value': 'SITE4'}
                                        ],
                                        placeholder='Select a Launch Site here',
                                        style={'text-align-last': 'center',
                                        'width': '80%',
                                        'padding':'3px',
                                        'font-size':'20px'})]
                                        
                                    # Place them next to each other using the division style
                                    ,

                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.Div([
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                        id='payload_slider',
                                        min=0,
                                        max=10000,
                                        step=1000,
                                        marks={
                                                0: '0',
                                                2000: '2k',
                                                4000: '4k',
                                                6000: '6k',
                                                8000: '8k',
                                                10000: '10k'
                                                },
                                        value=[min_payload, max_payload]
                                        )]),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output



@app.callback(  [Output(component_id='success-pie-chart', component_property='figure'),
                 Output(component_id='success-payload-scatter-chart', component_property='figure')],
                [Input(component_id='site_dropdown', component_property='value'),
                 Input(component_id='payload_slider', component_property='value')]
            
               
              )
def get_graph(site_dropdown, payload_slider):

        if site_dropdown == 'SITE':
            # Percentage of diverted airport landings per reporting airline
            
            pie_fig = px.pie(div_data, values='class', names='Launch Site', title='% of success rate in Different Sites')
            
            sc= spacex_df[spacex_df['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1], inclusive=True)]
            scatter_fig= px.scatter(sc, y="class", x="Payload Mass (kg)", color='Booster Version Category')

           # return [dcc.Graph(figure=pie_fig),
           #         dcc.Graph(figure=scatter_fig)]
            # REVIEW6: Return dcc.Graph component to the empty division
        elif site_dropdown == 'SITE1':
            pie_fig = px.pie(div_data1, names='class', title='% of success by CCAFS LC-40')
            

            sc1= div_data1[div_data1['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1], inclusive=True)]
            scatter_fig= px.scatter(sc1, y="class", x="Payload Mass (kg)", color='Booster Version Category')

           # return [dcc.Graph(figure=pie_fig),
           #         dcc.Graph(figure=scatter_fig)]

        elif site_dropdown == 'SITE2':
            pie_fig = px.pie(div_data2, names='class', title='% of success by CCAFS SLC-40')
            
            sc2= div_data2[div_data2['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1], inclusive=True)]
            scatter_fig= px.scatter(sc2, y="class", x="Payload Mass (kg)", color='Booster Version Category')

          #  return [dcc.Graph(figure=pie_fig),
           #         dcc.Graph(figure=scatter_fig)]

        elif site_dropdown == 'SITE3':
            pie_fig = px.pie(div_data3, names='class', title='% of success by KSC LC-39A')
            
            sc3= div_data3[div_data3['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1], inclusive=True)]
            scatter_fig= px.scatter(sc3, y="class", x="Payload Mass (kg)", color='Booster Version Category')

            #return [dcc.Graph(figure=pie_fig),
            #        dcc.Graph(figure=scatter_fig)]

        else:
            pie_fig = px.pie(div_data4, names='class', title='% of success by VAFB SLC-4E')
            
            sc4= div_data4[div_data4['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1], inclusive=True)]
            scatter_fig= px.scatter(sc4, y="class", x="Payload Mass (kg)", color='Booster Version Category')

            #return [dcc.Graph(figure=pie_fig),
            #        dcc.Graph(figure=scatter_fig)]
    
        return [pie_fig,scatter_fig]

            # REVIEW6: Return dcc.Graph component to the empty division
        
#get_graph('SITE', 5)         

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
