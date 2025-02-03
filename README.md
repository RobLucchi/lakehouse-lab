# Lakehouse Lab

A **Data Engineering** sandbox project aimed at exploring a local, self-contained “lakehouse” architecture. The project starts with **MinIO** (S3-compatible object store) and a Python script to interact with it, and gradually incorporates other tools such as **Trino**, **Hive**, **Iceberg**, **Kafka**, **dbt**, and more.

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
    - [4. Run the Stack with Docker Compose](#4-run-the-stack-with-docker-compose)
  - [Usage](#usage)
    - [MinIO Operations with Python](#minio-operations-with-python)
    - [Querying Data with Trino \& Hive](#querying-data-with-trino--hive)
  - [Trino and Hive Explained](#trino-and-hive-explained)
    - [What is Trino?](#what-is-trino)
    - [What is Hive?](#what-is-hive)
    - [AWS Equivalents](#aws-equivalents)
  - [Benefits and Best Practices](#benefits-and-best-practices)
    - [Benefits of This Approach](#benefits-of-this-approach)
    - [Best Practices for Efficiency](#best-practices-for-efficiency)
  - [Next Steps](#next-steps)
  - [License](#license)
    - [Explanation of New Sections](#explanation-of-new-sections)

---

## Overview

- **MinIO**: A lightweight, S3-compatible object storage solution. Perfect for local development and testing where you want S3 functionality without incurring cloud costs.
- **Python / `boto3`**: Python’s AWS SDK library is used here to upload, download, and list files in MinIO.
- **Trino**: A high-performance, distributed SQL query engine for interactive analytics. It enables you to query large datasets stored in object storage (or across multiple data sources) using standard SQL.
- **Hive**: A data warehousing solution that provides a metadata repository (the Hive Metastore) and an SQL-like language (HiveQL) to query large datasets stored in distributed storage systems.
- **Docker & Docker Compose**: Used to simplify deployment and orchestration of MinIO, Postgres (for Hive Metastore), Hive Metastore, and Trino.

### Goals

1. Practice basic S3 operations (list/upload/download files) on local MinIO.
2. Layer in more tools gradually (starting with Trino and Hive) to build a scalable data lakehouse.
3. Provide a cohesive environment to learn and experiment with modern data engineering workflows.

---

## Project Structure

```
lakehouse-lab/
├── docker-compose.yml         # Docker Compose file for MinIO, Postgres, Hive Metastore, and Trino
├── README.md                  # This readme document
├── requirements.txt           # Python dependencies (boto3, etc.)
├── lakehouse-lab-env/         # (Optional) Python virtual environment folder
├── data/                      # Contains configuration for Trino
│   └── trino/
│       └── etc/
│           ├── config.properties
│           ├── jvm.config
│           ├── log.properties
│           ├── node.properties
│           └── catalog/
│               └── hive.properties
└── src/
    └── minio_test.py         # Simple script to interact with MinIO
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
# or on Windows: lakehouse-lab-env\Scripts\activate
```

### 3. Install Python Dependencies
Inside your activated virtual environment:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(If you don’t have a `requirements.txt` yet, install boto3 manually: `pip install boto3`.)*

### 4. Run the Stack with Docker Compose
This project now uses a multi-service Docker Compose stack that includes:
- **MinIO** for S3-compatible storage.
- **Postgres** for the Hive Metastore database.
- **Hive Metastore** to manage table metadata (including for Delta Lake).
- **Trino** to query the data via SQL.

To start the stack:
```bash
docker-compose up -d
```
- **MinIO** is available at:
  - S3 API: `http://localhost:9000`
  - Web Console: `http://localhost:9090`
- **Trino** is available at `http://localhost:8080`.

---

## Usage

### MinIO Operations with Python
1. **Check MinIO Console:**
   - Open your browser to [http://localhost:9090](http://localhost:9090).
   - Log in with:
     - **Username:** `minioadmin`
     - **Password:** `minioadmin`
   - Create a bucket (e.g., `demo-bucket`).

2. **Run the Python Script:**
   ```bash
   cd src
   python minio_test.py
   ```
   The script will:
   - List existing buckets.
   - Upload a file (`hello.txt`) to the bucket.
   - Download the file and verify its contents.
   - List objects in the bucket.

### Querying Data with Trino & Hive
Once your stack is running:
1. **Trino Configuration:**
   - Your Trino configuration files (under `data/trino/etc`) include:
     - `config.properties`: Sets the node as a coordinator and specifies the HTTP port.
     - `jvm.config`: Configures JVM memory and garbage collection.
     - `log.properties`: Sets the logging level.
     - `node.properties`: Specifies the node’s environment, data directory, and plugin directory.
     - `catalog/hive.properties`: Configures the Hive connector to use the Hive Metastore (available at `thrift://hive-metastore:9083`) and connect to MinIO for S3 storage.
2. **Accessing Trino:**
   - Open your browser to [http://localhost:8080](http://localhost:8080) or use the Trino CLI to connect.
   - Run SQL commands to query your data on MinIO (once you register tables via Hive/Delta procedures).

---

## Trino and Hive Explained

### What is Trino?
- **Trino** is an open-source, distributed SQL query engine designed for fast, interactive analytics across large datasets.
- It can query data stored in various systems (S3, HDFS, databases) without moving the data.
- In this project, Trino’s Hive connector allows you to query Parquet and Delta Lake files stored in MinIO.

### What is Hive?
- **Apache Hive** is a data warehousing solution that uses an SQL-like language (HiveQL) for querying large datasets stored in distributed systems.
- A central component of Hive is the **Hive Metastore**, which stores metadata (schema, partitioning, table definitions) about your data.
- In our stack, Hive Metastore (running via the `starburstdata/hive` image) uses Postgres as its backend and stores table metadata that Trino can access.

### AWS Equivalents
- **Amazon Athena** is a serverless query service similar to running Trino for interactive SQL queries over S3 data.
- **AWS Glue Data Catalog** serves as a managed metadata store (like the Hive Metastore) for your data lake.
- **Amazon EMR** can run Hive or Trino (Presto) on clusters, offering a managed solution for large-scale data processing.

---

## Benefits and Best Practices

### Benefits of This Approach
- **Scalability & Cost Efficiency:**  
  Decouples storage (MinIO/S3) from compute (Trino/Hive), allowing independent scaling.
- **High Performance:**  
  Uses columnar storage (Parquet) and supports predicate pushdown and column pruning for efficient queries.
- **Flexibility:**  
  Enables multiple query engines to access the same data, and supports schema evolution.
- **Simplified Data Pipeline:**  
  Directly ingest data into Parquet files stored in object storage.
- **Local Development:**  
  MinIO emulates S3 locally for testing before production deployment on AWS.

### Best Practices for Efficiency
- **Optimize Data Layout:**  
  Partition data by relevant dimensions (e.g., date, region) and manage file sizes to avoid too many small files.
- **Leverage Query Engine Features:**  
  Use cost-based optimizers, caching, and metadata from Parquet files to skip unnecessary I/O.
- **Maintain a Metastore:**  
  Even with a lightweight or file-based metastore, maintaining consistent table metadata is key.
- **Monitor and Tune:**  
  Use logs and metrics to identify bottlenecks and adjust resource allocations.
- **Keep Local and Production Environments Similar:**  
  Develop locally with MinIO and replicate the configuration when moving to AWS S3.

---

## Next Steps

This project will evolve to include:
1. **Trino:** Further configure and optimize Trino for interactive querying across your data lake.
2. **Apache Iceberg:** Integrate Iceberg to enable ACID transactions, schema evolution, and versioning of your tables.
3. **Kafka:** Incorporate event streaming to simulate real-time data ingestion.
4. **dbt:** Add dbt for analytics transformations and data modeling.

As each new component is integrated, the README will be updated with configuration details, usage instructions, and best practices.

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
```

---

### Explanation of New Sections

- **Querying Data with Trino & Hive:**  
  This section explains how your newly added services (Trino and Hive Metastore) work together to enable SQL querying over data stored in MinIO. It also reminds you to check your Trino configuration (located under `data/trino/etc`) which includes essential configuration files like `config.properties`, `jvm.config`, and `catalog/hive.properties`.

- **Trino and Hive Explained:**  
  Provides a high-level overview of what Trino and Hive are, their roles in your architecture, and how they compare to AWS services such as Athena and Glue.

- **Benefits and Best Practices:**  
  Lists the benefits of storing data in Parquet on S3/MinIO and querying with a SQL engine, along with recommendations for efficient data organization and query performance.

- **Next Steps:**  
  Outlines the future evolution of the project, including additional tools and enhancements.

This updated README now reflects both the initial MinIO/Python functionality and the new components and concepts introduced with Trino and Hive, providing a comprehensive guide to your evolving data engineering POC.