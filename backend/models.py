from django.db import models

class PlayerModel(models.Model):
    name = models.CharField(max_length=100)

    ppr_position_tier = models.IntegerField(default=-1)
    ppr_flex_tier = models.IntegerField(default=-1)

    half_position_tier = models.IntegerField(default=-1)
    half_flex_tier = models.IntegerField(default=-1)

    standard_position_tier = models.IntegerField(default=-1)
    standard_flex_tier = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name