from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import *
from .serializers import *

class WarriorsAPIView(APIView):
    def get(self, request):
        warriors = Warrior.objects.all()
        serializer = WarriorSerializer(warriors, many=True)
        return Response({"Warriors": serializer.data})


class WarriorAPIView(APIView):
    def get(self, request, pk: int):
        try:
            warrior = Warrior.objects.get(pk=pk)
        except Warrior.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        serializer = WarriorSerializer(warrior)
        return Response(serializer.data)

    def delete(self, request, pk: int):
        try:
            warrior = Warrior.objects.get(pk=pk)
        except Warrior.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        warrior.delete()

        return Response()
    
    def patch(self, request: Request, pk: int):
        try:
            warrior = Warrior.objects.get(pk=pk)
        except Warrior.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        for k, v in request.data.items():
            setattr(warrior, k, v)
        warrior.save()

        return Response(request.data)


class ProfessionCreateView(APIView):
    def post(self, request):
        profession = request.data.get("profession")
        serializer = ProfessionSerializer(data=profession)

        if serializer.is_valid(raise_exception=True):
            profession_saved = serializer.save()

        return Response({"Success": "Profession '{}' created succesfully.".format(profession_saved.title)})


class SkillOfWarriorAPIView(APIView):
    def get(self, request: Request, warrior_pk: int):
        try:
            # Retrieve warrior
            try:
                warrior = Warrior.objects.get(pk=warrior_pk)
            except Warrior.DoesNotExist:
                return Response(None, status=status.HTTP_404_NOT_FOUND)

            # Retrieve all SkillOfWarrior instances from the database
            skills_of_warriors = SkillOfWarrior.objects.filter(warrior=warrior)

            # Serialize the data
            serializer = SkillOfWarriorSerializer(skills_of_warriors, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, format=None):
        try:
            # Deserialize the incoming data
            serializer = SkillOfWarriorSerializer(data=request.data)
            if serializer.is_valid():
                # Save the new SkillOfWarrior instance
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
