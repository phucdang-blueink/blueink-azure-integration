import azure.functions as func
import logging
import math
import json
from convert_to_pdf import ConvertToPdf

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

@app.route(route="upload", methods=["POST"])
def upload(req: func.HttpRequest) -> func.HttpResponse:
    if not req.files:
        return func.HttpResponse("No files uploaded", status_code=400)

    convert_to_pdf = ConvertToPdf()
    ressponse = convert_to_pdf.upload(req.files.get('file'))

    custom_response = {
        "response_from_blueink": {
            "file_name": req.files.get('file').filename,
            "file_size": convert_size(ressponse["size"]),
            "file_id": ressponse["id"],
        },
        "response_from_microsoft": ressponse
    }

    return func.HttpResponse(
        json.dumps(custom_response),
        status_code=200,
        mimetype='application/json'
    )

@app.route(route="download", methods=["GET"])
def download(req: func.HttpRequest) -> func.HttpResponse:
    file_id = req.params.get('file_id')
    if not file_id:
        return func.HttpResponse("No file_id provided", status_code=400)

    convert_to_pdf = ConvertToPdf()
    ressponse = convert_to_pdf.download(file_id)

    return func.HttpResponse(
        ressponse,
        status_code=200,
        mimetype='application/pdf'
    )
