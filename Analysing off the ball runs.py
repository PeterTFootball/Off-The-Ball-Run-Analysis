#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:39:23 2020

@author: Peter
"""


import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import Metrica_PitchControl as mpc
import numpy as np
import pandas as pd

# set up initial path to data
DATADIR = '/Users/Peter/Documents/Courses:Training/Friends Of Tracking/TrackingData/Metrica/sample-data-master/data'


game_id = 2 # let's look at sample match 2



# 2. How might you use the pitch control model to calculate how much space was created (or territory captured) 
# by an off the ball run?

# Hint: consider what the pitch control surface might have looked like if the player had *not* made a run.


# testing the 'hint'


# pass in behind with run creating space


events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')

params = mpc.default_model_params(3)

PPCF_actual,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF_actual, xgrid, ygrid, annotate=True )


# removing player 23 blue (away) team velocity

# selecting the frame we want to look at to speed up calculations



#tracking_away = tracking_away

tracking_away['Away_23_vx'] = 0
tracking_away['Away_23_vy'] = 0
tracking_away['Away_23_speed'] = 0

#PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
#mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=True )

PPCF_no_movement,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF_no_movement, xgrid, ygrid, annotate=True )


events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')

# values to plot
PPCF_plot = 0.5+(PPCF_actual-PPCF_no_movement)

mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away,PPCF_plot , xgrid, ygrid, annotate=True )






# Answer: 
# Calculate all possible runs the player could have made and take the average change in the teams pitch control all of
# these runs would have caused, then compare to the actual run that was executed and compare the net effect.

events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')


# looping player 23 blue (away) team possible velocities and averaging the pitch control values


#tracking_away = tracking_away



# df of all possible velocities 

possible_player_velx = np.arange(-12,12.1,0.5)
possible_player_vely = np.arange(-12,12.1,0.5)

possible_player_velx_df = pd.DataFrame(data=possible_player_velx, columns=["vx"])
possible_player_velx_df['dummy'] = 1

possible_player_vely_df = pd.DataFrame(data=possible_player_vely, columns=["vy"])
possible_player_vely_df['dummy'] = 1

possible_player_vel_df = pd.merge(possible_player_velx_df, possible_player_vely_df,on = 'dummy')

possible_player_vel_df['speed'] = np.sqrt( possible_player_vel_df['vy']**2 + possible_player_vel_df['vx']**2 )

possible_player_vel_df = possible_player_vel_df[possible_player_vel_df['speed']<12]


PPCF_vals = []
for i,row in possible_player_vel_df.iterrows():
    vx = row['vx']
    vy = row['vy']
    
    
    
    tracking_away['Away_23_vx'] = vx
    tracking_away['Away_23_vy'] = vy
    tracking_away['Away_23_speed'] = np.sqrt( tracking_away['Away_23_vy']**2 + tracking_away['Away_23_vx']**2 )
    
    PPCF_temp,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
    
    PPCF_vals.append( (i,vx,vy,PPCF_temp) )
    print(i)




PPCF_vals_av = np.mean( np.array([p[3] for p in PPCF_vals]), axis=0 )

events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')


#PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
#mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=True )

#PPCF2,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF_vals_av, xgrid, ygrid, annotate=True )


events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')

# values to plot
PPCF_plot = 0.5+(PPCF_actual-PPCF_vals_av)

mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away,PPCF_plot , xgrid, ygrid, annotate=True )


# figuring out the highest overall pitch control run

df = [np.sum(p[3]) for p in PPCF_vals]
df.index(max(df))

# index 1776 highest total pitch control, lets take a look at that run

[PPCF_vals[i] for i in [1776]]

# vx = 11.5
# vy = -3.0


events = mio.read_event_data(DATADIR,game_id)

# read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

# Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
tracking_home = mio.to_metric_coordinates(tracking_home)
tracking_away = mio.to_metric_coordinates(tracking_away)
events = mio.to_metric_coordinates(events)

# reverse direction of play in the second half so that home team is always attacking from right->left
tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)

# Calculate player velocities
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True)
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True)
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')



#PPCF_actual,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
#mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF_actual, xgrid, ygrid, annotate=True )


# removing player 23 blue (away) team velocity

# selecting the frame we want to look at to speed up calculations



#tracking_away = tracking_away

tracking_away['Away_23_vx'] = 11.5
tracking_away['Away_23_vy'] = -3.0
tracking_away['Away_23_speed'] = np.sqrt( tracking_away['Away_23_vy']**2 + tracking_away['Away_23_vx']**2 )

#PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
#mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=True )

PPCF_optimal_movement,xgrid,ygrid = mpc.generate_pitch_control_for_event(821, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away, PPCF_optimal_movement, xgrid, ygrid, annotate=True )


# optimal - actual
PPCF_plot = 0.5+(PPCF_optimal_movement-PPCF_actual)

mviz.plot_pitchcontrol_for_event( 821, events,  tracking_home, tracking_away,PPCF_plot , xgrid, ygrid, annotate=True )




# Then think of a way to recognise "realistic" runs, i.e. away from opposition?  not directly backwards?

# can also compare to the "optimal" run and see what % of the actual run was compared to "optimal" run.  
# i.e. the run that was taken gave the team 95% of the pitch control the "optimal" run did.  Obviously wouldn't expect 100% 
# very often but getting closer to 100% could be an aim of coaching/a team for a pitch controlling game model.


