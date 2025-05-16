
from vulny.sentiment import sid

log4j = """Apache Log4j Vulnerability Guidance - CISA www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance An adversary can exploit CVE-2021-44228 by submitting a specially crafted request to a vulnerable system that causes that system to execute arbitrary code. The request allows the adversary to take full control over the system. The adversary can then steal information, launch ransomware, or conduct other malicious activity. ..."""

ms_scripting_engine = """CVE-2025-30397: Critical Memory Corruption Flaw in Windows Scripting ... windowsforum.com/threads/cve-2025-30397-critical-memory-corruption-flaw-in-windows-scripting-engine-exploitation-threat.366062/ &nbsp; &nbsp; 2025-05-14T00:00:00.0000000 A newly disclosed security vulnerability, tracked as CVE-2025-30397, has captured the attention of the Windows community and cybersecurity professionals worldwide. This scripting engine memory corruption vulnerability in Microsoft&#x27;s Scripting Engine—commonly underpinning legacy browsers and critical scripting capabilities—demands careful analysis, not only for its technical underpinnings ..."""

def main():
    print(f"log4shell (CVE-2021-44228): {sid.polarity_scores(log4j)["compound"]}") #  -0.8689
    print(f"msedge (CVE-2025-30397) : {sid.polarity_scores(ms_scripting_engine)["compound"]}") # -0.5267

if __name__ == "__main__":
    main()