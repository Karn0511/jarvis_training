"""
Real-time Web Search Engine for Venom
Integrates Google Search with AI processing for intelligent answers.
"""

import asyncio
from datetime import datetime
from typing import Optional
from ai_core.core.logger import logger

try:
    from googlesearch import search

    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False

try:
    import google.generativeai as genai
    from ai_core.core.config import config

    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class VenomSearchEngine:
    """
    Advanced Real-time Search Engine with AI Processing.
    Performs Google searches and synthesizes results with AI.
    """

    def __init__(self):
        self.enabled = GOOGLE_SEARCH_AVAILABLE and GENAI_AVAILABLE

        if not GOOGLE_SEARCH_AVAILABLE:
            logger.warning("googlesearch-python not installed. Search unavailable.")
            logger.info("Install: pip install googlesearch-python")

        if not GENAI_AVAILABLE:
            logger.warning("Google Generative AI not available for search synthesis.")

        if self.enabled:
            logger.organ("SEARCH", "Real-time Search Engine ONLINE")
        else:
            logger.organ("SEARCH", "Search Engine OFFLINE (Missing dependencies)")

    async def google_search(self, query: str, num_results: int = 5) -> list[dict]:
        """
        Perform Google search and return structured results.

        Args:
            query: Search query
            num_results: Number of results to fetch

        Returns:
            List of dicts with title, description, url
        """
        if not GOOGLE_SEARCH_AVAILABLE:
            return []

        logger.organ("SEARCH", f"Searching: {query}")

        try:
            # Run search in executor to avoid blocking
            search_results = await asyncio.to_thread(
                lambda: list(search(query, advanced=True, num_results=num_results))
            )

            formatted_results = []
            for result in search_results:
                formatted_results.append(
                    {
                        "title": getattr(result, "title", "No title"),
                        "description": getattr(result, "description", "No description"),
                        "url": getattr(result, "url", ""),
                    }
                )

            logger.success(f"Found {len(formatted_results)} results for: {query}")
            return formatted_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def format_search_results(self, results: list[dict], query: str) -> str:
        """
        Format search results as a readable string.

        Args:
            results: List of search result dicts
            query: Original query

        Returns:
            Formatted string of results
        """
        if not results:
            return f"No results found for: {query}"

        output = f"Search results for '{query}':\n[START]\n\n"

        for i, result in enumerate(results, 1):
            output += f"{i}. {result['title']}\n"
            output += f"   {result['description']}\n"
            if result["url"]:
                output += f"   URL: {result['url']}\n"
            output += "\n"

        output += "[END]"
        return output

    async def search_and_synthesize(self, query: str, num_results: int = 5) -> str:
        """
        Search the web and synthesize an AI answer from results.

        Args:
            query: User's question/search query
            num_results: Number of search results to use

        Returns:
            AI-synthesized answer based on search results
        """
        if not self.enabled:
            return "Search engine unavailable. Please install required dependencies."

        # Perform search
        results = await self.google_search(query, num_results)

        if not results:
            return f"Could not find information about: {query}"

        # Format results for AI
        search_data = self.format_search_results(results, query)

        # Synthesize with AI
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            model = genai.GenerativeModel(config.SMART_MODEL)

            # Create context-aware prompt
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            synthesis_prompt = f"""You are an advanced AI assistant with real-time internet information.

Current Date/Time: {current_time}

User Question: {query}

Search Results:
{search_data}

Instructions:
- Provide a professional, accurate answer based on the search results
- Use proper grammar, punctuation, and formatting
- Cite information where relevant
- If the search results don't fully answer the question, say so
- Be concise but comprehensive

Answer:"""

            logger.organ("SEARCH", "Synthesizing answer with AI...")

            response = await asyncio.to_thread(
                lambda: model.generate_content(synthesis_prompt)
            )

            answer = response.text
            logger.success("Search synthesis complete")
            return answer

        except Exception as e:
            logger.error(f"AI synthesis failed: {e}")
            # Fallback to formatted results
            return search_data

    async def quick_search(self, query: str) -> str:
        """
        Quick search that returns formatted results without AI synthesis.
        Faster but less intelligent than search_and_synthesize.

        Args:
            query: Search query

        Returns:
            Formatted search results
        """
        if not self.enabled:
            return "Search unavailable."

        results = await self.google_search(query)
        return self.format_search_results(results, query)

    async def search_and_open(self, query: str):
        """
        Search and open top result in browser.

        Args:
            query: Search query
        """
        if not GOOGLE_SEARCH_AVAILABLE:
            return "Search unavailable."

        try:
            import webbrowser

            results = await self.google_search(query, num_results=1)

            if results and results[0]["url"]:
                webbrowser.open(results[0]["url"])
                return f"Opening: {results[0]['title']}"
            else:
                return "No results found."
        except Exception as e:
            logger.error(f"Failed to open result: {e}")
            return f"Error: {e}"


# Global instance
_search_engine_instance = None


def get_search_engine() -> VenomSearchEngine:
    """Get or create the global search engine instance."""
    global _search_engine_instance
    if _search_engine_instance is None:
        _search_engine_instance = VenomSearchEngine()
    return _search_engine_instance


if __name__ == "__main__":
    # Test
    async def test():
        engine = VenomSearchEngine()
        answer = await engine.search_and_synthesize("What is quantum computing?")
        print(answer)

    asyncio.run(test())
