from django.core.management.base import BaseCommand, CommandError
import json
from catalog.serializers import PetSerializer
from catalog.models import Pet


class Command(BaseCommand):
    help = 'pets info'

    def add_arguments(self, parser):
        parser.add_argument('--has_photo', action='store_true')

    def handle(self, *args, **options):
        arg = False
        if options['has_photo']:
            arg = True
        try:
            pets = Pet.objects.all().exclude(photo__isnull=arg)  # убрать all
            serialize_pet = PetSerializer(pets, many=True)
        except Pet.DoesNotExist:
            raise CommandError('Pets does not exist')
        self.stdout.write(json.dumps(serialize_pet.data), ending='')
