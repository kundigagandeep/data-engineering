from dash import Dash, html, dcc
import plotly.graph_objs as go
import pandas as pd

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/iris.csv")

# Create a Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Iris Data Set'),

    dcc.Graph(
        id='iris-scatterplot',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['class'] == i]['sepal_length'],
                    y=df[df['class'] == i]['sepal_width'],
                    mode='markers',
                    name=i
                ) for i in df['class'].unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Sepal Length'},
                yaxis={'title': 'Sepal Width'},
                hovermode='closest'
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
