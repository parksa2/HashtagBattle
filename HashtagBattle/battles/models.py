# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)
class Tag(models.Model):
	tag_text = models.CharField(max_length=200)

	def __str__(self):
		return self.tag_text

class Battle(models.Model):
	name = models.CharField(max_length=200)
	start_date = models.DateTimeField('start date')
	end_date = models.DateTimeField('end date')
	tags = models.ManyToManyField(Tag, through='BattleTag')

	def __str__(self):
		return self.name

class BattleTag(models.Model):
	typos = models.IntegerField(default=0)
	tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
	battle = models.ForeignKey(Battle, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.battle)+' : '+str(self.tag)

class Tweet(models.Model):
	create_date = models.DateTimeField('create date')
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	api_id = models.CharField(max_length=200) #id found provided in the twitter api
	typos = models.IntegerField(default=0)

@receiver(post_save, sender=Tweet)
def tweet_post_save(sender, instance, **kwargs): #Update all relevant battle-tags. Though it won't restart the stream for old previously halted comparisons.
	logger.info('Added New Tweet Into DB')
	relevantBattleTags = BattleTag.objects.filter(Q(tag=instance.tag))
	for tag in relevantBattleTags:
		if tag.battle.start_date<=instance.create_date and tag.battle.end_date>=instance.create_date:
			BattleTag.objects.filter(id=tag.id).update(typos=(tag.typos+instance.typos))

