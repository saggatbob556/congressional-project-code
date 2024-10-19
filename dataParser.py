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
    return df.at[df.query('CategoryNames == \'' + categoryName + '\'').index[0], 'Category']
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
#not exact, brand can be a substring of the entire brand name
def getData(brand):
    return df[df['Brand'].str.contains(brand)]
#brand is the exact brand name, used when user chooses a specific brand when searching and multiple brands with the substring come up
def getRatingOfSpecific(brand):
    return df.at[df.query('Brand == \'' + str(brand) + '\'').index[0], 'Rating']
def getPraiseOf(brand):
    return df.at[df.query('Brand == \'' + str(brand) + '\'').index[0], 'Praise']
def getCriticismOf(brand):
    return df.at[df.query('Brand == \'' + str(brand) + '\'').index[0], 'Criticism']
#def getAlternative(brand):

