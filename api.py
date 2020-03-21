import praw as p
import re
import os
import matplotlib.pyplot as plt
import numpy as np
import tqdm


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


def findCommentsInSubreddit(sub, numberOfPosts, numberOfComments, r, filterPath):
    data = ""
    totalComments = 0
    subreddit = r.subreddit(sub)
    os.mkdir(sub)
    for submission in subreddit.hot(limit=numberOfPosts):
        path = deEmojify(submission.title)
        path = re.sub('[\W_]+', '', path)
        path += '.txt'
        path = sub + '/' + path
        f = open(path, 'a+')
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            totalComments += 1
            body = comment.body
            body = deEmojify(body)
            data += body
            data += '\n\n'
            if totalComments > numberOfComments:
                break
    print("Total comments downloaded: ", totalComments)
    data = filterText(data, filterPath)
    f.write(data)
    return data


def findUserPosts(sub, numberOfPosts, r, filterPath):
    data = ""
    redditor = r.redditor(sub)
    f = open(sub + '.txt', 'a+')
    for submission in redditor.hot(limit=numberOfPosts):
        if isinstance(submission, p.reddit.Comment):
            path = deEmojify(submission.body)
        else:
            path = deEmojify(submission.title)
        data += path
        data += "\n\n"
    data = filterText(data, filterPath)
    f.write(data)
    return data


def filterText(text, filterPath):
    if filterPath == '':
        return text
    f = open(filterPath, "r")
    wordList = ""
    for line in f.readlines():
        wordList += line
    wordList.upper()
    text = text.upper()
    wordList = wordList.split("\n")
    for word in wordList:
        text.replace(word, "")
    return text


def dataAnalytics(data):
    countArray = []
    dataArray = []
    # remove useless characters
    data = filterText(data, "specialCharacters.txt")
    data = data.split()

    # count words in the array
    for word in data:
        if word not in dataArray:
            dataArray.append(word)
            countArray.append(1)
        else:
            countArray[dataArray.index(word)] += 1

    # Sorting arrays
    data = []
    for i in dataArray:
        data.append([i, countArray[dataArray.index(i)]])
    data.sort(key=lambda tup: tup[1], reverse=True)

    dataArray = []
    countArray = []
    for i in data:
        dataArray.append(i[0])
        countArray.append(i[1])

    # Plot graph
    yPos = np.arange(len(dataArray))
    plt.bar(yPos, countArray, align='center', alpha=0.5)
    plt.xticks(yPos, dataArray)
    plt.show()


print("-------------------------------------------")
print("Reddit Comment Downloader")
print("-------------------------------------------")
print()
sub = input("Type the name of subreddit (without the r/): ")
numberOfPosts = int(input("Type the amount of posts you want: "))
numberOfComments = int(input("Type how many comments per post you want: "))
r = p.Reddit(client_id='JWAodBCQtfEVIA', client_secret='FhUwy1rIAZnWuZC0YgOKLhVkA50', user_agent='Comment Collection Bot')

data = findCommentsInSubreddit(sub, numberOfPosts, numberOfComments, r, '')
print("Got Data!")
dataAnalytics(data)
