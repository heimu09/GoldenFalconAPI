from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Voter, Material, Nomination, VoteCandidate, Vote
from .serializers import VoterSerializer, MaterialSerializer, NominationSerializer, VoteCandidateSerializer, VoteSerializer
from django.contrib.auth.hashers import check_password


def authenticate(phone, password) -> VoteCandidate:
    try:
        vote_candidate = VoteCandidate.objects.get(phone=phone)
    except VoteCandidate.DoesNotExist:
        return None

    password_valid = check_password(password, vote_candidate.password)

    if password_valid:
        return vote_candidate

    return None


def cast_vote(vote_candidate_phone, vote_candidate_password, voter_id, nomination):
    vote_candidate = authenticate(phone=vote_candidate_phone, password=vote_candidate_password)
    if vote_candidate is None:
        return "Неверные учетные данные"
    
    if vote_candidate.votes < 1:
        return "У вас нет голосов для голосования"

    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        return "Голосуемый не найден"
    
    try:
        nomination = Nomination.objects.get(nomination=nomination)
    except Nomination.DoesNotExist:
        return "Номинация не найдена"
    
    if Vote.objects.filter(voter=voter, nomination=nomination).exists():
        return "Вы уже проголосовали в данной номинации"

    vote = Vote(voter=voter, vote_candidate=vote_candidate, nomination=nomination)
    vote.save()

    vote_candidate.votes -= 1
    vote_candidate.save()

    return "Голос успешно принят"


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class NominationViewSet(viewsets.ModelViewSet):
    queryset = Nomination.objects.all()
    serializer_class = NominationSerializer


class VoteCandidateViewSet(viewsets.ModelViewSet):
    queryset = VoteCandidate.objects.all()
    serializer_class = VoteCandidateSerializer


class VoteViewSet(viewsets.ViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            vote_candidate_phone = serializer.validated_data['vote_candidate_phone']
            vote_candidate_password = serializer.validated_data['vote_candidate_password']
            voter_id = serializer.validated_data['voter_id']
            nomination = serializer.validated_data['nomination']

            result = cast_vote(vote_candidate_phone, vote_candidate_password, voter_id, nomination)
            if result == "Голос успешно принят":
                return Response({"message": result}, status=status.HTTP_201_CREATED)

            return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
