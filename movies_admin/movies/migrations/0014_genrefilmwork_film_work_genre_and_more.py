# Generated by Django 4.1.3 on 2023-03-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0013_genrefilmwork_film_work_genre_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="genrefilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work_id", "genre_id"), name="film_work_genre"
            ),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work_id", "person_id", "role"),
                name="film_work_person_role",
            ),
        ),
    ]
