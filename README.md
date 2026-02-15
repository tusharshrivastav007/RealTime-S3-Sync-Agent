# S3 Auto Sync Service

Automatic background service to sync local folders to AWS S3 in real-time using Docker.

## 🚀 Features
- **Real-time Sync**: Uses `watchdog` to detect file changes instantly.
- **Robust Support**: Handles file creations, modifications, and moves (Drag & Drop).
- **Recursive Sync**: Uploads entire directory structures when copied or moved.
- **Multi-Folder Support**: Syncs multiple distinct local directories to separate S3 folders.
- **Dockerized**: specific dependencies are isolated in a lightweight container.

## 📋 Prerequisites
- **Docker** and **Docker Compose** installed.
- **AWS Account** with an S3 bucket.
- **IAM User** with `s3:PutObject` and `s3:ListBucket` permissions.

## 🛠️ Setup

1.  **Clone/Create Project Directory**:
    ```bash
    mkdir s3-auto-sync
    cd s3-auto-sync
    ```

2.  **Configure Environment (`.env`)**:
    Create a `.env` file in the project root:
    ```ini
    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_REGION=ap-south-1
    S3_BUCKET=your-bucket-name

    # Local Folders to Sync
    DIR_DOWNLOADS=/home/youruser/Downloads
    DIR_DOCUMENTS=/home/youruser/Documents
    DIR_DESKTOP=/home/youruser/Desktop
    DIR_INTERVIEW_PREPARATION="/home/youruser/Interview Preparation"
    DIR_PROJECTS=/home/youruser/Projects
    ```

3.  **Review `docker-compose.yml`**:
    Ensure the volumes map your environment variables to the correct targets inside the container (`/data/...`).

## ▶️ Running

Start the service in the background:
```bash
docker-compose up -d --build
```

View logs to verify uploads:
```bash
docker-compose logs -f
```

Stop the service:
```bash
docker-compose down
```

## 📂 Mapping Logic
The service maps local folders to subfolders in S3:

| Local Directory | Container Path | S3 Path |
| :--- | :--- | :--- |
| `${DIR_DOWNLOADS}` | `/data/Downloads` | `s3://bucket/Downloads/...` |
| `${DIR_PROJECTS}` | `/data/Projects` | `s3://bucket/Projects/...` |

##  troubleshoot
- **No Uploads?** Check logs (`docker-compose logs`). ensure your AWS credentials are correct.
- **Permission Error?** Ensure your IAM user has write access to the bucket.
- **Folder not syncing?** Ensure the path in `.env` is absolute and correct.
