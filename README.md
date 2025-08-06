# palmer_penguins

python3 -m venv venv
source venv/bin/activate
pip install pandas scikit-learn seaborn google-cloud-aiplatform
Instal gcloud https://cloud.google.com/sdk/docs/install

gcloud init
gcloud auth login
gcloud config set project robot-test-468201
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project=robot-test-468201

## Data Processing
python process_data.py
gsutil mb gs://test-datasets-ml
gsutil cp data/train.csv gs://test-datasets-ml/penguins/data/

## Training
python train.py
gsutil cp model/model.joblib gs://test-datasets-ml/penguins/model/

## Serving/Inference
python upload_model.py
View model in model registry https://console.cloud.google.com/vertex-ai/models?project=robot-test-468201
Create an endpoint
gcloud ai endpoints create \
  --project=robot-test-468201 \
  --region=us-central1 \
  --display-name="penguins-endpoint" Lets say the endpoint id is 6915984213804056576
  Deploy model to the endpoint. first get model id
  gcloud ai models list --region=us-central1 #lets say its 1999513572157161472
gcloud ai endpoints deploy-model 6915984213804056576 \
  --project=robot-test-468201 \
  --region=us-central1 \
  --model=1999513572157161472 \
  --display-name="v1" \
  --traffic-split=0=100
  
  Now test the model prediction using
  gcloud ai endpoints predict 6915984213804056576 \
  --region=us-central1 \
  --json-request=instances.json

  ## Monitoring
  gcloud ai model-monitoring-jobs create \
  --region=us-central1 \
  --display-name="penguin-monitoring-job" \
  --endpoint=YOUR_ENDPOINT_ID \
  --log-sample-rate=0.8 \
  --notification-channels=YOUR_EMAIL@example.com \
  --training-dataset="gs://test-datasets-ml/penguins/data/train.csv" \
  --target-field="species" \
  --feature-thresholds='{"bill_length_mm":0.1, "flipper_length_mm":0.1}'
