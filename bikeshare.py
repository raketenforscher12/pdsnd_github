import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_list = ["new york city", "washington", "chicago"]
month_list = ["all", "january", "february", "march", "april", "may", "june"]
day_list = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Would you like to explore data for Chicago, New York City, or Washington?")
        if city.lower() in city_list:
            print("Okay, let's explore data for {}!".format(city.title()))
            break
        else:
           print("That is not an option.")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to look at - january, february, march, april, may, june, or all?")
        if month.lower() in month_list:
            print("Okay, let's explore data for {}!".format(month.title()))
            break
        else:
           print("That is not an option.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input("Which day of the week would you like to evaluate - monday, tuesday ... sunday, or all?")
        if day.lower() in day_list:
            print("Okay, let's explore data for {}!".format(day.title()))
            break
        else:
           print("That is not an option.")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month,day, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print(df.columns)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is {}.".format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is {}.".format(popular_day))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is {}.".format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}.".format(popular_start))

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most commonly used end station is {}.".format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    popular_startend = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most commonly used combination of start and end station is: \n {}.".format(popular_startend))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total travel time is {} seconds or {} minutes.".format(total_travel.round(2), (total_travel/60).round(2)))

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds or {} minutes.".format(mean_travel.round(2), (mean_travel/60).round(2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types: \n{}".format(user_types))

    # TO DO: Display counts of gender
    def gender_data(df):
        try:
            gender = df['Gender'].value_counts()
            print("\nCounts of gender:\n{}".format(gender))
            return gender
        except:
            print('\nThere is no gender data for this city.')

    gender_data(df)


    # TO DO: Display earliest, most recent, and most common year of birth
    def birthday_data(df):
        try:
            earliest_year = df['Birth Year'].min()
            recent_year = df['Birth Year'].max()
            common_year = df['Birth Year'].mode()[0]
            print("\nThe earliest year of birth is {}, the most recent year of  birth is {}, and the most common year of birth is {}.".format(int(earliest_year),int(recent_year),int(common_year)))
            return earliest_year
        except:
            print('\nThere is no data on year of birth for this city.')
    birthday_data(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while view_data.lower() == "yes":
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display.lower() == "no":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
