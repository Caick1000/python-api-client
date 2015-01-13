import urllib2
import urllib
import json
from functools import partial
class Api():
	def __init__(self,apiKey,cache = None):
		self.apiKey = apiKey
		self.cache = cache

		self.CACHE_TIME = 86400

		self.SEARCH_ENDPOINT = 'http://food2fork.com/api/search'
		self.VIEW_ENDPOINT   = 'http://food2fork.com/api/get'

	def search(self,query,page,pageSize):
		url = self._urlHelper(self.SEARCH_ENDPOINT,q=query,page=page,count=pageSize)
		try:
			contents = self.cache('s_%s_%d_%d'%(query,page,pageSize), partial(self._getUrlContents,url), self.CACHE_TIME)
			data = json.loads(contents)
			self._doctorImage(data)
			return data
		except Exception as inst:
			print inst
			return None

	def getTopRated(self,page,pageSize):
		try:
			url = self._urlHelper(self.SEARCH_ENDPOINT,page=page,count=pageSize)
			contents = self.cache('top_%d_%d'%(page,pageSize), partial(self._getUrlContents,url), self.CACHE_TIME)
			
			print contents
			data = json.loads(contents)
			data = self._doctorImage(data)
			return data
		
		except Exception as inst:
			print inst
			return None
	
	def getTrending(self,page,pageSize):
		try:
			url = self._urlHelper(self.SEARCH_ENDPOINT,page=page,count=pageSize,sort='t')
			contents = self.cache('trend_%d_%d'%(page,pageSize), partial(self._getUrlContents,url), self.CACHE_TIME)
			
			print contents
			data = json.loads(contents)
			self._doctorImage(data)
			return data
		
		except Exception as inst:
			print inst
			return None

	def getRecipe(self,recipeId):
		url = self._urlHelper(self.VIEW_ENDPOINT,rId=recipeId)
		try:
			contents = self.cache('top_%s'%recipeId, partial(self._getUrlContents,url), self.CACHE_TIME)
			data = json.loads(contents)
			return data
		except Exception as inst:
			print inst
			return None

	def _urlHelper(self,endpoint,**kwargs):
		data = dict()
		data['key'] = self.apiKey
		for key,value in kwargs.iteritems():
			data[key] = value
		print data
		print endpoint + '?' + urllib.urlencode(data)
		return endpoint + '?' + urllib.urlencode(data)

	def _getUrlContents(self,url):
		try:
			response = urllib2.urlopen(url)
			contents = response.read()
		except Exception as inst:
			print inst
			return None

		return contents


	def _doctorImage(self,data):
		if 'recipes' in data:
			for recipe in data['recipes']:
				recipe['image_url'] = recipe['image_url'].replace('food2fork.com','firstrecipes.net')
		elif 'recipe' in data:
			data['recipe']['image_url'] = data['recipe']['image_url'].replace('food2fork.com', 'firstrecipes.net')

		return data


