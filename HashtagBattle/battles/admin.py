# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Battle, Tag, BattleTag, Tweet
from django.db.models import Q
from django.utils import timezone
from enchant.checker import SpellChecker
from datetime import datetime
from django.conf import settings
import logging
import tweepy
import json
import enchant
import pytz

APP_KEY = settings.TWITTER_AUTH['APP_KEY']
APP_SECRET = settings.TWITTER_AUTH['APP_SECRET']

OAUTH_TOKEN = settings.TWITTER_AUTH['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = settings.TWITTER_AUTH['OAUTH_TOKEN_SECRET']

logger = logging.getLogger(__name__)
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	def __init__(self, startDate, endDate, tagsDict):
		self.startDate = startDate
		self.endDate = endDate
		self.tagsDict = tagsDict
		super(MyStreamListener, self).__init__()

	def on_data(self, status):
		if timezone.now()>= self.endDate:
			return False

		data = json.loads(status)
		createdDate = data['created_at']
		apiId = data['id']
		text = data['text']
		truncated = data['truncated']
		lang = data['lang']
		if truncated:
			text = data['extended_tweet']['full_text']
			relevantTagData = data['extended_tweet']['entities']['hashtags']
		else:
			relevantTagData = data['entities']['hashtags']
		if lang == 'en':
			typos = self.__countTypos(text)

			convertedCreatedDate = datetime.strptime(createdDate,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)

			for val in self.__findRelevantTags(relevantTagData):
				tweet_instance = Tweet.objects.create(typos=typos,create_date=convertedCreatedDate,api_id=apiId,tag=val)
				tweet_instance.save()

	def __findRelevantTags(self, hashTags):
		relatedTags = []
		for tag in hashTags:
			if tag['text'] in self.tagsDict:
				relatedTags.append(self.tagsDict[tag['text']])
		return relatedTags

	def __countTypos(self, text):
		try:
			checker = SpellChecker("en_UK","en_US")
			if text is not None:
				checker.set_text(text)
				errCount = 0
				for err in checker:
					word = str(err.word)
					if word[0]=='#' or word[0]=='@' : #check if misspelled word is actually just a hashtag or @ tag. Can use natural language lib here 
						continue
					errCount = errCount+1
				return errCount;
			return 0
		except:
			logger.error("Problem with spell checker")
			return 0

	def on_error(self, status):		
		logger.error('Problem occurred in twitter stream data')

class SuperAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		tagsList = BattleTag.objects.filter(Q(battle=obj.battle)).exclude(id=obj.id)
		hashTag = obj.tag.tag_text
		startDate = obj.battle.start_date
		endDate = obj.battle.end_date
		try:
			if len(tagsList) >= 1: #only start filtering once tag has opponent
				filters = []
				tagsDict = {}
				filters.append('#'+hashTag)
				tagsDict[hashTag] = obj.tag
				for x in tagsList:
					filters.append('#'+x.tag.tag_text)
					tagsDict[x.tag.tag_text] = x.tag # map given text to complete hashTag object for easy database writing later
				myStreamListener = MyStreamListener(startDate, endDate, tagsDict)
				myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
				myStream.filter(track=filters, async=True)
		except tweepy.TweepError:
			logger.error('Error! Failed to get request token.')

		super().save_model(request, obj, form, change)

	def _callApi(self,startDate, endDate, hashTag):
		data = twitter.search(q=hashTag, count=100)
		return data

	readonly_fields = ('typos',)

admin.site.register(Battle)
admin.site.register(Tag)
admin.site.register(BattleTag, SuperAdmin)

# Register your models here.
