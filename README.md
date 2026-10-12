# Google Cloud Skills Boost Notes

![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Labs](https://img.shields.io/badge/challenge_labs-19-34A853)

My study notes and reference solutions for **Google Cloud Skills Boost challenge labs**, organised by domain. Each lab folder has an overview, the services involved, a step-by-step solution and notes on deprecated commands.

These labs were my hands-on preparation for the **Associate Cloud Engineer** and **Professional Cloud Architect** certifications.

> 🎮 Looking for current **Arcade** games and trivia? See [Google-Cloud-Challenge-Lab-Solutions-Latest](https://github.com/codewithgarry/Google-Cloud-Challenge-Lab-Solutions-Latest).

## 📚 Labs by domain

### 🌐 Compute & Networking

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP313 | [Create and Manage Cloud Resources](compute-networking/gsp313-create-and-manage-cloud-resources/) | Compute Engine, GKE, HTTP Load Balancing |
| GSP322 | [Build and Secure Networks in Google Cloud](compute-networking/gsp322-build-and-secure-networks/) | VPC firewall rules, IAP, bastion host |
| GSP321 | [Set Up and Configure a Cloud Environment](compute-networking/gsp321-set-up-and-configure-a-cloud-environment/) | VPC, Deployment Manager, Cloud SQL, GKE |
| GSP314 | [Deploy and Manage Cloud Environments](compute-networking/gsp314-deploy-and-manage-cloud-environments/) | Deployment Manager, GKE, Monitoring, Spinnaker |

### 🧱 Infrastructure as Code

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP302 | [Configure a Firewall and a Startup Script with Deployment Manager](infrastructure-as-code/gsp302-firewall-and-startup-script-with-deployment-manager/) | Deployment Manager, Jinja templates |

### ☸️ Kubernetes (GKE)

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP304 | [Build and Deploy a Docker Image to a Kubernetes Cluster](kubernetes/gsp304-build-and-deploy-docker-image-to-gke/) | Cloud Build, Container Registry, GKE |
| GSP318 | [Deploy to Kubernetes in Google Cloud](kubernetes/gsp318-deploy-to-kubernetes-in-google-cloud/) | Docker, GKE, Jenkins CI/CD |
| GSP319 | [Build a Website on Google Cloud](kubernetes/gsp319-build-a-website-on-google-cloud/) | GKE, microservices, Cloud Build |
| GSP335 | [Secure Workloads in Google Kubernetes Engine](kubernetes/gsp335-secure-workloads-in-gke/) | Network policies, Binary Authorization, cert-manager |

### 🔐 Security & IAM

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP342 | [Ensure Access & Identity in Google Cloud](security-iam/gsp342-ensure-access-and-identity/) | Custom IAM roles, service accounts, private GKE |

### 📊 Data & BigQuery

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP340 | [Build and Optimize Data Warehouses with BigQuery](data-bigquery/gsp340-build-and-optimize-data-warehouses/) | Partitioned tables, STRUCT, DML |
| GSP327 | [Engineer Data in Google Cloud](data-bigquery/gsp327-engineer-data-in-google-cloud/) | BigQuery ML, TRANSFORM |
| GSP341 | [Create ML Models with BigQuery ML](data-bigquery/gsp341-create-ml-models-with-bigquery-ml/) | BigQuery ML regression, evaluation |
| GSP787 | [Insights from Data with BigQuery](data-bigquery/gsp787-insights-from-data-with-bigquery/) | CTEs, window functions |
| — | [Exploring Cryptocurrency Public Datasets in BigQuery](data-bigquery/exploring-cryptocurrency-public-datasets/) | Bitcoin public dataset, UNNEST |

### 🤖 Machine Learning & AI

| Lab | Challenge lab | Key services |
|---|---|---|
| GSP329 | [Integrate with Machine Learning APIs](ml-ai/gsp329-integrate-with-machine-learning-apis/) | Vision API, Translation API, Python |
| GSP311 | [Automate Interactions with Contact Center AI](ml-ai/gsp311-automate-interactions-with-contact-center-ai/) | Speech-to-Text, Dataflow, DLP |
| GSP323 | [Perform Foundational Data, ML, and AI Tasks](ml-ai/gsp323-perform-foundational-data-ml-and-ai-tasks/) | Natural Language, Speech, Video Intelligence APIs |
| GSP324 | [Explore Machine Learning Models with Explainable AI](ml-ai/gsp324-explore-ml-models-with-explainable-ai/) | TensorFlow, What-If Tool |
## 🧭 How to use these notes

1. Try the lab on your own first.
2. Open the matching folder when you are stuck, or afterwards to compare approaches.
3. Replace placeholder values with the ones from **your** lab session. Names, zones and ports change every time.

Some labs date from 2020 and 2021. Where Google has since retired a feature, such as Deployment Manager, AI Platform or PodSecurityPolicy, the lab's README has a **Version notes** section with the modern replacement.

## 📁 Structure

```text
<domain>/<lab-id>-<lab-name>/
├── README.md        # overview, services, solution, notes
└── <files>          # real config or code where the lab needs it (Jinja, YAML, Python)
```

## 📌 Disclaimer

Independent study notes. Not affiliated with or endorsed by Google.

## 👤 Author

**Girish Sharma** · Cloud & DevOps Engineer · [GitHub](https://github.com/codewithgarry) · [LinkedIn](https://www.linkedin.com/in/codewithgarry/)
