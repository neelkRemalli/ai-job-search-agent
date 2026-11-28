"""Job search tool with clear handling for unavailable search services."""

from langchain.tools import tool
from langchain_tavily import TavilySearch

from app.config import get_settings


def _make_search_client() -> TavilySearch:
    """Build the Tavily client when a search is requested."""

    settings = get_settings()
    return TavilySearch(
        max_results=5,
        tavily_api_key=settings.tavily_api_key.get_secret_value(),
    )


@tool
def search_jobs(query: str) -> str:
    """Search the web for job postings and explain service failures clearly."""

    cleaned_query = query.strip()
    if not cleaned_query:
        return "Please provide a job search query."

    try:
        response = _make_search_client().invoke({"query": cleaned_query})
    except Exception as exc:
        # Do not return credentials or a traceback to the caller. Search results
        # should never be invented when the upstream service is unavailable.
        error_name = type(exc).__name__
        return (
            "Job search is temporarily unavailable because the search service "
            f"could not be reached ({error_name}). Please try again later."
        )

    return str(response)
