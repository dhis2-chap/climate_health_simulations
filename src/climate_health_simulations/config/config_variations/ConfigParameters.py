
class ConfigParameters:
    RAIN_FLAGS = {
        'is_realistic': [False, True],
        'is_season_dependent': [False, True]
    }

    TEMPERATURE_FLAGS = {
        'is_realistic': [False, True],
        'is_season_dependent': [False, True]
    }

    AUTOREGRESSIVE_OPTIONS = [False, True]
    EXPLANATORY_COMBINATIONS = [
        [],
        ['rain'],
        ['temperature'],
        ['season'],
        ['rain', 'temperature'],
        ['rain', 'season'],
        ['temperature', 'season'],
        ['rain', 'temperature', 'season']
    ]
    LAG_OPTIONS = [3]
