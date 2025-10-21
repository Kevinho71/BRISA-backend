# BRISA Backend

## Project Modules
- User Management
- Authentication
- API Endpoints
- Database Integration
- Error Handling

## Clone Instructions
To clone the repository, run the following command:
```bash
git clone https://github.com/Kevinho71/BRISA-backend.git
```

## Dependency Installation
After cloning the repository, navigate into the project directory and install the dependencies using pip:
```bash
pip install -r requirements.txt
```

## Virtual Environment Setup
It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment as follows:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

## Gitflow Methodology
Gitflow is a branching model that helps manage releases and features using branches. Here are the key components:
- `master`: Production-ready state
- `develop`: Latest development changes
- `feature/*`: Branches for specific features
- `release/*`: Branches for preparing new releases
- `hotfix/*`: Branches for quick fixes

## Git Flow Commands
Here are some common git flow commands:
- Start a new feature: `git flow feature start feature-name`
- Finish a feature: `git flow feature finish feature-name`
- Start a release: `git flow release start release-name`
- Finish a release: `git flow release finish release-name`
- Start a hotfix: `git flow hotfix start hotfix-name`
- Finish a hotfix: `git flow hotfix finish hotfix-name`