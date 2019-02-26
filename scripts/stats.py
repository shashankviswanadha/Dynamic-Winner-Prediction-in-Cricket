import math

class batting_stats():
    def __init__(self,matches,innings,not_outs,runs,average,balls,centuries,fifties,fours,sixes,zeros,hs,sr,span):
        self.matches_played = matches
        self.batt_innings = innings
        self.not_outs = not_outs
        self.runs_scored = runs
        self.average = average
        self.balls_faced = balls
        self.centuries = centuries
        self.fifties = fifties
        self.fours = fours
        self.sixes = sixes

        self.zeros = zeros
        self.highest_score = hs
        self.strike_rate = sr
        self.span = span

        if self.batt_innings!= 0:

            self.score = self.average*self.strike_rate

        else:
            self.score = 0.0
        self.normalized_score = None

    def __str__(self):
        out = ''
        out += '\nBatting Stats : \n'
        out += '\nMatches Played : ' + str(self.matches_played)
        out += '\nInnings Played : ' + str(self.batt_innings)
        out += '\nNot Outs : ' + str(self.not_outs)
        out += '\nRuns Scored : ' + str(self.runs_scored)
        out += '\nAverage : ' + str(self.average)
        out += '\nStrike Rate : ' + str(self.strike_rate)
        out += '\nBalls Faced : ' + str(self.balls_faced)
        out += '\nCenturies : ' + str(self.centuries)
        out += '\nFifties : ' + str(self.fifties)
        out += '\n4s : ' + str(self.fours)
        out += '\n6s: ' + str(self.sixes) + '\n'
        return out

class bowling_stats():
    def __init__(self,matches,innings,overs,runs,wickets,average,econ,fourwi,fivewi,sr,span):
        self.matches_played = matches
        self.bowl_innings = innings
        self.overs_bowled = overs
        i,d = divmod(self.overs_bowled,1)
        #print i,d
        self.balls_bowled = i * 6 + d * 10
        self.runs_conceded = runs
        self.wickets_taken = wickets
        self.average = average
        self.economy = econ
        self.fourwi = fourwi
        self.fivewi = fivewi

        self.strike_rate = sr
        self.span = span

        if self.bowl_innings != 0 and self.economy != 0 and self.strike_rate != 0:
            self.score = 100/(self.strike_rate*self.economy)
        else:
            self.score = 0.0
        self.normalized_score = None


    def calculate_overs_bowled(self):
        if self.balls_bowled != 0:
            self.overs_bowled = int(self.balls_bowled)/6 + (int(self.balls_bowled)%6)/10.0
        else:
            self.overs_bowled = 0.0


    def __str__(self):
        out = ''
        out += '\nBowling Stats : \n'
        out += '\nMatches Played : ' + str(self.matches_played)
        out += '\nInnings Played : ' + str(self.bowl_innings)
        out += '\nOvers Bowled : ' + str(self.overs_bowled)
        out += '\nBalls Bowled : ' + str(self.balls_bowled)
        out += '\nRuns Conceded : ' + str(self.runs_conceded)
        out += '\nWickets Taken : ' + str(self.wickets_taken)
        out += '\nAverage : ' + str(self.average)
        out += '\nEconomy : ' + str(self.economy)
        out += '\nStrike Rate : ' + str(self.strike_rate)
        out += '\n4 Wicket Innings : ' + str(self.fourwi)
        out += '\n5 Wicket Innings : ' + str(self.fivewi) + '\n'
        return out
