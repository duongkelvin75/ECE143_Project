import pandas as pd
from statsmodels.stats.proportion import proportion_confint as ci


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


def get_time_dicionary(df):
    """
    group the dataframe using the Course_ID, the average spending time for a particular course between different terms is calculated
    compare the time with other courses
    Args:
        df
    Returns:
        time: dict
    """
    df = df[['Course_ID', 'time']]

    # groupby to get average time for courses
    gb = df[['time', 'Course_ID']].groupby('Course_ID').mean().round(2)

    # average time spent for all courses
    average = float(gb.mean())

    # standard deviation of time spent for all courses
    sd = float(gb.std())

    # build the deviation column
    gb['dev'] = gb - average

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
        statement, color = get_statement_and_color(gb.loc[course, 'dev'], sd)
        time[course] = {'expected': str(float(gb.loc[course, 'time'])),
                        'statement': statement, 'color': color}

    return time


def get_grade_dictionary(df):
    """
    group the dataframe using the Course_ID, the average expected and actual gpa for a particular course between different terms is calculated
    compare the expected gpa and actual gpa
    Args:
        df
    Returns:
        grade: dict
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

    return grade


def get_prof_ranking_dictionary(df):
    """

    Args:
        df:

    Returns:

    """
    df = (df[['instr', 'course', 'evals', 'instr_weighted_evals']])

    gb = df.groupby(['course', 'instr']).sum()

    gb.loc[:, 'lower'], gb.loc[:, 'upper'] = ci(gb.instr_weighted_evals,
                                                gb.evals, method='wilson')

    # populate the dictionary
    ranking = {}
    for course, instr in gb.index:
        professors_sorted = gb.loc[course].sort_values(by='lower',
                                                       ascending=False)
        ranking[course] = list(professors_sorted.index)

    return ranking


# df = get_clean_cape_dataframe('data_clean.csv')
# print(get_grade_dictionary(df))
