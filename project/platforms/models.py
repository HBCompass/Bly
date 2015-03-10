from django.db import models
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from postgres.fields import ArrayField

# Models

#Users and permissions

class Collaborator(models.Model):
    """Class encompassing all of the possible roles in a story. Ex. Reporter, Editor, or Photographer."""

    STATUS = (
        ('ft','Full-time'),
        ('pt','Part-time'),
        ('fr','Freelance'),
        ('co','Contract'),
    )

    PERMISSIONS = (
        ('noncontent','Noncontent'),
        ('affiliate','Affiliate'),
        ('contributor','Contributor'),
        ('staff','Staff'),
        ('editor','Editor'),
        ('administrator','Administrator'),
    )

# #Should role be a choice or its own class?

#     ROLE = (
#         ('writer','Writer'),
#         ('editor','Editor'),
#         ('photographer','Photographer'),
#         ('videographer','Videographer'),
#         ('director','Director'),
#         ('producer','Producer'),
#         ('designer','Designer'),
#         ('developer','Developer'),
#     )

    name = models.CharField(max_length=35, unique=True)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100, nullable=False)
    phone = models.CharField(max_length=10, unique=True,
        validators=[
            RegexValidator(r"\d{10}",
                           'Phone numbers must be exactly 10 digits long, like "4155551212"')
        ]
    )
    roles = models.ManyToManyField(Role)
    status = models.CharField(max_length=1, choice=STATUS)
    permissions = models.CharField(max_length-1, choice=PERMISSIONS)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Team' 


class Role(models.Model):
    """The types of roles involved in a story."""
# How to set up model so the selection of each 
# Is role better suited as a choice or as a class?
# Users can have multiple roles within a story or across stories.
# No role is required other than writer and editor.

    writer = models.BooleanField(default=False)
    editor = models.BooleanField(default=False)
    photographer = models.BooleanField(default=False)
    videographer = models.BooleanField(default=False)
    director = models.BooleanField(default=False)
    producer = models.BooleanField(default=False)
    designer = models.BooleanField(default=False)
    developer =models.BooleanField(default=False)


#Stories and platforms

# MVP classes are Story and Web. 
# Print, Radio, Tv can be deferred.

class Story(models.Model):
    """The universal traits of any story. """
    storyid = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=20, nullable=False, unique=True)  #usually couple words plus date ex. "crash022315"
    
# Classes for each thread of a story. 
    
class Web(Story):
    """The general web post version of content. Regularly published web content. Ex: Daily news, articles, videos, photo galleries"""
    web_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=False)
    pub_date = models.DateTimeField(auto_now=False)
    byline = models.CharField(max_length=100, nullable=False)
    editor = models.CharField(max_length=100, nullable=False)
    headline = models.CharField(nullable=False)
    text = models.TextField()

# Completing remaining classes once Story and Web are complete.

class Print(Story):
    """ The print version of a story. """
    print_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=False)
    pub_date = models.DateTimeField(auto_now=False)
    byline = models.CharField(max_length=100, nullable=False)
    editor = models.CharField(max_length=100, nullable=False)
    headline = models.CharField(nullable=False)
    text = models.TextField()
    # To be continued

class Radio(Story):
    """ Scheduled radio programming. Ex: A single segment on Morning Edition. """
    radio_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=False)
    byline = models.CharField(max_length=100, nullable=False)
    editor = models.CharField(max_length=100, nullable=False)
    pub_date = models.DateTimeField(auto_now=False)
    text = models.TextField()
    # To be continued

class Tv(Story):
    """ A scheduled tv program. """
    tv_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=False)
    pub_date = models.DateTimeField(auto_now=False)
    byline = models.CharField(max_length=100, nullable=False)
    editor = models.CharField(max_length=100, nullable=False)
    text = models.TextField()
    # To be continued
    

# A created story
# class Entry(models.Model):
#     """A created story."""
#     entry = models.ForeignKey(StoryMaker)
#     respondent_id = models.IntegerField("respondent ID",)
#     created_at = models.DateTimeField(auto_now_add=True,)
#     def __str__(self):
#         return "%s %s" % (self.survey.name, self.id)


#Creating a story

class StoryMaker(models.Model):
    """Creating a story."""

    name = models.CharField(max_length=100)
    team = models.ManyToManyField(Collaborator, help_text='Which collaborators are participating in this story?',)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def get_absolute_url(self):
        return reverse('story.detail', kwargs={'pk': self.id})

# class Question(models.Model):
#     """A field in the storymaker."""

#     template = models.ForeignKey(SurveyTemplate)
#     label = models.CharField(max_length=25,)
#     question = models.CharField(max_length=100,)
#     position = models.IntegerField()
#     text_entry = models.BooleanField(default=False,
#         help_text='Check if this question accepts free-form text responses.',
#     )