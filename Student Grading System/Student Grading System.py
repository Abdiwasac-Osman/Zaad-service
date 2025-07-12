import tkinter as tk
from tkinter import messagebox
import json
import sys

# Function for grade calculation
def calculate_grade(marks):
    if marks >= 90:
        return 'A', 4
    elif marks >= 80:
        return 'B', 3
    elif marks >= 70:
        return 'C', 2
    elif marks >= 60:
        return 'D', 1
    else:
        return 'F', 0

class StudentGradingApp:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title(f"Student Grading System - Logged in as {username} ({role.capitalize()})")

        self.students = self.load_from_file()
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        if self.role in ['admin', 'teacher']:
            self.add_student_button = tk.Button(self.frame, text="Add Student", width=20, command=self.add_student)
            self.add_student_button.grid(row=0, column=0, padx=10, pady=5)

        self.show_grades_button = tk.Button(self.frame, text="Show Grades", width=20, command=self.show_grades)
        self.show_grades_button.grid(row=0, column=1, padx=10, pady=5)

        self.class_performance_button = tk.Button(self.frame, text="Class Performance", width=20,
                                                  command=self.class_performance)
        self.class_performance_button.grid(row=0, column=2, padx=10, pady=5)

        if self.role in ['admin', 'teacher']:
            self.update_student_button = tk.Button(self.frame, text="Update Student", width=20, command=self.update_student)
            self.update_student_button.grid(row=1, column=0, padx=10, pady=5)

        if self.role == 'admin':
            self.delete_student_button = tk.Button(self.frame, text="Delete Student", width=20, command=self.delete_student)
            self.delete_student_button.grid(row=1, column=1, padx=10, pady=5)

            self.save_button = tk.Button(self.frame, text="Save Data", width=20, command=self.save_to_file)
            self.save_button.grid(row=1, column=2, padx=10, pady=5)

        self.logout_button = tk.Button(self.frame, text="Logout", width=20, command=self.logout)
        self.logout_button.grid(row=2, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.frame, text="Search & Filter", width=20, command=self.search_and_filter)
        self.search_button.grid(row=2, column=0, padx=10, pady=5)

    def add_student(self):
        if self.role not in ['admin', 'teacher']:
            messagebox.showerror("Access Denied", "You do not have permission to add students.")
            return

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")

        def validate_numeric_input(P):
            return P.isdigit() or P == ""

        validate_cmd = add_window.register(validate_numeric_input)

        tk.Label(add_window, text="Enter student ID:").grid(row=0, column=0)
        student_id_entry = tk.Entry(add_window, validate="key", validatecommand=(validate_cmd, '%P'))
        student_id_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Enter Full Student Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)
#waa course si automate loo soo galiyay
        courses = [
            "Python Programming", "SQL Server", "Introduction to Software Engineering",
            "Web Design (HTML and CSS)", "Computer Applications and Maintenance", "Networking", "Security"
        ]

        course_entries = {}
        for idx, course in enumerate(courses):
            tk.Label(add_window, text=f"{course}:").grid(row=2 + idx, column=0)
            entry = tk.Entry(add_window)
            entry.grid(row=2 + idx, column=1)
            course_entries[course] = entry

        def save_student():
            student_id = student_id_entry.get().strip()
            name = name_entry.get().strip()
            if not student_id or not name:
                messagebox.showerror("Error", "Student ID and name are required.")
                return
            if student_id in self.students:
                messagebox.showerror("Error", "Student ID already exists!")
                return

            student_courses = {}
            for course, entry in course_entries.items():
                try:
                    marks = float(entry.get())
                    if not (0 <= marks <= 100):
                        raise ValueError("Marks should be between 0 and 100.")
                    grade, gpa = calculate_grade(marks)
                    student_courses[course] = {"marks": marks, "grade": grade, "gpa": gpa}
                except ValueError:
                    messagebox.showerror("Error", f"Invalid marks for {course}.")
                    return

            self.students[student_id] = {"name": name, "courses": student_courses}
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            add_window.destroy()

        save_button = tk.Button(add_window, text="Save Student", command=save_student)
        save_button.grid(row=9, column=0, columnspan=2)

    def show_grades(self):
        def search_grades():
            student_id = student_id_entry.get().strip()
            if student_id not in self.students:
                messagebox.showerror("Error", "Student ID not found!")
                return

            details = self.students[student_id]
            name = details["name"]

            grades_window = tk.Toplevel(self.root)
            grades_window.title(f"Grades for {name} (ID: {student_id})")

            text_frame = tk.Frame(grades_window)
            text_frame.pack(padx=10, pady=10)

            tk.Label(text_frame, text=f"Student: {name} (ID: {student_id})", font=("Arial", 14, "bold")).pack()

            text = ""
            total_gpa = 0
            course_count = 0
            for course, course_details in details["courses"].items():
                marks = course_details["marks"]
                grade = course_details["grade"]
                gpa = course_details["gpa"]
                total_gpa += gpa
                course_count += 1
                text += f"{course}: Marks = {marks}, Grade = {grade}, GPA = {gpa}\n"
            if course_count > 0:
                avg_gpa = total_gpa / course_count
                text += f"Average GPA: {avg_gpa:.2f}\n"

            tk.Label(text_frame, text=text, justify="left", anchor="w").pack()

        input_window = tk.Toplevel(self.root)
        input_window.title("Enter Student ID")

        frame = tk.Frame(input_window, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Enter Student ID:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        student_id_entry = tk.Entry(frame, width=30)
        student_id_entry.grid(row=0, column=1, pady=5)

        search_button = tk.Button(frame, text="Show Grades", command=search_grades, width=15)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

    def class_performance(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student data available.")
            return

        course_totals = {}
        course_counts = {}

        for details in self.students.values():
            for course, course_details in details["courses"].items():
                if course not in course_totals:
                    course_totals[course] = 0
                    course_counts[course] = 0
                course_totals[course] += course_details["marks"]
                course_counts[course] += 1

        text = "\n** Course Averages: **\n"
        for course in course_totals:
            average_marks = course_totals[course] / course_counts[course]
            text += f"{course}: {average_marks:.2f}\n"

        highest_avg_course = max(course_totals, key=lambda c: course_totals[c] / course_counts[c])
        lowest_avg_course = min(course_totals, key=lambda c: course_totals[c] / course_counts[c])

        text += f"\n** Class Performance: **\n"
        text += f"Course with Highest Average Marks: {highest_avg_course} ({course_totals[highest_avg_course] / course_counts[highest_avg_course]:.2f})\n"
        text += f"Course with Lowest Average Marks: {lowest_avg_course} ({course_totals[lowest_avg_course] / course_counts[lowest_avg_course]:.2f})\n"

        highest_gpa = -1
        lowest_gpa = float('inf')
        highest_student = None
        lowest_student = None

        for student_id, details in self.students.items():
            total_gpa = 0
            course_count = 0
            for course_details in details["courses"].values():
                total_gpa += course_details["gpa"]
                course_count += 1
            if course_count > 0:
                avg_gpa = total_gpa / course_count
                if avg_gpa > highest_gpa:
                    highest_gpa = avg_gpa
                    highest_student = details["name"]
                if avg_gpa < lowest_gpa:
                    lowest_gpa = avg_gpa
                    lowest_student = details["name"]

        if highest_student:
            text += f"Student with Highest in the class GPA: {highest_student} ({highest_gpa:.2f})\n"
        if lowest_student:
            text += (f"Student with Lowest in the class"
                     f" GPA: {lowest_student} ({lowest_gpa:.2f})\n")

        messagebox.showinfo("Class Performance", text)

    def update_student(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student Data")

        tk.Label(update_window, text="Enter student ID to update:").grid(row=0, column=0)
        student_id_entry = tk.Entry(update_window)
        student_id_entry.grid(row=0, column=1)

        def update_student_data():
            student_id = student_id_entry.get().strip()
            if student_id not in self.students:
                messagebox.showerror("Error", "Student not found!")
                return
            student = self.students[student_id]

            tk.Label(update_window, text=f"Updating information for {student['name']}").grid(row=1, column=0,
                                                                                             columnspan=2)

            tk.Label(update_window, text="Enter new name:").grid(row=2, column=0)
            new_name_entry = tk.Entry(update_window)
            new_name_entry.grid(row=2, column=1)

            tk.Label(update_window, text="Select course to update marks:").grid(row=3, column=0)
            course_choice = tk.StringVar(update_window)
            courses = list(student["courses"].keys())
            course_choice.set(courses[0])
            course_menu = tk.OptionMenu(update_window, course_choice, *courses)
            course_menu.grid(row=3, column=1)

            tk.Label(update_window, text="Enter new marks:").grid(row=4, column=0)
            marks_entry = tk.Entry(update_window)
            marks_entry.grid(row=4, column=1)

            def save_update():
                new_name = new_name_entry.get().strip()
                if new_name:
                    student["name"] = new_name

                course = course_choice.get()
                try:
                    new_marks = float(marks_entry.get())
                    if not (0 <= new_marks <= 100):
                        raise ValueError("Marks should be between 0 and 100.")
                    grade, gpa = calculate_grade(new_marks)
                    student["courses"][course] = {"marks": new_marks, "grade": grade, "gpa": gpa}
                    messagebox.showinfo("Success", "Student data updated!")
                    update_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid marks entered.")

            save_button = tk.Button(update_window, text="Save Update", command=save_update)
            save_button.grid(row=5, column=0, columnspan=2)

        update_button = tk.Button(update_window, text="Find Student", command=update_student_data)
        update_button.grid(row=1, column=0, columnspan=2)

    def delete_student(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Student")

        tk.Label(delete_window, text="Enter student ID to delete:").grid(row=0, column=0)
        student_id_entry = tk.Entry(delete_window)
        student_id_entry.grid(row=0, column=1)

        def delete_student_data():
            student_id = student_id_entry.get().strip()
            if student_id not in self.students:
                messagebox.showerror("Error", "Student not found!")
                return

            # Confirmation dialog
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {student_id}?")
            if confirm:
                del self.students[student_id]
                messagebox.showinfo("Success", f"Student {student_id} deleted!")
                delete_window.destroy()

        delete_button = tk.Button(delete_window, text="Delete Student", command=delete_student_data)
        delete_button.grid(row=1, column=0, columnspan=2)

    def search_and_filter(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search and Filter")

        tk.Label(search_window, text="Search by:").grid(row=0, column=0)
        search_options = ["Student ID", "Student Name", "Course Name", "Grade"]
        search_type = tk.StringVar(search_window)
        search_type.set(search_options[0])  # Default to Student ID
        search_menu = tk.OptionMenu(search_window, search_type, *search_options)
        search_menu.grid(row=0, column=1)

        tk.Label(search_window, text="Search term:").grid(row=1, column=0)
        search_term_entry = tk.Entry(search_window)
        search_term_entry.grid(row=1, column=1)

        def filter_results():
            search_term = search_term_entry.get().strip()
            filter_type = search_type.get()

            filtered_results = []

            if filter_type == "Student ID":
                if search_term in self.students:
                    filtered_results.append(self.students[search_term])
            elif filter_type == "Student Name":
                for student in self.students.values():
                    if search_term.lower() in student["name"].lower():
                        filtered_results.append(student)
            elif filter_type == "Course Name":
                for student in self.students.values():
                    for course, details in student["courses"].items():
                        if search_term.lower() in course.lower():
                            filtered_results.append(student)
                            break
            elif filter_type == "Grade":
                for student in self.students.values():
                    for course, details in student["courses"].items():
                        if details["grade"].lower() == search_term.lower():
                            filtered_results.append(student)
                            break

            if not filtered_results:
                messagebox.showinfo("No Results", f"No results found for '{search_term}' in {filter_type}.")
                return

            self.show_search_results(filtered_results)

        search_button = tk.Button(search_window, text="Search", command=filter_results)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)

    def show_search_results(self, results):
        results_window = tk.Toplevel(self.root)
        results_window.title("Search Results")

        text_frame = tk.Frame(results_window)
        text_frame.pack(padx=10, pady=10)

        for student in results:
            name = student["name"]
            student_id = list(self.students.keys())[list(self.students.values()).index(student)]

            tk.Label(text_frame, text=f"Student ID: {student_id} - Name: {name}", font=("Arial", 12, "bold")).pack()

            for course, details in student["courses"].items():
                marks = details["marks"]
                grade = details["grade"]
                gpa = details["gpa"]
                tk.Label(text_frame, text=f"{course}: Marks = {marks}, Grade = {grade}, GPA = {gpa}",
                         font=("Arial", 10)).pack()

            tk.Label(text_frame, text="-" * 50).pack()

    def save_to_file(self):
        if self.role != 'admin':
            messagebox.showerror("Access Denied", "Only admins can save data.")
            return
        try:
            with open("students_data.json", "w") as file:
                json.dump(self.students, file)
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")

    def load_from_file(self):
        try:
            with open("students_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            return {}

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            messagebox.showinfo("Goodbye!", "Thank you for using the Student Grading System!")
            self.root.quit()
            sys.exit()


def login_screen():
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    users = load_users()

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            login_window.destroy()
            root = tk.Tk()
            app = StudentGradingApp(root, username, role)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials")

    def register():
        login_window.destroy()
        registration_screen()

    tk.Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2)
    tk.Button(login_window, text="Register", command=register).grid(row=3, column=0, columnspan=2)
    login_window.mainloop()


def registration_screen():
    registration_window = tk.Tk()
    registration_window.title("Register")

    tk.Label(registration_window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=0, column=1)

    tk.Label(registration_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(registration_window, text="Role:").grid(row=2, column=0)
    role_var = tk.StringVar(registration_window)
    role_var.set("student")
    tk.OptionMenu(registration_window, role_var, "admin", "teacher", "student").grid(row=2, column=1)

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return

        users[username] = {"password": password, "role": role}
        save_users(users)
        messagebox.showinfo("Success", "Registration successful")
        registration_window.destroy()
        login_screen()

    tk.Button(registration_window, text="Register", command=register_user).grid(row=3, column=0, columnspan=2)
    registration_window.mainloop()


def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)


if __name__ == "__main__":
    login_screen()