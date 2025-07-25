import json
import uuid


class Student:
    def __init__(self, name, student_id=None, subjects=None):
        self.id = student_id or str(uuid.uuid4())  # Unique ID
        self.name = name
        self.subjects = subjects if subjects else {}

    def add_subject(self, subject, score):
        if 0 <= score <= 100:
            self.subjects[subject] = score
        else:
            raise ValueError("Score must be between 0 and 100")

    def calculate_average(self):
        if not self.subjects:
            return 0.0
        return sum(self.subjects.values()) / len(self.subjects)

    def get_grade(self):
        avg = self.calculate_average()
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 50:
            return 'C'
        else:
            return 'Fail'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "subjects": self.subjects
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["id"], data["subjects"])


class GradeManager:
    def __init__(self):
        self.students = []

    def add_student(self, name, subject_scores):
        student = Student(name)
        for subject, score in subject_scores.items():
            student.add_subject(subject, score)
        self.students.append(student)
        print(f"Student '{name}' added with ID: {student.id}")

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def update_scores(self, student_id, subject_scores):
        student = self.find_student(student_id)
        if student:
            for subject, score in subject_scores.items():
                student.add_subject(subject, score)
            print("Scores updated.")
        else:
            print("Student not found.")

    def view_report(self, student_id):
        student = self.find_student(student_id)
        if student:
            print(f"\nReport for {student.name} (ID: {student.id})")
            for subject, score in student.subjects.items():
                print(f"{subject}: {score}")
            avg = student.calculate_average()
            grade = student.get_grade()
            print(f"Average: {avg:.2f}")
            print(f"Grade: {grade}")
        else:
            print("Student not found.")

    def delete_student(self, student_id):
        student = self.find_student(student_id)
        if student:
            self.students.remove(student)
            print("Student deleted.")
        else:
            print("Student not found.")

    def save_to_file(self, filename='grades.json'):
        data = [student.to_dict() for student in self.students]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved to file.")

    def load_from_file(self, filename='grades.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
            print("Data loaded from file.")
        except FileNotFoundError:
            print("No saved data found.")


def main():
    manager = GradeManager()
    manager.load_from_file()

    while True:
        print("\n===== Student Report Card Manager =====")
        print("1. Add Student")
        print("2. Update Scores")
        print("3. View Report")
        print("4. Delete Student")
        print("5. Save to File")
        print("6. Load from File")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            subject_scores = {}
            while True:
                subject = input("Enter subject (or 'done'): ")
                if subject.lower() == 'done':
                    break
                try:
                    score = float(input(f"Enter score for {subject}: "))
                    subject_scores[subject] = score
                except ValueError:
                    print("Invalid score. Please enter a number.")
            manager.add_student(name, subject_scores)

        elif choice == '2':
            student_id = input("Enter student ID: ")
            subject_scores = {}
            while True:
                subject = input("Enter subject (or 'done'): ")
                if subject.lower() == 'done':
                    break
                try:
                    score = float(input(f"Enter new score for {subject}: "))
                    subject_scores[subject] = score
                except ValueError:
                    print("Invalid score. Please enter a number.")
            manager.update_scores(student_id, subject_scores)

        elif choice == '3':
            student_id = input("Enter student ID: ")
            manager.view_report(student_id)

        elif choice == '4':
            student_id = input("Enter student ID: ")
            manager.delete_student(student_id)

        elif choice == '5':
            manager.save_to_file()

        elif choice == '6':
            manager.load_from_file()

        elif choice == '7':
            manager.save_to_file()
            print("Exiting... Data saved.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
