class team():
    def __init__(self,name,players):
        self.name = name
        self.player_list = players
        self.score = 0
        self.wickets_lost = 0
        self.overs_completed = 0
        self.balls_completed = 0

        self.career_batting_score = None
        self.normalized_career_batting_score = None
        self.career_bowling_score = None
        self.normalized_career_bowling_score = None

    def get_player_by_name(self,name):
        for player in self.player_list:
            if name == player.name:
                return player
        print name
        raise Exception('Player name does not match')



    def calculate_overs_completed(self):
        self.overs_completed = self.balls_completed/6 + (self.balls_completed%6)/10.0

    def normalize_career_scores(self,ba,bo):

        for pl in self.player_list:
            pl.batting_stats.normalized_score = pl.batting_stats.score/ba
            pl.bowling_stats.normalized_score = pl.bowling_stats.score/bo

    def calculate_team_career_score(self):
        self.career_batting_score = 0
        self.normalized_career_batting_score = 0
        self.career_bowling_score = 0
        self.normalized_career_bowling_score = 0
        for pl in self.player_list:
            if pl.batting_stats.score != None:
                self.career_batting_score += pl.batting_stats.score
                self.normalized_career_batting_score += pl.batting_stats.normalized_score
            if pl.bowling_stats.score != None:
                self.career_bowling_score += pl.bowling_stats.score
                self.normalized_career_bowling_score += pl.bowling_stats.normalized_score
