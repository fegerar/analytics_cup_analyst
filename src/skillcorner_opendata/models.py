from django.db import models

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=100)

    def __str__(self):
        return self.short_name

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    home_team = models.ForeignKey(Team, related_name='matches_as_home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='matches_as_away_team', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    competition_id = models.IntegerField()
    season_id = models.IntegerField()
    competition_edition_id = models.IntegerField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date_time}"
    