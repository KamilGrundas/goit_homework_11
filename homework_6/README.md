# Homework #6

## Basic Task

Implement a database with the following schema:

1. **Table of Students**
2. **Table of Groups**
3. **Table of Lecturers**
4. **Table of Subjects** with information about the lecturer who teaches each subject.
5. **Table of Grades** with individual grades for each student, including the date when the grade was assigned.

Populate the database with random data (~30-50 students, 3 groups, 5-8 subjects, 3-5 lecturers, up to 20 grades for each student across all subjects). Use the **Faker** package for generating data.

### SQL Queries

Create SQL queries to retrieve the following information:

1. **Top 5 students** with the highest average grade across all subjects.
2. **Student with the highest average grade** in a specific subject.
3. **Average grade** in groups for a selected subject.
4. **Average grade** for all groups, considering all grades.
5. **Subjects taught by a selected lecturer.**
6. **List of students** in a selected group.
7. **Grades of students** in a selected group for a specific subject.
8. **Average grade** given by a lecturer for a specific subject.
9. **List of courses** attended by a student.
10. **List of courses** taught by a selected lecturer for a specific student.

For each query, create a separate file named `query_number.sql`, where `number` is the query number. Each file should contain an SQL statement that can be executed both in a database terminal and via `cursor.execute(sql)`.

