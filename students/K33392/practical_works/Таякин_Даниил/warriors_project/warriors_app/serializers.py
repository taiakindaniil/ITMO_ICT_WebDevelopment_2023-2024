from rest_framework import serializers
from .models import *

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["title"]


class WarriorSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer()
    skills = SkillSerializer(many=True)
    class Meta:
        model = Warrior
        fields = "__all__"


class SkillOfWarriorSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    class Meta:
        model = SkillOfWarrior
        fields = ["skill", "level", "warrior"]