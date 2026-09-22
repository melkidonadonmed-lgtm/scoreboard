#!/usr/bin/env python3
"""
scripts/export_drive_pwa.py
Milestone 5: Export and Upload PWA build zip to Google Drive folder 1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z
Using Google Drive API v3 multipart upload.
"""

import os
import sys
import json
import zipfile
import subprocess
import requests

FOLDER_ID = "1H6Mhm9sCHv9r6x38EnE12bDXC0bQK77Z"
ZIP_NAME = "scoreboard-app-build-neurocirurgia-pwa.zip"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
ZIP_PATH = os.path.join(PROJECT_ROOT, ZIP_NAME)
GCLOUD_BIN = "/home/melki/.local/bin/gcloud"
UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"

def get_auth_token():
    print("[1/5] Retrieving Google Cloud access token via gcloud...")
    cmd = [GCLOUD_BIN, "auth", "print-access-token"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        cmd_fallback = ["gcloud", "auth", "print-access-token"]
        result = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError(f"Failed to get auth token: {result.stderr}")
    token = result.stdout.strip()
    print("  ✓ Access token retrieved successfully.")
    return token

def package_dist_zip():
    print(f"[2/5] Packaging {DIST_DIR} into {ZIP_PATH}...")
    if not os.path.isdir(DIST_DIR):
        raise FileNotFoundError(f"Dist directory not found: {DIST_DIR}. Run 'npm run build' first.")
    
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, DIST_DIR)
                zf.write(full_path, rel_path)
    
    size_bytes = os.path.getsize(ZIP_PATH)
    size_kb = size_bytes / 1024.0
    print(f"  ✓ Archive created: {ZIP_NAME}")
    print(f"  ✓ Archive size: {size_bytes} bytes ({size_kb:.2f} KB)")
    return size_bytes

def upload_zip_to_drive(token):
    print(f"[3/5] Uploading {ZIP_NAME} to Google Drive folder {FOLDER_ID} via multipart upload...")
    with open(ZIP_PATH, "rb") as f:
        zip_bytes = f.read()

    metadata = {
        "name": ZIP_NAME,
        "parents": [FOLDER_ID]
    }

    boundary = "==============scoreboard_pwa_upload_boundary=============="
    delimiter = f"--{boundary}\r\n".encode("utf-8")
    close_delimiter = f"\r\n--{boundary}--\r\n".encode("utf-8")

    metadata_part = (
        delimiter +
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n" +
        json.dumps(metadata).encode("utf-8") +
        b"\r\n"
    )

    file_part = (
        delimiter +
        b"Content-Type: application/zip\r\n\r\n" +
        zip_bytes
    )

    multipart_body = metadata_part + file_part + close_delimiter

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/related; boundary={boundary}",
        "Content-Length": str(len(multipart_body))
    }

    res = requests.post(UPLOAD_URL, headers=headers, data=multipart_body, timeout=60)
    print(f"  ✓ HTTP Response Status: {res.status_code}")
    if res.status_code not in (200, 201):
        raise RuntimeError(f"Upload failed ({res.status_code}): {res.text}")

    resp_data = res.json()
    file_id = resp_data.get("id")
    file_name = resp_data.get("name")
    print(f"  ✓ Upload Successful!")
    print(f"  ✓ Uploaded File ID: {file_id}")
    print(f"  ✓ File Name: {file_name}")
    print(f"  ✓ Target Parent Folder ID: {FOLDER_ID}")
    return file_id

def verify_drive_upload(token, file_id):
    print(f"[4/5] Verifying uploaded file on Google Drive (ID: {file_id})...")
    url = f"{DRIVE_API_BASE}/files/{file_id}?fields=id,name,parents,size,mimeType,createdTime"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers, timeout=15)
    if res.status_code != 200:
        raise RuntimeError(f"Verification query failed ({res.status_code}): {res.text}")
    
    file_meta = res.json()
    print("  ✓ Verification Query Response:")
    print(f"    - ID: {file_meta.get('id')}")
    print(f"    - Name: {file_meta.get('name')}")
    print(f"    - MimeType: {file_meta.get('mimeType')}")
    print(f"    - Size: {file_meta.get('size')} bytes")
    print(f"    - Parents: {file_meta.get('parents')}")
    print(f"    - Created Time: {file_meta.get('createdTime')}")
    return file_meta

def main():
    print("=================================================================")
    print("📦 Scoreboard App: PWA Build Packaging, Upload & Drive Verify")
    print("=================================================================")
    try:
        token = get_auth_token()
        package_dist_zip()
        file_id = upload_zip_to_drive(token)
        verify_drive_upload(token, file_id)
        print("[5/5] All Google Drive release operations completed successfully! 🎉")
    except Exception as e:
        print(f"❌ Error during export/upload: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
