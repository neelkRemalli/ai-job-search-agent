from pydantic import BaseModel


class JobPosting(BaseModel):
    """A job posting returned by a job search."""

    title: str
    company: str
    location: str
    url: str
    description: str
    required_skills: list[str]


class JobSearchResponse(BaseModel):
    """The jobs found in a search response."""

    jobs: list[JobPosting]
