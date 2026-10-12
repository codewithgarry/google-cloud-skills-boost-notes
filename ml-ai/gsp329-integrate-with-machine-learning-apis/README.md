# Integrate with Machine Learning APIs: Challenge Lab (GSP329)

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Lab](https://img.shields.io/badge/Lab-GSP329-34A853)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Vision API](https://img.shields.io/badge/Cloud_Vision_API-4285F4?logo=googlecloud&logoColor=white)

Reference solution for the Google Cloud Skills Boost challenge lab **Integrate with Machine Learning APIs** (GSP329).

## 📖 Overview

A Python pipeline that turns images of signs into searchable, translated text:

```text
Cloud Storage images ──► Vision API (OCR) ──► Translation API (to English) ──► BigQuery
                                    └──► <image>.txt saved back to Cloud Storage
```

## 🧰 Services used

Cloud Vision API · Cloud Translation API · Cloud Storage · BigQuery · IAM service accounts · Python client libraries

## 📁 Repository structure

```text
.
├── README.md
└── analyze-images.py   # completed lab script
```

## 🚀 Solution

### Tasks 1 and 2: Create a service account with the required roles

```bash
export PROJECT_ID=$(gcloud config get-value project)
export SA_NAME=challenge
export SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME

for ROLE in roles/bigquery.admin roles/storage.admin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" --role="$ROLE"
done

gcloud iam service-accounts keys create sa-key.json --iam-account $SA_EMAIL
export GOOGLE_APPLICATION_CREDENTIALS=${PWD}/sa-key.json
```

### Task 3: Complete and run the script

Replace the lab's starter file with [`analyze-images.py`](analyze-images.py) from this repo, then run it against the lab bucket:

```bash
python3 analyze-images.py $PROJECT_ID $PROJECT_ID
```

### Task 4: Verify the results in BigQuery

```sql
SELECT locale, COUNT(locale) AS lcount
FROM image_classification_dataset.image_text_detail
GROUP BY locale
ORDER BY lcount DESC;
```

## 🔐 Security note

Service account keys are long-lived credentials. Delete `sa-key.json` when you finish the lab. In real projects, prefer Workload Identity or attached service accounts over key files.

---

## ⚠️ Notes

- Resource names, zones, regions and ports are generated per lab session. Always use the values shown in **your** lab instructions.
- These steps were written when the lab was live. Google revises labs over time, so the current version may differ.

## 📌 Disclaimer

This repository is a study reference. Attempt the lab on your own first, then compare approaches. It is not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
