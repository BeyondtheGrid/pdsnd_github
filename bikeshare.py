#python bike project
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
day_key =['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
month_key = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
df_mk = pd.DataFrame(month_key)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you to see data from which city, Chicago, New York City, Washington? ').lower()
    while city not in (CITY_DATA.keys()):
        print('Please select from one of the available options: Chicago, New York City, or Washington')
        city = input('Chicago, New York City, Washington? ').lower()
        print('Selected city:', city)

        # get user input for month (all, january, february, ... , june)
    filter_check = input('Would you like to apply a time filter to the data, yes or no? ')
    while filter_check not in (['yes', 'no']):
        print('please answer "yes" or "no" if you would like a filter applied to the data: ')
        filter_check = input('Filter the data, yes or no? ')

        #user has confirmed they want to filter, next we will ask them how to filer.
    if filter_check == 'yes':
        filter_1 = input('Would you like to filter by month, day or both?: ')

        #this section filters by month and has guardins for invalid inputs
        if filter_1 == 'month':
            month = input('Which month : January, February, March, April, May, or June?').lower()
            day = 'all'
            while month not in (month_key):
                print('Please select from the available months:', (month_key))
                month = input('Which month : January, February, March, April, May, or June?').lower()
                day = 'all'

        #This sections filters by day and has guardins for invalid inputs
        elif filter_1 == 'day':
            day = input('Which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
            month = 'all'
            while day not in day_key:
                print('Please select from the available days:', day_key)
                day = input('Which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
            month = 'all'

        #This section handles a 'both' filter selction from the user and has guardings for invalid inputs
        elif filter_1 == 'both':
            month = input('Which month: January, February, March, April, May, or June?').lower()
            while month not in (month_key):
                print('Please select from the available months: ', (month_key))
                month = input('Which month: January, February, March, April, May, or June?').lower()
            day = input('Which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
            while day not in day_key:
                print('Please select from the available days', day_key)
                day = input('Which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
    else:
        #Shows the users has selected no filter and selects all months and days.
        print('No filter selected')
        month = 'all'
        day = 'all'
    print('-' * 40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data onto a Panda DataFrame
    city_pull = pd.read_csv(CITY_DATA[city])

    #Takes Start Time column and coverts it to datetime formate.
    city_pull['Start Time'] = pd.to_datetime(city_pull['Start Time'])

    #seperates the day and month from the date in the column.
    city_pull['month'] = city_pull['Start Time'].dt.month
    city_pull['day_of_week'] =city_pull['Start Time'].dt.day_name()

    #filters the month based on input.
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month  = months.index(month) + 1
        #creates DataFrame from the filtered months.

        city_pull =city_pull[city_pull['month'] == month]

        #This filters out day selection from the input.

    if day != 'all':
        city_pull = city_pull[city_pull['day_of_week'] == day.title()]


    return city_pull



def time_stats(city_pull):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = city_pull['month'].mode()[0]
    print('The most common month is:', month)

    # display the most common day of week
    day = city_pull['day_of_week'].mode()[0]
    print('The most common weekday is:', day)

    # display the most common start hour
    city_pull['hour'] = city_pull['Start Time'].dt.hour
    pop_hour = city_pull['hour'].mode()[0]
    print('The most common start hour is:', pop_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(city_pull):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_str_stat = city_pull['Start Station'].mode()[0]
    print('The most popularly starting station is:', pop_str_stat)

    # display most commonly used end station
    pop_end_stat = city_pull['End Station'].mode()[0]
    print('The most popularly trip terminal station is:', pop_end_stat)

    # display most frequent combination of start station and end station trip
    pop_trip = city_pull['Start Station'] + ' to ' + city_pull['End Station']
    print('The most popular trip is from:', pop_trip.mode()[0])
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(city_pull):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_trvl_dur = (pd.to_datetime(city_pull['End Time']) - pd.to_datetime(city_pull['Start Time'])).sum()
    days = tot_trvl_dur.days
    hours = tot_trvl_dur.seconds // (60 * 60)
    minutes = tot_trvl_dur.seconds % (60 * 60) // 60
    seconds = tot_trvl_dur.seconds % (60 * 60) % 60
    print('Total trip time is:', days, ':days', hours, ':hours', minutes, ':minutes', seconds, ':seconds')


    # display mean travel time
    avg_trvl_dur = (pd.to_datetime(city_pull['End Time']) - pd.to_datetime(city_pull['Start Time'])).mean()
    days = avg_trvl_dur.days
    hours = avg_trvl_dur.seconds // (60 * 60)
    minutes = avg_trvl_dur.seconds % (60 * 60) // 60
    seconds = avg_trvl_dur.seconds % (60 * 60) % 60
    print('Average trip time is:', days, ':days', hours, ':hours', minutes, ':minutes', seconds, ':seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city_pull):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(city_pull['User Type'].value_counts())
    print()

    # Display counts of gender
    if 'Gender' in(city_pull.columns):
        print(city_pull['Gender'].value_counts())
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in(city_pull.columns):
        year = city_pull['Birth Year']
        print('Earliest birth year is:', year.min())
        print('The most recent is:', year.max())
        print('Most common birth year is:', year.mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(city_pull):
    """Ask the user if they wants to display the raw data, 5 rows at a time."""
    raw = input('View raw data?: ')
    if raw.lower() == 'yes' or 'y':
        count = 0
        while True:
            print(city_pull.iloc[count: count+5])
            count += 5
            ask = input('Next 5 rows?, yes or no :')
            if ask.lower() != 'yes':
                break



def main():
    while True:
        city, month, day = get_filters()
        data_load = load_data(city, month, day)

        time_stats(data_load)
        station_stats(data_load)
        trip_duration_stats(data_load)
        user_stats(data_load)
        display_raw(data_load)

        restart = input('\n Restart Program? Enter yes or no.\n')
        if restart.lower() != 'yes' or 'y':
            break


if __name__ == "__main__":
	main()
