import vaex
import numpy as np
import pandas as pd

x = np.arange(2)
y = np.array([10, 20])
z = np.array(['dog', 'cat'])

df_numpy = vaex.from_arrays(x=[1, 2, 3, 4, 5], y=[5, None, 3, 2, 1])

print(df_numpy)


@vaex.register_function(on_expression=False)
def re_sample(df):
    df = df.fillna(value=-1, column_names=["y"])

    return df


df= df_numpy.func.re_sample("linear", df_numpy)
print(df)

