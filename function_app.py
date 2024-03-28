import azure.functions as func
import logging
from convert_to_pdf import ConvertToPdf

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Make some minor changes to see the changes in the function app.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response. Make some minor changes to see the changes in the function app.",
             status_code=200
        )

@app.route(route="upload", methods=["POST"])
def upload(req: func.HttpRequest) -> func.HttpResponse:
    if not req.files:
        return func.HttpResponse("No files uploaded", status_code=400)

    file = req.files.get('file')
    logging.info(file.content_type)
    convert_to_pdf_service = ConvertToPdf()
    path = convert_to_pdf_service.build_path()
    logging.info(file.content_type)
    file_id = convert_to_pdf_service.file_service.upload_stream(path, file.read(), file.content_type)
    logging.info(file_id)

    return func.HttpResponse(path, status_code=200)

@app.route(route="convert_to_pdf", methods=["POST"])
def convert_to_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(req.files)
    convert_to_pdf_service = ConvertToPdf()
    path = convert_to_pdf_service.build_path()
    logging.info(path)
    # file_id = convert_to_pdf_service.file_service.upload_stream(path, req.get_data(), req.headers.get('Content-Type'))
    # logging.info(file_id)

    return func.HttpResponse(path, status_code=200)
