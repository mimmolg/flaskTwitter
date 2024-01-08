# Flask Twitter App

## Description
This is a project for a Twitter-like application developed with Flask.

## Prerequisites

Before running this project, make sure you have the following prerequisites installed:

- [Git](https://git-scm.com/): You can install Git by running the following commands:

  ```bash
  # On Debian/Ubuntu-based systems
  sudo apt-get update
  sudo apt-get install git
  ```
- [Python3](https://www.python.org/): Puoi installare python3 eseguendo i seguenti comandi:
  ```bash
  # On Debian/Ubuntu-based systems
  sudo apt-get update
  sudo apt-get install python3
  ```
- [Docker](https://www.docker.com/)
   ```bash
   # Follow the official Docker instructions for your operating system
   ```
- [MongoDB](https://www.mongodb.com/)
    ```bash
    # Follow the official Docker instructions for your operating system
     ```
## Configuration 

1. **Install Docker:** Ensure you have Docker installed on your machine. You can download it [here](https://www.docker.com).

2. **Download MongoDB image:** Run the following command to download the latest MongoDB image:

    ```bash
    docker pull mongo
    ```

3. **Create a persistent directory for MongoDB:** Create a directory to store MongoDB data. For example:

    ```bash
    mkdir mongodata
    ```

4. **Define the MONGODATA environment variable:** Set the MONGODATA environment variable to point to the data directory. For example:

    ```bash
    export MONGODATA="$PWD/mongodata"
    ```

5. **Launch the MongoDB container:** Start the MongoDB container with the following command:

    ```bash
    docker run -it -v $MONGODATA:/data/db -p 27017:27017 --name mongodb -d mongo
    ```

    Ensure the container is running with:

    ```bash
    docker ps
    ```
## Installation
1. Clone the repository: `git clone https://github.com/domenicolg/flaskTwitter.git`
2. Enter in the directory of the project: `cd flaskTwitter`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment::
    - Su Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Execution
 ```bash
    flask run
```
Now the application is accessible at http://localhost:5000/.


