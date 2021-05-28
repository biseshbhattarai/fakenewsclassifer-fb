from flask import Flask 
from flask_mongoengine import MongoEngine 
from difflib import SequenceMatcher
from flask import jsonify 
from flask import request
from flask_cors import CORS , cross_origin
from estimator import estimator
from Nepali_nl.Nepali_nlp.sentence_similar import Avg_vector_similar 
from Nepali_nl.Nepali_nlp.Embedding import Embeddings
import requests 
from bs4 import BeautifulSoup 
# from scraper import Scraper 
from sentiment import sentiment 
global_news = []
current_scraped_news = []


# app initiation 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGODB_SETTINGS'] = { 
	'db': 'fnews',
	'host' : 'localhost', 
	'port': 27017

}

logged_in_user = [] #Session 

db = MongoEngine()
db.init_app(app)


# database model 
class User(db.Document):
	username = db.StringField()
	email = db.StringField()
	password = db.StringField()

class News(db.Document):
	news_title = db.StringField()
	detection = db.StringField()
	tested = db.StringField()
	cause = db.StringField()
	similarlity = db.StringField()
	watched = db.StringField()
	source = db.StringField()

class Report(db.Document):
	title = db.StringField()
	news = db.StringField()
	username = db.StringField()


def check_user_exists(email):
	users = db.users 
	if users.find_one({"email":email}): 
		return False


def register_user(username , email, password):
	if(username != '' and email != '' and password != ''):
		if not check_user_exists(email):
			User(username=username, email=email, password=password).save()

# routings 
@app.route('/')
def index_page():
	return "Hello , World"

@app.route('/login' , methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		req_data = request.get_json()
		if req_data['email'] is not None and req_data['password'] is not None:
			print(req_data['email'], req_data['password'])
			userr = User.objects(email=req_data['email']).first()
			print(userr)
			if userr.password == req_data['password']:
				logged_in_user.append(req_data['email'])
				return "Success"
			else:
				print("Wrong password")
				return "Error"

		else:
			return "Error"
		


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		req_data = request.get_json()
		print(req_data)
		User(username=req_data['fullname'], email=req_data['email'], password=req_data['password']).save()
		return "GET"


@app.route('/current_user' , methods=['GET', 'POST'])
def current():
	c_u = ""
	if len(logged_in_user) != 0 : 
		c_u = logged_in_user[0]
		print(c_u)
	elif len(logged_in_user) == 0: 
		c_u = "guest"
	return c_u 

@app.route('/news', methods=['GET', 'POST'])
def receive_news():
	if request.method == 'POST':
		req_data = request.get_json()
		for i in req_data['lines']:
			if i not in current_scraped_news:

				News(news_title=i, detection="Not fake", tested="False", cause="", similarlity="", watched="False", source="Scraped from facebook").save()
				current_scraped_news.append(i)
		process_news()
		s = open('online_khabar.txt', 'r')
		data = s.read()
		cal = []
		
	return "Done"

@app.route('/report', methods=['GET', 'POST'])
def report():
	if request.method == 'POST':
		req_data = request.get_json()
		link = req_data['news']
		print(link)
		res = requests.get(link)
		soup = BeautifulSoup(res.content , 'html.parser')
		titles = soup.title.get_text()
		News(news_title=titles, detection="Fake", tested="True", similarlity="0").save()
		Report(title=titles , news=link, username=logged_in_user[0]).save()
		return "true"


@app.route('/get_report', methods=['GET'])
def get_report():
	report = Report.objects(username=logged_in_user[0]).all()
	a = jsonify(report)
	print(a)
	return a 


@app.route('/direct_detect', methods=['GET', 'POST'])
def direct_detect():
	if request.method == 'POST':
		req_data = request.get_json()
		print(req_data)
		link = req_data['lines']
		res = requests.get(link)
		print(link)
		soup = BeautifulSoup(res.content , 'html.parser')
		titles = soup.title.get_text()
		print("title", titles)
		s = open('online_khabar.txt', 'r')
		data = s.read()
		d = data.split('\n')
		cal = []
		total_s = []
		counter = 0 
		if 'Sidha Kura' in titles : 
			News(news_title=titles, detection="fake" ,tested="True" , cause="News looks irrelevant" , similarlity="0.5", watched='False', source="scraped directly").save()
		else: 
			for i in range(len(d) - 1):
				cal.append(titles)
				cal.append(d[counter])
				s = SequenceMatcher(None , cal[0], cal[1]).ratio()
				total_s.append(s)
				counter += 1 
				cal = []
			similarlity = max(total_s)*100 
			News(news_title=titles, detection="fake" ,tested="True" , cause="News looks irrelevant" , similarlity=str(similarlity), watched='False', source="scraped directly").save()



	
def process_news():

	s = open('online_khabar.txt', 'r')
	data = s.read()
	d = data.split('\n')
	cal = []
	news = News.objects(tested="False").first()
	# Actual detection being done here using AI . 
	senti = sentiment(news.news_title)
	total_s = []
	counter = 0 
	if 'Sidha Kura' in news.news_title:
		news.update(tested="True" , cause="News looks irrelevant" , similarlity="0.5")
	else:
		for i in range(len(d) - 1):

			cal.append(news.news_title)
			cal.append(d[counter])
			# Looks if the scraped news is in other known trusted site . 
			s = SequenceMatcher(None , cal[0], cal[1]).ratio()
			total_s.append(s)

			counter += 1 
			cal = []
		similarlity = max(total_s)*100
		print(similarlity) 
		news.update(tested="True" , cause="News not in trusted site" , similarlity=str(similarlity))


@app.route('/get_news', methods=['GET'])
def get_news():
# gives news to the frontend . 
	news = News.objects(tested="True", watched="False").all()

	a = jsonify(news)
	news.update(watched="True")
	print(a)
	return a
	
	






if __name__ == '__main__':

	app.run(debug=True)
