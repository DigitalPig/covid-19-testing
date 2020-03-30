# COVID-19 Tests per Capita in Different States in US

App is [here](https://covid-19-testing-heroku18.herokuapp.com)

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

Copyright 2020 by Zhenqing Li
