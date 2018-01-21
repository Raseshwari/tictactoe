from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
#from django.urls import reverse

# Create your models here.
GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)


class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )


@python_2_unicode_compatible
class Game(models.Model):
    first_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_first_player")
    second_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games_second_player")
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F',
                              choices=GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()

    def board(self):
        board_size =3
        board = [[None for x in range(board_size)] for y in range(board_size)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        return (user == self.first_player and self.status == 'F' or
                (user == self.second_player and self.status == 'S'))

   # def get_absolute_url(self):
    #    return reverse('gameplay_detail', args=[self, id])

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)


class Move(models.Model): #base class is Model of models imported
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField(editable=False)

    game = models.ForeignKey(Game, on_delete=models.CASCADE, editable=False) #when a game is deleted all moves of the game are deleted
