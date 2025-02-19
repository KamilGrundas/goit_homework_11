SELECT students.name, AVG(grades.value) AS avg_grade
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.id
ORDER BY avg_grade DESC
LIMIT 5;