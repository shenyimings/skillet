"""Semantic tier: chunking and schema-constrained labelling."""

from __future__ import annotations

from .chunk import Chunk, ChunkKind, chunk_file, chunk_package
from .client import Completion, DeepSeekClient, ScriptedClient
from .labeller import EXTRACTOR, SYSTEM_PROMPT, label_package
from .schema import ChunkLabels, Label, parse_labels

__all__ = [
    "EXTRACTOR",
    "SYSTEM_PROMPT",
    "Chunk",
    "ChunkKind",
    "ChunkLabels",
    "Completion",
    "DeepSeekClient",
    "Label",
    "ScriptedClient",
    "chunk_file",
    "chunk_package",
    "label_package",
    "parse_labels",
]
