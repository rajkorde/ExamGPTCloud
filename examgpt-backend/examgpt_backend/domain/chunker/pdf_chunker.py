import re
from typing import Generator

from domain.model.core.chunk import TextChunk
from domain.model.utils.logging import app_logger
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents.base import Document

logger = app_logger.get_logger()


class SimplePDFChunker:
    def __init__(self, chunk_size: int = 3000):
        self.chunk_size = chunk_size

    def _cleanup_text(self, text: str) -> str:
        # remove page numbers
        def is_page_number(line: str) -> bool:
            return bool(re.fullmatch(r"\d+", line.strip()))

        # combine multiple newlines
        def combine_empty_lines(text: str) -> str:
            text = re.sub(r"\s*\n\s*", "\n", text)
            return re.sub(r"\n+", "\n", text).strip()

        lines = text.split("\n")
        clean_lines = [line for line in lines if not is_page_number(line)]
        clean_lines = combine_empty_lines("\n".join(clean_lines))
        return clean_lines

    def _combine_pages(
        self, pages: list[Document], exam_code: str
    ) -> Generator[TextChunk, None, None]:
        chunk: str = ""
        current_chunk_size = 0

        for page in pages:
            page_content = self._cleanup_text(page.page_content)
            page_size = len(page_content)

            if page_size + current_chunk_size > self.chunk_size:
                if chunk:
                    yield TextChunk(exam_code=exam_code, text=chunk)
                chunk: str = ""
                current_chunk_size = 0

            chunk += str(page_content)
            current_chunk_size += page_size

        if chunk:
            yield TextChunk(exam_code=exam_code, text=chunk)

    def chunk(self, location: str, exam_code: str) -> list[TextChunk]:
        loader = PyMuPDFLoader(location)
        pages = loader.load()
        logger.debug(
            f"Parsing complete for pdf file: {location}. The PDF has {len(pages)} pages."
        )

        return list(self._combine_pages(pages, exam_code))
