import json
import logging

from models.authentication_options import AuthenticationOptions
from models.pdf_options import PdfOptions

from services.authentication_service import AuthenticationService
from services.file_service import FileService

def transform_config(config, prefix):
    prefix_values = {k: v for k, v in config.items() if k.startswith(prefix)}
    remove_prefix_values = {k.replace(prefix, ''): v for k, v in prefix_values.items()}
    return remove_prefix_values

class ConvertToPdf:
    def __init__(self):
        with open('credentials.json', 'r') as f:
            self.config = json.load(f)["Values"]

        graph_values = transform_config(self.config, 'graph:')
        self.graph_config = graph_values
        self.authentication_options = AuthenticationOptions(**self.graph_config)

        pdf_values = transform_config(self.config, 'pdf:')
        self.pdf_config = pdf_values
        self.pdf_options = PdfOptions(**self.pdf_config)

        self.authentication_service = AuthenticationService(self.authentication_options)
        self.file_service = FileService(self.authentication_service)

    def _build_path(self):
        site_path = f"{self.pdf_config['graph_endpoint']}sites/{self.pdf_config['site_id']}/drive/items/"
        logging.info(f"Site Path: {site_path}")
        return site_path

    def upload(self, file):
        path = self._build_path()
        return self.file_service.upload_stream(path, file)
    
    def download(self, file_id):
        path = self._build_path()
        return self.file_service.download_converted_file(path, file_id)

