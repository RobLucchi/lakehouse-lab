# Lakehouse Lab

A **Data Engineering** sandbox project aimed at exploring a local, self-contained “lakehouse” architecture. The project starts with **MinIO** (S3-compatible object store), a Python script that interacts with MinIO, and will gradually incorporate **Trino**, **Iceberg**, **Kafka**, **dbt**, and more.

## Table of Contents
- [Lakehouse Lab](#lakehouse-lab)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Goals](#goals)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Setup](#setup)
    - [1. Clone this Repository](#1-clone-this-repository)
    - [2. Create a Python Virtual Environment](#2-create-a-python-virtual-environment)
    - [3. Install Python Dependencies](#3-install-python-dependencies)
    - [4. Run MinIO with Docker Compose](#4-run-minio-with-docker-compose)
  - [Usage](#usage)
    - [Check MinIO Console](#check-minio-console)
    - [Run the Python Script](#run-the-python-script)
  - [Next Steps](#next-steps)
  - [License](#license)

---

## Overview

- **MinIO**: A lightweight, S3-compatible object storage solution. Perfect for local development environments where you want to mimic S3 functionality without using AWS.
- **Python / `boto3`**: Python’s AWS SDK library, used here to upload, download, and list files in MinIO.
- **Docker & Docker Compose**: Simplifies deployment of MinIO and other services we’ll integrate later.

### Goals

1. Practice basic S3 operations (list/upload/download files) on local MinIO.  
2. Gradually layer in more tools such as Trino (SQL query engine), Iceberg (table format), Kafka (event streaming), dbt (analytics transformations), etc.  
3. Provide a cohesive environment to learn and experiment with modern data engineering workflows.

---

## Project Structure

```
lakehouse-lab/
├── docker-compose.yml     # Docker Compose file for MinIO (and future services)
├── README.md              # This readme document
├── requirements.txt       # Python dependencies (boto3, etc.)
├── lakehouse-lab-env/     # (Optional) Python virtual environment folder
├── src/
│   └── minio_test.py      # Simple script to interact with MinIO
└── ...
```

---

## Requirements

- **Python** 3.8+  
- **Docker** 20.10+  
- **Docker Compose** 1.29+  

*(Versions shown are approximate; anything recent should work.)*

---

## Setup

### 1. Clone this Repository
```bash
git clone https://github.com/your-username/lakehouse-lab.git
cd lakehouse-lab
```

### 2. Create a Python Virtual Environment
We recommend a Python virtual environment to isolate dependencies:

```bash
python3 -m venv lakehouse-lab-env
source lakehouse-lab-env/bin/activate  # On Linux/Mac
# or, on Windows:
# lakehouse-lab-env\Scripts\activate
```

### 3. Install Python Dependencies
Inside your activated virtual environment:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(If you don’t have a `requirements.txt` yet, just manually install `boto3` for now: `pip install boto3`.)*

### 4. Run MinIO with Docker Compose
Use Docker Compose to spin up the MinIO service:

```bash
docker-compose up -d
```

- **Ports**:
  - MinIO **S3** endpoint: `http://localhost:9000`
  - MinIO **Console** endpoint: `http://localhost:9090`

- **Default Credentials**:
  - **Access Key**: `minioadmin`
  - **Secret Key**: `minioadmin`

You can confirm the container is running:

```bash
docker ps
```

---

## Usage

### Check MinIO Console
1. Open your browser to [http://localhost:9090](http://localhost:9090).
2. Log in with:
   - **Username**: `minioadmin`
   - **Password**: `minioadmin`
3. Create a new bucket (e.g., `demo-bucket`).

### Run the Python Script
1. Ensure your Python environment is active (`source lakehouse-lab-env/bin/activate`).
2. Execute the `minio_test.py` script:

    ```bash
    cd src
    python minio_test.py
    ```

**What the script does**:
- Lists existing buckets on MinIO.
- Uploads a small text file (`hello.txt`) to the specified bucket.
- Downloads it to verify the content.
- Lists objects in that bucket.

**Sample Output**:
```
Buckets: ['demo-bucket']
Uploaded 'test-folder/hello.txt' to bucket 'demo-bucket'.
File content: Hello from MinIO!
Objects in bucket:
 - test-folder/hello.txt
```

To confirm, visit the MinIO console at [http://localhost:9090](http://localhost:9090) and check the contents of `demo-bucket`.

---

## Next Steps
This project will evolve to include:
1. **Trino**: A high-performance SQL engine to query data in MinIO.  
2. **Apache Iceberg**: A table format for large analytic datasets on object storage.  
3. **Kafka**: For event streaming use cases.  
4. **dbt**: For analytics transformations and data modeling.  

Stay tuned for incremental updates in the [README](README.md) as we layer in new services.

---

## License

MIT License

Copyright (c) 2025 Ahmed Mousa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
