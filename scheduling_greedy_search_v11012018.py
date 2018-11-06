# -*- coding: utf-8 -*-
"""
BIW modular alg demo

A PPPR test

input: BIW task list of project A, SOB of project A (25 cars), initial day of the week, resourse info.
output: Gantt chart 
"""

# In[0]: import packages
import numpy as np
import pandas as pd


# In[1]: standarized input
tasklist = pd.read_csv('projA_input.csv',sep=',',index_col='Veh_No')
gantt_s = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns)
gantt_s = gantt_s.drop(['SOB'],1)
gantt_e = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns)
gantt_e = gantt_e.drop(['SOB'],1)
for col in gantt_s.columns:
    for ind in gantt_s.index:
        if tasklist[col][ind]==0:
            gantt_s[col][ind] = -1
            gantt_e[col][ind] = -1
Iday = 1 # Fisrt day: 1-Monday, 2-Tuesday, 3-Wednesday, 4-Thursday, 5-Friady
ResourceMax = {'LaserRoom':2,'ManualWelding':9,'ManualDoorOp':12,'CMM':2}
ResourcePool = {'LaserRoom':2,'ManualWelding':9,'ManualDoorOp':12,'CMM':2}
TimeMax = {'LaserRoom':8,'CMM':8}
TimeOcp = {'CL100':0.8,'LS101':0.65,'A metric':5,'B metric':6}
tasktime = pd.read_csv('taskduration.csv',sep=',')
ProcessingTime = dict(zip(tasktime.task,tasktime.time))
processinglist = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # list of processing tasks (at most 3 at the same time)
taskprior = pd.read_csv('taskpriority.csv',sep=',')
Taskpriority = dict(zip(taskprior.task,taskprior.priority))

# Process Tree
def pending_tasks(single_checklist,single_processinglist):
    if sum(single_checklist.values)==0 or sum(single_processinglist.values)==3 or single_checklist['SOB']==1:
        return 'None' # no pending tasks
    else: # to do list not full and less than 3 ongoing tasks
        # (i) check process tree
        pending = pd.DataFrame(columns=['task','prior'])
        # layer 0
        if single_checklist['SOB']==0:
            pending.task = ['MC101','RF101','FF101','BS101','CL100','CL101','CL102']
            pending.prior = [Taskpriority[pending.task[i]] for i in range(len(pending.task))]
        # layer 1
        if single_checklist['MC101']==0:
            pending = pending.loc[pending.task!='MC101']
            pending = pending.append(pd.Series(['MC201',Taskpriority['MC201']], index=pending.columns),ignore_index=True)
        if single_checklist['RF101']==0:
            pending = pending.loc[pending.task!='RF101']
            pending = pending.append(pd.Series(['RF201',Taskpriority['RF201']], index=pending.columns),ignore_index=True)
        if single_checklist['FF101']==0:
            pending = pending.loc[pending.task!='FF101']
        if single_checklist['BS101']==0:
            pending = pending.loc[pending.task!='BS101']
            pending = pending.append(pd.Series(['BS201',Taskpriority['BS201']], index=pending.columns),ignore_index=True)
        if single_checklist['CL100']==0:
            pending = pending.loc[pending.task!='CL100']
        if single_checklist['CL101']==0:
            pending = pending.loc[pending.task!='CL101']
        if single_checklist['CL102']==0:
            pending = pending.loc[pending.task!='CL102']
        if single_checklist['CL101']+single_checklist['CL102']==0 :
            pending = pending.append(pd.Series(['CL201',Taskpriority['CL201']], index=pending.columns),ignore_index=True)
        # layer 2
        if single_checklist['MC201']==0:
            pending = pending.loc[pending.task!='MC201']
            pending = pending.append(pd.Series(['MC301',Taskpriority['MC301']], index=pending.columns),ignore_index=True)
        if single_checklist['RF201']==0:
            pending = pending.loc[pending.task!='RF201']
            pending = pending.append(pd.Series(['RF301',Taskpriority['RF301']], index=pending.columns),ignore_index=True)
        if single_checklist['BS201']==0:
            pending = pending.loc[pending.task!='BS201']
        if single_checklist['CL201']==0:
            pending = pending.loc[pending.task!='CL201']
        # layer 3
        if single_checklist['MC301']==0:
            pending = pending.loc[pending.task!='MC301']
        if single_checklist['RF301']==0:
            pending = pending.loc[pending.task!='FR301']
        if single_checklist['MC301']+single_checklist['RF301']+single_checklist['FF101']==0:
            pending = pending.append(pd.Series(['UB101',Taskpriority['UB101']], index=pending.columns),ignore_index=True)
        # layer 4
        if single_checklist['UB101']==0:
            pending = pending.loc[pending.task!='UB101']
        if single_checklist['UB101']+single_checklist['BS101']==0:
            pending = pending.append(pd.Series(['FI101',Taskpriority['FI101']], index=pending.columns),ignore_index=True)
        # layer 5
        if single_checklist['FI101']==0:
            pending = pending.loc[pending.task!='FI101']
        if single_checklist['FI101']+single_checklist['BS201']==0:
            pending = pending.append(pd.Series(['FO101',Taskpriority['FO101']], index=pending.columns),ignore_index=True)
        # layer 6
        if single_checklist['FO101']==0:
            pending = pending.loc[pending.task!='FO101']
        if single_checklist['FO101']+single_checklist['CL100']==0:
            pending = pending.append(pd.Series(['LS101',Taskpriority['LS101']], index=pending.columns),ignore_index=True)
        # layer 7
        if single_checklist['LS101']==0:
            pending = pending.loc[pending.task!='LS101']
            pending = pending.append(pd.Series(['A metric',Taskpriority['A metric']], index=pending.columns),ignore_index=True)
        if single_checklist['LS101']+single_checklist['CL201']==0:
            pending = pending.append(pd.Series(['B metric',Taskpriority['B metric']], index=pending.columns),ignore_index=True)
        # layer 8
        if single_checklist['A metric']==0:
            pending = pending.loc[pending.task!='A metric']
        if single_checklist['B metric']==0:
            pending = pending.loc[pending.task!='B metric']
            pending = pending.append(pd.Series(['AS101',Taskpriority['AS101']], index=pending.columns),ignore_index=True)
        # layer 9
        if single_checklist['AS101']==0:
            pending = pending.loc[pending.task!='AS101']
            pending = pending.append(pd.Series(['C metric',Taskpriority['C metric']], index=pending.columns),ignore_index=True)
            pending = pending.append(pd.Series(['BS Audit',Taskpriority['BS Audit']], index=pending.columns),ignore_index=True)
        # layer 10
        if single_checklist['C metric']==0:
            pending = pending.loc[pending.task!='C metric']
        if single_checklist['BS Audit']==0:
            pending = pending.loc[pending.task!='BS Audit']
        
        # eliminate processing tasks
        ongoing = [tsk for tsk in single_processinglist.index if single_processinglist[tsk]==1]
        pending = pending[~pending.task.isin(ongoing)]
        if len(pending)==0:
            return 'None'
        else:
            pending = pending.sort_values(['prior'])
            pending = pending.reset_index(drop=True)
            return pending

# Production constraints
def new_tasks(single_pending,single_processinglist,TimeRem,ResourcePool,t):
    num_processing = sum(single_processinglist.values)
    if num_processing == 3 or single_pending is 'None': # cannot process more than 3 tasks at the same time or there is no pending tasks
        return 'None'
    else:
        new_ind = np.arange(3-num_processing)
        new = single_pending.loc[new_ind]
        for ind in new.index:
            newtemp = new.loc[ind] # Note: this is a Series
            eventtemp = newtemp['task']
            if ProcessingTime[eventtemp]>(480*(np.floor(t/480)+1)-t):
                new = new.drop(ind)
            else:
                # CL100
                if eventtemp=='CL100':
                    if ResourcePool['LaserRoom']==0 or TimeRem['LaserRoom']<0.8:
                        new = new.drop(ind)
                # CL101
                if eventtemp=='CL101':
                    if ResourcePool['ManualWelding']==0:
                        new = new.drop(ind)
                # CL102
                if eventtemp=='CL102':
                    if ResourcePool['ManualWelding']==0:
                        new = new.drop(ind)
                # LS101
                if eventtemp=='LS101':
                    if ResourcePool['LaserRoom']==0 or TimeRem['LaserRoom']<0.65:
                        new = new.drop(ind)
                # A metric
                if eventtemp=='A metric':
                    if ResourcePool['CMM']==0 or TimeRem['CMM']<5:
                        new = new.drop(ind)
                # B metric
                if eventtemp=='B metric':
                    if ResourcePool['CMM']==0 or TimeRem['CMM']<6:
                        new = new.drop(ind)
                # CL201
                if eventtemp=='CL201':
                    if ResourcePool['ManualDoorOp']==0:
                        new = new.drop(ind)
            if len(new)==0:
                return 'None'
            else:
                new = new.dropna().reset_index(drop=True)
                return new
            
        
# In[2]: Calcualte Gantt: each component has a start time and an end time, work day operating time is 8*60=480 min

Itime = 0 # start working time of the day
t = 0 # cummulated working time: need to be equal to Itime if evaluate in the middle of a day!!!

# create tasks check list to derive stopflag - 0 stop, >0 continue looping
checklist = tasklist.copy(deep=True) # create a seperate task checklist
checklist.SOB = np.ones_like(tasklist.SOB)
stopflag = checklist.values.sum()

# create event list and add SOB into event list
eventlist = pd.DataFrame(columns = ['event','Veh','starttime','endtime'])
eventlist.event = ['SOB' for car in gantt_s.index]
eventlist.Veh = gantt_s.index
eventlist.starttime = [(val-1)*480 for val in tasklist.SOB.values]
eventlist.endtime = eventlist.starttime+ProcessingTime['SOB']

# start looping
while stopflag>0:
    # check day tag
    cday = np.floor(t/480) # current day
    
    if cday==t/480: # check if this is the start of a day
        TimeRem = {'LaserRoom':8,'CMM':8}
        eventlist = eventlist.append(pd.Series(['CurrentDay','all',t,t+480], index=eventlist.columns),ignore_index=True) # add day end event
        eventlist = eventlist.sort_values(['endtime']).reset_index(drop=True)
    
    # finish-up current events
    events_current = eventlist.loc[eventlist.endtime==t]
    for ind in events_current.index:
        eventtemp = events_current.loc[ind]
        if eventtemp['event']=='CurrentDay':
            eventlist = eventlist.drop(ind) # take off end-of-day event
        else:
            eventlist = eventlist.drop(ind) # task finished 
            checklist = checklist.set_value(eventtemp['Veh'],eventtemp['event'],0) # mark task as finished
            processinglist = processinglist.set_value(eventtemp['Veh'],eventtemp['event'],0) # mark task as finished
            # release reusable resourece to ResourcePool
            # CL100
            if eventtemp['event']=='CL100':
                ResourcePool['LaserRoom'] = ResourcePool['LaserRoom']+1
            # CL101
            if eventtemp['event']=='CL101':
                ResourcePool['ManualWelding'] = ResourcePool['ManualWelding']+1
            # CL102
            if eventtemp['event']=='CL102':
                ResourcePool['ManualWelding'] = ResourcePool['ManualWelding']+1
            # LS101
            if eventtemp['event']=='LS101':
                ResourcePool['LaserRoom'] = ResourcePool['LaserRoom']+1
            # A metric
            if eventtemp['event']=='A metric':
                ResourcePool['CMM'] = ResourcePool['CMM']+1
            # B metric
            if eventtemp['event']=='B metric':
                ResourcePool['CMM'] = ResourcePool['CMM']+1
            # CL201
            if eventtemp['event']=='CL201':
                ResourcePool['ManualDoorOp'] = ResourcePool['ManualDoorOp']+1

    
    # for each car, search for pending tasks, update new events
    for car in checklist.index:
        car_checklist = checklist.loc[car]
        car_processinglist = processinglist.loc[car]
        car_pending = pending_tasks(car_checklist,car_processinglist)
        car_new = new_tasks(car_pending,car_processinglist,TimeRem,ResourcePool,t)
        # seize reusable resource from ResourcePool, consume time in TimeRem
        # CL100
        if 'CL100' in car_new:
            ResourcePool['LaserRoom'] = ResourcePool['LaserRoom']-1
            TimeRem['LaserRoom'] = TimeRem['LaserRoom']-0.8
        # CL101
        if 'CL101' in car_new:
            ResourcePool['ManualWelding'] = ResourcePool['ManualWelding']-1
        # CL102
        if 'CL102' in car_new:
            ResourcePool['ManualWelding'] = ResourcePool['ManualWelding']-1
        # LS101
        if 'LS101' in car_new:
            ResourcePool['LaserRoom'] = ResourcePool['LaserRoom']-1
            TimeRem['LaserRoom'] = TimeRem['LaserRoom']-0.65
        # A metric
        if 'A metric' in car_new:
            ResourcePool['CMM'] = ResourcePool['CMM']-1
            TimeRem['CMM'] = TimeRem['CMM']-5
        # B metric
        if 'B metric' in car_new:
            ResourcePool['CMM'] = ResourcePool['CMM']-1
            TimeRem['CMM'] = TimeRem['CMM']-6
        # CL201
        if 'CL201' in car_new:
            ResourcePool['ManualDoorOp'] = ResourcePool['ManualDoorOp']-1
        
        # add new event to eventlist:
        if not(car_new is 'None'):
            for ind in car_new.index:
                car_newtemp = car_new.loc[ind] # Note: this is a Series
                eventlist = eventlist.append(pd.Series([car_newtemp['task'],car,t,t+ProcessingTime[car_newtemp['task']]], index=eventlist.columns),ignore_index=True)
                gantt_s[car_newtemp['task']][car] = t
                gantt_e[car_newtemp['task']][car] = t+ProcessingTime[car_newtemp['task']]
                processinglist = processinglist.set_value(car,car_newtemp['task'],1) # mark task as processing
    # identify next event, move time tic to the time point
    eventlist = eventlist.sort_values(['endtime'])
    t = np.min(eventlist.endtime.values)      
    stopflag = checklist.values.sum()

# In[3]: Twick to real time scale based on Iday and Itime
firstday_span = 480-Itime
week_end = firstday_span + (5-Iday)*480
gantt_s_tuned = gantt_s.copy(deep=True)
gantt_e_tuned = gantt_e.copy(deep=True)

days_afterfirstweek = np.ceil((t-week_end)/480)
weeks_afterfirstweek = np.floor(days_afterfirstweek/5)
days_lastweek = np.mod(days_afterfirstweek,5)
weekend_labels = [week_end]+[week_end+(i+1)*5*480 for i in np.arange(weeks_afterfirstweek)]
for tsk in gantt_s_tuned.columns:
    for car in gantt_s_tuned.index:
        current_element = gantt_s_tuned[tsk][car]
        if current_element!=0 and current_element!=-1:
            for lb in weekend_labels:
                if current_element>=lb:
                    gantt_s_tuned[tsk][car] = gantt_s_tuned[tsk][car]+480*2
                    gantt_e_tuned[tsk][car] = gantt_e_tuned[tsk][car]+480*2
    
