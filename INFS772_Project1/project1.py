__author__ = 'Juan Harrington'#Please type your name here. 
import json
import sys
import matplotlib.pyplot as plt
import datetime
import string

def processWords(inputfile, outputfile):
    # inputfile is the original file
    # outputfile is the updated file
    # sort words alphabetically in updated files
    input = open(inputfile, "r").readlines()
    lines_set = set(input)
    out = open(outputfile,"w")
    for line in sorted(lines_set):
        out.write(line)
    out.close()
    return

def read_stocktwits():
    f = open("BAC.json","r")
    json_txt = f.read()
    root = json.loads(json_txt)
    f.close()
    output = []
    lis  = []
    for row in root:
        body = row["body"].encode("ascii","ignore").lower().replace("\n","").translate(string.maketrans("",""), string.punctuation)
        if row["entities"]["sentiment"] is None:
            sentiment = "Unknown"
        else:
            sentiment = row["entities"]["sentiment"]["basic"].encode("ascii","ignore")
        created = datetime.datetime.fromtimestamp(float(row["created_at"]["$date"])/1000.).strftime("%Y-%m-%d %H:%M:%S")
        s = created +","+ body +","+ sentiment
        lis.append(s)
    f = open("BAC.csv","w")
    for item in lis:
        f.write("%s\n" % item)
    f.close()
    return

def sentiment_analysis():
    # init list
    output = []
    posCount = -1
    negCount = -1
    # open and read file
    f = open("BAC.csv","r")
    lines = f.readlines()
    f.close()
    # loop through rows and conduct sentiment analysis
    for line in lines:
        # split line into an array
        lis = line.split(",")
        # assign assign array values to variables
        created = lis[0]
        body = lis[1]
        sentiment = lis[2].strip() # remove new line character "\n"
        # check if sentiment unknown
        if sentiment == "Unknown":
            # for each tweet count the number of positive and negative words in the tweets
            # if the numbers are equal or they are both 0, you designate the sentiment of the tweet to be "Neutral".
            # if there are more positive words than negative ones, the sentiment is "Bullish", and "Bearish" otherwise.
            # do negative analysis
            f = open("negative_words_updated.txt","r")
            neg_list = f.readlines()
            f.close()
            body_list = list(body.split(" "))
            negCount = count_string_occurences(neg_list, body_list)
            # do positive analysis
            f = open("positive_words_updated.txt","r")
            pos_list = f.readlines()
            f.close()
            posCount = count_string_occurences(pos_list, body_list)
            # compare positive and negative word counts
            if posCount == negCount or posCount + negCount == 0:
                sentiment = "Neutral"
            if posCount > negCount:
                sentiment = "Bullish"
            if negCount > posCount:
                sentiment = "Bearish"
        # create string with created date and sentiment
        s = created +","+ sentiment 
        #print s
        output.append(s)
    # create file
    f = open("BAC2.csv","w")
    for item in output:
        f.write("%s\n" % item)
    f.close()

    return

def get_sentiment_dates(start_date, end_date):
    positive_dict = {} 
    negative_dict = {}
    neutral_dict = {}

    # create the datetime.datetime class instance.
    start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    start_dt = start_dt.date()
    end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    end_dt = end_dt.date()
        
    f = open("BAC2.csv","r")
    rows = f.readlines()
    f.close()

    for row in rows:
        lis = row.split(",")
        created = lis[0]
        sentiment = lis[1].strip()
      
        # create the datetime.datetime class instance.
        dt = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
        dt = dt.date()

        # Compare the subsequent dates.
        if dt >= start_dt and dt <= end_dt:
            if sentiment == "Bullish":
                #add count to date
                if not dt in positive_dict:
                    positive_dict[dt] = 1
                else:
                    positive_dict[dt] = positive_dict[dt] + 1
            if sentiment == "Bearish":
                #add count to date
                if not dt in negative_dict:
                    negative_dict[dt] = 1
                else:
                    negative_dict[dt] = negative_dict[dt] + 1
            if sentiment == "Neutral":
                #add count to date
                if not dt in neutral_dict:
                    neutral_dict[dt] = 1
                else:
                    neutral_dict[dt] = neutral_dict[dt] + 1
 
    return [positive_dict,negative_dict,neutral_dict]

def drawing_pie(start_date, end_date):
    r = get_sentiment_dates(start_date, end_date)

    positive_sum = sum(r[0].values())
    negative_sum = sum(r[1].values())
    neutral_sum = sum(r[2].values())
    total_sum = positive_sum + negative_sum + neutral_sum

    positive_ratio =  100 * float(positive_sum)/float(total_sum)
    negative_ratio = 100 * float(negative_sum)/float(total_sum)
    neutral_ratio = 100 * float(negative_sum)/float(total_sum)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [positive_ratio, negative_ratio, neutral_ratio]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title("Sentiment is ")
    plt.show()
    return

def drawing_lines(start_date, end_date):
    r = get_sentiment_dates(start_date, end_date)

    positive_sorted = sorted(r[0].iteritems())
    px,py=zip(*positive_sorted)
   
    negative_sorted = sorted(r[1].iteritems())
    nx,ny = zip(*negative_sorted)

    neutral_sorted = sorted(r[2].iteritems())
    tx,ty = zip(*neutral_sorted)

    fig, ax = plt.subplots()
    ax.plot(px,py, 'o-', label='Positive')
    ax.plot(nx,ny, 'o-', label='Negative')
    ax.plot(tx,ty, 'o-', label='Neutral')
    ax.set_title("Sentiment between %s and %s" % (start_date,end_date))
    ax.legend(loc='upper right')
    fig.autofmt_xdate()
    plt.show()
    return

# utility function to count occurences of words in a string from a reference list
def count_string_occurences(ref_list,input_list):
    total_occurences = 0
    for w in ref_list:
        total_occurences += input_list.count(w.strip())
    return total_occurences

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
