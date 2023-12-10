from flask import Flask, request
import shutil
import docker
import uuid
import os
import zipfile

app = Flask(__name__)


@app.route('/run', methods=['POST'])
def index():
    folderName = f'/data/{uuid.uuid4()}'
    runnerZipFile = f'{folderName}/runner.zip'
    submitZipFile = f'{folderName}/submit.zip'
    os.mkdir(f'{folderName}')

    request.files['runnerCode'].save(runnerZipFile)
    request.files['submition'].save(submitZipFile)

    with zipfile.ZipFile(submitZipFile, "r") as zip_ref:
        zip_ref.extractall(folderName)

    with zipfile.ZipFile(runnerZipFile, "r") as zip_ref:
        zip_ref.extractall(folderName)

    client = docker.from_env()
    res = client.containers.run(
        image="python:3.9-alpine",
        command=["python3", f"{folderName}/main.py"],
        name=uuid.uuid4(),
        working_dir=folderName,
        volumes_from=['docker-proxy'],
        remove=True,
    )

    shutil.rmtree(folderName)

    return res.decode('ascii')
