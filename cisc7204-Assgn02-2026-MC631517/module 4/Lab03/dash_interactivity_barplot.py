# Import required libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read airline dataset
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

# Create Dash application
app = dash.Dash(__name__)

# Create dashboard layout
app.layout = html.Div(
    children=[
        html.H1(
            'Total number of flights to the destination state split by reporting airline',
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'fontSize': 40
            }
        ),

        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id='input-year',
                    value=2010,
                    type='number',
                    style={
                        'height': '50px',
                        'fontSize': 35
                    }
                )
            ],
            style={'fontSize': 40}
        ),

        html.Br(),
        html.Br(),

        html.Div(
            dcc.Graph(id='bar-plot')
        )
    ]
)

# Add callback
@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)
def get_graph(entered_year):

    # Select data based on entered year
    df = airline_data[
        airline_data['Year'] == int(entered_year)
    ]

    # Calculate total flights by destination state and airline
    bar_data = (
        df.groupby(
            ['DestState', 'Reporting_Airline']
        )['Flights']
        .sum()
        .reset_index()
    )

    # Create bar chart
    fig = px.bar(
        bar_data,
        x='DestState',
        y='Flights',
        color='Reporting_Airline',
        title='Total number of flights to the destination state split by reporting airline'
    )

    return fig

# Run the application
if __name__ == '__main__':
    app.run()