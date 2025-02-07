from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class IndependentVariable(BaseModel):
    type: str
    is_realistic: bool
    is_season_dependent: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def type_must_be_valid(cls, values):
        v = values.get('type')
        if v not in ('rain', 'temperature', 'season'):
            raise ValueError('type must be rain, temperature, or season')
        return values

    @model_validator(mode='after')
    def check_season_dependencies(self):
        if self.type == 'season' and self.is_season_dependent is not None:
            raise ValueError('season cannot have is_season_dependent attribute')
        if self.type != 'season' and self.is_realistic is None:
            raise ValueError('rain and temperature must have is_realistic attribute')
        if self.is_realistic and not self.is_season_dependent:
            raise ValueError('rain and temperature cannot be realistic and not season dependent')
        return self


class ExplanatoryVariable(BaseModel):
    type: str
    lag: Optional[int] = None

    @model_validator(mode='before')
    @classmethod
    def type_must_be_valid(cls, values):
        v = values.get('type')
        if v not in ('rain', 'temperature', 'season'):
            raise ValueError('type must be rain, temperature, or season')
        return values

    @model_validator(mode='after')
    def check_lag(self):
        if self.type == 'season' and self.lag is not None:
            raise ValueError('season cannot have lag attribute')
        return self


class DependentVariable(BaseModel):
    is_autoregressive: bool
    explanatory_variables: List[ExplanatoryVariable]
    population: int

    @model_validator(mode='before')
    @classmethod
    def population_must_be_int(cls, values):
        v = values.get('population')
        if v is not None and not isinstance(v, int):
            raise ValueError("population must be an integer in string format")
        return values


class Config(BaseModel):
    independent_variables: List[IndependentVariable]
    dependent_variable: DependentVariable
    n_time_points: int = Field(gt=0)

    def get_max_lag(self):
        max_lag = 0
        for exp_var in self.dependent_variable.explanatory_variables:
            if exp_var.lag is not None:
                max_lag = max(max_lag, exp_var.lag)
        return max_lag

    def get_independent_variable_properties(self, var_type):
        for var in self.independent_variables:
            if var.type == var_type:
                return var.is_realistic, var.is_season_dependent
        return None
