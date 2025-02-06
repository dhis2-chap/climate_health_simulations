import numpy as np
import pandas as pd
import plotly.express as px
from simulator.ClimateData import ClimateData


class ClimateHealth:
    def __init__(self, climate_data: ClimateData, disease_cases: np.ndarray, max_lag: int):
        self.climate_data = climate_data
        self.disease_cases = disease_cases
        self.max_lag = max_lag

    def get_data(self):
        if len(self.disease_cases) != len(self.climate_data.rainfall):
            self.disease_cases = np.insert(self.disease_cases, 0, 0)
        # print(len(self.disease_cases))
        # print(len(self.climate_data.rainfall))
        # print(len(self.climate_data.temperature))
        # print(len(self.climate_data.season))
        # print(len(self.climate_data.population))
        df = pd.DataFrame({'time_period': self.climate_data.season,
                           'rainfall': self.climate_data.rainfall,
                           'temperature': self.climate_data.temperature,
                           'disease_cases': self.disease_cases,
                           'population': self.climate_data.population})
        df.loc[:(self.max_lag - 1), 'disease_cases'] = None
        return df

    def plot_data(self):
        df = self.get_data()
        df = df.reset_index().melt(id_vars='index', var_name='variable', value_name='value')
        df = df.rename(columns={'index': 'Month'})
        fig = px.line(df, x='Month', title='Climate and Health Data', facet_row='variable', y='value')
        fig.update_yaxes(matches=None)
        for i, var_name in enumerate(np.flip(df['variable'].unique())):
            fig.update_yaxes(title_text=var_name, row=i + 1)
        for annotation in fig['layout']['annotations']:
            annotation['text'] = ''
        fig.show()
