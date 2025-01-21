from simulator.season.Season import Season


class SeasonGenerator:
    def create_season(self, name, start_date, end_date):
        return Season(name, start_date, end_date)