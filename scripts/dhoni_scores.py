from match_sim import *
import math

ball_by_ball = load_ball_by_ball_data('598027.yaml')
matchState = initialize_match(ball_by_ball,'598027.yaml')
#simulate_match(ball_by_ball,matchState)
#simulate_innings(1,ball_by_ball,matchState)
#matchState.change_innings()
first = ball_by_ball['innings'][0]['1st innings']
second = ball_by_ball['innings'][1]['2nd innings']
simulate_n_overs(first,matchState,20)


m = matchState.team_a.get_player_by_name('CH Gayle').batting_stats.score
smith = matchState.team_a.get_player_by_name('CH Gayle')
#print smith.name
#print team_b_scores['SPD Smith']

boun = 5*smith.num_fours + 10*smith.num_sixes

play = 2*smith.balls_played + m*smith.is_batting#*(1+(20-matchState.team_a.overs_completed)/20.0)
sr = (smith.runs_scored/float(smith.balls_played))*100.0
inst_score = 0.3*boun + 0.4*sr + 0.3*play

'''print 'boun :',boun
print 'play :',play
print 'sr :',sr

print 'balls : ',smith.balls_played
print 'runs: ' ,smith.runs_scored
print 'fours:',smith.num_fours
print 'sixes:',smith.num_sixes
print 'bouns:',boun
print 'career score: ',m
print 'Instant score:', inst_score
print "Overall score: ",0.6*inst_score + 0.4*m'''



for pl in matchState.team_a.player_list:
    print '\n',pl.name
    print pl.batting_stats.normalized_score
    print pl.bowling_stats.score

for pl in matchState.team_b.player_list:
    print '\n',pl.name
    print pl.batting_stats.normalized_score
    print pl.bowling_stats.score
print '\n'

print matchState.team_a.name
print 'Batting: ',matchState.team_a.career_batting_score
print 'Normalized:',matchState.team_a.normalized_career_batting_score
print 'Bowling:',matchState.team_a.career_bowling_score
print 'Normalized:',matchState.team_a.normalized_career_bowling_score
print '\n'
print matchState.team_b.name
print 'Batting: ',matchState.team_b.career_batting_score
print 'Normalized:',matchState.team_b.normalized_career_batting_score
print 'Bowling:',matchState.team_b.career_bowling_score
print 'Normalized:',matchState.team_b.normalized_career_bowling_score


print '\n\n SCORE : = ',matchState.team_a.normalized_career_batting_score/matchState.team_b.normalized_career_bowling_score - matchState.team_b.normalized_career_batting_score/matchState.team_a.normalized_career_bowling_score
#print matchState.team_a.get_player_by_name('Z Khan').dot_balls_bowled
