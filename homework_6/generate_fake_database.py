from sqlalchemy import create_engine
from faker import Faker
from random import randint

fake = Faker()


if __name__ == "__main__":
    uri = "sqlite:///school"
    engine = create_engine(uri)

    # Groups table
    engine.execute(
        """
            CREATE TABLE IF NOT EXISTS groups (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """
    )

    # Students table
    engine.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            "group_id" INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );
        """
    )

    # Lectures table
    engine.execute(
        """
        CREATE TABLE IF NOT EXISTS lecturers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
    )

    # Subjects table
    engine.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            "lecturer_id" INTEGER NOT NULL,
            FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
        );
        """
    )

    # Grades table
    engine.execute(
        """
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            value REAL NOT NULL,
            date DATE NOT NULL,
            "student_id" INTEGER NOT NULL,
            "subject_id" INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
            FOREIGN KEY (subject_id) REFERENCES subjcets(id)
        );
        """
    )

    # Make groups
    engine.execute(
        """
            INSERT INTO groups (id, name)
            VALUES
                ('1', 'A'),
                ('2', 'B'),
                ('3', 'C')
        """
    )

    # Insert students
    for i in range(randint(30, 50)):
        engine.execute(
            'INSERT INTO students (id, name, "group_id") VALUES (:id, :name, :group_id)',
            id=i + 1,
            name=fake.name(),
            group_id=randint(1, 3),
        )

    # Insert lecturers
    for i in range(randint(3, 5)):
        engine.execute(
            "INSERT INTO lecturers (id, name) VALUES (:id, :name)",
            id=i + 1,
            name=fake.name(),
        )

    lecturers = engine.execute("SELECT * FROM lecturers")
    number_of_lectures = len(lecturers.fetchall())

    # Insert subjects
    for i in range(randint(5, 8)):
        engine.execute(
            'INSERT INTO subjects (id, name, "lecturer_id") VALUES (:id, :name, :lecturer_id)',
            id=i + 1,
            name=fake.word(),
            lecturer_id=randint(1, number_of_lectures),
        )

    subjcets = engine.execute("SELECT * FROM subjects")
    number_of_subjects = len(subjcets.fetchall())

    students = engine.execute("SELECT * FROM students")
    number_of_students = len(students.fetchall())

    counter = 1

    # Insert grades
    for i in range(number_of_students):
        # From 10 to 20 grades for each student
        for j in range(randint(10, 20)):
            engine.execute(
                'INSERT INTO grades (id, value, date, "student_id", "subject_id") VALUES (:id, :value, :date, :student_id, :subject_id)',
                id=counter,
                value=randint(1, 5),
                date=fake.date_time_between(start_date="-130d", end_date="now"),
                student_id=i + 1,
                subject_id=randint(1, number_of_subjects),
            )
            counter += 1
