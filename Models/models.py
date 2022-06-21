from email.policy import default
from django.db import models

class Person(models.Model):
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    sex = models.CharField(max_length=6, blank=True, default='')
    birth_date = models.DateField('birth date', blank=True, null=True)
    birth_year = models.IntegerField(default=None, blank=True, null=True)
    origin = models.CharField(max_length=3, blank=True, default='')
    totem = models.CharField(max_length=20, blank=True, default='')

    fide_id = models.IntegerField(default=None)
    title = models.CharField(max_length=30, blank=True, default='')
    standard_elo = models.IntegerField(default=None, blank=True, null=True)
    rapid_elo = models.IntegerField(default=None, blank=True, null=True)
    blitz_elo = models.IntegerField(default=None, blank=True, null=True)
    elo_history = models.JSONField('elo history', blank=True, default=dict)
    standard_games_history = models.JSONField('standard games history', blank=True, default=dict)
    rapid_games_history = models.JSONField('rapid games history', blank=True, default=dict)
    blitz_games_history = models.JSONField('blitz games history', blank=True, default=dict)
    

    world_rank = models.IntegerField(default=None, blank=True, null=True)
    continental_rank = models.IntegerField(default=None, blank=True, null=True)
    national_rank = models.IntegerField(default=None, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    



    
