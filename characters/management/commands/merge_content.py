from django.core.management.base import BaseCommand, CommandError
from characters.models import Monster, NPC


class Command(BaseCommand):
    help = 'Merges traits, actions, and notes fields into content field'

    # need to do a merge for: monsters, npcs
    # fields: traits, actions, notes

    def merge(self, obj):
        content = ""
        if obj.traits:
            content += "<h3>Traits</h3>"
            content += obj.traits
            if obj.actions or obj.notes:
                content += "<hr>"
        if obj.actions:
            content += "<h3>Actions</h3>"
            content += obj.actions
            if obj.notes:
                content += "<hr>"
        if obj.notes:
            content += "<h3>Notes</h3>"
            content += obj.notes

        if not content == "":
            obj.content = content
            obj.save()


    def handle(self, *args, **options):
        monsters = Monster.objects.all()
        if monsters:
            print("going through monsters now")
            for monster in monsters:
                self.merge(monster)

        npcs = NPC.objects.all()
        if npcs:
            print("going through npcs now")
            for npc in npcs:
                self.merge(npc)