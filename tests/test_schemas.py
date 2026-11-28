import unittest

from pydantic import ValidationError

from app.schemas import JobPosting, JobSearchResponse


class JobSchemaTests(unittest.TestCase):
    def test_job_posting_can_be_created(self):
        job = JobPosting(
            title="Software Engineer",
            company="Example Co",
            location="Remote",
            url="https://example.com/jobs/1",
            description="Build useful software.",
            required_skills=["Python"],
        )

        self.assertEqual(job.title, "Software Engineer")
        self.assertEqual(job.required_skills, ["Python"])

    def test_search_response_accepts_job_postings(self):
        job = JobPosting(
            title="Software Engineer",
            company="Example Co",
            location="Remote",
            url="https://example.com/jobs/1",
            description="Build useful software.",
            required_skills=["Python"],
        )

        response = JobSearchResponse(jobs=[job])

        self.assertEqual(response.jobs, [job])

    def test_missing_required_job_posting_field_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            JobPosting(
                company="Example Co",
                location="Remote",
                url="https://example.com/jobs/1",
                description="Build useful software.",
                required_skills=["Python"],
            )

    def test_invalid_required_skills_type_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            JobPosting(
                title="Software Engineer",
                company="Example Co",
                location="Remote",
                url="https://example.com/jobs/1",
                description="Build useful software.",
                required_skills="Python",
            )


if __name__ == "__main__":
    unittest.main()
