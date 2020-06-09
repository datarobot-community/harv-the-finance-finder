import os
import datarobot as dr
from dotenv import load_dotenv

load_dotenv()

# Environment setup
DR_API_KEY = os.environ["DATAROBOT_API_KEY"]
DR_API_URL = os.environ["DATAROBOT_URL"]
ENDPOINT = DR_API_URL+"/api/v2"

dr.Client(token=DR_API_KEY, endpoint=ENDPOINT)

print("Uploading training dataset to DataRobot")
project = dr.Project.create('data/stock_quotes_esg_train.csv', project_name='Stock ESG ratings')

print(f'Project with name {project.project_name} created. \n Project id is {project.id}.')

print("Starting autopilot for training models...")
# project.set_target(target='esg_category', mode=dr.AUTOPILOT_MODE.FULL_AUTO)
project.set_target(target='esg_category', quickrun=True)

project.wait_for_autopilot()

print("Autopilot finished!")

top_model = project.get_models()[0]

print("Top performing model: ")
print(top_model)
print(top_model.id)
					
prediction_server_id = dr.PredictionServer.list()[0].id

deployment = dr.Deployment.create_from_learning_model(
      model_id = top_model.id, 
      label='Financial ESG model', 
      description='Model for scoring financial quote data',
      default_prediction_server_id=prediction_server_id
)

print(f'Deployment created: {deployment}')
