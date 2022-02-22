import json

from flask import Flask, make_response, jsonify
import pandas as pd
import requests
import io


app = Flask(__name__)


@app.route('/average_rainfall')
def average_rainfall():
    destination_url = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/UK.txt'
    s = requests.get(destination_url).content
    data = pd.read_csv(io.StringIO(s.decode('utf-8')), skiprows=5, sep='\s+', header=None)
    data.reset_index(drop=True)
    new_header = data.iloc[0]
    data = data[1:]
    data.columns = new_header
    data = data.dropna(how='any')
    month_data = data.loc[:, "jan":"dec"]
    yearly_annual_rainfall = []
    for i, row in data.iterrows():
        yearly_annual_rainfall.append(json.loads(row[['year', 'ann']].to_json()))

    summer_max = data['sum'].astype(float).max()
    summer_min = data['sum'].astype(float).min()
    highest_max_rainfall = month_data.astype(float).max()
    lowest_max_rainfall = month_data.astype(float).min()

    return make_response(jsonify({"Maximum rainfall according to month": yearly_annual_rainfall,
                                  "Monthly rainfall for all years": json.loads(month_data.to_json()),
                                  "highest maximum rainfall monthly": json.loads(highest_max_rainfall.to_json()),
                                  "lowest maximum rainfall monthly": json.loads(lowest_max_rainfall.to_json()),
                                  "maximum rainfall in summer": summer_max,
                                  "minimum rainfall in summer": summer_min}))


if __name__ == "__main__":
    app.run()
