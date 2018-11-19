# -*- coding: utf-8 -*-
"""
Total alg demo

A PPPR test

Work day version
"""

# Import Packages
import numpy as np
import pandas as pd
import datetime as dt
from copy import deepcopy

# Global
ResourceMax = {'LaserRoom':2,'ManualWelding':9,'ManualDoorOp':12,'CMM':2, 'CDworker':1,'Hoist':8}
TimeDayMax = {'LaserRoom':8,'CMM':8}
TaskDayMax = {'C metric':2,'D metric':1,'DVT':8,'BLT001':1,'BLT002':1,'WT001':2,'WT003':2,'RQA':1}
TimeOcp = {'CL100':0.8,'LS101':0.65,'A metric':5,'B metric':6}
ResourceOcpDict = {'LaserRoom':['CL100','LS101'],'ManualWelding':['CL101','CL102'],'ManualDoorOp':['CL201'],'CMM':['A metric','B metric'], 'CDworker':['C metric','D metric'],'Hoist':['T1','T2','T3','T4','T5','T6','C1','C2','C3','C4','NF001','DF001','FI001','DC001','LV001','VFC','ATF','RQA']}
tasktime = pd.read_csv('taskduration.csv',sep=',')
PaintLocation = 'shanghai'
taskprior = pd.read_csv('taskpriority.csv',sep=',')
Taskpriority = dict(zip(taskprior.task,taskprior.priority))
tasksingle = pd.read_csv('tasksingleday.csv',sep=',')
task_single = tasksingle.loc[tasksingle.singleday==1].task.tolist()
task_multi = tasksingle.loc[tasksingle.singleday==0].task.tolist()

# Process Tree
def pending_tasks(single_checklist,single_processinglist):
    if sum(single_checklist.values)==0 or sum(single_processinglist.values)==3 or single_checklist['BIWSOB']==1:
        return 'None' # no pending tasks
    else: # to do list not full and less than 3 ongoing tasks
        pendinglist = deepcopy(single_checklist)
        # (i) check process tree
        # layer 0
        pendinglist['BIWSOB'] = np.min([1,single_checklist['BIWSOB']])
        # layer 1
        for tsk in ['MC101','RF101','FF101','BS101','CL100','CL101','CL102']:
            pendinglist[tsk] = np.min([1-single_checklist['BIWSOB'],single_checklist[tsk]])
        # layer 2
        pendinglist['MC201'] = np.min([1-single_checklist['MC101'],single_checklist['MC201']])
        pendinglist['RF201'] = np.min([1-single_checklist['RF101'],single_checklist['RF201']])
        pendinglist['BS201'] = np.min([1-single_checklist['BS101'],single_checklist['BS201']])
        pendinglist['CL201'] = np.min([1-(single_checklist['CL101'] or single_checklist['CL102']),single_checklist['CL201']])
        # layer 3
        pendinglist['MC301'] = np.min([1-single_checklist['MC201'],single_checklist['MC301']])
        pendinglist['RF301'] = np.min([1-single_checklist['RF201'],single_checklist['RF301']])
        # layer 4 
        pendinglist['UB101'] = np.min([1-(single_checklist['MC301'] or single_checklist['RF301'] or single_checklist['FF101']),single_checklist['UB101']])
        # layer 5
        pendinglist['FI101'] = np.min([1-(single_checklist['UB101'] or single_checklist['BS101']),single_checklist['FI101']])
        # layer 6
        pendinglist['FO101'] = np.min([1-(single_checklist['FI101'] or single_checklist['BS201']),single_checklist['FO101']])
        # layer 7
        pendinglist['LS101'] = np.min([1-(single_checklist['FO101'] or single_checklist['CL100']),single_checklist['LS101']])
        # layer 8
        pendinglist['A metric'] = np.min([1-single_checklist['LS101'],single_checklist['A metric']])
        pendinglist['B metric'] = np.min([1-(single_checklist['LS101'] or single_checklist['CL201']),single_checklist['B metric']])
        # layer 9
        pendinglist['AS101'] = np.min([1-(single_checklist['LS101'] or single_checklist['CL201'] or single_checklist['B metric']),single_checklist['AS101']])
        # layer 10
        pendinglist['C metric'] = np.min([1-single_checklist['AS101'],single_checklist['C metric']])
        pendinglist['BS Audit'] = np.min([1-single_checklist['AS101'],single_checklist['BS Audit']])
        # layer 11
        pendinglist['TRANSSOB'] = np.min([1-(single_checklist['AS101'] or single_checklist['BS Audit'] or single_checklist['C metric']),single_checklist['TRANSSOB']])
        # layer 12
        pendinglist['TRANS1'] = np.min([1-single_checklist['TRANSSOB'],single_checklist['TRANS1']])
        # layer 13
        pendinglist['PAINT'] = np.min([1-single_checklist['TRANS1'],single_checklist['PAINT']])
        # layer 14
        pendinglist['TRANS2'] = np.min([1-single_checklist['PAINT'],single_checklist['TRANS2']])
        # layer 15
        pendinglist['GASOB'] = np.min([1-single_checklist['TRANS2'],single_checklist['GASOB']])
        pendinglist['BLT001'] = np.min([1-single_checklist['TRANS2'],single_checklist['BLT001']])
        # layer 16
        pendinglist['T1'] = np.min([1-single_checklist['GASOB'],single_checklist['T1']])
        pendinglist['PTI'] = np.min([1-single_checklist['GASOB'],single_checklist['PTI']])
        pendinglist['DR'] = np.min([1-single_checklist['GASOB'],single_checklist['DR']])
        # layer 17
        pendinglist['T2'] = np.min([1-single_checklist['T1'],single_checklist['T2']])
        # layer 18
        pendinglist['WT001'] = np.min([1-single_checklist['T2'],single_checklist['WT001']])
        # layer 19
        pendinglist['T3'] = np.min([1-single_checklist['WT001'],single_checklist['T3']])
        # layer 20
        pendinglist['T4'] = np.min([1-single_checklist['T3'],single_checklist['T4']])
        # layer 21
        pendinglist['T5'] = np.min([1-single_checklist['T4'],single_checklist['T5']])
        # layer 22
        pendinglist['C1'] = np.min([1-(single_checklist['T5'] or single_checklist['PTI']),single_checklist['C1']])
        # layer 23
        pendinglist['C2'] = np.min([1-single_checklist['C1'],single_checklist['C2']])
        # layer 24
        pendinglist['C3'] = np.min([1-single_checklist['C2'],single_checklist['C3']])
        # layer 25
        pendinglist['C4'] = np.min([1-(single_checklist['C3'] or single_checklist['DR']),single_checklist['C4']])
        # layer 26
        pendinglist['NF001'] = np.min([1-single_checklist['C4'],single_checklist['NF001']])
        # layer 27
        pendinglist['DF001'] = np.min([1-single_checklist['NF001'],single_checklist['DF001']])
        # layer 28
        pendinglist['FI001'] = np.min([1-single_checklist['DF001'],single_checklist['FI001']])
        # layer 29
        pendinglist['DC001'] = np.min([1-single_checklist['FI001'],single_checklist['DC001']])
        # layer 30
        pendinglist['LV001'] = np.min([1-single_checklist['DC001'],single_checklist['LV001']])
        # layer 31
        pendinglist['SI001'] = np.min([1-single_checklist['LV001'],single_checklist['SI001']])
        # layer 32
        pendinglist['VFC'] = np.min([1-single_checklist['SI001'],single_checklist['VFC']])
        # layer 33
        pendinglist['ATF'] = np.min([1-single_checklist['VFC'],single_checklist['ATF']])
        # layer 34
        pendinglist['QC001'] = np.min([1-(single_checklist['ATF'] or single_checklist['VFC']),single_checklist['QC001']])
        # layer 35
        pendinglist['DVT'] = np.min([1-single_checklist['QC001'],single_checklist['DVT']])
        # layer 36
        pendinglist['QC002'] = np.min([1-single_checklist['DVT'],single_checklist['QC002']])
        # layer 37
        pendinglist['QC003'] = np.min([1-single_checklist['QC002'],single_checklist['QC003']])
        # layer 38
        for tsk in ['QC004','BLT002','WT002','WT003','D metric','RQA','GCA']:
            pendinglist[tsk] = np.min([1-single_checklist['QC003'],single_checklist[tsk]])
        # layer 39
        pendinglist['CAMO'] = np.min([1-(single_checklist['QC004'] or single_checklist['BLT002'] or single_checklist['WT002'] or single_checklist['WT002'] or single_checklist['D metric'] or single_checklist['RQA'] or single_checklist['GCA'] or single_checklist['BLT001']),single_checklist['CAMO']])
        # layer 40
        pendinglist['GLD001'] = np.min([1-single_checklist['CAMO'],single_checklist['GLD001']])
        # layer 41
        pendinglist['VehicleEOB'] = np.min([1-single_checklist['GLD001'],single_checklist['VehicleEOB']])
        # layer 40
        pendinglist['PACK1'] = np.min([1-single_checklist['VehicleEOB'],single_checklist['PACK1']])
        pending = pd.DataFrame(columns=['task','prior'])
        pending['task'] = [ind for ind in pendinglist.index.values if pendinglist[ind]==1]
        pending['prior'] = [Taskpriority[ind] for ind in pending['task']]
        # (ii) eliminate processing tasks
        ongoing = [tsk for tsk in single_processinglist.index if single_processinglist[tsk]==1]
        pending = pending[~pending.task.isin(ongoing)]
        if len(pending)==0:
            return 'None'
        else:
            pending = pending.sort_values(['prior'])
            pending = pending.dropna().drop_duplicates().reset_index(drop=True)
            return pending

# Production constraints
def new_tasks(single_pending,single_processinglist,TimeRem,TaskRem,ResourcePool,t,car,ProcessingTime):
    slot = (16*60+30)-(t.hour*60+t.minute) # time left to end of shift
    if single_pending is 'None' or slot<=0 or t.weekday()>4:
        return 'None'
    else:
        new = single_pending.copy(deep=True)
        for ind in new.index:
            newtemp = new.loc[ind] # This is a Series
            eventtemp = newtemp['task']
            # (i) check if remaining time allows scheduling of new single day tasks
            if (eventtemp in task_single) and (ProcessingTime[car][eventtemp]>slot) and len(new)>0:
                new = new.drop(ind)
            else:
                dropflag = False
                # (ii) check resource pool
                for rurs in ResourceOcpDict.keys(): # rurs: reusable resource
                    if (eventtemp in ResourceOcpDict[rurs]) and ResourcePool[rurs]<=0 and len(new)>0:
                        dropflag = True
                # (iii) check daily resource time pool
                for drs in TimeRem.keys():
                    if eventtemp in ResourceOcpDict[drs]:
                        if TimeOcp[eventtemp]>TimeRem[drs] and len(new)>0:
                            dropflag = True               
                # (iv) check daily task count pool
                if eventtemp in TaskRem.keys():
                    if TaskRem[eventtemp]<=0 and len(new)>0:
                        dropflag = True
                if dropflag == True:
                    new = new.drop(ind)
        new = new.reset_index(drop=True)
        new = new.iloc[np.arange(np.min([3-sum(single_processinglist.values),len(new)]))]
        new = new.dropna().reset_index(drop=True)
        if len(new)==0:
            return 'None'
        else:
            return new

# main function
def main(csv_input,t = dt.datetime(2018,10,1,8,30)):
    # standarized input
    tasklist = pd.read_csv(csv_input,sep=',',index_col='Veh_No')
    ResourcePool = deepcopy(ResourceMax)
    gantt = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # gantt chart info
    gantt = gantt.drop(['FirstDay'],1)
    for col in gantt.columns:
        for ind in gantt.index:
            if tasklist[col][ind]==0:
                gantt[col][ind] = str(-1)+'$'+str(-1)

    ProcessingTime = dict.fromkeys(tasklist.index)
    for car in tasklist.index:
        if car>=4:
            specs = ['BIW',PaintLocation,'GA4','ELEC','GA_R','QC','PACK']
            timelisttemp = tasktime.loc[tasktime.spec.isin(specs)]
            ProcessingTime[car] = dict(zip(timelisttemp.task,timelisttemp.duration))
        elif car==1:
            specs = ['BIW',PaintLocation,'GA1','ELEC','GA_R','QC','PACK']
            timelisttemp = tasktime.loc[tasktime.spec.isin(specs)]
            ProcessingTime[car] = dict(zip(timelisttemp.task,timelisttemp.duration))
        elif car==2:
            specs = ['BIW',PaintLocation,'GA2','ELEC','GA_R','QC','PACK']
            timelisttemp = tasktime.loc[tasktime.spec.isin(specs)]
            ProcessingTime[car] = dict(zip(timelisttemp.task,timelisttemp.duration))
        else:
            specs = ['BIW',PaintLocation,'GA3','ELEC','GA_R','QC','PACK']
            timelisttemp = tasktime.loc[tasktime.spec.isin(specs)]
            ProcessingTime[car] = dict(zip(timelisttemp.task,timelisttemp.duration))
    processinglist = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # list of processing tasks (at most 3 at the same time)

    # create tasks check list to derive stopflag - 0 stop, >0 continue looping
    checklist = tasklist.copy(deep=True) # create a seperate task checklist
    checklist = checklist.drop(['FirstDay'],1)
    # create event list and add BIWSOB into event list
    eventlist = pd.DataFrame(columns = ['event','veh','starttime','endtime']) 
    eventlist.event = ['BIWSOB' for car in checklist.index]
    eventlist.veh = checklist.index
    eventlist.starttime = [dt.datetime.strptime(tm, '%m/%d/%Y %H:%M') for tm in tasklist.FirstDay]
    eventlist.endtime = [dt.datetime.strptime(tm, '%m/%d/%Y %H:%M') for tm in tasklist.FirstDay]
    for car in gantt.index:
        gantt['BIWSOB'][car]=str(tasklist['FirstDay'][car])+'$'+'1'
    
    # eliminate started BIWSOB event (for real-time update function)
    for car in checklist.index:
        carsob = dt.datetime.strptime(tasklist['FirstDay'][car], '%m/%d/%Y %H:%M')
        checker = int(carsob>=t)
        checklist.at[car,'BIWSOB'] = checker
    eventlist = eventlist.loc[eventlist.endtime>=t]
    # start looping
    stopflag = checklist.values.sum()
    n = 0
    while stopflag>0:
        # check if this is the start of a day (8:30 to 4:30 -- 8 hour shift)
        if (t.hour*60+t.minute)==(8*60+30) or n==0:
            TimeRem = deepcopy(TimeDayMax) # reset time constraints
            TaskRem = deepcopy(TaskDayMax) # reset task constraints
            # add day end event
            if n==0:
                if (t.hour*60+t.minute)>990:
                    eventlist = eventlist.append(pd.Series(['EndofDay','all',t,dt.datetime(t.year,t.month,t.day,8,30)+dt.timedelta(days=1)], index=eventlist.columns),ignore_index=True)
                else:
                    eventlist = eventlist.append(pd.Series(['EndofDay','all',dt.datetime(t.year,t.month,t.day,16,30),dt.datetime(t.year,t.month,t.day,8,30)+dt.timedelta(days=1)], index=eventlist.columns),ignore_index=True)
            else:
                eventlist = eventlist.append(pd.Series(['EndofDay','all',t+dt.timedelta(minutes=480),t+dt.timedelta(days=1)], index=eventlist.columns),ignore_index=True) 
            eventlist = eventlist.sort_values(['endtime']).reset_index(drop=True)
        # finish-up current event
        events_current = eventlist.loc[eventlist.endtime==t]
        for ind in events_current.index:
            eventtemp = events_current.loc[ind]
            if eventtemp['event']=='EndofDay':
                eventlist = eventlist.drop(ind) # take off end-of-day event
            else:
                eventlist = eventlist.drop(ind) # task finished 
                checklist.at[eventtemp['veh'],eventtemp['event']] = 0
                # checklist = checklist.set_value(eventtemp['veh'],eventtemp['event'],0) # mark task as finished
                processinglist.at[eventtemp['veh'],eventtemp['event']] = 0
                # processinglist = processinglist.set_value(eventtemp['veh'],eventtemp['event'],0) # mark task as finished
                # release reusable resource to ResourcePool
                for rurs in ResourceOcpDict.keys():
                    if eventtemp['event'] in ResourceOcpDict[rurs]:
                        ResourcePool[rurs] = ResourcePool[rurs]+1            
        # for each car, search for pending tasks, update new events
        for car in checklist.index:
            car_checklist = checklist.loc[car]
            car_processinglist = processinglist.loc[car]
            car_pending = pending_tasks(car_checklist,car_processinglist)
            car_new = new_tasks(car_pending,car_processinglist,TimeRem,TaskRem,ResourcePool,t,car,ProcessingTime)
            # seize reusable resource from ResourcePool, consume time in TimeRem, consume task count in TaskRem
            if not(car_new is 'None'):
                for ind in car_new.index:
                    eventtemp = car_new.loc[ind] # This is a Series
                    for rurs in ResourceOcpDict.keys():
                        if eventtemp['task'] in ResourceOcpDict[rurs]:
                            ResourcePool[rurs] = ResourcePool[rurs]-1
                    for drs in TimeRem.keys():
                        if eventtemp['task'] in ResourceOcpDict[drs]:
                            TimeRem[drs] = TimeRem[drs]-TimeOcp[eventtemp['task']]
                    if eventtemp['task'] in TaskRem.keys():
                        TaskRem[eventtemp['task']] = TaskRem[eventtemp['task']]-1        
            # add new event to eventlist, calculate event end time:
            if not(car_new is 'None'):
                for ind in car_new.index:
                    car_newtemp = car_new.loc[ind] # Note: this is a Series
                    duration_temp = ProcessingTime[car][car_newtemp['task']]
                    if car_newtemp['task'] in task_multi:
                        if car_newtemp['task'] not in ['TRANS1','TRANS2']:
                            trmw = (t.weekday()+1)*480 - t.hour*60-t.minute # remaining time in current week
                            trmd = 16*60+30 - t.hour*60-t.minute # remaining time today
                            tleft = np.max([0,duration_temp -trmd]) # left-over task time
                            ngap = np.floor(tleft/480) # night gaps
                            duration_temp = duration_temp+ngap*960
                            if trmw<duration_temp:
                                duration_temp = duration_temp+2880 # add weekend gap into duration
                    eventlist = eventlist.append(pd.Series([car_newtemp['task'],car,t,t+dt.timedelta(minutes=duration_temp)], index=eventlist.columns),ignore_index=True)
                    duration_workday = int(ProcessingTime[car][car_newtemp['task']])
                    gantt.loc[car,car_newtemp['task']] = str(t)+'$'+str(duration_workday)  
                    processinglist.at[car,car_newtemp['task']] = 1
        
        # identify next event, move time tic to the time point
        eventlist = eventlist.sort_values(['endtime'])
        t = eventlist.endtime.values[0]
        t_trans = np.floor((t - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
        t = dt.datetime.utcfromtimestamp(t_trans)
        stopflag = checklist.values.sum()    
        n = n+1
        # gantt.to_csv('gantt.csv',sep=',')
    # output
    return gantt.to_csv(sep=',')
    

  