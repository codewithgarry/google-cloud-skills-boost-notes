"""Integrate with Machine Learning APIs: Challenge Lab (GSP329).

Reads every image in a Cloud Storage bucket, extracts text with the Vision API,
translates non-English text with the Translation API, saves the raw text back
to Cloud Storage and loads the results into BigQuery.

Usage:
    python3 analyze-images.py <PROJECT_ID> <BUCKET_NAME>

Target table: image_classification_dataset.image_text_detail
"""
import os
import sys

from google.cloud import bigquery, storage, translate_v2, vision

DATASET = "image_classification_dataset"
TABLE = "image_text_detail"


def check_environment() -> None:
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds:
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS is not set.")
    if not os.path.exists(creds):
        sys.exit(f"Credentials file not found: {creds}")
    if len(sys.argv) < 3:
        sys.exit(f"Usage: python3 {sys.argv[0]} <PROJECT_ID> <BUCKET_NAME>")


def main() -> None:
    check_environment()
    project_name, bucket_name = sys.argv[1], sys.argv[2]

    storage_client = storage.Client()
    bq_client = bigquery.Client(project=project_name)
    vision_client = vision.ImageAnnotatorClient()
    translate_client = translate_v2.Client()

    table = bq_client.get_table(f"{project_name}.{DATASET}.{TABLE}")
    bucket = storage_client.bucket(bucket_name)
    rows_for_bq = []

    print("Processing image files from GCS. This will take a few minutes...")

    for blob in bucket.list_blobs():
        if not blob.name.lower().endswith((".jpg", ".png")):
            continue

        # Detect text in the image
        image = vision.Image(content=blob.download_as_bytes())
        response = vision_client.text_detection(image=image)
        if not response.text_annotations:
            continue

        annotation = response.text_annotations[0]
        desc, locale = annotation.description, annotation.locale

        # Save the detected text next to the image as <name>.txt
        txt_name = blob.name.rsplit(".", 1)[0] + ".txt"
        bucket.blob(txt_name).upload_from_string(desc, content_type="text/plain")

        # Translate non-English text to English
        if locale == "en":
            translated_text = desc
        else:
            translated_text = translate_client.translate(desc, target_language="en")["translatedText"]
        print(translated_text)

        rows_for_bq.append((desc, locale, translated_text, blob.name))

    print("Writing Vision API image data to BigQuery...")
    errors = bq_client.insert_rows(table, rows_for_bq)
    assert errors == [], errors


if __name__ == "__main__":
    main()
