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
# COVID-19 Tests per Capita in Different States in US

## Introductions

[COVID-19](https://www.who.int/emergencies/diseases/novel-coronavirus-2019) is declared by WHO as pandemic. It is affecting almost
all countries in the world at this moment.

The virus starts human-to-human transmission in Wuhan, China. After almost 2 months of brutal lockdown by stopping almost all economical
activities, China starts to see the lights from the end of tunnel, with a huge cost. The virus also spreads to S.Korea and Japan. S.Korea
has an initial exponetial growth of the confirmed cases, but it is quickly brought under the control. Besides, it is also very impressive that S.Korean government achieves this without an extensive lockdown the country or shutdown the border. On this awesome chart made by Financial Times, you can see that S.Korean has a truly "flatterned" curve.

![FT COVID-19 cases by time](https://www.ft.com/__origami/service/image/v2/images/raw/http%3A%2F%2Fcom.ft.imagepublish.upp-prod-us.s3.amazonaws.com%2F0d6318d6-71fc-11ea-95fe-fcd274e920ca?fit=scale-down&quality=highest&source=next&width=1260)

## How do S.Koreans achieve this?

Testing! Test as many as you can, and tract their contacts and test those contacts as soon as possible. By doing so, you are able to identify any potential contagious people at the early stage and stop healthy people to contract the virus.

## Why we need a fast test?

**Testing and Tracing** seems to be an effective method for a society that wants to have a healthy balance between controlling the virus
and minimizing the impact to the economy.

What about the US? How do we do in terms of coronavirus testing? Can we grip the coronavirus as soon as we can like S. Korea
without huge impact to the economy?

If we want to do that, ramping up the test is the number 1 issue. I made this quick Dash application to give you a better idea about how many tests are conducted currently in your states and what the number looks like comparing to S.Korean.

### Data Source
We get the testing date from [Covid Tracking Project](https://covidtracking.com/api/) and the US population by states
from [US Census Bureau](https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-total.html). Please be
aware that not all states report the number of testing cases with the same quality. Please refer to the data source
for the data quality assessment.

### Where to contribute
Code can be found on [Github](https://github.com/DigitalPig/covid-19-testing).

Copyright 2020 by Zhenqing Li

"""


app.layout = html.Div(
    [
        dcc.Markdown(introduction),
        html.Label("Select States", style={"fontWeight": "bold"}),
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
        title="COVID-19 Testing Conducted per Capita",
        xaxis_title="Date",
        yaxis_title="Number of Tests per Million People",
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
