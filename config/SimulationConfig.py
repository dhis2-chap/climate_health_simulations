class SimulationConfig:
    def __init__(self, use_interactions=False, non_linear_effects=False,
                 use_lag=False, autoregressive=False, realistic_data=False):
        self.use_interactions = use_interactions
        self.non_linear_effects = non_linear_effects
        self.use_lag = use_lag
        self.autoregressive = autoregressive
        self.realistic_data = realistic_data
