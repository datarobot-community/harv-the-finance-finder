import os
import sys
import json
import requests
from dotenv import load_dotenv
import datarobot as dr
import csv

load_dotenv()

DR_API_KEY = os.environ["DATAROBOT_API_KEY"]
DR_API_URL = os.environ["DATAROBOT_URL"]
ENDPOINT = DR_API_URL+"/api/v2"
# TODO: copy this in from previous step - or from DR GUI
deployment_id = 'YOUR_DEPLOYMENT_ID' 

# Getting prediction server using the DR Python SDK. This shouldn't change often, so you could store it in an environment variable
dr.Client(token=DR_API_KEY, endpoint=ENDPOINT)
prediction_server = dr.PredictionServer.list()[0]

prediction_server_url = prediction_server.url
datarobot_key = prediction_server.datarobot_key # This is only needed for Cloud / Self Service DataRobot deployments

all_quotes_filename = 'data/stock_quotes_all.csv'

headers = {
    'Content-Type': 'text/plain; charset=UTF-8', 
    'Authorization': f'Bearer {DR_API_KEY}',
    'datarobot-key': datarobot_key
}

url = f'{prediction_server_url}/predApi/v1.0/deployments/{deployment_id}/predictions?passthroughColumns=symbol'
data = open(all_quotes_filename, 'rb').read()
data_size = sys.getsizeof(data) # This type of prediction/scoring is limited to 50MB data upload. For bigger requests use Batch Prediction API

predictions_response = requests.post(
        url,
        data=data,
        headers=headers,
)

predictions = predictions_response.json()['data']

# Transform predictions into a csv of the format:
# symbol, esg_category
# Where symbol is a vallue passed through from the prediction request

esg_categories = [['symbol', 'esg_category']]
for prediction in predictions:
    symbol = prediction['passthroughValues']['symbol']
    value = int(prediction['prediction'])

    esg_entry = [symbol, value]
    esg_categories.append(esg_entry)

# Write the file
with open('data/stocks_esg_scores.csv', mode='w') as out_csv:
    csv_writer = csv.writer(out_csv)
    csv_writer.writerows(esg_categories)
