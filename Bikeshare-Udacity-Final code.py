#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please pick as city: Chicago, New York City, Washington:\n").lower()
        if city not in CITY_DATA:
            print('Ah oh! that is not an opion!\n')
            continue
        else:
            break
        
    # get user input for month (all, january, february, ... , june)
    while True:
        months= ['January','February','March','April','May','June','All']
        month = input("Pick a month between January and June(both inclusive) or 'All' to select all the months:\n").title()
        if month in months:
            break
        else:
            print("\n Please enter a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        day = input("Please pick a weekday or 'All' for all the days:\n").title()
        if day in days:
            break
        else:
            print("\n Please enter a valid month")

    print('-'*60)
    return city, month, day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by day of month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January','February','March','April','May','June','All']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month] 

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Times of Travel:\n')
    start_time = time.time()
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    
    #Used conditional statements to give most common month if all the months or all the days are selected.
    #Got mentor's help to implement my logic
    # display the most common month
    busy_month = df['Month'].mode()[0]
    if df['month'].nunique() > 1:
        print("The most common month is {}".format(busy_month))
    else:
        print("The current month is {}".format(busy_month))

    # display the most common day of week
    busy_day = df['Day'].mode()[0]
    if df['day_of_week'].nunique() > 1:
        print("The most common day is {}".format(busy_day))
    else:
        print("The current day is {}".format(busy_day))
        
    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    busy_hour = df['Start Hour'].mode()[0]
    print("The most common Start Hour is {}:00 hrs".format(busy_hour))


    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*60)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('Station Stats:\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(common_start_station))


    # display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"to"+" "+ df['End Station']
    common_combination= df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(common_combination))


    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*60)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Trip Duration Stats:\n')
    start_time = time.time()
    print('Total Trips = {:,}'.format(len(df)))
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minute,second = divmod(total_travel_time,60)
    hour,minute = divmod(minute,60)
    print('Total Travel time is {:,} hour(s) {} mins {}sec'.format(hour,minute,second))
    
    # display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean())
    minute,second = divmod(avg_travel_time,60)
    hour,minute = divmod(minute,60)
    print('Avg Travel time is {} hour(s) {} mins {} sec'.format(hour,minute,second))
    
    print("\nThis took {:.8f} seconds.".format(time.time() - start_time))
    print('-'*60)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('User Stats:\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:',user_types)
    
    
    #Washington doesn't have a few columns,so used try & except (idea from Udacity Knowledge)
    # Display counts of gender
    try:
        print('The counts of gender are: ', df['Gender'].value_counts())
    except KeyError:
        ('NA')
    
    # Display earliest, most recent, and most common year of birth
    #earliest
    try:
        print ('The oldest customer was born in {} year'.format(int(df['Birth Year'].min())))
    except KeyError :
        ('NA')
    #most recent   
    try:
        print ('The youngest customer was born in {} year'.format(int(df['Birth Year'].max())))
    except KeyError :
        ('NA')
    #most common year of birth   
    try:
        print('Most customers are born in {} year'.format(int(df['Birth Year'].mode()[0])))
    except KeyError : 
        ('NA')
    
    print("\nThis took {:.5f} seconds.".format(time.time() - start_time))
    print('-'*60)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:




