from django.db import migrations

def create_data(apps, schema_editor):
    Student = apps.get_model('assets', 'Asset')
    Student(name="Aquatorium", description="Riverfront at Monongahela").save()

class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]