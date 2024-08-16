from domain.model.core.chunk import TextChunk
from domain.model.utils.logging import app_logger
from langchain_community.document_loaders import PyMuPDFLoader

logger = app_logger.get_logger()


class SimplePDFChunker:
    def chunk(self, location: str, exam_code: str) -> list[TextChunk]:
        logger.info(f"Starting PDF chunker: {location}")
        loader = PyMuPDFLoader(location)
        pages = loader.load()
        logger.info(f"Chunking complete. The PDF has {len(pages)} pages.")

        chunks: list[TextChunk] = []
        for i, page in enumerate(pages):
            chunk = TextChunk(
                exam_code=exam_code, text=page.page_content, page_number=i
            )
            chunks.append(chunk)
        return chunks
