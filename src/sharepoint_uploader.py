import os
import logging
from pathlib import Path
import requests
from requests.exceptions import HTTPError
from urllib.parse import quote

from TokenManager import get_token_manager
from logger import build_process_logger
from secret import read_secret



def get_site_id(token_manager, domain, site_name):
    url = f"https://graph.microsoft.com/v1.0/sites/{domain}:/sites/{site_name}"   #Obtain the ID of site from SharePoint.
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]



def get_drive_id(token_manager, site_id, drive_name="Documents"):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"  #Obtain the ID from drive(library documents) from site
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    drives = response.json().get("value", [])
    for drive in drives:
        if drive["name"] == drive_name:
            return drive["id"]
    raise Exception(f"Drive '{drive_name}' no encontrado en el site.")




def ensure_remote_folder(token_manager, drive_id, parent_path, folder_name):
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{parent_path}:/children"  #Create the remote folder if don't exist, return the complete path.
    headers = {
        "Authorization": f"Bearer {token_manager.get_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "replace"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code not in (200, 201):
        response.raise_for_status()

    # Normalize path separators to forward slashes (Graph API format)
    return os.path.join(parent_path, folder_name).replace("\\", "/")


def upload_file(token_manager, drive_id, remote_path, local_file_path):
    """Upload a single file to the SharePoint drive."""
    logger_instance = logging.getLogger("sharepoint_upload")
    logger = build_process_logger(logger_instance, "upload_file")

    logger.info(f"Uploading from local path {local_file_path} to {remote_path}")
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{remote_path}:/content"
    headers = {
        "Authorization": f"Bearer {token_manager.get_token()}",
        "Content-Type": "application/octet-stream"
    }

    with open(local_file_path, "rb") as f:
        data = f.read()

    response = requests.put(url, headers=headers, data=data)
    response.raise_for_status()
    logger.info("✅ Upload Done")


# Uploads a file to the SharePoint site 'Institutional Strengthening'.
def upload_file_sharepoint(file_path: Path, target_folder: str = ""):   #Args: file_path: Local file path to upload.  target_folder: Relative path inside drive(ex:'Uploads/2025-10').
    logger_instance = logging.getLogger("sharepoint_upload")
    logger = build_process_logger(logger_instance, "upload_file_sharepoint")

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

        #  1.Obtain secrets and token
    sharepoint_domain = read_secret("SHAREPOINT_DOMAIN")
    site_name = "Institutional Strengthening"
    token_manager = get_token_manager()

        # 2.Resolve site and drive
    try:
        site_id = get_site_id(token_manager, sharepoint_domain, site_name)
        drive_id = get_drive_id(token_manager, site_id, "Documents")
    except HTTPError as e:
        logger.error(f"Error resolviendo site/drive: {e}")
        raise


         # 3.Create remote folder if target_folder was specified
    remote_folder = target_folder.strip("/")
    if remote_folder:
        # Crear estructura de carpetas recursiva
        parts = remote_folder.split("/")
        current_path = ""
        for part in parts:
            current_path = ensure_remote_folder(token_manager, drive_id, current_path, part)
    else:
        current_path = ""


         #  4.Upload file
    filename = file_path.name
    remote_path = f"{current_path}/{filename}".strip("/")

    try:
        upload_file(token_manager, drive_id, remote_path, str(file_path))
        logger.info(f"✅ Archivo '{filename}' subido correctamente a SharePoint.")
    except HTTPError as e:
        logger.error(f"❌ Error al subir el archivo: {e.response.status_code} - {e.response.text}")
        raise

         # 5.Return URL confirmation
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{remote_path}"
    headers = {"Authorization": f"Bearer {token_manager.get_token()}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    item = response.json()
    web_url = item.get("webUrl")

    logger.info(f"🌐 Archivo disponible en: {web_url}")
    return web_url


   # EXAMPLE TEST FOR USE
if __name__ == "__main__":
    # Esto solo es para pruebas locales
    test_path = Path("uploads/test.xlsx")
    upload_file_sharepoint(test_path, "Uploads/Tests")





