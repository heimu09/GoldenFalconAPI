from django.contrib import admin
from .models import Voter, Material, Nomination, VoteCandidate, Vote

admin.site.register(Voter)
admin.site.register(Material)
admin.site.register(Nomination)
admin.site.register(VoteCandidate)
admin.site.register(Vote)
