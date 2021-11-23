from fastapi import FastAPI
from pydantic import BaseModel

import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ProjectRow(BaseModel):
    title: str
    author: str
    url: str

@app.get("/groupbuys", response_model=list[ProjectRow])
async def groupbuys():
    url = "https://geekhack.org/index.php?board=70.0"

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        tbody = soup.find("tbody")
        rows = list(tbody.find_all("tr"))
        rows.pop(0) # Remove first row in list

        # Iterate through list of rows
        subjects = []
        for i in range(len(rows)):
            row = rows[i]

            subject = row.find(class_="subject windowbg2")
            if subject is not None:
                links = list(subject.find_all("a", href=True))
                
                title = links[0].get_text()
                title_link = links[0]["href"]
                author = links[1].get_text()
                
                subjects.append(ProjectRow(title=title, author=author, url=title_link))

        return subjects
    except Exception as e:
        print('Scraping failed with exception...')
        print(e)