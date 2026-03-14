from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from tasks.models import Task, SubTask, Note, Priority, Category
import random


class Command(BaseCommand):
    help = "Generate fake data"

    def handle(self, *args, **kwargs):

        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        task_distribution = [
            ("Pending", 25),
            ("In Progress", 15),
            ("Completed", 10),
        ]

        for status, count in task_distribution:

            for _ in range(count):

                task = Task.objects.create(
                    title=fake.sentence(nb_words=5),
                    description=fake.paragraph(nb_sentences=3),
                    status=status,
                    deadline=timezone.make_aware(fake.date_time_this_month()),
                    priority=random.choice(priorities),
                    category=random.choice(categories)
                )

                # Subtasks
                for _ in range(random.randint(1,3)):
                    SubTask.objects.create(
                        title=fake.sentence(nb_words=4),
                        status=random.choice(["Pending","In Progress","Completed"]),
                        parent_task=task
                    )

                # Notes
                for _ in range(random.randint(1,2)):
                    Note.objects.create(
                        task=task,
                        content=fake.paragraph()
                    )

        self.stdout.write(self.style.SUCCESS("50 Tasks with subtasks and notes generated!"))