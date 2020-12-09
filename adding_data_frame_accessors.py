import vaex
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


@vaex.register_dataframe_accessor('scale')
class ScalingOps(object):
    def __init__(self, df):
        self.df = df
        self.time = None
        self.value = None
        self.column_name = None

    def sep_column(self):
        df = self.df.copy()
        self.column_name = df.get_column_names(strings=False)

        self.time = df[self.column_name[0]].tolist()
        self.value = df[self.column_name[1]].tolist()

    def mul(self, a):
        df = self.df.copy()
        for col in df.get_column_names(strings=False):
            if df[col].dtype:
                df[col] = df[col] * a
        return df

    @staticmethod
    def float_range(start, stop, step):
        r = start
        while r < stop:
            yield r
            r += step

    def fill_values(self):
        self.value = pd.Series(self.value).interpolate(method="linear", limit_direction='both')

    def extrapolate_data(self):
        pass

    def interpolate_data(self):
        interp = interp1d(self.time, self.value, kind="linear", bounds_error=False)  # Linear interpolation function

        sampled_time_object = self.float_range(1.0, 4.0, 0.5)
        self.time = [x for x in sampled_time_object]

        self.value = interp(self.time)

    def create_vaex_data_frame(self):
        # method for step by step
        self.sep_column()
        self.fill_values()
        self.interpolate_data()

        time = self.column_name[0]
        value = self.column_name[1]

        pandas_data_frame = pd.DataFrame(
            {time: self.time,
             value: self.value,

             })

        final_data_frame = vaex.from_pandas(pandas_data_frame)

        return final_data_frame


df_import = vaex.from_arrays(time=[1,2,3,4,56], value=[23, None, 12, 12, 11])
print(df_import)
# x_series = df_.y.tolist()
# print("............")
# print(x_series)
# print(type(x_series))
# value = pd.Series(x_series).interpolate(method="linear", limit_direction='both')
# print("++++",value)
# # asd = value.tolist()
# print(asd)
# df_ = vaex.from_arrays(y=value)
# print(df_)
# print(type(value))
# df_["new_col"] = value
# print(df_)
asd = df_import.scale.create_vaex_data_frame()
print(asd)




