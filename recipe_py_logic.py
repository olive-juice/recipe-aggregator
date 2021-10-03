# imports
import requests
from bs4 import BeautifulSoup as bs
import re

# GLOBALS
loveandlemonsdict = {
    "site": 'Love and Lemons',
    "head": 'https://www.loveandlemons.com/?s=',
    "tail": '&submit=',
    "splitter": '+',
    "link": 'entry-title'
} 
food52dict = {
    "site": 'Food 52',
    "head": 'https://food52.com/recipes/search?q=',
    "tail": '',
    "splitter": '%20'
} 
sitesList = [loveandlemonsdict,food52dict]
# sitesList = [food52dict]

optionsdict = {}
    # optionsdict will hold the list options from all sources of recipes
    # optionsdict is generated in Search&Return, and then used in ReturnAbbreviated

# Search and Return Results
def listsearchresults(search,optionsdict):
    inc = 1
    for s in sitesList:
        site = s["site"]
        head = s["head"]
        mid = ''
        tail = s["tail"]

        mid = search.replace(' ',s["splitter"])
        page = head+mid+tail

        ## Returning listed results with href links
        page = requests.get(page)
        soup = bs(page.content, 'html.parser')

        limit = 1

        print('\n')
        

        if s['site'] == 'Love and Lemons':
            recipes = soup.find_all(class_="entry-title")

            for recipe in recipes:
                if limit < 4:
                    print(' ', inc, ": ", recipe.get_text())
                    linky = recipe.a.get('href')
                    print(' ', linky,'\n')
                    optionsdict[str(inc)] = [site,linky]
                    inc += 1
                    limit += 1
                else:
                    break
        elif s['site'] == 'Food 52':
            recipes = soup.find_all(class_='collectable__name')

            for recipe in recipes:
                if limit < 4:
                    print(' ', inc, ": ", recipe.get_text())
                    linky = 'https://food52.com'+recipe.a.get('href')
                    print(' ', linky,'\n')
                    optionsdict[str(inc)] = [site,linky]
                    inc += 1
                    limit += 1
                else:
                    break     
                
    return optionsdict

# Return Abbreviated Recipe
def returnrecipe(page,source):
    # Initialize soup
    page = requests.get(page)
    soup = bs(page.content, 'html.parser')
    
# LOVE AND LEMONS
    if source == 'Love and Lemons':
        # flow A
        try:
            print('')
            title = soup.find(class_='wprm-recipe-name wprm-block-text-bold').get_text().strip()
            print('Source: ',source)
            print('Recipe: ',title)

            print('\nIngredients:')

            ingredients = soup.find_all(class_='wprm-recipe-ingredient')
            inc = 1
            for li in ingredients:
                print('>', li.get_text())
                inc += 1

            print('\nInstructions:')

            inc = 1
            instructions = soup.find(class_='wprm-recipe-instructions').find_all('li')
            for li in instructions:
                print(inc, ': ', li.get_text())
                inc += 1

        # flow B
        except:
            print('')
            title = soup.find(class_='ERSName').get_text().strip()
            print(title)

            print('')
            print('Ingredients:')

            ingredients = soup.find_all(itemprop='recipeIngredient')
            inc = 1
            for li in ingredients:
                print('>', li.get_text())
                inc += 1

            print('')
            print('Instructions:')

            ingredients = soup.find_all(itemprop='recipeInstructions')
            inc = 1
            for li in ingredients:
                print(inc, ': ', li.get_text())
                inc += 1
# FOOD 52
    elif source == 'Food 52':
        # flow A
        try:
            print('')
            title = soup.find(class_='recipe__title').get_text().strip()
            print('Source: ',source)
            print('Recipe: ',title)

            print('\nIngredients:')

            ingredients = soup.find(class_='recipe__list--ingredients').find_all('li')
            inc = 1
            for li in ingredients:
                print('>', li.get_text().replace('\n',' ').replace('  ',' '))
                inc += 1

            print('\nInstructions:')

            inc = 1
            instructions = soup.find(class_='recipe__list--steps')
            instructions = instructions.findAll('span')
            for li in instructions:
                print(inc, ': ', li.string.replace('\r','').replace('\n',' ').replace('  ',' '))
                inc += 1
        except:
            source = source


# Ask for search phrase
print('======================================='*3)
search_terms = input("What would you like to search for? \n")
print('======================================='*3)

# Return search page options
listsearchresults(search_terms,optionsdict)

# Ask for a recipe choice
print('======================================='*3)
recipechoice = input("Which recipe would you like to look at?\nPlease type only the number of the recipe. \n")
print('======================================='*3)

# Return recipe summary
source = optionsdict[recipechoice][0]
returnrecipe(optionsdict[recipechoice][1],source)