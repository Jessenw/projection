import requests
from bs4 import BeautifulSoup

class Scraper:

    def scrape(self):
        file_service = FileService()

        url = "https://geekhack.org/index.php?board=70.0"

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

                print("Title:" + title + " " + "Author: " + author)
                
                subjects.append((title, author, title_link))

                # Now we want to get data from each post
                post_url = title_link
                post_page = requests.get(post_url)
                post_soup = BeautifulSoup(post_page.content, "html.parser")

                post = post_soup.find("div", class_="inner")
                content = post.contents
                file_service.export(title, content)

class FileService:
    def export(self, filename, content):
        output_file = open(filename + '.txt', 'w')

        for j in range(len(content)):
            output_file.write(str(content[j]))
            output_file.write("\n")

        output_file.close()

scraper = Scraper()
scraper.scrape()