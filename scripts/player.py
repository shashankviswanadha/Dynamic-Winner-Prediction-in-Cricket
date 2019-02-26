

class player():
    def __init__(self,name,team,batt,bowl):
        self.name = name
        self.team_name = team
        self.batting_stats = batt
        self.bowling_stats = bowl

        self.runs_scored = 0
        self.balls_played = 0
        self.overs_played = 0
        self.num_fours = 0
        self.num_sixes = 0
        self.is_batting = 0
        self.has_batted = 0

        self.wickets_taken = 0
        self.balls_bowled = 0
        self.overs_bowled = 0
        self.runs_conceded = 0
        self.dot_balls_bowled = 0

    def calculate_overs_played(self):
        if self.balls_played != 0:
            self.overs_played = int(self.balls_played)/6 + (int(self.balls_played)%6)/10.0
        else:
            self.overs_played = 0.0

    def calculate_overs_bowled(self):
        if self.balls_bowled != 0:
            self.overs_bowled = int(self.balls_bowled)/6 + (int(self.balls_bowled)%6)/10.0
        else:
            self.overs_bowled = 0.0




    def __str__(self):
        out = ''
        out += '\n' + self.name + ':\n'
        out += self.batting_stats.__str__()
        out += self.bowling_stats.__str__()
        return out
