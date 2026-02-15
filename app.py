import time
import boto3
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
WATCH_DIRECTORY = "/data"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

class UploadHandler(FileSystemEventHandler):
    def _upload_file(self, file_path):
        """Helper to upload a single file."""
        if os.path.isdir(file_path):
            return

        try:
            # Calculate S3 key (path in bucket) relative to the watched directory
            s3_key = os.path.relpath(file_path, WATCH_DIRECTORY)
            logging.info(f"Uploading {file_path} to s3://{S3_BUCKET}/{s3_key}")
            s3.upload_file(file_path, S3_BUCKET, s3_key)
            logging.info(f"Successfully uploaded: {s3_key}")
        except Exception as e:
            logging.error(f"Error uploading {file_path}: {e}")

    def _process_directory(self, dir_path):
        """Recursively upload all files in a directory."""
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                self._upload_file(file_path)

    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            logging.info(f"Directory created: {event.src_path}. Scanning contents...")
            self._process_directory(event.src_path)
        else:
            # Wait a brief moment to ensure file is fully written
            time.sleep(1)
            self._upload_file(event.src_path)

    def on_modified(self, event):
        """Called when a file is modified."""
        if not event.is_directory:
            self._upload_file(event.src_path)

    def on_moved(self, event):
        """Called when a file or directory is moved or renamed."""
        if event.is_directory:
            logging.info(f"Directory moved/renamed to: {event.dest_path}. Scanning contents...")
            self._process_directory(event.dest_path)
        else:
            self._upload_file(event.dest_path)

if __name__ == "__main__":
    if not S3_BUCKET:
        logging.error("S3_BUCKET environment variable is not set.")
        exit(1)
        
    logging.info(f"Starting S3 Sync Service...")
    logging.info(f"Watching directory: {WATCH_DIRECTORY}")
    logging.info(f"Target Bucket: {S3_BUCKET}")
    
    observer = Observer()
    observer.schedule(UploadHandler(), WATCH_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping S3 Sync Service...")

    observer.join()
