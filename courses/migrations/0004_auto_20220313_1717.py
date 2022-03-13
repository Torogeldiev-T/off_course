# Generated by Django 3.1.3 on 2022-03-13 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('courses', '0003_auto_20220309_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='owners',
        ),
        migrations.AddField(
            model_name='course',
            name='enrollement_key',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to='accounts.teacher'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('text', 'video', 'image', 'file', 'quiz', 'assignment', 'topic')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='module',
            name='type',
            field=models.CharField(choices=[('Assignment', 'Assignment'), ('Test', 'Test'), ('Quiz', 'Quiz'), ('Topic', 'Topic')], max_length=12),
        ),
        migrations.CreateModel(
            name='CourseParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False)),
                ('enrolled', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
