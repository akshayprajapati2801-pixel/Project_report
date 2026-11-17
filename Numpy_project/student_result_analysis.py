
import numpy as np

# Student names
students = np.array([
    "Aman",
    "Priya",
    "Rahul",
    "Neha",
    "Rohit"
])

# Marks in 5 subjects: English, Maths, Science, Computer, Hindi
marks = np.array([
    [78, 85, 90, 95, 80],
    [88, 92, 84, 90, 86],
    [45, 55, 60, 50, 58],
    [95, 98, 92, 96, 94],
    [30, 45, 50, 40, 35]
])

subjects = ["English", "Maths", "Science", "Computer", "Hindi"]

# Calculate total, average, and percentage
total = np.sum(marks, axis=1)
average = np.mean(marks, axis=1)
percentage = (total / (len(subjects) * 100)) * 100

# Check whether students passed every subject
passed = np.all(marks >= 33, axis=1)

# Function to assign grades
def calculate_grade(percent, has_passed):
    if not has_passed:
        return "F"
    elif percent >= 90:
        return "A+"
    elif percent >= 80:
        return "A"
    elif percent >= 70:
        return "B"
    elif percent >= 60:
        return "C"
    elif percent >= 50:
        return "D"
    else:
        return "E"

grades = [
    calculate_grade(percentage[i], passed[i])
    for i in range(len(students))
]

# Display individual student results
print("\n===== STUDENT RESULT ANALYSIS =====")
print("-" * 85)
print(f"{'Name':<10}{'Total':<10}{'Average':<12}"
      f"{'Percentage':<14}{'Grade':<10}{'Result':<10}")
print("-" * 85)

for i in range(len(students)):
    result = "Pass" if passed[i] else "Fail"

    print(
        f"{students[i]:<10}"
        f"{total[i]:<10}"
        f"{average[i]:<12.2f}"
        f"{percentage[i]:<14.2f}"
        f"{grades[i]:<10}"
        f"{result:<10}"
    )

# Find the topper and lowest scorer by average marks
topper_index = np.argmax(average)
lowest_index = np.argmin(average)

# Class statistics
class_average = np.mean(average)
highest_mark = np.max(marks)
lowest_mark = np.min(marks)
pass_count = np.sum(passed)
fail_count = len(students) - pass_count
pass_percentage = (pass_count / len(students)) * 100

# Display analysis
print("\n===== CLASS PERFORMANCE =====")
print("Class Average:", round(class_average, 2))
print("Highest Subject Mark:", highest_mark)
print("Lowest Subject Mark:", lowest_mark)

print("Class Topper:", students[topper_index])
print("Topper Average:", round(average[topper_index], 2))

print("Lowest Scorer:", students[lowest_index])
print("Students Passed:", pass_count)
print("Students Failed:", fail_count)
print("Class Pass Percentage:", round(pass_percentage, 2), "%")
