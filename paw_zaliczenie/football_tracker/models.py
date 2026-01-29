from django.db import models

# Model reprezentujący piłkarzy
class Player(models.Model):

    # Lista wartości do wyboru dla zmiennej preffered_foot
    FOOT = (
        ('R', 'Right'),
        ('L', 'Left')
    )

    # Lista wartości do wyboru dla zmiennej position
    POSITIONS = (
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=False, blank=False)

    nationality = models.CharField(max_length=3, help_text="Three letter country code, eg. POL, GER, ENG")

    preffered_foot = models.CharField(max_length=1, choices=FOOT)
    height = models.PositiveIntegerField(help_text="Player height (in cm)")
    position = models.CharField(max_length=2, choices=POSITIONS, default='GK')

    club = models.ForeignKey('Club', null=True, blank=True, on_delete=models.SET_NULL, related_name="players")

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Model reprezentujący kluby piłkarskie
class Club(models.Model):
    club_name = models.CharField(max_length=70)
    foundation_year = models.PositiveIntegerField()
    stadium = models.CharField(max_length=70)

    manager = models.ForeignKey('Manager', null=True, blank=True, on_delete=models.SET_NULL)
    league = models.ForeignKey('League', null=False, blank=False, on_delete=models.CASCADE, related_name="clubs")

    def __str__(self):
        return self.club_name



# Model reprezentujący menedzerów klubów piłkarskich
class Manager(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=False, blank=False)
    nationality = models.CharField(max_length=3, help_text="Three letter country code, eg. POL, GER, ENG")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Model reprezentujący klubowe turnieje piłkarskie
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(null=False, blank=False)

    man_of_the_match = models.ForeignKey('Player', null=True, blank=True, on_delete=models.SET_NULL)
    final_winner = models.ForeignKey('Club', null=True, blank=True, related_name="tournament_winner", on_delete=models.SET_NULL)
    final_second_place = models.ForeignKey('Club', null=True, blank=True, related_name="tournament_second_place", on_delete=models.SET_NULL)

    winner_score = models.PositiveIntegerField(blank=True, null=True)
    second_place_score = models.PositiveIntegerField(blank=True, null=True)

    city = models.CharField(max_length=70)
    venue = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.name} {self.year}"



# Model reprezentujący ligi piłkarskie
class League(models.Model):
    league_name = models.CharField(max_length=70)
    country = models.CharField(max_length=3, help_text="Three letter country code, eg. POL, GER, ENG")
    founding_year = models.PositiveIntegerField()
    top_scorer = models.ForeignKey('Player', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.league_name