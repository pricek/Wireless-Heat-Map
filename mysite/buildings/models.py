from django.db import models

class Building(models.Model):
    number = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=100)
    baseline_clients = models.PositiveIntegerField(default=0)
    baseline_bandwidth = models.PositiveIntegerField(default=0)
    has_render = models.BooleanField(default=False)
    render = models.TextField(default="None")
    def get_name(self):
        if self.name != "":
            return self.name
        else:
            return "Building: " + str(self.number)
    def __str__(self):
        return self.get_name()
    def get_base_clients(self):
        bc = self.baseline_clients
        for floor in self.floor_set.all():
            bc += floor.baseline_clients
        for room in self.room_set.all():
            bc += room.baseline_clients
        return bc

class Floor(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    baseline_clients = models.PositiveIntegerField(default=0)
    baseline_bandwidth = models.PositiveIntegerField(default=0)
    has_render = models.BooleanField(default=False)
    render = models.TextField(default="None")
    def __str__(self):
        return self.building.get_name() + " | Floor: " + str(self.number)
    def get_base_clients(self):
        bc = self.baseline_clients
        for room in self.room_set.all():
            bc += room.baseline_clients
        return bc
    class Meta:
        ordering = ['building', 'number']
        constraints = [
            models.UniqueConstraint(fields=['building', 'number'], name='unique_floor')
        ]

class Room(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    baseline_clients = models.PositiveIntegerField(default=0)
    baseline_bandwidth = models.PositiveIntegerField(default=0)
    has_render = models.BooleanField(default=False)
    render = models.TextField(default="None")
    def __str__(self):
        return self.building.get_name() + " | Floor " + str(self.floor.number) + " | Room " + self.number
    def get_base_clients(self):
        bc = self.baseline_clients
        return bc
    class Meta:
        ordering = ['building', 'floor', 'number']
        constraints = [
            models.UniqueConstraint(fields=['building', 'floor', 'number'], name='unique_room')
        ]

# Create your models here.
