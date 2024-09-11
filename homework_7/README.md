
# Homework #7

## Introduction

In this homework assignment, we will continue working with the homework from the previous module. In this assignment, we will use the PostgreSQL database. In the command line, run a Docker container:

```bash
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

Instead of `some-postgres`, choose a container name, and instead of `mysecretpassword`, come up with a password to connect to the database.

If you agree with your mentor and technically cannot use PostgreSQL, you may replace it with SQLite.

## Steps to complete the homework:

### Step One

Implement your SQLAlchemy models for tables:
- Students table;
- Groups table;
- Lecturers table;
- Subjects table with an indication of the lecturer teaching the subject;
- A table where each student has grades from subjects with an indication of when the grade was received;

### Step Two

Use Alembic to create migrations in the database.

### Step Three

Write a script `seed.py` and fill the resulting database with random data (~30-50 students, 3 groups, 5-8 subjects, 3-5 lecturers, up to 20 grades for each student in all subjects). Use the Faker package for filling. During the filling, use the SQLAlchemy session mechanism.

### Step Four

Make the following selections from the database:

1. Find 5 students with the highest average grade from all subjects.
2. Find the student with the highest average grade from a specific subject.
3. Find the average score in groups for a specific subject.
4. Find the average score in a group (across the entire grades table).
5. Find the subjects taught by a specific lecturer.
6. Find the list of students in a specific group.
7. Find the grades of students in a specific group from a given subject.
8. Find the average grade given by a specific lecturer from his subjects.
9. Find the list of subjects passed by a given student.
10. Find the list of courses taught by a specific lecturer to a specific student.

For queries, create a separate file `my_select.py`, which will contain 10 functions from `select_1` to `select_10`. The functions should return the same result as in the previous homework assignment. While creating queries, use the SQLAlchemy session mechanism.

## Tips and Advice

This task will test your ability to use SQLAlchemy documentation. However, we will give you the main tips and advice on solving it right away.

Let's assume we have the following query: Find 5 students with the highest GPA from all subjects.

Let's try to translate it into an SQLAlchemy ORM query. Assume we have a session in the variable `session`. We have described the Student and Grade models for the respective tables. Assume the database is already filled with data. SQLAlchemy stores aggregate functions in the `func` object. It must be specifically imported from `from sqlalchemy import func`, and then we can use the methods `func.round` and `func.avg`. So, the first line of the SQL query should look like this: `session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))`.

Here, we used a different label `label('avg_grade')`, so the ORM could name the field with the average grade using the AS statement.

Next, `FROM grades g` is replaced by the method `select_from(Grade)`. Replacing the JOIN statement is simple, it is the function `join(Student)`, the rest is handled by ORM. Grouping by field is performed by the `group_by(Student.id)` function. The `order_by` function is responsible for sorting, which defaults to sort as ASC, but we explicitly need DESC mode, also by the `avg_grade` field we created in the query. Import from `from sqlalchemy import func, desc` and the final form `order_by(desc('avg_grade'))`. The limit of five values is the function of the same name `limit(5)`. That's all, our query is ready. The final version of the query for SQLAlchemy ORM.

For the rest of the queries, you should build them similarly to the above example. Last tip: if you decide to create nested queries, use [scalar-selects](https://docs.sqlalchemy.org/en/14/core/tutorial.html#scalar-selects).
