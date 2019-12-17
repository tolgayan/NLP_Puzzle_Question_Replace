"""
This program scrapes all puzzle clues and answers from https://nytimescrosswordanswers.com/new-york-times-the-mini-crossword-answers

@date: 13.12.2019
"""

from requests import get
from bs4 import BeautifulSoup
import csv

# =====================================================================================================================================================================

# CONSTANTS

numOfPages  = 92 # number of pages to scrape. There are 92 pages in total. Code checks for non-exist pages, so big numbers does not crash the code.
root_url    = 'https://nytimescrosswordanswers.com/new-york-times-the-mini-crossword-answers'
website_url = "https://nytimescrosswordanswers.com"

# =====================================================================================================================================================================

def getPuzzleUrls(url: str) -> list:
    """
    Auxiliary function for getAllPuzzleUrls
    Returns all urls from a single page. (There are 91 pages and approximately 20 puzzle link in each page.)
        :param url:str: a url to parse puzzle urls
    """
    try:
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        puzzle_containers = html_soup.find_all('div', class_ = 'result')
        puzzle_urls = [website_url + container.a["href"] for container in puzzle_containers]
        return puzzle_urls
    
    except:
        print("getPuzzleUrls: URL error " + str(url))
        return None 

# =====================================================================================================================================================================

def getAllPuzzleUrls(root_url: str) -> list:
    """
    finds and returns all the urls of the puzzles
        :param root_url:str: root url of the puzzles
    """
    url = None
    all_puzzle_urls = []
    
    for i in range(1, numOfPages + 1):   
        print("current page: " + str(i))     
        url = root_url + "?page=" + str(i)
        puzzle_urls = getPuzzleUrls(url)
        
        if puzzle_urls != None:
            all_puzzle_urls += puzzle_urls

    return all_puzzle_urls

# =====================================================================================================================================================================

def getSolutionUrls(url: str) -> list:
    """
    auxiliary function for getAllSolutionUrls.
    gets the solutions of a single url. In other words, solutions of a single puzzle
        :param url:str: url to scrape
    """
    
    try:
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        soln_containers = html_soup.find_all('div', class_ = 'result')
        solutionUrls = [website_url + container.h1.a["href"] for container in soln_containers]
        return solutionUrls
    except:
        print("getSolutionUrls: URL error: " + str(url))
        return None


# =====================================================================================================================================================================

def getAllSolutionUrls(urls: list) -> list:
    """
    finds and returns all the solution-clue urls
        :param urls:list: list of urls to scrape
    """
    allSolutionUrls = []

    for index, url in enumerate(urls):
        print("current puzzle: " + str(index))
        solutionUrls = getSolutionUrls(url)

        if solutionUrls != None:
            allSolutionUrls += solutionUrls

    return allSolutionUrls    

# =====================================================================================================================================================================

def getSolutionCluePair(url: str) -> tuple:
    
    try:
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        clue = html_soup.find("div", class_ = "jumbotron").h1.text
        
        answer = ""

        answerContainer = html_soup.find("div", class_ = "letters")
        spans = answerContainer.find_all("span")

        for span in spans:
            answer += span.text

        saveToCSV((clue, answer))
        return (clue, answer)
    except:
        print("error in the url" + str(url))
        return None


# =====================================================================================================================================================================

def getAllSolutionCluePairs(urls: list) -> list:
    
    solutionPairs = []

    for index, url in enumerate(urls):
        print("scraping clue - answer pair: " + str(index))
        pair = getSolutionCluePair(url)

        if pair != None:
            solutionPairs.append(pair)

    return solutionPairs

# =====================================================================================================================================================================

def saveToCSV(pair: tuple):
    
    with open('puzzlepairs.csv', "a", newline="") as f:
        wr = csv.writer(f)        
                
        if len(pair[1]) <= 5:
            wr.writerow(pair)

# =====================================================================================================================================================================

if __name__ == "__main__":

    urls = getAllPuzzleUrls(root_url)    
    print("num of puzzle urls found: " + str(len(urls)))
    
    solutionUrls = getAllSolutionUrls(urls)
    print("num of solution urls found: " + str(len(solutionUrls)))

    solutionPairs = getAllSolutionCluePairs(solutionUrls)
    
    
