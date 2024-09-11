from models import Base, Grade, Group, Student, Lecturer, Subject
from session import Session


def main():

    # Tworzenie tabel
    Base.metadata.create_all()
    session = Session()


if __name__ == "__main__":
    main()
