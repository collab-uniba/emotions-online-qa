import csv, re
from HTMLParser import HTMLParser
import string
import jpype
import os

body1 = "The worldwide diffusion of social media has profoundly changed the way we communicate and access information. Increasingly, people try to solve domain-specific problems through interaction on social online Question and Answer (Q&A) sites. The enormous success of Stack Overflow, a community of 2.9 million programmers asking and providing answers about code development, attests this increasing trend. One of the biggest drawbacks of communication through social media is to appropriately convey sentiment through text. While display rules for emotions exist and are widely accepted for traditional face-to-face interaction, people might not be prepared for effectively dealing with the barriers of social media to non-verbal communication. Though, emotions matter, especially in the context of online Q&A communities where social reputation is a key factor for successful knowledge sharing. As a consequence, the design of systems and mechanisms for fostering emotional awareness in computer-mediated communication is becoming an important technical and social challenge for research in computer-supported collaborative work and social computing."

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def del_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def del_code(html):
	return re.sub('\<code>(.*?)\</code>', '', html)

def clean_body(html):
	return del_tags(del_code(html))

def del_punctuation(text):
	return text.translate(string.maketrans ("" , ""), string.punctuation)

def get_senti_score(corpus):
	print os.path.abspath("..")+"/lib"
	jpype.startJVM("/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea", "-Djava.class.path="+os.path.abspath(".")+";"+os.path.abspath("..")+"/lib/SentiStrength.jar")
	S = jpype.JClass('Sentiment')
	sentiment = S()
	#print a.sayHi()

	corpus_cleaned = corpus#del_punctuation(clean_body(corpus))

	senti_score = sentiment.SentiStrengthgetScore(corpus_cleaned)
	s = senti_score.split(",")
	pos = s[0]
	neg = s[1]
	print "Pos: ",pos
	print "Neg: ",neg
	jpype.shutdownJVM()
	return senti_score



get_senti_score(body1)

