import numpy as np
import pandas as pd
import json
import plotly.express as px
from climate_health_simulations.simulator.ClimateData import ClimateData


class ClimateHealth:
    def __init__(self, climate_data: ClimateData, disease_cases: np.ndarray, max_lag: int, n_time_points_train: int):
        self.climate_data = climate_data
        self.disease_cases = disease_cases
        self.max_lag = max_lag
        self.n_time_points_train = n_time_points_train

    def get_data(self):
        if len(self.disease_cases) != len(self.climate_data.rainfall):
            self.disease_cases = np.insert(self.disease_cases, 0, 0)
        df = pd.DataFrame({'time_period': self.climate_data.season,
                           'rainfall': self.climate_data.rainfall,
                           'temperature': self.climate_data.temperature,
                           'disease_cases': self.disease_cases,
                           'population': self.climate_data.population})
        df.loc[:(self.max_lag - 1), 'disease_cases'] = None
        return df

    def plot_data(self, output_path=None, config_dict=None):
        df = self.get_data()
        df = df.drop(columns=['time_period', 'population'])
        df = df.reset_index().melt(id_vars='index', var_name='variable', value_name='value')
        df = df.rename(columns={'index': 'Month'})
        fig = px.line(df, x='Month', title='Climate and Health Data', facet_row='variable', y='value')
        fig.update_yaxes(matches=None)
        for i, var_name in enumerate(np.flip(df['variable'].unique())):
            fig.update_yaxes(title_text=var_name, row=i + 1)
        for annotation in fig['layout']['annotations']:
            annotation['text'] = ''

        # --- Add vertical line at n_time_points_train + 0.5 ---
        train_test_split = self.n_time_points_train + 0.5
        n_vars = len(df['variable'].unique())

        for row in range(1, n_vars + 1):
            fig.add_vline(x=train_test_split, line_width=2, line_dash="dash", line_color="red", row=row, col=1)

        if config_dict is not None:
            fig = self._print_config_on_plot(config_dict, fig)
        if output_path:
            fig.write_html(output_path)
        else:
            fig.show()

    def _print_config_on_plot(self, config_dict, fig):
        config_str = json.dumps(config_dict, indent=2)
        fig.add_annotation(
            x=0.05,  # Left position (5% from left)
            y=0.95,  # Top position (95% from bottom)
            xref="paper",
            yref="paper",
            text=f"<b>Configuration:</b>\n<pre>{config_str}</pre>",
            showarrow=False,
            align="left",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#ffffff"
            ),
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#2d3436"
        )
        fig.update_layout(margin=dict(l=150, r=20, t=40, b=20))
        return fig

    def save_data(self, output_path):
        df = self.get_data()
        df.to_csv(output_path, index=False)
