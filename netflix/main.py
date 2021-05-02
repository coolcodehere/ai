import numpy as np 
import pandas as pd 
from scipy import spatial

netflix = pd.read_csv("./netflix_ratings.csv")

# make encoding dict of sentences in rating descriptions.
def getEncodingDict():
  encodingDict = {}
  ratings = netflix['ratingDescription'].values
  ratings = [x.split('.') for x in ratings if isinstance(x, str)]
  ratings = list(np.concatenate(ratings).flat)
  ratings = list(filter(lambda x: x != '', ratings))
  ratings = list(set(ratings))
  ratings = list(map(lambda x: x.strip(), ratings))
  for rating in ratings:
    encodingDict[rating] = np.random.rand(15)
  
  return encodingDict

def addMatrices(title, encodingDict):
  sum_ = np.zeros(15)

  data = netflix[['title', 'ratingDescription']]
  data = data.loc[data['title'] == title]
  data = data['ratingDescription'].values[0]
  if not isinstance(data, str):
    return sum_
  
  data = list(filter(lambda x: x != '', data.split(".")))
  data = list(map(lambda x: x.strip(), data))
  
  for description in data:
    sum_ = np.add(sum_, encodingDict[description])

  return sum_

def getMovieDict(encodingDict):
  movieDict = {}
  for title in netflix['title'].values:
    movieDict[title] = addMatrices(title, encodingDict)
  userRatings = netflix[['title', 'user rating score']].dropna()
  for title in userRatings.values:
    movieDict[title[0]] = np.append(movieDict[title[0]], title[1])
  
  for key in movieDict.keys():
    movieDict[key] = movieDict[key][0:16]

  return movieDict

encodingDict = getEncodingDict()
movieDict = getMovieDict(encodingDict)
similarityDict = {}

movieDict["Naruto"]

for key in movieDict.keys():
  if len(movieDict[key]) != 16 or key == "Naruto":
    continue
  similarityDict[key] = 1 - spatial.distance.cosine(movieDict["Naruto"], movieDict[key])


print("The 10 closest shows/movies to Naruto are:")
i = 1
for item in sorted(similarityDict.items(), key=lambda x: x[1])[:10]:
  print(str(i) + ": " + item[0])
  i += 1