# coding=utf-8
"""
Translate a given text or sentense in the desired language
"""
import requests
import json
from bs4 import BeautifulSoup
lang_names = ["Arabic|ar","Bulgarian|bg","Catalan|ca","Chinese Simplified|zh-CHS","Chinese Traditional|zh-CHT","Czech|cs","Danish|da","Dutch|nl","English|en","Estonian|et","Finnish|fi","French|fr","German|de","Greek|el","Haitian Creole|ht","Hebrew|he","Hindi|hi","Hmong Daw|mww","Hungarian|hu","Indonesian|id","Italian|it","Japanese|ja","Klingon|tlh","Klingon (pIqaD)|tlh-Qaak","Korean|ko","Latvian|lv","Lithuanian|lt","Malay|ms","Maltese|mt","Norwegian|no","Persian|fa","Polish|pl","Portuguese|pt","Romanian|ro","Russian|ru","Slovak|sk","Slovenian|sl","Spanish|es","Swedish|sv","Thai|th","Turkish|tr","Ukrainian|uk","Urdu|ur","Vietnamese|vi","Welsh|cy"]

sentence = "A dictionary’s keys are almost arbitrary values. Values that are not hashable, that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys. Numeric types used for keys obey the normal rules for numeric comparison: if two numbers compare equal (such as 1 and 1.0) then they can be used interchangeably to index the same dictionary entry. (Note however, that since computers store floating-point numbers as approximations it is usually unwise to use them as dictionary keys."
sentence2 = "I am heading to a restaurant to have lunch, afterwhich we are planning to catch up a movie"

def get_header():
	"""
	Return the Header which is to be passes in each translate get requests
	"""

	post_req_para = {'client_id':'ravirnjn88', 'client_secret':'gDKLRV3lWnmP8EDsGvqoYSF1CCQvA2VRKYfyCjwGaNw=', 'scope':'http://api.microsofttranslator.com', 'grant_type':'client_credentials'}
	r = requests.post("https://datamarket.accesscontrol.windows.net/v2/OAuth2-13",data=post_req_para)
	headers = {}
	headers['Authorization'] = "Bearer %s" % (r.json()['access_token'])
	return headers

def translate_text(text,from_lang,to_lang):
	"""
	Translate the given text in desired language
	"""
	translate_req_para = {'text':text,'from':from_lang,'to':to_lang}
	r = requests.get("http://api.microsofttranslator.com/V2/Http.svc/Translate",params=translate_req_para,headers=get_header())
	soup = BeautifulSoup(r.content)
	return soup.find('string').string.encode('utf-8')

#print translate_text(sentence2,'en','fr')

def break_sentences(text,from_lang):
	"""
	Returns the list type: 
	Length of the list is the no of sentences in the text
	Values of the list is the letter count of that sentence
	"""
	break_sent_para={'text':text,'language':from_lang}
	r = requests.get("http://api.microsofttranslator.com/V2/Http.svc/BreakSentences",params=break_sent_para,headers=get_header())
	soup = BeautifulSoup(r.content)
	words_in_sent = []
	for sent_length in soup.findAll('int'):
		words_in_sent.append(str(sent_length.text))
	return words_in_sent

#print len(break_sentences(sentence,'en'))

def frndly_name_lang(lang):
	"""
	get the friendly name of the language. Input is a list of desired language i.e.['en','fr','hi'] 
	api not working: giving friendly name of all the languages instead of for the ask one

	"""
	lang_names = ["Arabic|ar","Bulgarian|bg","Catalan|ca","Chinese Simplified|zh-CHS","Chinese Traditional|zh-CHT","Czech|cs","Danish|da","Dutch|nl","English|en","Estonian|et","Finnish|fi","French|fr","German|de","Greek|el","Haitian Creole|ht","Hebrew|he","Hindi|hi","Hmong Daw|mww","Hungarian|hu","Indonesian|id","Italian|it","Japanese|ja","Klingon|tlh","Klingon (pIqaD)|tlh-Qaak","Korean|ko","Latvian|lv","Lithuanian|lt","Malay|ms","Maltese|mt","Norwegian|no","Persian|fa","Polish|pl","Portuguese|pt","Romanian|ro","Russian|ru","Slovak|sk","Slovenian|sl","Spanish|es","Swedish|sv","Thai|th","Turkish|tr","Ukrainian|uk","Urdu|ur","Vietnamese|vi","Welsh|cy"]
	friendly_name =[]
	for elements1 in lang:
		for elements2 in lang_names:
			if elements2.split('|')[1] == elements1:
				friendly_name.append(elements2.split('|')[0])
				break 
	return friendly_name
#ravi = ['en','fr','hi','nl','et']
#print frndly_name_lang(ravi)

def detect_lang(text):
	"""
	Detect the language of the given text
	"""
	detect_lang_para={'text':text}
	r = requests.get("http://api.microsofttranslator.com/V2/Http.svc/Detect",params=detect_lang_para,headers=get_header())
	soup = BeautifulSoup(r.content) 
	return frndly_name_lang([soup.find('string').text])[0]

#print detect_lang('مطعم لتناول')

def command_line():
	def check_lang_in_list(lang):
		lang =lang
		flag =0
		for element in lang_names:
			if element.split('|')[1]==lang:
				flag =1
				break
		if flag ==0:
			print 'language not in list Terminating !!!!'

	def comm_trans_text():
		print "You have selected to translate a given text. Available Language for Translation are :"
		print "English Name \t Language Code"
		for elements in lang_names:
			print "%s \t \t %s" %(elements.split('|')[0],elements.split('|')[1])
		print "\nEnter the text for translation"
		z = raw_input()
		print "What is the Language Code of the input text"
		a = raw_input()
		print "Enter the Language Code to which it is translated"
		b = raw_input()
		print "Your Translate text is %s" %(translate_text(z,a,b))

	def comm_detect_lang():
		print "You want to detect the language of the given text"
		print "Enter the text"
		c = raw_input()
		print "Given text is in %s" %(detect_lang(c))

	def comm_count_letters():
		print "Enter the text for letter calculation"
		d = raw_input()
		print "What is the language code for this text"
		e = raw_input()
		f= break_sentences(d,e)
		print "No of Sentence in the given text are %s and the letters in each word are %s" % (len(f), f)

	print "Welcome to microsoft translator"
	print "Enter the Desired Option"
	print "1. Translate text 	2. Detect Language 	3. Calculate Sentenses and and letters"
	y = input()
	if y==1:
		comm_trans_text()
	if y==2:
		comm_detect_lang()
	if y==3:
		comm_count_letters()
	if y!=1 and y!=2 and y!=3:
		print "Wrong Input !!! Lets Start again"
		command_line()
command_line()

