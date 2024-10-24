# chatapp
chat application for real time chat


### Python Installation
```sh
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-distutils -y
```
## Usage

### Activate Environment
```sh
pipenv shell
```

### Install packages from Pipfile
```sh
pipenv install 
pipenv install --dev # for development environments
```

### Install packages from requirements.txt
```sh
pipenv install -r requirements.txt
```

### Install/Add new package
```sh
pipenv install <package_name>
```
### Install/Add new package as development dependency
```sh
pipenv install -D <package_name>
```
### Generating requirements files from a Pipfile
```sh
pipenv requirements > requirements.txt
pipenv requirements --dev > dev-requirements.txt
```
### Pre-commit Installation
NOTE: Installing git hook
```sh
pre-commit install
```
now pre-commit will run automatically on git commit

NOTE: Run against all the files
```sh
pre-commit run --all-files
```