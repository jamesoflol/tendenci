from django.db import models
from forms_builder.forms.models import FormEntry, FieldEntry
from user_groups.models import Group

# Create your models here.
class GroupSubscription(models.Model):
    group = models.ForeignKey(Group)
    subscriber = models.ForeignKey(FormEntry, related_name='group_subscriber')
    
    create_dt = models.DateTimeField(auto_now_add=True, editable=False)
    update_dt = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.subscriber.pk , self.group.name)
        
    @property
    def display(self):
        try:
            first_name = self.subscriber.fields.get(field__label__iexact="first name").value
        except FieldEntry.DoesNotExist:
            first_name = None
        try:
            last_name = self.subscriber.fields.get(field__label__iexact="last name").value
        except FieldEntry.DoesNotExist:
            last_name = None
        try:
            email = self.subscriber.fields.get(field__label__iexact="email").value
        except FieldEntry.DoesNotExist:
            email = None
        name = "%s %s(%s)" % (first_name, last_name, email)
        print "Name: " + name
        if first_name or last_name or email:
            return name
        return "Info Unavailable"
    
    class Meta:
        unique_together = ('group', 'subscriber',)
        verbose_name = "Group Subscription"
        verbose_name_plural = "Group Subscriptions"
