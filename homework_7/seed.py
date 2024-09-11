from faker import Faker
from models import Base, Grade, Group, Student, Lecturer, Subject
from session import Session
from random import randint, choice


def main():
    Base.metadata.create_all()
    session = Session()
    fake = Faker()

    # Make groups
    groups = [Group(name=name) for name in ["A", "B", "C"]]
    session.add_all(groups)

    # Insert students
    group_ids = [group.id for group in session.query(Group).all()]
    students = [
        Student(name=fake.name(), group_id=choice(group_ids))
        for _ in range(randint(30, 50))
    ]
    session.add_all(students)

    # Insert lecturers
    lecturers = [Lecturer(name=fake.name()) for _ in range(randint(3, 5))]
    session.add_all(lecturers)

    # Insert subjects
    lecturer_ids = [lecturer.id for lecturer in session.query(Lecturer).all()]
    subjects = [
        Subject(name=fake.word(), lecturer_id=choice(lecturer_ids))
        for _ in range(randint(5, 8))
    ]
    session.add_all(subjects)

    # Insert grades
    subject_ids = [subject.id for subject in session.query(Subject).all()]
    for student in students:
        for _ in range(randint(10, 20)):
            grade = Grade(
                value=randint(1, 5),
                date=fake.date_between(start_date="-130d", end_date="today"),
                student_id=student.id,
                subject_id=choice(subject_ids),
            )
            session.add(grade)

    session.commit()


if __name__ == "__main__":
    main()
