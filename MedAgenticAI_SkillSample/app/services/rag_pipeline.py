"""
MedCore+ RAG Pipeline
Hybrid search (BM25 + dense) with clinical reranking.
"""
from dataclasses import dataclass
from typing import Any
import structlog

log = structlog.get_logger()


@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float
    evidence_grade: str  # A, B, C, D
    icd10_tags: list[str]


class RAGPipeline:
    """Core retrieval pipeline for clinical evidence."""

    def __init__(self, config: Any):
        self.config = config
        self._retriever = None  # initialized lazily
        self._reranker = None

    async def retrieve(
        self, query: str, top_k: int = 10
    ) -> list[RetrievedChunk]:
        """
        Hybrid BM25 + dense retrieval, then rerank.
        Returns top-k clinically relevant chunks.
        """
        log.info("rag.retrieve.start", query_len=len(query), top_k=top_k)

        bm25_results = await self._bm25_search(query, top_k * 2)
        dense_results = await self._dense_search(query, top_k * 2)
        merged = self._reciprocal_rank_fusion(bm25_results, dense_results)
        reranked = await self._rerank(query, merged, top_k)

        log.info("rag.retrieve.done", returned=len(reranked))
        return reranked

    async def _bm25_search(self, query: str, k: int) -> list[RetrievedChunk]:
        raise NotImplementedError

    async def _dense_search(self, query: str, k: int) -> list[RetrievedChunk]:
        raise NotImplementedError

    def _reciprocal_rank_fusion(
        self, a: list[RetrievedChunk], b: list[RetrievedChunk]
    ) -> list[RetrievedChunk]:
        raise NotImplementedError

    async def _rerank(
        self, query: str, chunks: list[RetrievedChunk], top_k: int
    ) -> list[RetrievedChunk]:
        raise NotImplementedError
