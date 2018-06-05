from rest_framework import serializers
from .models import Battle, BattleTag, Tag

class BattleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Battle
		fields = ('id', 'name', 'start_date', 'end_date',)

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('tag_text','id')

class BattleTagSerializer(serializers.ModelSerializer):
	tag = TagSerializer('tag')
	class Meta:
		model = BattleTag
		fields = ('typos','tag')