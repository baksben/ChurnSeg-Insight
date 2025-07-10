import dash
from dash import dcc, html, dash_table, Output, Input
import plotly.express as px
import pandas as pd

# Load your processed dataset with Cluster, Churn, and RFM columns
df = pd.read_excel(r'D:\Portfolio\churn\deliveroo\data\after_segmentation.xlsx')  # Replace with your dataset path

# Initialize the Dash app
app = dash.Dash(__name__)

# Precompute figures
# 1. Churn by Cluster
churn_fig = px.bar(df.groupby(['Cluster', 'Churn']).size().reset_index(name='Count'),
                   x='Cluster', y='Count', color='Churn', barmode='group',
                   title='Churn Count by Customer Segment (Cluster)')

# 2. Segment Size
segment_fig = px.pie(df, names='Cluster', title='Customer Segment Distribution')

# 3. Total Spend by Segment
total_spend_fig = px.bar(df.groupby('Cluster')['Total Spend'].sum().reset_index(),
                         x='Cluster', y='Total Spend', color='Cluster',
                         title='Average Total Spent by Customer Segment')

# App layout
app.layout = html.Div([
    html.H1('Customer Insights Dashboard', style={'textAlign': 'center'}),

    html.Div([
        html.Div([dcc.Graph(figure=churn_fig)], className='six columns'),
        html.Div([dcc.Graph(figure=segment_fig)], className='six columns')
    ], className='row'),

    html.Div([
        dcc.Graph(figure=total_spend_fig)
    ]),

    html.Div([
        html.H3('Explore Raw Data'),
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            filter_action='native',
            sort_action='native'
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
