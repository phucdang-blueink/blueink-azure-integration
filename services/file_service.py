import uuid
import mimetypes
import requests
import json
import logging
from typing import Optional

from services.authentication_service import AuthenticationService

# File Serivce
# Upload a file to SharePoint
# Convert the file to pdf
# Delete the original file in SharePoint

# https://blueink0.sharepoint.com/sites/pdfconversion
# https://graph.microsoft.com/v1.0/sites/blueink0.sharepoint.com:/sites/pdfconversion/?$select=id


class FileService:
    def __init__(self, authentication_service: AuthenticationService):
        self._authentication_service = authentication_service
        self._session = requests.Session()

    def create_authorized_http_client(self) -> Optional[requests.Session]:
        if self._session.headers.get('Authorization'):
            return self._session

        token = self._authentication_service.get_access_token()
        logging.info(f"Token: {token}")
        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})
            return self._session
        else:
            return None

    def upload_stream(self, path: str, content: bytes, content_type: str) -> Optional[str]:
            session = self.create_authorized_http_client()
            logging.info(f"Session: {session}")
            if not session:
                return None

            tmp_file_name = f"{uuid.uuid4()}.{mimetypes.guess_extension(content_type)}"
            logging.info(tmp_file_name)
            request_url = f"{path}root:/{tmp_file_name}:/content"
            DRIVE_ID = "01JOND5LD27WBE6IZMMZB3SZ2K26VTPQRT"
            DRIVE_ID = "01JOND5LF6Y2GOVW7725BZO354PWSELRRZ"
            # request_url = f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}/root:/Documents/{tmp_file_name}:/content"
            # https://graph.microsoft.com/v1.0/sites/uithcm.sharepoint.com,0bdb4156-bef8-402d-890a-da7bf933849c,7ab5c5b5-e477-4376-bf6c-25a37756801b/drive/items/root:/d336ad8b-93ef-4e64-9d6d-5a9b901b2a94..txt:/content
            # https://graph.microsoft.com/v1.0/me/drive/root:/Documents/content
            # https://graph.microsoft.com/v1.0/me/drive/root:/20ef40e6-9f63-47ce-bd72-d8aef443f704..txt:/content
            # https://graph.microsoft.com/v1.0/drives/6ee845a4252321ad/root:/Documents/content
            # https://graph.microsoft.com/v1.0/drives/6ee845a4252321ad/items/6EE845A4252321AD!111/children
            logging.info(request_url)
            headers = {"Content-Type": content_type}
            response = session.put(request_url, data=content, headers=headers)
            logging.info(response)

            if response.status_code == 200:
                file = json.loads(response.text)
                return file.get('id')
            else:
                message = response.text
                raise Exception(f"Upload file failed with status {response.status_code} and message {message}")

    def download_converted_file(self, path: str, file_id: str, target_format: str) -> Optional[bytes]:
            session = self.create_authorized_http_client()
            if not session:
                return None

            request_url = f"{path}{file_id}/content?format={target_format}"
            response = session.get(request_url)

            if response.status_code == 200:
                return response.content
            else:
                message = response.text
                raise Exception(f"Download of converted file failed with status {response.status_code} and message {message}")
