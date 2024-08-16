from typing import Any

from domain.commands.content_commands import CreateUploadURLs, DownloadFile
from domain.model.utils.misc import ErrorMessage
from domain.ports.content_service import ContentService


def create_upload_urls(
    command: CreateUploadURLs, content_service: ContentService
) -> Any:
    signed_urls = []
    for source in command.sources:
        response = content_service.create_upload_url(source)
        if isinstance(response, ErrorMessage):
            return response
        signed_urls.append(response)

    return signed_urls


def download_file(command: DownloadFile, content_service: ContentService) -> str:
    path = content_service.download_file(
        source=command.source,
        destination=command.destination,
        bucket_name=command.bucket_name,
    )
    return path
