# Generated by Django 4.1.2 on 2022-11-08 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0007_alter_user_managers_remove_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuisine',
            options={'verbose_name_plural': 'Cuisines'},
        ),
        migrations.AddIndex(
            model_name='branch',
            index=models.Index(fields=['country', 'city'], name='branch_location_index'),
        ),
        migrations.AddIndex(
            model_name='branch',
            index=models.Index(fields=['country'], name='branch_country_index'),
        ),
        migrations.AddIndex(
            model_name='branch',
            index=models.Index(fields=['city'], name='branch_city_index'),
        ),
        migrations.AddIndex(
            model_name='branch',
            index=models.Index(fields=['discounts'], name='branch_discounts_index'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['name'], name='company_name_index'),
        ),
        migrations.AddIndex(
            model_name='cuisine',
            index=models.Index(fields=['name'], name='cuisine_name_index'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['rating'], name='review_rating_index'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['date_joined'], name='user_date_joined_index'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_active'], name='user_is_active_index'),
        ),
    ]