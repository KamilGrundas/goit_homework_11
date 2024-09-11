from sqlalchemy import func
from models import Base, Grade, Group, Student, Lecturer, Subject
from session import Session


# Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
def select_1(session):
    result = (
        session.query(Student.name, func.avg(Grade.value))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.name)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )
    return f"Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów:\n{result}"


# Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu.
def select_2(session, subject_id):
    result = (
        session.query(Student.name, func.avg(Grade.value))
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.name)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )
    return (
        f"Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu:\n{result}"
    )


# Znajdź średni wynik w grupach dla określonego przedmiotu.
def select_3(session, subject_id):
    result = (
        session.query(Group.name, func.avg(Grade.value).label("avg_grade"))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    return f"Znajdź średni wynik w grupach dla określonego przedmiotu:\n{result}"


# Znajdź średni wynik w grupie (w całej tabeli ocen).
def select_4(session, group_id):
    result = (
        session.query(func.avg(Grade.value).label("avg_grade"))
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.group_id == group_id)
        .scalar()
    )
    return f"Znajdź średni wynik w grupie (w całej tabeli ocen):\n{result}"


# Znajdź przedmioty, których uczy określony wykładowca.
def select_5(session, lecturer_id):
    result = (
        session.query(Subject.name).filter(Subject.lecturer_id == lecturer_id).all()
    )
    return f"Znajdź przedmioty, których uczy określony wykładowca:\n{result}"


# Znajdź listę studentów w określonej grupie.
def select_6(session, group_id):
    result = session.query(Student.name).filter(Student.group_id == group_id).all()
    return f"Znajdź listę studentów w określonej grupie:\n{result}"


# Znajdź oceny studentów w określonej grupie z danego przedmiotu.
def select_7(session, group_id, subject_id):
    result = (
        session.query(Student.name, Grade.value)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    return f"Znajdź oceny studentów w określonej grupie z danego przedmiotu:\n{result}"


# Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
def select_8(session, lecturer_id):
    result = (
        session.query(func.avg(Grade.value).label("avg_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.lecturer_id == lecturer_id)
        .scalar()
    )
    return f"Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów:\n{result}"


# Znajdź listę przedmiotów zaliczonych przez danego studenta.
def select_9(session, student_id):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id, Grade.value >= 3)
        .group_by(Subject.id)
        .all()
    )
    return f"Znajdź listę przedmiotów zaliczonych przez danego studenta:\n{result}"


# Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta.
def select_10(session, lecturer_id, student_id):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Subject.lecturer_id == lecturer_id, Grade.student_id == student_id)
        .group_by(Subject.id)
        .all()
    )
    return f"Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta:\n{result}"


def main():
    Base.metadata.create_all()
    session = Session()
    print(select_1(session))
    print(select_2(session, 3))
    print(select_3(session, 3))
    print(select_4(session, 3))
    print(select_5(session, 2))
    print(select_6(session, 3))
    print(select_7(session, 1, 1))
    print(select_8(session, 3))
    print(select_9(session, 3))
    print(select_10(session, 1, 1))


if __name__ == "__main__":
    main()
