
class match_state():
    def __init__(self,team_a,team_b,toss,match_type,venue,winner,toss_win,home_team):
        self.team_a = team_a
        self.team_b = team_b
        self.batting_first = toss # 0 if team_a batting first
        self.current_innings = 0  # 0 if 1st innings
        self.match_type = match_type
        self.venue = venue
        self.winning_team_name = winner
        self.toss_winner = toss_win #name of team who won the toss
        self.home_team_name = home_team #name of home team, 'neutral' if in a neutral venue

    def change_innings(self):
        self.current_innings = 1

    def normalize_career_scores(self):
        ba = 0
        bo =0
        for pl in self.team_a.player_list:
            if pl.batting_stats.score > ba:
                ba = pl.batting_stats.score
            if pl.bowling_stats.score > bo:
                bo = pl.bowling_stats.score
        for pl in self.team_b.player_list:
            if pl.batting_stats.score > ba:
                ba = pl.batting_stats.score
            if pl.bowling_stats.score > bo:
                bo = pl.bowling_stats.score
        self.team_a.normalize_career_scores(ba,bo)
        self.team_b.normalize_career_scores(ba,bo)


    def __str__(self):
        if self.current_innings == self.batting_first :
            batt_team = self.team_a
            bowl_team = self.team_b
        else:
            batt_team = self.team_b
            bowl_team = self.team_a
        t = '\n\n 1st Innings:\n'
        if self.current_innings == 0:
            t = self.innings_print(batt_team,bowl_team)
        else:
            t += self.innings_print(bowl_team,batt_team)
            t += '\n\n 2nd Innings:\n'
            t += self.innings_print(batt_team,bowl_team)
        return t

    def innings_print(self,batt_team,bowl_team):
        score = 'Score :' + str(batt_team.score) + '\nWickets lost :' + str(batt_team.wickets_lost) + '\nOvers completed :' + str(batt_team.overs_completed)
        batt_scorecard = ''
        bowl_scorecard = ''

        for pl in batt_team.player_list:
            batt_scorecard = batt_scorecard + pl.name + ':' + str(pl.runs_scored) + '(' + str(pl.balls_played) + ')\n'

        for pl in bowl_team.player_list:
            bowl_scorecard = bowl_scorecard + pl.name + ':' + str(pl.overs_bowled) + '(' + str(pl.runs_conceded) + '/' + str(pl.wickets_taken) + ')\n'
        return '\n\n' +  batt_team.name + ':\n' + score + '\n\nScorecard:\n' + batt_team.name + ' Batting:\n' + batt_scorecard + '\n\n' + bowl_team.name + ' Bowling:\n' + bowl_scorecard
