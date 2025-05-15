#! /usr/bin/env python3

""" 
    Classes for interacting with GitHub Security Advisory Database and enriching CVE data
    Author: Kieran

"""

import aiohttp
import asyncio
import os
from sentiment import sid

class GitHubError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EnrichmentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class GHSA:
    """
    Representation of a connection to GitHub Security Advisories.

    Example:

    ```python

    ```
    
    """
    apikey: str
    session: aiohttp.ClientSession | None
    advisories : list
    def __init__(self, apikey: str, session: aiohttp.ClientSession | None = None):
        self.apikey = apikey
        self.session = session
        self.advisories = [] # list of dict representation of GHSA objects as described https://docs.github.com/en/rest/security-advisories/global-advisories?apiVersion=2022-11-28#list-global-security-advisories

    def _get_session(self) -> aiohttp.ClientSession:
        """return a handle on an aiohttp session"""
        if not self.session:
            _session = aiohttp.ClientSession(trust_env=True)
            self.session = _session
        return self.session

    async def get_recent(self):
        """retrieve recent CVE data from GHSA"""
        
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization" : f"Bearer {self.apikey}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        async with self._get_session():
            async with self.session.get(
                "https://api.github.com/advisories", 
                headers=headers) as resp:
                if not resp.ok:
                    raise GitHubError(f"unexpected response from GSA : {resp.status}")
                self.advisories = [adv for adv in await resp.json() if adv.get("cve_id") is not None]

class CVE:
    """
    Representation of a CVE.
    
    To get an enrichment of a CVE
    """
    cve_id: str
    session: aiohttp.ClientSession | None
    strings: list[str] # list of raw strings

    def __init__(self, cve_id: str, session: None | aiohttp.ClientSession = None):
        """initialise CVE"""
        self.cve_id = cve_id.lower()
        self.session = session
    
    def _get_session(self) -> aiohttp.ClientSession:
        """return a handle on an aiohttp session"""
        if not self.session:
            _session = aiohttp.ClientSession(trust_env=True)
            self.session = _session
        return self.session
        
    async def get_data(self):
        """gets data for the CVE"""
        async with self._get_session():
            await self.scrape_ddg()
            # TODO: get further context on top of DDG
    
    async def scrape_ddg(self):
        """
        get context text on the vulnerability and set the `strings`
        attribute.
        """
        params = {
            "url": f"https://html.duckduckgo.com/html/?q={self.cve_id}",
            "selector": ".result__body",
            "scrape": "text",
            "pretty": "false"
        }
        async with self.session.get(
            "https://web.scraper.workers.dev/", 
            params=params) as resp:
            if not resp.ok:
                raise EnrichmentError(f"unexpected status from web scraper: {resp.status}")
            j = await resp.json()
            self.strings = j["result"][".result__body"]


async def generate_test_data():
    apikey = os.environ["GITHUB_APIKEY"]
    test_data = []
    # generate test data
    async with aiohttp.ClientSession(trust_env=True) as session:
        ghsa = GHSA(apikey=apikey, session=session)
        await ghsa.get_recent()
        for advisory in ghsa.advisories:
            print(f'{advisory["published_at"]}: {advisory["cve_id"]}')
            cve = CVE(advisory["cve_id"])
            await cve.get_data()
            advisory["_enrichment"] = cve.strings
            ss = sid.polarity_scores(" ".join(cve.strings))
            advisory["_sentiment"] = ss["compound"]
            test_data.append(advisory)
    # dump test data
    import json
    from pathlib import Path
    outfile = Path("test_data.json")
    with outfile.open(mode="wt") as f:
        f.write(json.dumps(test_data, indent=2, ensure_ascii=False))
if __name__ == "__main__":
    asyncio.run(generate_test_data())
