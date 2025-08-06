from google.cloud import aiplatform

# --- Configuration ---
PROJECT_ID = "robot-test-468201"
REGION = "us-central1"
BUCKET_NAME = "gs://test-datasets-ml" # Use your bucket name here
MODEL_DISPLAY_NAME = "penguin-classifier-sdk"

# --- The GCS path to your saved model artifact ---
# This path is inside your bucket
ARTIFACT_URI = f"{BUCKET_NAME}/penguins/model/"

# --- The pre-built container image for scikit-learn predictions ---
SERVING_CONTAINER_URI = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"


# 1. Initialize the Vertex AI SDK
# The staging_bucket is where Vertex AI can store temporary files.
aiplatform.init(project=PROJECT_ID, location=REGION, staging_bucket=BUCKET_NAME)


# 2. Upload the model to the Vertex AI Model Registry
print(f"Uploading model '{MODEL_DISPLAY_NAME}' from {ARTIFACT_URI}...")

model = aiplatform.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    artifact_uri=ARTIFACT_URI,
    serving_container_image_uri=SERVING_CONTAINER_URI,
)

# 3. Print the results
print("Model upload complete.")
print(f"Display Name: {model.display_name}")
print(f"Resource Name: {model.resource_name}")