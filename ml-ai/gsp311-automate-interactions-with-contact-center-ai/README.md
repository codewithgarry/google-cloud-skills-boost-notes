# Automate Interactions with Contact Center AI: Challenge Lab (GSP311)

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Lab](https://img.shields.io/badge/Lab-GSP311-34A853)
![Dataflow](https://img.shields.io/badge/Dataflow-4285F4?logo=googlecloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

Reference solution for the Google Cloud challenge lab **Automate Interactions with Contact Center AI** (GSP311).

## 📖 Overview

You deploy Google's **Speech Analysis Framework** for call-center recordings. When an audio file lands in Cloud Storage, a Cloud Function starts a Speech-to-Text job. Pub/Sub hands the result to a Dataflow pipeline, which enriches it with Natural Language API sentiment and entities and writes it to BigQuery. Finally, Cloud DLP scans the transcripts for sensitive data.

## 🏗️ Architecture

```text
Audio file ──► Cloud Storage ──► Cloud Function ──► Speech-to-Text
                                                        │
                                   Pub/Sub ◄────────────┘
                                      │
                                   Dataflow ──► Natural Language API ──► BigQuery ──► Cloud DLP scan
```

## 🧰 Services used

Cloud Storage · Cloud Functions · Speech-to-Text · Pub/Sub · Dataflow (Apache Beam) · Natural Language API · BigQuery · Cloud DLP

## ✅ Prerequisites

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export AUDIO_BUCKET="<audio-bucket-name>"
export STAGING_BUCKET="<staging-bucket-name>"
export TOPIC="<topic-name>"

git clone https://github.com/GoogleCloudPlatform/dataflow-contact-center-speech-analysis.git
cd dataflow-contact-center-speech-analysis
```

## 🚀 Solution

### Task 1: Create the audio upload bucket

```bash
gsutil mb -l $REGION gs://$AUDIO_BUCKET/
```

### Task 2: Deploy the Cloud Function

```bash
cd saf-longrun-job-func
gcloud functions deploy safLongRunJobFunc \
  --no-gen2 \
  --runtime nodejs20 \
  --region $REGION \
  --trigger-resource $AUDIO_BUCKET \
  --trigger-event google.storage.object.finalize
cd ..
```

### Task 3: Create the BigQuery dataset

```bash
bq mk saf
```

### Task 4: Create the Pub/Sub topic

```bash
gcloud pubsub topics create $TOPIC
```

### Task 5: Create the staging bucket

```bash
gsutil mb -l $REGION gs://$STAGING_BUCKET/
```

Create a folder named `DFaudio` in that bucket from the console.

### Task 6: Deploy the Dataflow pipeline

```bash
cd saf-longrun-job-dataflow
python3 -m venv env && source env/bin/activate
pip install 'apache-beam[gcp]' dateparser

python saflongrunjobdataflow.py \
  --project=$PROJECT_ID \
  --region=$REGION \
  --input_topic=projects/$PROJECT_ID/topics/$TOPIC \
  --runner=DataflowRunner \
  --temp_location=gs://$STAGING_BUCKET/DFaudio \
  --output_bigquery=$PROJECT_ID:saf.transcripts \
  --requirements_file=requirements.txt
```

### Task 7: Upload sample audio files

The object metadata tells the function how to process each file.

```bash
for FILE in speech_commercial_mono.flac speech_commercial_stereo.wav; do
  STEREO=$([[ $FILE == *stereo* ]] && echo true || echo false)
  gsutil \
    -h x-goog-meta-callid:1234567 \
    -h x-goog-meta-stereo:$STEREO \
    -h x-goog-meta-pubsubtopicname:$TOPIC \
    -h x-goog-meta-year:2019 \
    -h x-goog-meta-month:11 \
    -h x-goog-meta-day:06 \
    -h x-goog-meta-starttime:1116 \
    cp gs://qwiklabs-bucket-gsp311/$FILE gs://$AUDIO_BUCKET/
done
```

Wait until rows appear in `saf.transcripts`. This can take several minutes.

### Task 8: Run a Data Loss Prevention job

```sql
SELECT *
FROM (
  SELECT entities.name, entities.type, COUNT(entities.name) AS count
  FROM saf.transcripts, UNNEST(entities) AS entities
  GROUP BY entities.name, entities.type
  ORDER BY count ASC
)
WHERE count > 5;
```

Save the results to a new BigQuery table. Then, on that table, choose **Export → Scan with DLP**.

## 🔎 Version notes

The original lab used the `nodejs8` runtime, which is decommissioned. Use a supported runtime such as `nodejs20`.

---

## ⚠️ Notes

- Resource names, zones, regions and ports are generated per lab session. Always use the values shown in **your** lab instructions.
- These steps were written when the lab was live. Google revises labs over time, so the current version may differ.

## 📌 Disclaimer

This repository is a study reference. Attempt the lab on your own first, then compare approaches. It is not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
