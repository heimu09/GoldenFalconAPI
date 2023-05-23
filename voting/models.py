from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField



NOMINATIONS = [
    ('VER', 'За верность профессии'),
    ('ACT', 'За активную жизненную позицию'),
    ('OBJ', 'Мастер объектива'),
    ('RUR', 'Лучшее освещение сельской тематики'),
    ('SOC', 'Лучшее освещение социальной тематики'),
    ('IND', 'Лучшее освещение производственной тематики'),
    ('SUC', 'За первые успехи'),
    ('WOR', 'Лучшая творческая работа года'),
    ('STY', 'За стиль и функциональность'),
    ('NET', 'За лучшее освещение актуальных проблем в социальных сетях'),
]


class Voter(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='voters/')
    phone = PhoneNumberField()
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return self.name


class Nomination(models.Model):
    voter = models.ForeignKey(Voter, related_name='nominations', on_delete=models.CASCADE)
    nomination = models.CharField(max_length=3, choices=NOMINATIONS)

    def __str__(self):
        return self.get_nomination_display()


class Material(models.Model):
    voter = models.ForeignKey(Voter, related_name='materials', on_delete=models.CASCADE)
    info = models.TextField()
    links = models.URLField(max_length=200)

    def __str__(self):
        return self.info

    def save(self, *args, **kwargs):
        if self.voter.materials.count() >= 5:
            raise ValidationError("У одного участника не может быть больше пяти материалов")
        super().save(*args, **kwargs)


class VoteCandidate(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    position = models.CharField(max_length=255, null=True)
    votes = models.PositiveIntegerField(default=10, editable=False)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    vote_candidate = models.ForeignKey(VoteCandidate, on_delete=models.CASCADE)
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'nomination')

    def __str__(self):
        return f'{self.vote_candidate.name} voted for {self.voter.name}'
