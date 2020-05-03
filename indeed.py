# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

LIMIT =  50
URL = "https://www.indeed.com/jobs?q=python&limit={}".format(LIMIT)

def extract_indeed_pages():
    #indeed url & parsing
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    #finding page-lists
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')

    #storing pages
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
        title = html.find("h2", {"class": "title"}).find("a")["title"]
        company = html.find("span", {"class": "company"})
        company_anchor = company.find("a")
        if company.find("a") != None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
        location = html.find("div", {"class": "recJobLoc"})['data-rc-loc']
        job_id = html["data-jk"]

        return {'title': title,
                'company': company,
                'location': location,
                "link": "https://www.indeed.com/viewjob?jk={}".format(job_id)
                }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print("Scrapping page {}".format(page))
        result = requests.get("{}&start={}".format(URL, 0*LIMIT))
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs
