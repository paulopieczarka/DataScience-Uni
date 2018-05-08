import numpy as np
import pandas as pd
data = pd.read_csv('base\\austin_crime.csv', names = ["address","census_tract","clearance_date","clearance_status","council_district_code","description","district","latitude","location","location_description","longitude","primary_type","timestamp","unique_key","x_coordinate","y_coordinate","year","zipcode"])
data = data.drop('address',axis=1)
data = data.drop('census_tract',axis=1)
data = data.drop("location",axis=1)
data = data.drop("location_description",axis=1)
data = data.drop("primary_type",axis=1)
data = data.drop("unique_key",axis=1)
data = data.drop("x_coordinate",axis=1)
data = data.drop("y_coordinate",axis=1)
data = data.drop("year",axis=1)
data = data.drop("zipcode",axis=1)
data.to_csv('base\\austin_crime01.csv', index=False, sep=',', encoding='utf-8')

