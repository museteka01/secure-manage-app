# 🚀 DevSecOps Project – Secure Manage App

A **production-style DevSecOps project** demonstrating secure API development, containerization, automated CI/CD pipelines, security scanning, testing, and infrastructure-as-code.

This project is built to showcase **real-world DevSecOps, Cloud, and Security skills** to recruiters and hiring managers.

---

## 🛡️ Project Overview

**Secure Manage App** is a containerized Python API connected to a PostgreSQL database, designed with **security, automation, and scalability** as first-class concerns.

The project demonstrates how modern DevSecOps teams:
- Secure application code
- Automate testing and security checks
- Enforce quality through CI/CD pipelines
- Deploy consistently using containers
- Manage infrastructure using code

---

## 🎓 Certifications

- 🏅 **Google Cybersecurity Professional Certificate**  
  👉 https://coursera.org/share/9875eee197686ac6fdcc162ea3ac1398

---

## ⚙️ Tech Stack

- **Backend:** Python (FastAPI-style / Flask-style architecture)
- **Database:** PostgreSQL
- **Containers:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Infrastructure as Code:** Terraform
- **Testing:** pytest
- **Code Quality:** flake8
- **Security Scanning:** bandit

---

## 🔐 DevSecOps & Security Practices

This project applies **real DevSecOps best practices**:

- 🔒 Secure database connections using environment variables
- 🧪 Automated unit testing with `pytest`
- 🔍 Code quality enforcement using `flake8`
- 🛡️ Static security analysis using `bandit`
- 🔄 CI/CD pipeline enforcing security and quality gates
- 📦 Fully containerized services for environment consistency
- 🏗️ Infrastructure provisioning using Terraform
- ❌ Builds fail automatically if tests or security checks fail

---

## 🔁 CI/CD Pipeline (GitHub Actions)

A complete **CI/CD pipeline** is implemented using GitHub Actions.

### Continuous Integration (CI)
On every **push** or **pull request**, the pipeline automatically:

- Installs project dependencies
- Runs unit tests using `pytest`
- Performs linting using `flake8`
- Executes security scans using `bandit`
- Fails the pipeline if any quality or security checks fail

This ensures **only secure, high-quality code** is merged.

### Continuous Delivery (CD)
- A Docker image is built after successful CI checks
- Services are deployed consistently using Docker Compose
- Environment variables are securely managed using `.env` files

📁 **Pipeline location:**  
