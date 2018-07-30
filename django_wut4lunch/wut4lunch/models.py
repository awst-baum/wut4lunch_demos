from django.db import models

class Lunch(models.Model):
    submitter = models.CharField(max_length=63)
    food = models.CharField(max_length=255)
    
    def odd_food(self):
        if self.food is None: return False;
        return len(self.food) % 2 == 1;
    
    def __str__(self):
        return "{} ate {}".format(self.submitter, self.food)