import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-f1", required = True, help = "path of training file")
ap.add_argument("-f2", required = True, help = "path of testing file")
ap.add_argument("-o", required = True, help = "path of output file")
args = vars(ap.parse_args())
train_file = args['f1']
test_file = args['f2']
output_file = args['o']

wordict = set() # to keep track of unique words
actualclass = [] # actual class 
predictedclass = [] # predicted class
word_lists = {} # unique words dict
c_prob = {} # conditional probabailites

def initialization():
    trainingfile = open(train_file,'r')
    for evryline in trainingfile:
        newline = evryline.split(" ")
        for i in range(2, len(newline), 2):
            wordict.add(newline[i])
    c_prob["spam"] = {}
    c_prob["ham"] = {}
    word_lists["spam"] = {}
    word_lists["ham"] = {}
    for w in wordict:
        word_lists["spam"][w] = 0
        word_lists["ham"][w] = 0
    trainingfile.close()

def classifier():
    total_mails = 0
    mail_types = {}
    mail_types["spam"] = 0
    mail_types["ham"] = 0
    trainingfile = open(train_file,'r')
    for evryline in trainingfile:
        newline = evryline.split(" ")
        total_mails += 1
        mail_types[newline[1]] += 1
        for i in range(2, len(newline), 2):
            word_lists[newline[1]][newline[i]] += 1
    l = len(wordict)
    # calculate cond_probabalities
    for w, c in word_lists["spam"].items():
        c_prob["spam"][w] = float(c + 1) / float(mail_types["spam"] + l)
    for w, c in word_lists["ham"].items():
        c_prob["ham"][w] = float(c + 1) / float(mail_types["ham"] + l)

def classify():
    s = 0
    h = 0
    test_data = open(test_file,'r')
    output_data = open(output_file,'w')
    # count total spam word and ham word counts
    for w, c in word_lists["spam"].items():
        s += c
    for w, c in word_lists["ham"].items():
        h += c
    for evryline in test_data:
        ph = 0.0
        ps = 0.0
        newline = evryline.split(" ")
        actualclass.append(newline[1])
        # using laplace smoothing
        for i in range(2, len(newline), 2):
            ps += math.log10(c_prob["spam"][newline[i]])
            ph += math.log10(c_prob["ham"][newline[i]])
        if ps > ph:
             predictedclass.append("spam")
             output_data.write(newline[0]+ " " + "spam" + "\n")
        else:
            predictedclass.append("ham")
            output_data.write(newline[0] + " " + "ham" + "\n")
    test_data.close()
    output_data.close()

def measureperformance():
    correct_s = 0
    correct_h = 0
    incorrect_s = 0
    incorrect_h = 0

    for val1, val2 in zip(actualclass, predictedclass):
        if val1 in "spam" and val2 in "spam":
            correct_s += 1
        elif val1 in "spam" and val2 in "ham":
            incorrect_s += 1
        elif val1 in "ham" and val2 in "ham":
            correct_h += 1
        else:
            incorrect_h += 1
    # spam and ham accuracy
    p = (float(correct_s) /float(correct_s + incorrect_s)) * 100
    h = (float(correct_h) / float(correct_h + incorrect_h)) * 100
    print("Spam Detection Precision : " + str(p))
    print("Ham Detection Precision : " + str(h))

if __name__ == "__main__":
    initialization()
    classifier()
    classify()
    measureperformance()