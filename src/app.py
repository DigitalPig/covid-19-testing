from typing import Dict, List, Tuple
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    "COVID-19 Testing per Capita By US States",
    external_stylesheets=external_stylesheets,
)

STATES_SEL = [
    {"label": "AL", "value": "AL"},
    {"label": "AK", "value": "AK"},
    {"label": "AZ", "value": "AZ"},
    {"label": "AR", "value": "AR"},
    {"label": "CA", "value": "CA"},
    {"label": "CO", "value": "CO"},
    {"label": "CT", "value": "CT"},
    {"label": "DE", "value": "DE"},
    {"label": "DC", "value": "DC"},
    {"label": "FL", "value": "FL"},
    {"label": "GA", "value": "GA"},
    {"label": "HI", "value": "HI"},
    {"label": "ID", "value": "ID"},
    {"label": "IL", "value": "IL"},
    {"label": "IN", "value": "IN"},
    {"label": "IA", "value": "IA"},
    {"label": "KS", "value": "KS"},
    {"label": "KY", "value": "KY"},
    {"label": "LA", "value": "LA"},
    {"label": "ME", "value": "ME"},
    {"label": "MD", "value": "MD"},
    {"label": "MA", "value": "MA"},
    {"label": "MI", "value": "MI"},
    {"label": "MN", "value": "MN"},
    {"label": "MS", "value": "MS"},
    {"label": "MO", "value": "MO"},
    {"label": "MT", "value": "MT"},
    {"label": "NE", "value": "NE"},
    {"label": "NV", "value": "NV"},
    {"label": "NH", "value": "NH"},
    {"label": "NJ", "value": "NJ"},
    {"label": "NM", "value": "NM"},
    {"label": "NY", "value": "NY"},
    {"label": "NC", "value": "NC"},
    {"label": "ND", "value": "ND"},
    {"label": "OH", "value": "OH"},
    {"label": "OK", "value": "OK"},
    {"label": "OR", "value": "OR"},
    {"label": "PA", "value": "PA"},
    {"label": "RI", "value": "RI"},
    {"label": "SC", "value": "SC"},
    {"label": "SD", "value": "SD"},
    {"label": "TN", "value": "TN"},
    {"label": "TX", "value": "TX"},
    {"label": "UT", "value": "UT"},
    {"label": "VT", "value": "VT"},
    {"label": "VA", "value": "VA"},
    {"label": "WA", "value": "WA"},
    {"label": "WV", "value": "WV"},
    {"label": "WI", "value": "WI"},
    {"label": "WY", "value": "WY"},
]


def curr_test_ts_states(url: str) -> pd.DataFrame:
    """
    This function is to read the current testing from https://covidtracking.com/api/
    and return the pandas dataframe
    """
    states_daily = pd.read_csv(url)
    states_daily["date"] = pd.to_datetime(states_daily["date"], format="%Y%m%d")
    states_total_by_dates = states_daily.pivot_table(
        index="date", columns="state", values="totalTestResults"
    )
    return states_total_by_dates


# Read the US population table
def us_pop(loc: str) -> Dict[str, int]:
    """
    Read the US population data and return as a pandas dataframe
    """
    states_pop = pd.read_csv(loc)
    state_pops = (
        states_pop.rename(columns={"State_Code": "Name", "2019 Estimate": "Pop"})
        .set_index("Name")
        .loc[:, "Pop"]
        .to_dict()
    )
    return state_pops


def normalize_testing(test_df: pd.DataFrame, pop_df: Dict[str, int]) -> pd.DataFrame:
    """
    Normalizing the testing dataframe with state population
    """
    drop_states = [x for x in test_df.columns if x not in list(pop_df.keys())]
    test_df_norm_by_pop = test_df.drop(drop_states, axis=1).copy(deep=True)
    for state, pop in pop_df.items():
        test_df_norm_by_pop.loc[:, state] = (
            test_df_norm_by_pop.loc[:, state] / pop * 1e6
        )
    return test_df_norm_by_pop


raw_testing = curr_test_ts_states("http://covidtracking.com/api/states/daily.csv")
us_populations = us_pop("./data/states_population.csv")
norm_df = normalize_testing(raw_testing, us_populations)

introduction = """
## Why we need a fast test?

S. Korea has the exponential growth initially. But after that, due to extensive testing and rigrous contact tracing,
it seems to grip the Coronavirus so far. The S. Korea lessons learned is: **Testing and Tracing**.

What about the US? How do we do in terms of coronavirus testing? Can we grip the coronavirus as soon as we can like S. Korea
without huge impact to the economy? If we want to do that, ramping up the test is the number 1 issue. Here is the testing conducted currently by state
at different dates till today.

We get the testing date from [Covid Tracking Project](https://covidtracking.com/api/) and the US population by states
from [US Census Bureau](https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-total.html)

"""


app.layout = html.Div(
    [
        html.H1("US Testing per Capita Time Series by States"),
        dcc.Markdown(introduction),
        html.Label("States"),
        dcc.Dropdown(
            id="select-states",
            options=STATES_SEL,
            value=["NY", "WA", "CA", "VA"],
            multi=True,
        ),
        dcc.Graph(id="time-series-chart"),
        # Hidden div inside the app that stores the intermediate value
        html.Div(id="intermediate-value", style={"display": "none"}),
    ]
)


@app.callback(
    Output(component_id="time-series-chart", component_property="figure"),
    [Input(component_id="select-states", component_property="value")],
)
def gen_figure(states: List[str]) -> go:
    """
    Using the input normalized dataframe and the list states to generate the graph
    """
    fig = go.Figure()
    for state in states:
        fig.add_trace(
            go.Scatter(
                x=norm_df.index,
                y=norm_df.loc[:, state],
                mode="lines+markers",
                name=state,
            )
        )
    fig.update_layout(
        title="COVID-19 Testing Conducted per Capita in Each States",
        xaxis_title="Date",
        yaxis_title="Number of Tests per Million People",
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
