from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoterViewSet, MaterialViewSet, NominationViewSet, VoteCandidateViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'voters', VoterViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'nominations', NominationViewSet)
router.register(r'candidates', VoteCandidateViewSet)
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
