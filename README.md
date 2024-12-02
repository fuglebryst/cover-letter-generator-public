# 📝 Cover Letter Generator

> An AI-powered platform that generates personalized cover letters and matches users with relevant job opportunities.

## 📑 Table of Contents
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Required Secrets](#-required-secrets)
- [Architecture](#️-architecture)
- [Deployment](#-deployment)
- [Dependencies](#-dependencies)
- [Configuration](#-configuration)
- [Development Guidelines](#-development-guidelines)
- [Troubleshooting](#-troubleshooting)
- [Resources](#-resources)
- [Advanced Features](#-advanced-features)

## ✨ About
The Cover Letter Generator is a cutting-edge application that automates the tedious process of writing cover letters and matching users with relevant job opportunities. It utilizes AI (GPT-4), natural language processing, and cloud-based infrastructure to deliver a seamless experience.

1. **Smart Cover Letter Generation**
   - Upload your CV
   - Provide a Finn.no job listing URL
   - Get an AI-tailored cover letter instantly
   - Download as Word or receive via email

2. **Automated Job Matching**
   - Upload your CV and preferences
   - Set location filters
   - Receive matched jobs from the last 7 days
   - Get personalized cover letters by email for top matches

## ✨ Features
- **AI-Powered Cover Letters**: Tailored to specific job descriptions using GPT-4
- **Job Matching System**: Matches CVs to relevant jobs using semantic embeddings
- **Location-Based Filtering**: Support for all Norwegian counties and municipalities
- **Email Automation**: Sends personalized cover letters directly to your inbox

## 🛠️ Technology Stack

### AI & Machine Learning
- **OpenAI GPT-4**: Advanced language model for generating personalized cover letters
- **Text Embeddings**: Semantic job matching using OpenAI embeddings
- **Document Parsing**: Intelligent handling of CVs and job descriptions

### Infrastructure & Cloud
- **Azure Cloud Services**: Leveraging multiple Azure services for a scalable, serverless architecture
- **Infrastructure as Code (IaC)**: Using Bicep for automated, version-controlled infrastructure deployment
- **CI/CD**: Automated deployment pipeline using GitHub Actions
- **Serverless Computing**: Azure Functions with Python runtime
- **Static Web Hosting**: Azure Static Web Apps for hosting the frontend React application

### Backend Technologies
- **Python 3.11**: Core backend programming language
- **Azure Functions**: Serverless compute service
- **Azure Cosmos DB**: NoSQL database for job data
- **Azure Service Bus**: Message queue for asynchronous processing
- **Azure Blob Storage**: Document and file storage

### Frontend Technologies
- **React 18+**: Modern frontend framework
- **TypeScript**: Type-safe frontend development
- **Azure Static Web Apps**: Hosting and automatic deployment
- **Modern CSS**: Responsive design with CSS modules

### DevOps & Tools
- **GitHub Actions**: CI/CD pipeline automation
- **Azure CLI**: Command-line management of Azure resources
- **VS Code**: Primary development environment with Azure extensions
- **ESLint & Prettier**: Code quality and formatting

## 🔐 Required Secrets

### GitHub Repository Secrets
The following secrets must be configured in your GitHub repository settings:

```
# Azure Configuration
AZURE_CREDENTIALS          # Service Principal credentials JSON
AZURE_SUBSCRIPTION        # Azure Subscription ID
AZURE_RG                 # Azure Resource Group name

# API Keys
OPENAI_API_KEY           # OpenAI API key for GPT-4 and embeddings

# SMTP Configuration (for email notifications)
SMTP_PASSWORD           # SMTP password (e.g., Gmail App Password)
SMTP_USERNAME          # SMTP username (your email)
SMTP_SERVER            # SMTP server (default: smtp.gmail.com)
```

### Obtaining Required Credentials

1. **Azure Credentials**:
   ```bash
   # Login to Azure
   az login

   # Create Service Principal and get credentials
   az ad sp create-for-rbac --name "CoverLetterApp" --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
     --sdk-auth
   ```
   Save the output JSON as `AZURE_CREDENTIALS` in GitHub secrets.

2. **OpenAI API Key**:
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Create an API key in your account settings
   - Save as `OPENAI_API_KEY` in GitHub secrets

3. **SMTP Configuration**:
   - For Gmail:
     1. Enable 2-factor authentication
     2. Generate an App Password
     3. Use this as `SMTP_PASSWORD`

## 🏗️ Architecture

The application uses several Azure services:
- Azure Functions (Python)
- Azure Cosmos DB
- Azure Service Bus
- Azure Blob Storage
- Azure Static Web Apps

### Function Apps
1. **generate_cover_letter**: HTTP trigger for generating cover letters
2. **enqueue_request**: HTTP trigger that queues job matching requests
3. **process_task**: Service Bus trigger for processing queued tasks from 'job-matching-queue'
4. **scrape_jobs**: Timer trigger for job scraping
5. **precompute_job_embeddings**: Queue trigger for processing scraped jobs

## 🚀 Deployment

### Prerequisites
- Python 3.11
- Azure Functions Core Tools
- Azure CLI
- Visual Studio Code with Azure Functions extension

### GitHub Actions Deployment
The project uses GitHub Actions for automated deployment. The workflow:
1. Deploys Azure infrastructure using Bicep
2. Deploys the Static Web App
3. Installs Python dependencies
4. Deploys the Function App

Key workflow file: `.github/workflows/deploy-infrastructure.yml`

### 💻 Local Development

1. **Clone and Install**
   ```bash
   git clone https://github.com/yourusername/cover-letter-generator
   cd cover-letter-generator
   python -m venv .venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Configure Local Settings**
   ```bash
   cp local.settings.example.json local.settings.json
   # Edit local.settings.json with your values
   ```

3. **Run the Project**
   ```bash
   func start
   ```

## 📦 Dependencies

The application uses several Python packages:

### Core Azure Packages
- azure-functions
- azure-cosmos
- azure-storage-blob
- azure-servicebus
- azure-identity
- azure-keyvault-secrets

### Document Processing
- docx2txt
- python-docx
- pypdf

### AI/ML
- openai
- scikit-learn
- numpy

### Web/HTTP
- aiohttp
- requests
- beautifulsoup4

## 🔧 Configuration

### Function Configuration
The `host.json` file contains important settings:
- Function timeout: 10 minutes
- Queue settings
- Cosmos DB connection settings

### Infrastructure
Infrastructure is defined using Bicep templates that deploy:
- Function App with Linux hosting
- Cosmos DB account
- Service Bus namespace
- Storage account
- Application Insights

### Post-Deployment

1. **Verify Deployment**:
   - Check Azure Portal for resources
   - Test frontend URL
   - Monitor GitHub Actions logs

2. **Configure Custom Domain** (optional):
   ```bash
   # First, validate domain ownership by adding the required DNS records
   az staticwebapp hostname show --name YourStaticWebApp --hostname your-domain.com

   # After DNS validation, bind the custom domain
   az staticwebapp hostname set \
     --name YourStaticWebApp \
     --hostname your-domain.com
   ```

   You'll need to:
   1. Add the validation DNS records to your domain provider
   2. Wait for DNS propagation
   3. Run the hostname set command

3. **Monitor Application**:
   - Set up Azure Application Insights alerts
   - Check Function App logs
   - Monitor Cosmos DB performance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.