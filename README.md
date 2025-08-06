# Palmer Penguins on Vertex AI

This project trains a simple RandomForest classifier on the [Palmer Penguins dataset](https://allisonhorst.github.io/palmerpenguins/) and deploys it to Google Cloud Vertex AI.

## Prerequisites

- Python 3.10+
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- A Google Cloud project with billing enabled.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas scikit-learn seaborn google-cloud-aiplatform
```

Authenticate and configure gcloud:

```bash
gcloud init
gcloud auth login
gcloud config set project <YOUR_PROJECT_ID>
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com
```

Create a Cloud Storage bucket to hold data and model artifacts:

```bash
gsutil mb gs://<YOUR_BUCKET_NAME>
```

Replace `<YOUR_PROJECT_ID>` and `<YOUR_BUCKET_NAME>` with your details.

## Data Processing

Download and clean the dataset:

```bash
python process_data.py
```

Upload the training data to the bucket:

```bash
gsutil cp data/train.csv gs://<YOUR_BUCKET_NAME>/penguins/data/
```

## Training

Train the model locally:

```bash
python train.py
```

Upload the trained model artifact:

```bash
gsutil cp model/model.joblib gs://<YOUR_BUCKET_NAME>/penguins/model/
```

## Serving / Inference

Upload the model to Vertex AI:

```bash
python upload_model.py
```

Create an endpoint and deploy the model:

```bash
gcloud ai endpoints create \
  --project=<YOUR_PROJECT_ID> \
  --region=us-central1 \
  --display-name="penguins-endpoint"

gcloud ai models list --region=us-central1   # note the model ID

gcloud ai endpoints deploy-model <ENDPOINT_ID> \
  --project=<YOUR_PROJECT_ID> \
  --region=us-central1 \
  --model=<MODEL_ID> \
  --display-name="v1" \
  --traffic-split=0=100
```

Send a sample prediction:

```bash
gcloud ai endpoints predict <ENDPOINT_ID> \
  --region=us-central1 \
  --json-request=instances.json
```

## Monitoring (optional)

```bash
gcloud ai model-monitoring-jobs create \
  --region=us-central1 \
  --display-name="penguin-monitoring-job" \
  --endpoint=<ENDPOINT_ID> \
  --log-sample-rate=0.8 \
  --notification-channels=<YOUR_EMAIL@example.com> \
  --training-dataset="gs://<YOUR_BUCKET_NAME>/penguins/data/train.csv" \
  --target-field="species" \
  --feature-thresholds='{"bill_length_mm":0.1, "flipper_length_mm":0.1}'
```

## Cleanup

Delete the endpoint and models when finished to avoid charges:

```bash
gcloud ai endpoints delete <ENDPOINT_ID> --region=us-central1
gcloud ai models delete <MODEL_ID> --region=us-central1
gsutil rm -r gs://<YOUR_BUCKET_NAME>/penguins
```

