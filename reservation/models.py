from django.db import models

# Create your models here.

class Reservation(models.Model):
    EVENT_CHOICE =  (
        (None, 'Event Type'), 
        ('Wedding', 'Wedding'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ('Party', 'Party'),
        ('Other', 'Other')
    )

    PEOPLE_CHOICE = (
        (None, 'Number of People'),
    )


    PEOPLE_CHOICE += tuple([(i,i) for i in range(1,26)])

    STATUS_CHOICE = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    )

    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    event = models.CharField(max_length=100, choices= EVENT_CHOICE)
    people = models.IntegerField(choices = PEOPLE_CHOICE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length = 100, choices=STATUS_CHOICE, default = 'Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
