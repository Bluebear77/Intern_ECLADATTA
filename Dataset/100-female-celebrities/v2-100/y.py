from bs4 import BeautifulSoup

def extract_wiki_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    if not tables:
        return None, "No tables found"
    
    results = []
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr'):
            cols = tr.find_all('td')
            if cols:
                rows.append([td.get_text(strip=True) for td in cols])
        results.append({'headers': headers, 'rows': rows})
    
    return results if results else (None, "No data extracted")

# Example usage
html_content = """
{| class="wikitable"
! Header1
! Header2
|-
| Row1-Cell1
| Row1-Cell2
|-
| Row2-Cell1
| Row2-Cell2
|}
"""
data, message = extract_wiki_table_data(html_content)
print(data, message)
