# -*- coding: utf-8 -*-
"""
Total alg demo

A PPPR test
"""

# Import Packages
import numpy as np
import pandas as pd
import datetime as dt
from copy import deepcopy

# Global
ResourceMax = {'LaserRoom':2,'ManualWelding':9,'ManualDoorOp':12,'CMM':2, 'CDworker':1,'Hoist':8}
ResourcePool = deepcopy(ResourceMax)
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
        # (i) check process tree
        pending = pd.DataFrame(columns=['task','prior'])
        # layer 0
        if single_checklist['BIWSOB']==0:
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
            pending = pending.loc[pending.task!='RF301']
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
            pending_temp = pd.DataFrame([['C metric',Taskpriority['C metric']],['BS Audit',Taskpriority['BS Audit']]],columns=pending.columns)
            pending = pending.append(pending_temp,ignore_index=True)            
        # layer 10
        if single_checklist['C metric']==0:
            pending = pending.loc[pending.task!='C metric']
        if single_checklist['BS Audit']==0:
            pending = pending.loc[pending.task!='BS Audit']
        if single_checklist['AS101']+single_checklist['C metric']+single_checklist['BS Audit']==0:
            pending = pending.append(pd.Series(['TRANSSOB',Taskpriority['TRANSSOB']], index=pending.columns),ignore_index=True)
        # layer 11
        if single_checklist['TRANSSOB']==0:
            pending = pending.loc[pending.task!='TRANSSOB']
            pending = pending.append(pd.Series(['TRANS1',Taskpriority['TRANS1']], index=pending.columns),ignore_index=True)
        # layer 12
        if single_checklist['TRANS1']==0:
            pending = pending.loc[pending.task!='TRANS1']
            pending = pending.append(pd.Series(['PAINT',Taskpriority['PAINT']], index=pending.columns),ignore_index=True)
        # layer 13
        if single_checklist['PAINT']==0:
            pending = pending.loc[pending.task!='PAINT']
            pending = pending.append(pd.Series(['TRANS2',Taskpriority['TRANS2']], index=pending.columns),ignore_index=True)
        # layer 14
        if single_checklist['TRANS2']==0:
            pending = pending.loc[pending.task!='TRANS2']
            pending_temp = pd.DataFrame([['GASOB',Taskpriority['GASOB']],['BLT001',Taskpriority['BLT001']]],columns=pending.columns)
            pending = pending.append(pending_temp,ignore_index=True)
        # layer 15
        if single_checklist['GASOB']==0:
            pending = pending.loc[pending.task!='GASOB']
            pending_temp = pd.DataFrame([['T1',Taskpriority['T1']],['PTI',Taskpriority['PTI']],['DR',Taskpriority['DR']]],columns=pending.columns)
            pending = pending.append(pending_temp,ignore_index=True)
        if single_checklist['BLT001']==0:
            pending = pending.loc[pending.task!='BLT001']
        # layer 16
        if single_checklist['T1']==0:
            pending = pending.loc[pending.task!='T1']
            pending = pending.append(pd.Series(['T2',Taskpriority['T2']], index=pending.columns),ignore_index=True)
        if single_checklist['PTI']==0:
            pending = pending.loc[pending.task!='PTI']
        if single_checklist['DR']==0:
            pending = pending.loc[pending.task!='DR']
        # layer 17
        if single_checklist['T2']==0:
            pending = pending.loc[pending.task!='T2']
            pending = pending.append(pd.Series(['WT001',Taskpriority['WT001']], index=pending.columns),ignore_index=True)
        # layer 18
        if single_checklist['WT001']==0:
            pending = pending.loc[pending.task!='WT001']
            pending = pending.append(pd.Series(['T3',Taskpriority['T3']], index=pending.columns),ignore_index=True)
        # layer 19
        if single_checklist['T3']==0:
            pending = pending.loc[pending.task!='T3']
            pending = pending.append(pd.Series(['T4',Taskpriority['T4']], index=pending.columns),ignore_index=True)
        # layer 20
        if single_checklist['T4']==0:
            pending = pending.loc[pending.task!='T4']
            pending = pending.append(pd.Series(['T5',Taskpriority['T5']], index=pending.columns),ignore_index=True)
        # layer 21
        if single_checklist['T5']==0:
            pending = pending.loc[pending.task!='T5']
        if single_checklist['T5']+single_checklist['PTI']==0:
            pending = pending.append(pd.Series(['C1',Taskpriority['C1']], index=pending.columns),ignore_index=True)
        # layer 22
        if single_checklist['C1']==0:
            pending = pending.loc[pending.task!='C1']
            pending = pending.append(pd.Series(['C2',Taskpriority['C2']], index=pending.columns),ignore_index=True)
        # layer 23
        if single_checklist['C2']==0:
            pending = pending.loc[pending.task!='C2']
            pending = pending.append(pd.Series(['C3',Taskpriority['C3']], index=pending.columns),ignore_index=True)
        # layer 24
        if single_checklist['C3']==0:
            pending = pending.loc[pending.task!='C3']
        if single_checklist['C3']+single_checklist['DR']==0:
            pending = pending.append(pd.Series(['C4',Taskpriority['C4']], index=pending.columns),ignore_index=True)
        # layer 25
        if single_checklist['C4']==0:
            pending = pending.loc[pending.task!='C4']
            pending = pending.append(pd.Series(['NF001',Taskpriority['NF001']], index=pending.columns),ignore_index=True)
        # layer 26
        if single_checklist['NF001']==0:
            pending = pending.loc[pending.task!='NF001']
            pending = pending.append(pd.Series(['DF001',Taskpriority['DF001']], index=pending.columns),ignore_index=True)
        # layer 27
        if single_checklist['DF001']==0:
            pending = pending.loc[pending.task!='DF001']
            pending = pending.append(pd.Series(['FI001',Taskpriority['FI001']], index=pending.columns),ignore_index=True)
        # layer 28
        if single_checklist['FI001']==0:
            pending = pending.loc[pending.task!='FI001']
            pending = pending.append(pd.Series(['DC001',Taskpriority['DC001']], index=pending.columns),ignore_index=True)
        # layer 29
        if single_checklist['DC001']==0:
            pending = pending.loc[pending.task!='DC001']
            pending = pending.append(pd.Series(['LV001',Taskpriority['LV001']], index=pending.columns),ignore_index=True)
        # layer 30
        if single_checklist['LV001']==0:
            pending = pending.loc[pending.task!='LV001']
            pending = pending.append(pd.Series(['SI001',Taskpriority['SI001']], index=pending.columns),ignore_index=True)
        # layer 31
        if single_checklist['SI001']==0:
            pending = pending.loc[pending.task!='SI001']
            pending = pending.append(pd.Series(['VFC',Taskpriority['VFC']], index=pending.columns),ignore_index=True)
        # layer 32
        if single_checklist['VFC']==0:
            pending = pending.loc[pending.task!='VFC']
            pending = pending.append(pd.Series(['ATF',Taskpriority['ATF']], index=pending.columns),ignore_index=True)
        # layer 33
        if single_checklist['ATF']==0:
            pending = pending.loc[pending.task!='ATF']
        if single_checklist['VFC']+single_checklist['ATF']==0:
            pending = pending.append(pd.Series(['QC001',Taskpriority['QC001']], index=pending.columns),ignore_index=True)
        # layer 34
        if single_checklist['QC001']==0:
            pending = pending.loc[pending.task!='QC001']
            pending = pending.append(pd.Series(['DVT',Taskpriority['DVT']], index=pending.columns),ignore_index=True)
        # layer 35
        if single_checklist['DVT']==0:
            pending = pending.loc[pending.task!='DVT']
            pending = pending.append(pd.Series(['QC002',Taskpriority['QC002']], index=pending.columns),ignore_index=True)
        # layer 36
        if single_checklist['QC002']==0:
            pending = pending.loc[pending.task!='QC002']
            pending = pending.append(pd.Series(['QC003',Taskpriority['QC003']], index=pending.columns),ignore_index=True)
        # layer 37
        if single_checklist['QC003']==0:
            pending = pending.loc[pending.task!='QC003']            
            pending_temp = pd.DataFrame([['QC004',Taskpriority['QC004']],['BLT002',Taskpriority['BLT002']],['WT002',Taskpriority['WT002']],['WT003',Taskpriority['WT003']],['D metric',Taskpriority['D metric']],['RQA',Taskpriority['RQA']],['GCA',Taskpriority['GCA']]],columns=pending.columns)
            pending = pending.append(pending_temp,ignore_index=True)
        # layer 38
        for tsk in ['QC004','BLT002','WT002','WT003','D metric','RQA','GCA','BLT001']:
            if single_checklist[tsk]==0:
                pending = pending.loc[pending.task!=tsk]
        if sum([single_checklist[tsk] for tsk in ['QC004','BLT002','WT002','WT003','D metric','RQA','GCA','BLT001']])==0:
            pending = pending.append(pd.Series(['CAMO',Taskpriority['CAMO']], index=pending.columns),ignore_index=True)
        # layer 39
        if single_checklist['CAMO']==0:
            pending = pending.loc[pending.task!='CAMO']
            pending = pending.append(pd.Series(['GLD001',Taskpriority['GLD001']], index=pending.columns),ignore_index=True)
        # layer 40
        if single_checklist['GLD001']==0:
            pending = pending.loc[pending.task!='GLD001']
            pending = pending.append(pd.Series(['VehicleEOB',Taskpriority['VehicleEOB']], index=pending.columns),ignore_index=True)
        # layer 41
        if single_checklist['VehicleEOB']==0:
            pending = pending.loc[pending.task!='VehicleEOB']
            pending = pending.append(pd.Series(['PACK1',Taskpriority['PACK1']], index=pending.columns),ignore_index=True)
        # layer 41
        if single_checklist['PACK1']==0:
            pending = pending.loc[pending.task!='PACK1']
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
            if (eventtemp in task_single) and (ProcessingTime[car][eventtemp]>slot):
                new = new.drop(ind)
            else:
                # (ii) check resource pool
                for rurs in ResourceOcpDict.keys(): # rurs: reusable resource
                    if (eventtemp in ResourceOcpDict[rurs]) and ResourcePool[rurs]<=0 and len(new)>0:
                        new = new.drop(ind)
                # (iii) check daily resource time pool
                for drs in TimeRem.keys():
                    if eventtemp in ResourceOcpDict[drs]:
                        if TimeOcp[eventtemp]>TimeRem[drs] and len(new)>0:
                            new = new.drop(ind)                
                # (iv) check daily task count pool
                if eventtemp in TaskRem.keys():
                    if TaskRem[eventtemp]<=0 and len(new)>0:
                        new = new.drop(ind)
        new = new.reset_index(drop=True)
        new = new.iloc[np.arange(np.min([3-sum(single_processinglist.values),len(new)]))]
        new = new.dropna().reset_index(drop=True)
        if len(new)==0:
            return 'None'
        else:
            return new

# main function
def main(csv_input='projA_input2.csv',t = dt.datetime(2018,10,1,8,30)):
    # standarized input
    tasklist = pd.read_csv(csv_input,sep=',',index_col='Veh_No')
    gantt_s = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # gantt chart start time
    gantt_s = gantt_s.drop(['FirstDay'],1)
    gantt_e = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # gantt chart end time
    gantt_e = gantt_e.drop(['FirstDay'],1)
    gantt_d = pd.DataFrame(0,index=tasklist.index,columns=tasklist.columns) # gantt chart utilization of workdays
    gantt_d = gantt_d.drop(['FirstDay'],1)
    for col in gantt_s.columns:
        for ind in gantt_s.index:
            if tasklist[col][ind]==0:
                gantt_s[col][ind] = -1
                gantt_e[col][ind] = -1
                gantt_d[col][ind] = -1

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
    eventlist.starttime = [dt.datetime.strptime(tm, '%m/%d/%Y %I:%M') for tm in tasklist.FirstDay]
    eventlist.endtime = [dt.datetime.strptime(tm, '%m/%d/%Y %I:%M') for tm in tasklist.FirstDay]
    gantt_s['BIWSOB'] = eventlist.starttime.values
    gantt_e['BIWSOB'] = eventlist.endtime.values
    # eliminate started BIWSOB event (for real-time update function)
    for car in checklist.index:
        carsob = eventlist.endtime[car-1]
        checker = int(carsob>=t)
        checklist.at[car,'BIWSOB'] = checker
    eventlist = eventlist.loc[eventlist.endtime>=t]
    # start looping
    stopflag = checklist.values.sum() 
    while stopflag>0:
        # check if this is the start of a day (8:30 to 4:30 -- 8 hour shift)
        if (t.hour*60+t.minute)==(8*60+30):
            TimeRem = deepcopy(TimeDayMax) # reset time constraints
            TaskRem = deepcopy(TaskDayMax) # reset task constraints
            # add day end event
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
                    eventlist = eventlist.append(pd.Series([car_newtemp['task'],car,t,t+dt.timedelta(minutes=duration_temp)], index=eventlist.columns),ignore_index=True)
                    gantt_s.at[car,car_newtemp['task']] = t
                    gantt_e.at[car,car_newtemp['task']] = t+dt.timedelta(minutes=duration_temp)
                    gantt_d.at[car,car_newtemp['task']] = duration_temp
                    processinglist.at[car,car_newtemp['task']] = 1
        
        # identify next event, move time tic to the time point
        eventlist = eventlist.sort_values(['endtime'])
        t = eventlist.endtime.values[0]
        t_trans = np.floor((t - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
        t = dt.datetime.utcfromtimestamp(t_trans)
        stopflag = checklist.values.sum()         
    # output
    gantt_s.to_csv('gantt_s.csv',sep=',')
    gantt_e.to_csv('gantt_e.csv',sep=',') 
    gantt_d.to_csv('gantt_d.csv',sep=',')  
    return 'gantt_s.csv','gantt_d.csv'