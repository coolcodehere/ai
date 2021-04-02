import random
import math

def getFiles(mode):
  ret = []
  
  if mode == "SPAM":
    i = 0
    for i in range(1, 601):
      f = open(f"data/spam/{i}.txt", "r")
      words = f.readlines()[0].replace("\n", "").split(" ")
      ret.append(words)
      f.close
  elif mode == "HAM":
    for i in range(1, 301):
      f = open(f"data/ham/1/{i}.txt", "r")
      words = f.readlines()[0].replace("\n", "").split(" ")
      ret.append(words)
      f.close
    for i in range(1, 301):
      f = open(f"data/ham/2/{i}.txt", "r")
      words = f.readlines()[0].replace("\n", "").split(" ")
      ret.append(words)
      f.close
  
  random.shuffle(ret)
  return ret

def countWords(data):
  wordMap = {}
  numWords = 0

  for email in data:
    seen = []
    for word in email:
      if word in seen:
        continue
      if word in wordMap:
        wordMap[word] += 1
      else:
        wordMap[word] = 1
      seen.append(word)
      numWords += 1

  return numWords, wordMap


def train(data, counts):
  prob = {}
  for word in data:
      prob[word] = (data[word] + 1) / (counts + len(list(data.keys())))

  return prob

def classify(data, probs):
  tPos = 0
  tNeg = 0
  fPos = 0
  fNeg = 0

  for email in data:
    pSpam = 0
    pHam = 0
    for word in email[0]:
      pHam += probs[0][word] if word in probs[0] else 0.5
      pSpam += probs[1][word] if word in probs[1] else 0.5

    if email[1] == 1 and pSpam < pHam:
      tPos += 1
    elif email[1] == 0 and pHam < pSpam:
      tNeg += 1
    elif email[1] == 1 and pSpam > pHam:
      fPos += 1
    elif email[1] == 0 and pHam > pSpam:
      fNeg += 1

  accuracy = (tPos + tNeg) / (tPos + tNeg + fPos + fNeg)
  precision = (tPos) / (tPos + fPos)
  recall = (tPos) / (tPos + fNeg)
  f1 = 2 * (precision * recall) / (precision + recall)
  print(f"Accuracy: {round(accuracy * 100, 2)}%.")
  print(f"Precision: {round(precision * 100, 2)}%.")
  print(f"Recall: {round(recall * 100, 2)}%.")
  print(f"F1: {round(f1 * 100, 2)}%.")


hamFiles = getFiles("HAM")
spamFiles = getFiles("SPAM")
totalEmails = len(hamFiles) + len(spamFiles)
numTraining = 1000

print("Training with", numTraining, "emails.")
testing = []
random.shuffle(hamFiles)
random.shuffle(spamFiles)
for i in range(0, totalEmails - numTraining, 2):
  testing.append((hamFiles[0], 0))
  hamFiles.pop(0)
  testing.append((spamFiles[0], 1))
  spamFiles.pop(0)

hamCounts, totalHamWords = countWords(hamFiles)
spamCounts, totalSpamWords = countWords(spamFiles)

pSpam = train(totalSpamWords, spamCounts)
pHam = train(totalHamWords, hamCounts)

classify(testing, (pHam, pSpam))