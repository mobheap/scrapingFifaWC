from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [i for i in range(1930, 2025, 4)]       #remember that there were no world cups during 1942 and 1946
years.remove(1942)
years.remove(1946)

def get_matches(year):
    website = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(website)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for year {year}")
        return pd.DataFrame()
    
    content = response.text
    
    soup = BeautifulSoup(content, 'lxml')

    matches = soup.find_all('div', class_='footballbox')

    home = []
    score = []
    away = []

    for match in matches:
        home_team = match.find('th', class_='fhome')
        score_result = match.find('th', class_='fscore')
        away_team = match.find('th', class_='faway')
        
        if home_team and score_result and away_team:
            home.append(home_team.get_text().strip())
            score.append(score_result.get_text().strip())
            away.append(away_team.get_text().strip())

    matches_dict = {'home': home, 'score': score, 'away': away}
    football_df = pd.DataFrame(matches_dict)
    football_df['year'] = year
    return football_df

fifa = pd.DataFrame()
for year in years:
    matches_df = get_matches(year)
    fifa = pd.concat([fifa, matches_df], ignore_index=True)

fifa.to_csv('fifa_world_cup_matches.csv', index=False)