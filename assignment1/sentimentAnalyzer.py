from dataclasses import dataclass

#Stores data from reviews
@dataclass
class Review:
  rating: str
  post: list

  def __init__(self, rating, post):
    self.rating = rating
    self.post = post

#Class to store data for negative and positive words
@dataclass
class Word:
  word: str
  sentiment: float

  def __init__(self, word):
    self.word = word
    self.sentiment = 0

#Parses review file to create Review instances.
def getReviews():
  data = []
  with open('./data/posts', 'r') as f:
    rating = ""
    post = []

    for line in f:
      lineText = line.split()

      if lineText[0] == "rating:":
        rating = lineText[1]
      if lineText[0] == "review:":
        data.append(Review(rating, lineText[1::]))
  return data


# Gets positive/negative words from a file
def getWordsFromFile(filename):
  words = []

  with open(filename, "r") as f:
    for line in f:
      if (line[len(line) - 1] == '\n'):
        words.append(Word(line[:-1:]))
  return words

# Calculates a word's sentiment. Higher is better for positive,
#     while the opposite is true for negative.
def getSentiment(targetWord, reviews):
  ratingCounts = {
    "1.0": 0,
    "2.0": 0,
    "3.0": 0,
    "4.0": 0,
    "5.0": 0
  }

  # Count occurences of word in reviews with each rating.
  for review in reviews:
    for word in review.post:
      if targetWord.word == word:
        ratingCounts[review.rating] += 1
  
  # Calculate score 
  totalHits = sum(ratingCounts.values())
  score = 0
  if (totalHits > 0):
    score = ((ratingCounts["5.0"] * 5 ) + (ratingCounts["4.0"] * 4) + (ratingCounts["3.0"] * 3) + (ratingCounts["2.0"] * 2) + ratingCounts["1.0"]) / totalHits
  return score

# Processes a word list and prints result
def processList(wordList, shouldReverse):
  listName = "negative" if shouldReverse else "positive"
  for word in wordList:
    word.sentiment = getSentiment(word, posts)

  wordList.sort(key=lambda x: x.sentiment, reverse=shouldReverse)

  print(f'Most {listName} words: {[word.word for word in wordList[:10]]}')

print("Parsing words...")
negative = getWordsFromFile("./data/negative")
positive = getWordsFromFile("./data/positive")
print("Parsing reviews...")
posts = getReviews()

print("Scoring negative words...")
processList(negative, True)

print("Scoring positive words...")
processList(positive, False)

