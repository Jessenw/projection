from fastapi import FastAPI

import requests
from bs4 import BeautifulSoup

from models.project_preview import ProjectPreview
from models.project import Project

api = FastAPI()

@api.get("/groupbuys/{project_id}", response_model=Project)
async def groupbuy(project_id: str):
    # TODO: Need to find a better solution since the seesion id is likely to be temporary
    url = "https://geekhack.org/index.php?PHPSESSID=a3u8pj2r51sr3cd3ka19v60mu8tg4tuo&topic=" + project_id

    print("Scraping... " + url)

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # This doesn't include comments
        post = soup.find("div", class_="inner")
        # print(post.contents)
        contents = str(post.contents)

        # We need to perform some clean up before returning
        contents = contents.replace("\'", " ")

        contents = contents.replace(">,", ">")
        contents = contents.replace(", <", "<")

        contents = contents.replace("> ", ">")
        contents = contents.replace(" <", "<")
        contents = contents.replace("> ", ">")

        print(contents)
        return Project(content=contents)
    except Exception as e:
        print('Scraping failed with exception...')
        print(e)


@api.get("/groupbuys", response_model=list[ProjectPreview])
async def groupbuys():
    url = "https://geekhack.org/index.php?board=70.0"

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

                projects.append(ProjectPreview(title=title, author=author, id=id))

        return projects
    except Exception as e:
        print('Scraping failed with exception...')
        print(e)