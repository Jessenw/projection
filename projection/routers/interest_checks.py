from fastapi import APIRouter

import requests
from bs4 import BeautifulSoup

from models.project import Project
from models.project_preview import ProjectPreview, ProjectPreviews


router = APIRouter()


@router.get("/interest_checks", response_model=ProjectPreviews)
async def interest_checks():
    url = "https://geekhack.org/index.php?board=132.0"

    print("Scraping... {url}")

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        tbody = soup.find("tbody")
        rows = list(tbody.find_all("tr"))

        # The first row can be discarded since it only shows
        # number of users viewing the board 
        rows.pop(0)

        # Iterate through list of rows
        projects = []
        for i in range(len(rows)):
            row = rows[i]

            subject = row.find(class_="subject windowbg2")
            if subject is not None:
                # Find the url on the title
                links = list(subject.find_all("a", href=True))
                title_url = links[0]["href"]

                # Extract the topic id from the url
                topic_substring = 'topic='
                topic_index = title_url.find(topic_substring) + len(topic_substring)
                id = title_url[topic_index:]
                
                title = links[0].get_text()
                author = links[1].get_text()

                # Sanitise title
                title = str(title).replace("[GB] ", "")

                projects.append(ProjectPreview(title=title, author=author, id=id))

        return ProjectPreviews(projects=projects)
    except Exception as e:
        print('Scraping failed with exception...')
        print(e)
