#!/usr/bin/env python3

import re
import csv
import operator

error_count = {}
error_count_header = ["Error", "Count"]    # Error's report header.
user_count = {}
user_count_header = ["Username", "INFO", "ERROR"]   # User's report header.

regex_error = r"ticky: (ERROR|INFO) ([\w\s']*)"    # Regex to extract ERROR or INFO data from the file.
regex_user = r"\(([\w\s.-]*)\)"    # Regex to extract the username of the user who generated the ERROR or INFO.


def writing_dictionary(file_path):
    """Extracting the data from the data source, parsing and storing into dictionaries, which will be used to generate
    the reports."""

    try:

        with open(file_path, encoding='utf-16') as file:

            for line in file:

                error = re.search(regex_error, line)
                user = re.search(regex_user, line)

                if user[1] not in user_count:
                    user_count[user[1].strip()] = {"ERROR": 0, "INFO": 0}

                if error[1].upper() == "ERROR":
                    error_count[error[2].strip()] = error_count.get(error[2].strip(), 0) + 1
                    user_count[user[1]]["ERROR"] += 1

                if error[1].upper() == "INFO":
                    user_count[user[1]]["INFO"] += 1

        file.close()

    except UnicodeDecodeError:

        print("Wrong decoding format while opening file!\nTry using 'utf-16' or 'utf-8' to decode the file or try"
              "opening as a regular file")


def writing_error_report(filename):
    """Generating the report using the error's extracted data."""

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerow(error_count_header)
        write.writerows([count, value] for count, value in sorted(error_count.items(), key=operator.itemgetter(1),
                                                                  reverse=True))

    file.close()


def writing_user_report(filename):
    """Generating the report using the user's extracted data."""

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerow(user_count_header)
        write.writerows([user, types["INFO"], types["ERROR"]] for user, types in sorted(user_count.items()))

    file.close()


writing_dictionary("syslog.log")
writing_error_report("error_message.csv")
writing_user_report("user_statistics.csv")
