#EXPLORE BIKESHARE DATA
import time
import pandas as pd
import numpy as np
import datetime as dt

print('*'*40)
print('Hello! Let\'s explore some US bikeshare data!')
print('*'*40)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june','july',
'august','september','october','november','december']

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #take city input(chicago,new york,washington)
    city = input('Would you like to see data from \n\tChicago? \n\tNew York? \n\tWashington?\n--')
    city = city.lower()
    while city not in ('chicago', 'new york', 'washington'):
        city = input('Would you like to see data from \n\tChicago? \n\tNew York? \n\tWashington?\n--')
        city = city.lower()

    #take month input(may,june,....)
    month = input('Enter month to filter(Type "all" for no month filter):')
    month = month.lower()

    while month not in months:
        if( month != "all"):
            month = input('Enter month to filter(Type "all" for no month filter):')
            month = month.lower()
        else:
            break

    #take day input(monday,tuesday,...)
    day = input('Enter day to filter(Type "all" for no day filter):')
    day = day.lower()

    while day not in days:
        if(day != 'all'):
            day = input('Enter day to filter(Type "all" for no day filter):')
            day = day.lower()
        else:
            break

    print('-'*40)
    print('-'*40)
    return city, month, day

def load(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read the data of the given input city in dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time to datetime for extraction of required data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #filter according to month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #filter according to day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:',popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour:',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:',common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:',common_end_station)

    # display most frequent combination of start station and end station trip
    df_common_trip = df['Start Station']+" till "+df['End Station']
    common_trip = df_common_trip.mode().tolist()
    print('Most Common Combination:',common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:',total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    if 'Gender' in df and 'Birth Year' in df:
        # Display counts of gender
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth:",df['Birth Year'].min())
        print("Recent Year of Birth:",df['Birth Year'].max())
        print("Common Year of Birth:",df['Birth Year'].mode().tolist())
    else:
        print('No Gender Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load(city, month, day)
        #chceck if no data exists for the filter
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            #view the raw data
            view_data = input("Would you like to see the raw data ? (yes/no):")
            while view_data not in ('yes','no'):
                view_data = input("Would you like to see the raw data ? (yes/no):")

            if(view_data.lower() == 'yes'):
                go_on = 'yes'
                i = 0
                j = 50
                while j in range(df.shape[0]) and go_on != 'no':
                    print(df.iloc[i:j])
                    i += 50
                    j +=50
                    go_on = input('Would you like to see more? (yes/no)')
                    while go_on not in ('yes','no'):
                        go_on = input('Would you like to see more? (yes/no)')

                print('That\'s it !')

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            while restart not in ('yes','no'):
                restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            print('NO DATA AVAILABLE FOR FILTER')

if __name__ == "__main__":
	main()
