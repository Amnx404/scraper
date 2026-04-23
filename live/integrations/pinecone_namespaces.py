from __future__ import annotations

from dataclasses import dataclass

from pinecone import Pinecone

from live.engines.pinecone_upsert import collect_namespace_names, previous_and_next_live_namespaces


@dataclass(frozen=True)
class LiveNamespaceInfo:
    previous_live_namespace: str | None
    live_namespace: str


def compute_next_live_namespace(*, api_key: str, index_host: str, live_prefix: str) -> LiveNamespaceInfo:
    pc = Pinecone(api_key=api_key)
    with pc.Index(host=index_host) as index:
        all_ns = collect_namespace_names(index)
    prev_ns, next_ns = previous_and_next_live_namespaces(all_ns, live_prefix)
    return LiveNamespaceInfo(previous_live_namespace=prev_ns, live_namespace=next_ns)
