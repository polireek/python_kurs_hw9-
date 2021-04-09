from academy.models import Group, Lecturer, Student

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for i in range(2):
            new_lecturer = Lecturer.objects.create(
                first_name=fake.unique.first_name(),
                last_name=fake.unique.last_name(),
                email=fake.email(),
            )
            new_lecturer.save()

            new_group = Group.objects.create(
                course="G"+str(fake.pyint()),
                teacher=new_lecturer,
            )

            # Create new students:
            for j in range(10):
                new_student = Student.objects.create(
                    first_name=fake.unique.first_name(),
                    last_name=fake.unique.last_name(),
                    email=fake.email(),
                )
                new_student.save()
                new_group.students.add(new_student)

            new_group.save()
            self.stdout.write(self.style.SUCCESS("Группа успешно создана!!!"))
