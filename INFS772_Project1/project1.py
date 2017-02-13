__author__ = 'Juan Harrington'#Please type your name here. 
import json
import sys
import matplotlib.pyplot as plt
import datetime

def processWords(inputfile, outputfile):
    # inputfile is the original file
    # outputfile is the updated file
    # sort words alphabetically in updated files
    lines = open(inputfile, "r").readlines()
    lines_set = set(lines)
    out = open(outputfile,"w")
    for line in sorted(lines_set):
        out.write(line)
    return

def read_stocktwits():
    import string
    f = open("C:/Users/jharrington/Documents/_DSU-MSA/INFS772/Project1/BAC.json")
    json_txt = f.read()
    root = json.loads(json_txt)
    output = []
    lis  = []
    for row in root:
        body = row["body"]
        if row["entities"]["sentiment"] is None:
            sentiment = "Unknown"
        else:
            sentiment = row["entities"]["sentiment"]["basic"]
        created = datetime.datetime.fromtimestamp(float(row["created_at"]["$date"])/1000.)
        if len(lis) < 3:
            lis.append(created.strftime("%Y-%m-%d %H:%M:%S"))
            lis.append(body.encode("ascii","ignore").lower().translate(string.maketrans("",""), string.punctuation))
            lis.append(sentiment.encode("ascii","ignore"))
        if len(lis) == 3:
            output.append(lis)
            lis = []
    fi = open("BAC.csv","w")
    for item in output:
        string = ",".join(item)
        fi.write("%s\n" % string)
    return

def sentiment_analysis():
    return

def get_sentiment_dates(start_date, end_date):
    positive_dict = {} 
    negative_dict = {}
    neutral_dict = {}
    return [positive_dict,negative_dict,neutral_dict]

def drawing_pie(start_date, end_date):
    return

def drawing_lines(start_date, end_date):
    r = get_sentiment_dates(start_date, end_date)
    r.sort()
    r = r[-30]

    # first we'll do it the default way, with gaps on weekends
    fig, ax = plt.subplots()
    ax.plot(r.update, r.adj.close, 'o-')
    fix.autofmt_xdate()
    return

def main():
    processWords("positive_words.txt", "positive_words_updated.txt")
    processWords("negative_words.txt", "negative_words_updated.txt")
    read_stocktwits()# output: BAC.csv
    sentiment_analysis() # output BAC2.csv
    get_sentiment_dates('2013-01-02', '2013-01-31')
    #output of get_sentiment :[{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}][{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}][{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}][datetime.date(2013, 1, 2), datetime.date(2013, 1, 3), datetime.date(2013, 1, 4), datetime.date(2013, 1, 5), datetime.date(2013, 1, 6), datetime.date(2013, 1, 7), datetime.date(2013, 1, 8), datetime.date(2013, 1, 9), datetime.date(2013, 1, 10), datetime.date(2013, 1, 11), datetime.date(2013, 1, 12), datetime.date(2013, 1, 13), datetime.date(2013, 1, 14), datetime.date(2013, 1, 15), datetime.date(2013, 1, 16), datetime.date(2013, 1, 17), datetime.date(2013, 1, 18), datetime.date(2013, 1, 19), datetime.date(2013, 1, 20), datetime.date(2013, 1, 21), datetime.date(2013, 1, 22), datetime.date(2013, 1, 23), datetime.date(2013, 1, 24), datetime.date(2013, 1, 25), datetime.date(2013, 1, 26), datetime.date(2013, 1, 27), datetime.date(2013, 1, 28), datetime.date(2013, 1, 29), datetime.date(2013, 1, 30), datetime.date(2013, 1, 31)]#As you can see in the output, I used datetime.date objects as keys of a dictionary. You can also do this, you can use date strings as keys.
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png - you can see a graph in a pop-up window. you don't need to save the graph
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return

if __name__ == '__main__':
    main()
