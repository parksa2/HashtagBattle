from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Battle, BattleTag
from .serializers import BattleSerializer, BattleTagSerializer
from django.db.models import Count, Min, Sum, Avg, Max
import json
@api_view(['GET'])
def battle_list(request):
	if request.method == 'GET':
		battles = Battle.objects.all()
		serializer = BattleSerializer(battles, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def winner(request, pk):
	if request.method == 'GET':
		if pk is None:
			return Response({"Error: battle id not found"}, status=status.HTTP_400_BAD_REQUEST)
		battleTags = BattleTag.objects.filter(battle=pk)
		minimum = battleTags.all().aggregate(Min('typos'))
		m=battleTags.filter(typos= minimum['typos__min'])[0]
		battle = Battle.objects.filter(id=pk)
		serializedBattle = BattleSerializer(battle, many=True)
		serializedMax = BattleTagSerializer(m, many=False)

		resp = {
			'battle': serializedBattle.data,
			'tags': BattleTagSerializer(battleTags, many= True).data,
			'winning': serializedMax.data
		}
		return Response(resp)