import pandas as pd
from statsmodels.stats.proportion import proportion_confint as ci
from natsort import natsorted
import numpy as np


def get_clean_cape_dataframe(filepath):
    """
    read the cleaned data as dataframe
    Args:
        filepath: str
        the location of the csv file
    Returns:
        dataframe
    """
    df = pd.read_csv(filepath)
    return df


def get_depts_and_courses_dictionary(df):
    """
    get all courses for departments
    Args:
        df: dataframe

    Returns:
        depths_courses: dict

    Examples:
    --------
        # >>> df = get_clean_cape_dataframe(filepath)
        # >>> get_depts_and_courses_dictionary(df)
        depths_courses = {'AAS': ['10', '11', '170', '190'], 'ANAR': ['100', '114', '115', '116', '135', '135S', '143']}

    """
    df = (df['Course_ID'].str.split(expand=True)
          .rename(columns={0: 'dept', 1: 'course'})
          .drop_duplicates())

    depts = natsorted(df.dept.unique())
    df = df.set_index(['dept', 'course']).sort_index()

    depts_courses = {dept: natsorted(df.loc[dept].index) for dept in depts}

    return depts_courses


def get_time_dicionary(df):
    """
    group the dataframe using the Course_ID, the average spending time for a particular course between different terms is calculated
    compare the time with other courses
    Args:
        df
    Returns:
        time: dict

    Examples:
    --------
        # >>> df = get_clean_cape_dataframe(filepath)
        # >>> get_time_dictionary(df)

        new_df:
                time  depart_avg_time  ...  depart_time_diff  total_time_diff
        Course_ID                         ...
        AAS 10     3.80             3.50  ...              0.30        -1.747582
        AAS 11     4.15             3.50  ...              0.65        -1.397582
        AAS 170    3.06             3.50  ...             -0.44        -2.487582
        AAS 190    2.18             3.50  ...             -1.32        -3.367582

        time:
        {'AAS 10': {'expected': '3.8', 'statement': 'This course will take an average amount of time outside of class.',
        'color': 'black'}, 'AAS 11': {'expected': '4.15',
        'statement': 'This course will take an average amount of time outside of class.', 'color': 'black'}
    """

    df = df[['Course_ID', 'time']]
    # groupby to get average time for same courses in different quarters
    gb = df[['time', 'Course_ID']].groupby('Course_ID').mean().round(2)
    # print(gb)

    # for departments
    depths_time = {}
    depths_courses = get_depts_and_courses_dictionary(df)
    for dept, courses in depths_courses.items():
        times = []
        for course in courses:
            mask = df['Course_ID'].str.startswith(dept + ' ' + course)
            if mask.any():
                times.extend(df.loc[mask, 'time'])

        if times:
            average_time = np.mean(times)
            std_deviation = np.std(times)
            depths_time[dept] = (average_time, std_deviation)

    # for all courses
    total_average = float(gb.mean())
    total_sd = float(gb.std())

    df['department'] = df['Course_ID'].str.split().str[0]
    df['depart_avg_time'] = df['department'].map(lambda x: depths_time[x][0] if x in depths_time else None)

    gb = df.groupby('Course_ID').mean().round(2)
    gb['total_avg_time'] = total_average
    gb['depart_time_diff'] = gb['time'] - gb['depart_avg_time']
    gb['total_time_diff'] = gb['time'] - total_average

    # warning statements
    warning = (
        'This course will take more time outside of class than average.'
    )
    normal = (
        'This course will take an average amount of time outside of class.'
    )
    relax = (
        'This course might take less time outside of class than average.'
    )

    def get_statement_and_color(dev, sd):
        if (dev > sd):
            statement = warning
            color = 'red'
        elif (abs(dev) < sd):
            statement = normal
            color = 'black'
        else:
            statement = relax
            color = 'green'
        return statement, color

    time = {}
    for course in gb.index:
        statement, color = get_statement_and_color(gb.loc[course, 'depart_time_diff'], total_sd)
        time[course] = {'expected': str(float(gb.loc[course, 'time'])),
                        'statement': statement, 'color': color}

    return time, gb


def get_grade_dictionary(df):
    """
    group the dataframe using the Course_ID, the average expected and actual gpa for a particular course between different terms is calculated
    compare the expected gpa and actual gpa
    Args:
        df
    Returns:
        grade: dict

    Examples:
    --------
        # >>> df = get_clean_cape_dataframe(filepath)
        # >>> get_grade_dictionary(df)

        new_df:
                        expected_gpa  actual_gpa   dev
        Course_ID
        AAS 10             3.70        3.68 -0.02
        AAS 11             3.84        3.71 -0.13
        AAS 170            3.88        3.80 -0.08
        AAS 190            3.93        4.00  0.07

        grade:
        {'AAS 10': {'expected': 'B+', 'color': 'black', 'statement': 'Students tend to get the grade they expect for this course.'},
        'AAS 11': {'expected': 'A-', 'color': 'black', 'statement': 'Students tend to get the grade they expect for this course.'},
        'AAS 170': {'expected': 'A-', 'color': 'black', 'statement': 'Students tend to get the grade they expect for this course.'}

    """
    df = df[['Course_ID', 'expected_gpa', 'actual_gpa']]

    # groupby to get the mean grade and round to 2 decimal places
    gb = df.groupby('Course_ID').mean().round(2)
    gb['dev'] = gb['actual_gpa'] - gb['expected_gpa']

    # warning statements
    warning = (
        'Students tend to get lower grades than they expect for this course.'
    )
    normal = (
        'Students tend to get the grade they expect for this course.'
    )
    relax = (
        'Students tend to get higher grades than they expect for this course.'
    )

    def GPA_val_to_grade(val):
        if val == 4.0:
            grade = 'A'
        elif val >= 3.7:
            grade = 'A-'
        elif val >= 3.3:
            grade = 'B+'
        elif val >= 3.0:
            grade = 'B'
        elif val >= 2.7:
            grade = 'B-'
        elif val >= 2.3:
            grade = 'C+'
        elif val >= 2.0:
            grade = 'C'
        elif val >= 1.7:
            grade = 'C-'
        elif val >= 1.0:
            grade = 'D'
        return grade

    def get_statement_and_color(dev):
        if dev > 0.4:
            color = 'green'
            statement = relax
        elif dev < -0.4:
            color = 'red'
            statement = warning
        else:
            color = 'black'
            statement = normal

        return statement, color

    grade = {}
    for course in gb.index:
        statement, color = get_statement_and_color(gb.loc[course, 'dev'])
        grade[course] = {
            'expected': GPA_val_to_grade(gb.loc[course, 'actual_gpa']),
            'color': color,
            'statement': statement
        }

    return grade, gb


# def get_prof_ranking_dictionary(df):
#     """
#     get the professor ranking dictionary
#     Args:
#         df
#     Returns:
#         ranking: dict
#     """
#     df = (df[['instr', 'course', 'evals', 'instr_weighted_evals']])
#
#     gb = df.groupby(['course', 'instr']).sum()
#
#     gb.loc[:, 'lower'], gb.loc[:, 'upper'] = ci(gb.instr_weighted_evals,
#                                                 gb.evals, method='wilson')
#
#     # populate the dictionary
#     ranking = {}
#     for course, instr in gb.index:
#         professors_sorted = gb.loc[course].sort_values(by='lower',
#                                                        ascending=False)
#         ranking[course] = list(professors_sorted.index)
#
#     return ranking


# df = get_clean_cape_dataframe('data_clean.csv')
# depts_courses = get_depts_and_courses_dictionary(df)
# print(get_grade_dictionary(df))
