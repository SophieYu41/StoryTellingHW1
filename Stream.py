import requests, sys, time, json

def main():
	key = "df13fde30560ad95a2adfdacc44b7b2f:17:74351984"
	url = "http://api.nytimes.com/svc/news/v3/content/all/all?api-key=" + key 
	while True:
		response = requests.get(url)
		re = response.json()
		dem = rep = 1
		score_dem = score_rep = 0
		# print time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
		for res in re['results']:
			title = res['title']
			content = res['abstract'] + ' ' + title
			if has_keyword(content, True):
				rep += 1
				score_rep += get_sentiment(res['url'])
			if has_keyword(content, False):
				dem += 1
				score_dem += get_sentiment(res['url'])
		arr = {}
		arr['dem'] = dem
		arr['rep'] = rep
		arr['dem_score'] = 0
		arr['rep_score'] = 0
		if dem != 0:
			arr['dem_score'] = score_dem/dem
		if rep != 0:
			arr['rep_score'] = score_rep/rep
		print json.dumps(arr)
		sys.stdout.flush()		
		time.sleep(10)
	

def has_keyword(content, is_republican):
	keywords_dem = ['Hillary Clinton', 'Bernie Sanders', 'Democratic']
	keywords_rep = ['Jeb Bush', 'Ben Carson', 'Chris Christie', 'Ted Cruz', 'Carly Fiorina',
		 'Donald Trump', 'Jim Gilmore', 'John Kasich', 'Marco Rubio', 'Republican']
	keywords = keywords_dem
	if is_republican:
		keywords = keywords_rep
	for word in keywords:
		if word.lower() in content.lower():
			return True
	return False


def get_sentiment(url):
	base_url = 'http://gateway-a.watsonplatform.net/calls/url/URLGetTextSentiment'
	apikey = '766183b17bf3536a0230746c9943ba3626ac79db'
	entire_url = base_url + '?url=' + url + '&apikey=' + apikey + '&outputMode=json'
	response = requests.get(entire_url)
	re = response.json()
	if 'docSentiment' in re:
		if re['docSentiment']['type'] == 'neutral':
			return 0
		else:
			return float(re['docSentiment']['score'])
	return 0


#print get_sentiment('http://iht-retrospective.blogs.nytimes.com/2016/02/10/1941-britain-breaks-with-rumania/')
#print get_sentiment('http://zeroviscosity.com/d3-js-step-by-step/step-1-a-basic-pie-chart')

main()