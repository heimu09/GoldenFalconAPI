from rest_framework import serializers
from .models import Voter, Material, Nomination, VoteCandidate


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class NominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomination
        fields = '__all__'


class VoterSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    nominations = NominationSerializer(many=True, read_only=True)

    class Meta:
        model = Voter
        fields = ['name', 'photo', 'phone', 'email', 'bio', 'materials', 'nominations']


class VoteCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteCandidate
        fields = ['id', 'name', 'phone', 'position', 'votes', 'password']
        read_only_fields = ['votes']


class VoteSerializer(serializers.Serializer):
    vote_candidate_phone = serializers.CharField()
    vote_candidate_password = serializers.CharField(write_only=True)
    voter_id = serializers.IntegerField()
    nomination = serializers.CharField(max_length=3)
