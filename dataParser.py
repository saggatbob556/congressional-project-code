import pandas as pd
import re

df = pd.read_csv('unsorted.csv')
def getProductsInCategoryNum(category):
    return df[df['Category'] == category]
def getProductsInCategoryName(categoryName):
    return df[df['CategoryNames'] == categoryName]
def getNameOfCategoryNum(category):
    return df.at[df.query('Category == ' + str(category)).index[0], 'CategoryNames']
def getNumOfCategoryName(categoryName):
    try:
        return df.at[df.query('CategoryNames == \'' + categoryName + '\'').index[0], 'Category']
    except:
        return getLastCategoryNum() + 1
def getLastCategoryNum():
    return df['Category'].max()
def getBestOfCategory(category):
    if not df.query('Category == ' + str(category) + ' and Rating == \'A\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'A\'')
    if not df.query('Category == ' + str(category) + ' and Rating == \'B\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'B\'')
    if not df.query('Category == ' + str(category) + ' and Rating == \'C\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'C\'')
    if not df.query('Category == ' + str(category) + ' and Rating == \'D\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'D\'')
    if not df.query('Category == ' + str(category) + ' and Rating == \'F\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'F\'')
    if not df.query('Category == ' + str(category) + ' and Rating == \'?\'').empty:
        return df.query('Category == ' + str(category) + ' and Rating == \'?\'')
def getData(brand):
    print(brand)
    return "Brand: " + brand + "     Category: " + getCategoryNameOf(brand)
#not exact, brand can be a substring of the entire brand name
def getLine(brand):
    return df[df['Brand'].str.contains(brand)]
#brand is the exact brand name, used when user chooses a specific brand when searching and multiple brands with the substring come up
def getRatingOf(line):
    return df.loc[line, 'Rating']
def getPraiseOf(line):
    return df.at[line, 'Praises']
def getCriticismOf(line):
    return df.at[line, 'Criticisms']
def getCategoryOf(line):
    return df.loc[line, 'Category']
def getCategoryNameOf(line):
    return df.loc[line, 'CategoryNames']
def getAlternativeBrand(line):
    print("aoidj: " + str(line))
    return getBestOfCategory(getCategoryOf(line))
def getAlternativeCategory(category):
    return getBestOfCategory(category)
def addNewProduct(brand, rating, category, criticism, praise, categoryName):
    with open('unsorted.csv', 'a') as df:
        df.write('\n' + brand + ',' + rating + ',' + str(category) + ',' + criticism + ',' + praise + ',' + categoryName)
        df = pd.read_csv('unsorted.csv')
def searchBrandWithinCategory(brand, categoryName):
    return df.query('Brand.str.contains(\'' + str(brand) + '\', case=False)' + ' and CategoryNames.str.contains(\'' + str(categoryName) + '\', case=False)')
