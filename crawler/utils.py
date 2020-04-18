from typing import Sequence, Generator


def chunks_by_size(seq: Sequence, chunk_size: input) -> Generator:
    for i in range(0, len(seq), chunk_size):
        yield seq[i:i+chunk_size]


def chunks_by_count(seq: Sequence, chunks_count: input):
    for i in range(chunks_count):
        yield seq[i::chunks_count]


__all__ = [chunks_by_size, chunks_by_count]
