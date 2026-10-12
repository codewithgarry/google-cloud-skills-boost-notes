# Ensure Access & Identity in Google Cloud: Challenge Lab (GSP342)

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Lab](https://img.shields.io/badge/Lab-GSP342-34A853)
![Topic](https://img.shields.io/badge/Topic-IAM_%26_Security-red)

Reference solution for the Google Cloud Skills Boost challenge lab **Ensure Access & Identity in Google Cloud** (GSP342).

## 📖 Overview

You apply **least privilege** to a private GKE cluster:

1. Create a custom IAM role with only the storage permissions needed.
2. Create a dedicated service account and bind only the required roles.
3. Create a private GKE cluster that uses that service account.
4. Deploy an app to the private cluster from an authorized jumphost.

## 🧰 Services used

IAM custom roles · Service accounts · Google Kubernetes Engine (private cluster) · Cloud Logging · Cloud Monitoring

## 📁 Repository structure

```text
.
├── README.md
└── role-definition.yaml   # custom role used in Task 1
```

## ✅ Prerequisites

```bash
export PROJECT_ID=$(gcloud config get-value project)
export ZONE="us-east1-b"
export SA_NAME="orca-private-cluster-sa"
export SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
```

## 🚀 Solution

### Task 1: Create a custom security role

```bash
gcloud iam roles create orca_storage_update \
  --project $PROJECT_ID \
  --file role-definition.yaml
```

### Task 2: Create a service account

```bash
gcloud iam service-accounts create $SA_NAME --display-name "Orca private cluster SA"
```

### Task 3: Bind the custom role and minimal monitoring roles

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member "serviceAccount:$SA_EMAIL" \
  --role "projects/$PROJECT_ID/roles/orca_storage_update"

for ROLE in roles/monitoring.viewer roles/monitoring.metricWriter roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member "serviceAccount:$SA_EMAIL" \
    --role "$ROLE"
done
```

### Task 4: Create a private GKE cluster

The control plane is reachable only from the jumphost (`192.168.10.2/32`).

```bash
gcloud container clusters create orca-test-cluster \
  --zone $ZONE \
  --num-nodes 1 \
  --network orca-build-vpc \
  --subnetwork orca-build-subnet \
  --service-account $SA_EMAIL \
  --enable-ip-alias \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr 172.16.0.64/28 \
  --enable-master-authorized-networks \
  --master-authorized-networks 192.168.10.2/32
```

### Task 5: Deploy an app from the jumphost

SSH to `orca-jumphost`, then run:

```bash
gcloud container clusters get-credentials orca-test-cluster \
  --internal-ip --zone us-east1-b --project <PROJECT_ID>

kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0
```

---

## ⚠️ Notes

- Resource names, zones, regions and ports are generated per lab session. Always use the values shown in **your** lab instructions.
- These steps were written when the lab was live. Google revises labs over time, so the current version may differ.

## 📌 Disclaimer

This repository is a study reference. Attempt the lab on your own first, then compare approaches. It is not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
