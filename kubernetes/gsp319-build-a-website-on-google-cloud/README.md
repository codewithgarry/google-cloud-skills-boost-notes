# Build a Website on Google Cloud: Challenge Lab (GSP319)

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Lab](https://img.shields.io/badge/Lab-GSP319-34A853)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)

Reference solution for the Google Cloud Skills Boost challenge lab **Build a Website on Google Cloud** (GSP319).

## 📖 Overview

You migrate the **FancyStore** e-commerce site from a monolith to microservices on GKE. The monolith is deployed first, then split into separate **orders**, **products** and **frontend** services, each with its own container image and load balancer.

## 🧰 Services used

Cloud Build · Container Registry · Google Kubernetes Engine · Node.js / React

## ✅ Prerequisites

```bash
export PROJECT_ID=$(gcloud config get-value project)
gcloud config set compute/zone us-central1-a
gcloud services enable cloudbuild.googleapis.com container.googleapis.com
```

## 🚀 Solution

### Task 1: Build the monolith container

```bash
cd ~
git clone https://github.com/googlecodelabs/monolith-to-microservices.git
cd ~/monolith-to-microservices && ./setup.sh

cd ~/monolith-to-microservices/monolith
gcloud builds submit --tag gcr.io/$PROJECT_ID/fancytest:1.0.0 .
```

### Task 2: Create the cluster and deploy the monolith

```bash
gcloud container clusters create fancy-cluster --num-nodes 3

kubectl create deployment fancytest --image=gcr.io/$PROJECT_ID/fancytest:1.0.0
kubectl expose deployment fancytest --type=LoadBalancer --port 80 --target-port 8080
```

### Task 3: Containerize the microservices

```bash
cd ~/monolith-to-microservices/microservices/src/orders
gcloud builds submit --tag gcr.io/$PROJECT_ID/orders:1.0.0 .

cd ~/monolith-to-microservices/microservices/src/products
gcloud builds submit --tag gcr.io/$PROJECT_ID/products:1.0.0 .
```

### Task 4: Deploy the microservices

```bash
kubectl create deployment orders --image=gcr.io/$PROJECT_ID/orders:1.0.0
kubectl expose deployment orders --type=LoadBalancer --port 80 --target-port 8081

kubectl create deployment products --image=gcr.io/$PROJECT_ID/products:1.0.0
kubectl expose deployment products --type=LoadBalancer --port 80 --target-port 8082

kubectl get services --watch   # note the EXTERNAL-IPs of orders and products
```

### Task 5: Point the frontend at the new services

Edit `~/monolith-to-microservices/react-app/.env` and replace the API URLs with the external IPs from Task 4:

```ini
REACT_APP_ORDERS_URL=http://<ORDERS_IP>/api/orders
REACT_APP_PRODUCTS_URL=http://<PRODUCTS_IP>/api/products
```

Rebuild the React app so the frontend picks up the change:

```bash
cd ~/monolith-to-microservices/react-app
npm run build
```

### Task 6: Containerize the frontend

```bash
cd ~/monolith-to-microservices/microservices/src/frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/frontend:1.0.0 .
```

### Task 7: Deploy the frontend

```bash
kubectl create deployment frontend --image=gcr.io/$PROJECT_ID/frontend:1.0.0
kubectl expose deployment frontend --type=LoadBalancer --port 80 --target-port 8080
```

## 🏗️ Architecture

```text
                ┌──────────────► orders   (:8081)
Browser ──► frontend (:8080)
                └──────────────► products (:8082)
```

---

## ⚠️ Notes

- Resource names, zones, regions and ports are generated per lab session. Always use the values shown in **your** lab instructions.
- These steps were written when the lab was live. Google revises labs over time, so the current version may differ.

## 📌 Disclaimer

This repository is a study reference. Attempt the lab on your own first, then compare approaches. It is not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
