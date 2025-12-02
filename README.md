🚀 Student Performance Prediction – MLOps Pipeline

This project demonstrates a full end-to-end MLOps workflow for deploying a machine-learning model using:

Python + Flask

Docker containerization

AWS ECR (Elastic Container Registry)

AWS EC2 (Compute instance for deployment)

GitHub Actions CI/CD pipeline

Automated image building and deployment

The ML model predicts student performance based on input attributes. The entire project is productionized using modern DevOps practices.

📌 Project Overview

This project includes:

✔️ 1. Machine Learning Pipeline

Exploratory Data Analysis (EDA)

Feature engineering

Model training with GridSearchCV

Saving best model using pickle/dill

Flask API for inference

✔️ 2. Containerization (Docker)

The project is packaged into a Docker image:

Uses Python 3.12 slim image

Installs all dependencies via requirements.txt

Runs the Flask application (application.py) as the entrypoint

✔️ 3. AWS Cloud Deployment

The final Docker image is pushed to:

AWS ECR (Docker registry)

AWS EC2 instance, where the container runs continuously

✔️ 4. CI/CD Pipeline (GitHub Actions)

Automatic steps on every push to main:

Run tests / linting

Build Docker image

Push image to AWS ECR

SSH into EC2 through a self-hosted runner

Pull the latest image

Restart the container with the updated version

This ensures zero-touch deployment — every code change updates production automatically.

🧱 Project Structure
MLOps-Project/
│
├── application.py           # Flask app for prediction
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── src/                     # ML training pipeline & utils
│   ├── components/
│   ├── pipeline/
│   ├── model.py
│   └── utils.py
├── artifacts/               # Saved models, logs, data
│
├── .github/
│   └── workflows/
│       └── deploy.yaml      # CI/CD pipeline
│
└── README.md

🐳 Docker Setup
Build the image locally:
docker build -t studentperformance-app .

Run the container:
docker run -p 8000:8000 studentperformance-app

☁️ AWS Deployment
1. Push Docker Image to ECR

GitHub Actions automatically handles:

AWS authentication

ECR login

Docker build

Docker push

2. Pull & Run Image on EC2

The EC2 runner pulls latest image:

docker pull <aws_ecr_uri>/studentperformance-app:latest
docker run -d -p 8000:8000 studentperformance-app

🔄 CI/CD Pipeline (deploy.yaml)

Your GitHub Actions workflow:

Runs on every push to main

Performs CI checks

Builds the Docker image

Pushes to ECR

Connects to EC2 self-hosted runner

Deploys the latest container

This ensures true continuous integration & continuous deployment.

🛠️ Technologies Used
Machine Learning

Pandas, NumPy

Scikit-learn

Dill / Pickle

Backend

Python Flask

Jinja2 Templates

DevOps / MLOps

Docker

Docker Hub

AWS ECR

AWS EC2

GitHub Actions

Self-hosted runners

🧪 How to Use the Application

Go to:

http:// <EC2-public-ip> :8000


Enter student parameters → click Predict → see predicted performance.

🎯 Key Achievements

✔️ Fully automated ML deployment pipeline
✔️ Dockerized & cloud-ready application
✔️ CI/CD pipeline with GitHub Actions
✔️ AWS-based scalable inference system
✔️ Reproducible & production-grade MLOps workflow

🙌 Future Enhancements

Monitoring with Prometheus / Grafana

EKS (Kubernetes) deployment

Model drift detection

Auto retraining pipeline (Airflow / Prefect)
