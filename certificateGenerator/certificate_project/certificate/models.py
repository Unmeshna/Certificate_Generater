from django.db import models
import hashlib

class Certificate(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField()
    description=models.TextField()
    unique_identifier=models.CharField(max_length=100, unique=True)
    content= models.TextField()


    def generate_hash(self):
        hash_input=f"{self.name}{self.date}{self.description}{self.unique_identifier}{self.content}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

