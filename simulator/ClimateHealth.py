import numpy as np
import pandas as pd
import plotly.express as px


class ClimateHealth:
    def __init__(self, rainfall, disease_cases, max_lag, temperature=None, season=None):
        self.rainfall = rainfall
        self.temperature = temperature
        self.season = season
        self.max_lag = max_lag
        self.disease_cases = disease_cases

    def get_data(self):
        if self.rainfall is not None:
            df = pd.DataFrame({'rainfall': self.rainfall, 'disease_cases': self.disease_cases})
        else:
            df = pd.DataFrame({'disease_cases': self.disease_cases})
        df.loc[:(self.max_lag - 1), 'disease_cases'] = None
        if self.temperature is not None:
            df.insert(1, 'temperature', self.temperature)
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
