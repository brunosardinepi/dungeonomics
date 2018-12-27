from django.core.management.base import BaseCommand, CommandError

from characters.models import Monster, NPC, Player, GeneralCharacter, Attribute
from tavern.models import Review


class Command(BaseCommand):
    help = 'Migrates all monsters, NPCs, and players to the GeneralCharacter model'

    field_replacements = {
        'alignment': 'Alignment',
        'size': 'Size',
        'languages': 'Languages',
        'strength': 'Strength',
        'dexterity': 'Dexterity',
        'constitution': 'Constitution',
        'intelligence': 'Intelligence',
        'wisdom': 'Wisdom',
        'charisma': 'Charisma',
        'armor_class': 'Armor class',
        'hit_points': 'Hit points',
        'speed': 'Speed',
        'saving_throws': 'Saving throws',
        'creature_type': 'Character type',
        'damage_vulnerabilities': 'Damage vulnerabilities',
        'damage_immunities': 'Damage immunities',
        'damage_resistances': 'Damage resistances',
        'condition_immunities': 'Condition immunities',
        'senses': 'Senses',
        'challenge_rating': 'Challenge rating',
        'npc_class': 'Class',
        'race': 'Race',
        'age': 'Age',
        'height': 'Height',
        'weight': 'Weight',
        'proficiency_bonus': 'Proficiency bonus',
        'character_class': 'Class',
        'xp': 'Experience points',
        'background': 'Background',
}

    additional_notes_fields = {
        'bonds': 'Bonds',
        'flaws': 'Flaws',
        'ideals': 'Ideals',
        'personality': 'Personality',
        'equipment': 'Equipment',
        'feats': 'Feats',
        'proficiencies': 'Proficiencies',
        'skills': 'Skills',
        'spells': 'Spells',
        'attacks': 'Attacks',
        'notes': 'Notes',
        'traits': 'Traits',
        'content': 'Content',
    }

    def migrate(self, obj):
        # create a GeneralCharacter with the same basic fields
        character = GeneralCharacter.objects.create(
            user=obj.user,
            name=obj.name,
            is_published=obj.is_published,
            published_date=obj.published_date,
            tavern_description=obj.tavern_description,
        )

        # copy importers to new character
        for importer in obj.importers.all():
            character.importers.add(importer)

        # copy review to new character
        if isinstance(obj, Monster):
            reviews = Review.objects.filter(monster=obj)
        elif isinstance(obj, NPC):
            reviews = Review.objects.filter(npc=obj)
        elif isinstance(obj, Player):
            reviews = Review.objects.filter(player=obj)

        if reviews:
            for review in reviews:
                date = review.date
                review.pk = None
                review.character = character
                review.save()
                Review.objects.filter(pk=review.pk).update(date=date)

        # copy campaigns to new character
        if isinstance(obj, Player):
            for campaign in obj.campaigns.all():
                character.campaigns.add(campaign)

        # watch for creature_type field
        # if there is one, set the character type to the creature_type
        # if not, set the character type to the model type
        creature_type = False

        # for all remaining fields, create an attribute (ignore the player_name on players)
        # see if this field is in the dict
        # if key matches, create an attribute with dict value as the name
        # and field's value as the object's value
        # players will need the character_name to overwrite the character's name field
        for field in obj._meta.get_fields():
            try:
                value = getattr(obj, field.name)
            except AttributeError:
                value = ''

            if value != '':
                if isinstance(obj, Player) and field.name == 'character_name':
                    character.name = value
                elif field.name in self.field_replacements:
                    if field.name == 'creature_type':
                        creature_type = True

                    if field.name == 'alignment':
                        attribute = Attribute.objects.create(
                            character=character,
                            name=self.field_replacements[field.name],
                            value=obj.get_alignment_display(),
                        )
                    elif field.name == 'size':
                        attribute = Attribute.objects.create(
                            character=character,
                            name=self.field_replacements[field.name],
                            value=obj.get_size_display(),
                        )
                    else:
                        attribute = Attribute.objects.create(
                            character=character,
                            name=self.field_replacements[field.name],
                            value=value,
                        )
                elif field.name in self.additional_notes_fields:
                # copy the additional_notes_fields into the character notes
                    character.notes += "<h3>{}</h3>".format(
                        self.additional_notes_fields[field.name])
                    character.notes += "<p>{}</p>".format(value)

                character.save()

        if creature_type == False:
            attribute = Attribute.objects.create(
                character=character,
                name='Character type',
                value=obj.__class__.__name__,
            )

    def handle(self, *args, **options):
        monsters = Monster.objects.all()
        if monsters:
            print("going through monsters now")
            for monster in monsters:
                self.migrate(monster)

        npcs = NPC.objects.all()
        if npcs:
            print("going through npcs now")
            for npc in npcs:
                self.migrate(npc)

        players = Player.objects.all()
        if players:
            print("going through players now")
            for player in players:
                self.migrate(player)
