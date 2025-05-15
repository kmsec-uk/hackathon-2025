import feedparser
import aiohttp
import asyncio

# TODO: do something with RSS feeds

headers = {
    "Accept": "application/rss+xml, application/rdf+xml;q=0.8, application/atom+xml;q=0.6, application/xml;q=0.4, text/xml;q=0.4"
}
class RSSError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RSS:
    session: aiohttp.ClientSession | None

    def __init__(self, session: aiohttp.ClientSession | None = None):
        self.session = session

    def _get_session(self) -> aiohttp.ClientSession:
        """return a handle on an aiohttp session"""
        if not self.session:
            _session = aiohttp.ClientSession(trust_env=True)
            self.session = _session
        return self.session
    
    async def parse_feed(self, url: str):
        async with self._get_session():
            async with self.session.get(url, headers=headers) as resp:
                if not resp.ok:
                    raise RSSError(f"unexpected status from {url} : {resp.status}")
                
                feedparser.parse(resp.read())

async def test():
    async with aiohttp.ClientSession(trust_env=True) as session:
        rss = RSS()
        rss.parse_feed("")

if __name__ == "__main__":
    asyncio.run(test())