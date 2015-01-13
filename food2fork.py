import urllib2
import urllib
import json
from functools import partial


class food2fork():
	'''
	Usage:
		import food2fork
		f2f = food2fork("My Api Key")

		recipes = f2f.search("chicken, rice")

		moreRecipes = f2f.search("chicken, rice", 2)


	'''

	def __init__(self,apiKey, debug=False):
		self.apiKey = apiKey

		self.debugMode = debug

		self.SEARCH_ENDPOINT = 'http://food2fork.com/api/search'
		self.VIEW_ENDPOINT   = 'http://food2fork.com/api/get'
		self.MAX_PAGESIZE = 30

	def search(self,query,page = 1,pageSize = 30):
		try:
			url = self._urlHelper(self.SEARCH_ENDPOINT,q=query,page=page,count=pageSize)

			contents = self._getUrlContents(url)

			data = json.loads(contents)

			if(self.debugMode): print contents

			return data

		except Exception as inst:
			if(self.debugMode): print inst

			return None

	def getTopRated(self,page = 1,pageSize = 30):
		if(pageSize > self.MAX_PAGESIZE): pageSize = self.MAX_PAGESIZE

		try:
			url = self._urlHelper(self.SEARCH_ENDPOINT,page=page,count=pageSize)

			contents = self._getUrlContents(url)
			
			data = json.loads(contents)

			if(self.debugMode): print contents

			return data
		
		except Exception as inst:
			if(self.debugMode): print inst

			return None
	
	def getTrending(self,page = 1,pageSize = 30):
		try:
			url = self._urlHelper(self.SEARCH_ENDPOINT,page=page,count=pageSize,sort='t')

			contents = self._getUrlContents(url)

			data = json.loads(contents)

			if(self.debugMode): print contents

			return data
		
		except Exception as inst:
			if(self.debugMode): print inst

			return None

	def getRecipe(self,recipeId):
		try:
			url = self._urlHelper(self.VIEW_ENDPOINT,rId=recipeId)

			contents = self._getUrlContents(url)

			data = json.loads(contents)

			return data

		except Exception as inst:
			if(self.debugMode): print inst

			return None

	def _urlHelper(self,endpoint,**kwargs):
		data = { 'key' : self.apiKey }

		for key, value in kwargs.iteritems():
			data[key] = value

		if(debugMode):
			print "Url:", endpoint + '?' + urllib.urlencode(data)

		return endpoint + '?' + urllib.urlencode(data)

	def _getUrlContents(self,url):
		try:
			response = urllib2.urlopen(url)

			contents = response.read()

			return contents

		except Exception as inst:
			if(self.debugMode): print inst

			return None



