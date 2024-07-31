import pandas as pd
import numpy as np

def load_data(city):
    """
    Load data for the specified city and preprocess it.
    
    Args:
    city (str): The name of the city to load data for.

    Returns:
    df (DataFrame): The preprocessed data for the city.
    """
    CITY_info = {
        'chicago': '/Users/jouda/Downloads/chicago.csv',
        'new york city': '/Users/jouda/Downloads/new_york_city.csv',
        'washington': '/Users/jouda/Downloads/washington.csv'
    }
    df = pd.read_csv(CITY_info[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    return df

def load_data_filtered(city, month=None, day=None):
    """
    Load and filter data for the specified city, month, and/or day.

    Args:
    city (str): The name of the city to load data for.
    month (str): The month to filter by (optional).
    day (str): The day of week to filter by (optional).

    Returns:
    df (DataFrame): The filtered data for the city.
    """
    df = load_data(city)
    if month:
        month = month.title()
        month_number = pd.to_datetime(month, format='%B').month
        df = df[df['month'] == month_number]

    if day:
        day = day.title()
        df = df[df['day_of_week'] == day]

    return df

def most_common_hour(df):
    """
    Find the most common start hour in the data.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    int: The most common start hour.
    """
    return df['hour'].mode()[0]

def user_types_count(df):
    """
    Count the number of users of each type.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    Series: Counts of user types.
    """
    return df['User Type'].value_counts()

def gender_count(df):
    """
    Count the number of users of each gender.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    Series: Counts of gender.
    """
    return df['Gender'].value_counts()

def birth_year_stats(df):
    """
    Calculate statistics about birth years.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    tuple: Earliest year, most recent year, and most common year of birth.
    """
    earliest_year = int(df['Birth Year'].min())
    most_recent_year = int(df['Birth Year'].max())
    most_common_year = int(df['Birth Year'].mode()[0])
    return earliest_year, most_recent_year, most_common_year

def most_common_month(df):
    """
    Find the most common month in the data.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    int: The most common month.
    """
    return df['month'].mode()[0]

def most_common_day(df):
    """
    Find the most common day of week in the data.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    str: The most common day of the week.
    """
    return df['day_of_week'].mode()[0]

def total_travel_time(df):
    """
    Calculate the total travel time.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    int: The total travel time in seconds.
    """
    return df['Trip Duration'].sum()

def average_travel_time(df):
    """
    Calculate the average travel time.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    float: The average travel time in seconds.
    """
    return df['Trip Duration'].mean()

def most_common_stations(df):
    """
    Find the most common start and end stations, and the most common trip.

    Args:
    df (DataFrame): The data to analyze.

    Returns:
    tuple: Most common start station, end station, and trip.
    """
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    return common_start_station, common_end_station, common_trip

def display_raw_data(df):
    """
    Display 5 lines of raw data at a time upon user request.

    Args:
    df (DataFrame): The data to display.
    """
    start = 0
    while True:
        show_data = input("Do you want to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_data != 'yes':
            break
        print(df.iloc[start:start + 5])
        start += 5

def main():
    """
    Main function to handle user input and display statistics.
    """
    while True:
        city = input("Enter city name (Chicago, New York City, Washington): ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("Invalid city name. Please enter either Chicago, New York City, or Washington.")
            continue
        month = input("Enter month name (e.g., January) or 'all' for no filter: ").lower()
        day = input("Enter day of week (e.g., Monday) or 'all' for no filter: ").lower()

        if month != 'all' and day != 'all':
            df = load_data_filtered(city, month, day)
        elif month != 'all':
            df = load_data_filtered(city, month=month)
        elif day != 'all':
            df = load_data_filtered(city, day=day)
        else:
            df = load_data(city)

        print(f"\nCalculating statistics for {city.title()}...\n")

        print(f"Most common month: {most_common_month(df)}")
        print(f"Most common day of week: {most_common_day(df)}")
        print(f"Most common start hour: {most_common_hour(df)}")

        start_station, end_station, trip = most_common_stations(df)
        print(f"Most common start station: {start_station}")
        print(f"Most common end station: {end_station}")
        print(f"Most common trip: {trip}")

        print(f"Total travel time: {total_travel_time(df)} seconds")
        print(f"Average travel time: {average_travel_time(df)} seconds")

        user_types = user_types_count(df)
        print(f"Counts of user types:\n{user_types}")

        if city in ['chicago', 'new york city']:
            gender = gender_count(df)
            print(f"Counts of gender:\n{gender}")

            earliest, recent, common = birth_year_stats(df)
            print(f"Earliest year of birth: {earliest}")
            print(f"Most recent year of birth: {recent}")
            print(f"Most common year of birth: {common}")

        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no: ").lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
