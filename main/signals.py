from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from main.models import Customer


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            email=instance.email,
            name=instance.first_name + " " + instance.last_name
        )
        print("Customer created")


#post_save.connect(create_customer, sender=User)


@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.save()
        print("Customer updated")


#post_save.connect(update_customer, sender=User)
