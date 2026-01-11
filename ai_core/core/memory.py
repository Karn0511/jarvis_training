import chromadb
import uuid
import time
from collections import deque
from .config import config
from .logger import logger


class VenomMemory:
    """
    Advanced Cognitive Memory System.

    Structure:
    1. Working Memory (Short-Term): Deque buffer for immediate context (last N interactions).
    2. Episodic Memory (Long-Term): Vector Database for recalling past events.
    3. Semantic Memory (Knowledge): (Future) Clean facts storage.
    """

    def __init__(self):
        # working memory size = 10 turns
        self.working_memory = deque(maxlen=10)

        # Long Term Memory
        try:
            self.client = chromadb.PersistentClient(path=config.MEMORY_DIR)
            self.collection = self.client.get_or_create_collection(
                name="venom_episodic", metadata={"hnsw:space": "cosine"}
            )
            # logger.success("Memory Core Loaded (Episode Store)")
        except Exception as e:
            logger.error(f"Memory Init Failed: {e}")
            self.collection = None

    def store(self, text, role="user", mood="neutral"):
        """Stores a thought in both STM and LTM."""
        if not text:
            return

        # 1. Add to Working Memory
        memory_obj = {
            "role": role,
            "content": text,
            "timestamp": time.time(),
            "mood": mood,
        }
        self.working_memory.append(memory_obj)

        # 2. Add to Long Term Memory (Episodic)
        # We only persist "significant" thoughts or periodically merge STM to LTM (consolidation)
        # For now, we persist everything for simplicity but separate by role
        if self.collection:
            try:
                self.collection.add(
                    documents=[text],
                    metadatas=[{"role": role, "timestamp": time.time(), "mood": mood}],
                    ids=[str(uuid.uuid4())],
                )
            except Exception as e:
                logger.error(f"LTM Storage Error: {e}")

    def recall(self, query, n_results=3, include_recent=True):
        """
        Retrieves context.
        Combines Working Memory (recent context) + Relevant Episodic Memory (past context).
        """
        context = []

        # Get immediate context from STM
        if include_recent:
            context.extend(list(self.working_memory))

        # Retrieve similar past memories
        if self.collection and query:
            try:
                results = self.collection.query(
                    query_texts=[query], n_results=n_results
                )
                if results and results.get("documents"):
                    for i, doc in enumerate(results["documents"][0]):
                        context.append(
                            {
                                "role": "system_recall",
                                "content": doc,
                                "metadata": results["metadatas"][0][i],
                            }
                        )
            except Exception as e:
                logger.error(f"LTM Recall Failed: {e}")

        return context

    def get_working_context_str(self):
        """Returns STM formatted for LLM Prompt."""
        return "\n".join(
            [f"{m['role'].upper()}: {m['content']}" for m in self.working_memory]
        )
