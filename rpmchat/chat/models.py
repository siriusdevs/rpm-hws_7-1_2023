from django.db import models


class Message(models.Model):
    name = models.TextField()
    text = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.text}"

    @classmethod
    def get_all_messages(cls):
        return cls.objects.all()

    @classmethod
    def create_message(cls, name, text):
        message = cls(name=name, text=text)
        message.save()
