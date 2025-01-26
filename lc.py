import requests
from bs4 import BeautifulSoup

def scrape_leetcode_problem(url):
    try:
        # Send a GET request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the problem statement
        problem_statement = soup.find('div', {'class': 'content__u3I1 question-content__JfgR'})
        if problem_statement:
            problem_statement = problem_statement.get_text(separator='\n')
        else:
            print("Problem statement not found.")
            problem_statement = None
        
        # Extract the starter code (usually inside a <code> tag within a <pre> tag)
        starter_code = soup.find('pre')
        if starter_code:
            starter_code = starter_code.get_text()
        else:
            print("Starter code not found.")
            starter_code = None
        
        return problem_statement, starter_code
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return None, None

# Example usage
url = 'https://leetcode.com/problems/two-sum/'  # Replace with the URL of the problem you want to scrape
problem_statement, starter_code = scrape_leetcode_problem(url)

if problem_statement:
    print("Problem Statement:")
    print(problem_statement)

if starter_code:
    print("\nStarter Code:")
    print(starter_code)