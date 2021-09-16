from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse

#getting username
parser = argparse.ArgumentParser()
parser.add_argument('--uname', type=str, help='Enter your username')
args = parser.parse_args()
def repoConnection(username):
    
    #Establishing connection ...
    reponse = requests.get('https://github.com/' + username +  '?tab=repositories')
    if reponse.status_code != 200:
        raise Exception("Failed to find the user kindly check your 'username'")
   
    #Getting text document
    url_page = reponse.text
    
    #Getting document as beautiful soup object
    soup = BeautifulSoup(url_page , 'html.parser')
    return soup
repo_con = repoConnection(username=args.uname)

def gitRepository(repo_con):
    
    #Pretifying will clean the unnecesary tags
    repo_con.prettify()
    
    #Finding parent class for repository using class name
    repo_tags = "wb-break-all"
    repository = repo_con.find_all('h3',{'class':repo_tags})

    #Repository List
    repo_list = []
    
    #Finding repostiory name
    for i in range(len(repository)):
        repo = repository[i].find('a')
        repo = repo.text.strip()
        repo_list.append(repo)
    return repo_list

gitrepo = gitRepository(repo_con)

#Repository dictionary
repo_dict = {f'{args.uname} Repository List': gitrepo}

#Repository dataframe
repo_df = pd.DataFrame(repo_dict)
repo_df.head()
repo_df.to_csv(f'{args.uname} repository list.csv',index =None)





