import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    """Scrapes full textual content from a given URL using BeautifulSoup."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = []

        # Extract headings (H1-H6)
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            content.append(heading.get_text(strip=True) + "\n")

        # Extract paragraphs
        for paragraph in soup.find_all('p'):
            content.append(paragraph.get_text(strip=True) + "\n")

        # Extract list items (unordered and ordered lists)
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li'):
                content.append("• " + li.get_text(strip=True))  # Bullet point format

        for ol in soup.find_all('ol'):
            for index, li in enumerate(ol.find_all('li'), start=1):
                content.append(f"{index}. {li.get_text(strip=True)}")  # Numbered format

        # Extract text from common article sections
        for section in soup.find_all(['div', 'span', 'article', 'section', 'aside']):
            text = section.get_text(strip=True)
            if text and text not in content:
                content.append(text + "\n")  # Avoid duplicate content

        # Extract table data
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                row_text = ' | '.join(col.get_text(strip=True) for col in cols)
                content.append(row_text)

        # Remove duplicates and empty lines
        final_content = list(dict.fromkeys(filter(lambda x: x.strip(), content)))

        return '\n'.join(final_content)

    return None