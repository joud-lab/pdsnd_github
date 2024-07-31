"""
This module provides a command-line interface for analyzing
bikeshare data for Chicago, New York City, and Washington.
"""

import pandas as pd
import numpy as np
def load_data(city):

    CITY_DATA = {
        'chicago': '/Users/jouda/Downloads/chicago.csv',
        'new york city': '/Users/jouda/Downloads/new_york_city.csv',
        'washington': '/Users/jouda/Downloads/washington.csv'
    }
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    return df
def load_data_filtered(city, month=None, day=None):


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

    return df['hour'].mode()[0]

def user_types_count(df):

    return df['User Type'].value_counts()

def gender_count(df):

    return df['Gender'].value_counts()

def birth_year_stats(df):

    earliest_year = int(df['Birth Year'].min())
    most_recent_year = int(df['Birth Year'].max())
    most_common_year = int(df['Birth Year'].mode()[0])
    return earliest_year, most_recent_year, most_common_year

def most_common_month(df):

    return df['month'].mode()[0]

def most_common_day(df):

    return df['day_of_week'].mode()[0]

def total_travel_time(df):

    return df['Trip Duration'].sum()

def average_travel_time(df):

    return df['Trip Duration'].mean()

def most_common_stations(df):

    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    return common_start_station, common_end_station, common_trip

def display_raw_data(df):

    start = 0
    while True:
        show_data = input("Do you want to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_data != 'yes':
            break
        print(df.iloc[start:start + 5])
        start += 5

def main():
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

