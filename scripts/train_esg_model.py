import os
import datarobot as dr
from datarobot.enums import TARGET_TYPE
from dotenv import load_dotenv

load_dotenv()

# Environment setup
DR_API_KEY = os.environ["DATAROBOT_API_KEY"]
DR_API_URL = os.environ["DATAROBOT_URL"]
ENDPOINT = DR_API_URL+"/api/v2"

dr.Client(token=DR_API_KEY, endpoint=ENDPOINT)

print("Uploading training dataset to DataRobot and starting to train models")
project = dr.Project.create(sourcedata='data/stock_quotes_esg_train.csv', project_name='Stock ESG ratings - categorical')

# Transform esg_category from integer into categorical feature 
project.create_type_transform_feature(
    "esg_category_categorical",  # new feature name
    "esg_category",       # parent name
    dr.enums.VARIABLE_TYPE_TRANSFORM.CATEGORICAL_INT
)

# This kicks off modeling - quick autopilot
project.set_target(
    target='esg_category_categorical',
    mode=dr.enums.AUTOPILOT_MODE.QUICK
)

print(f'Project with name {project.project_name} created. \n Project id is {project.id}.')
print("Starting autopilot for training models...")

# Time for a cup of tea or coffee - this might take ~15 mins
project.wait_for_autopilot()

print("Autopilot finished!")

recommendation = dr.ModelRecommendation.get(project.id)
recommended_model = recommendation.get_model()

print(f'Recommended model is {recommended_model}')
					
prediction_server_id = dr.PredictionServer.list()[0].id

deployment = dr.Deployment.create_from_learning_model(
      model_id = recommended_model.id, 
      label='Financial ESG model', 
      description='Model for scoring financial quote data',
      default_prediction_server_id=prediction_server_id
)

print(f'Deployment created: {deployment}, deployment id: {deployment.id}')
