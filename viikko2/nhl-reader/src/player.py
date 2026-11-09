class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.team = player_dict['team']
        self.goals = player_dict['goals']
        self.assists = player_dict['assists']
    
    @property
    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return (f"{self.name:<24} {self.team:<15} "
                f"{self.goals:>2} + {self.assists:>2} = {self.points}")
