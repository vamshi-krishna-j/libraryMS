import time
import requests


class OpenLibraryApi:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, rate_limit=1.0):
        self.rate_limit = rate_limit  # seconds between requests
        self.last_request_time = 0

    def _throttle(self):
        """Ensure rate limit of 1 request per second."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def _get(self, endpoint):
        """Make a throttled GET request to the Open Library API."""
        self._throttle()
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API request failed for {url}: {e}")
            return {}

    def search_author(self, author_name):
        """
        Search for an author by name.
        Returns the API response with matching author entries.
        """
        return self._get(f"/search/authors.json?q={author_name}")

    def get_author_works(self, author_key):
        """
        Get list of works for a given author key.
        """
        return self._get(f"/authors/{author_key}/works.json")

    def get_work_details(self, work_key):
        """
        Get detailed information about a specific work.
        """
        clean_key = work_key.split("/")[-1]
        return self._get(f"/works/{clean_key}.json")

    def get_work_editions(self, work_key: str) -> dict:
        """
        Get edition data for a specific work, including ISBNs.
        """
        key = work_key.split("/")[-1]
        return self._get(f"/works/{key}/editions.json")

    def fetch_works(self, author_key, limit=10):
        """
        Get a limited list of works for a given author.
        """
        data = self.get_author_works(author_key)
        return data.get("entries", [])[:limit]
