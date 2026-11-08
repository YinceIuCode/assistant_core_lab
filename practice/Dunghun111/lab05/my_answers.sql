-- Write ONE query under each marker. Do not delete the markers.
-- Check with:  python check.py
-- Q1  (all columns of all students)
select * from students;

-- Q2  (name and year of every student)
select name, year from students;

-- Q3  (names of CS students)
select name from students where program = "CS";

-- Q4  (name and year of students in year 3 or higher)
select name, year from students where year >= 3;

-- Q5  (student names, Z to A)
select name from students order by name desc;

-- Q6  (title and credits of 4-credit courses, by title)
select title, credits from courses where credits = 4 order by title asc;

-- Q7  (how many students?)
select count(id) as student_amounts from students;

-- Q8  (number of students per program, by program)
select program, count(id) as student_amounts from students group by program;

-- Q9  (average grade in CSC10004, rounded to 2 decimals)
select avg(grade) from enrollments where course_code = "CSC10004";

-- Q10 (student_id and course_code of enrollments without a grade, by student_id)
select student_id, course_code from enrollments where grade is null;

-- Q11 (name and grade of graded students in CSC10014, by name)
select name, avg(grade) from students
inner join enrollments
    on students.id = enrollments.student_id
where course_code = "CSC10014" and grade is not null
group by name;

-- Q12 (course title and number of enrolled students, most first, then by title)
select title, count(student_id) from enrollments
inner join courses
    on enrollments.course_code = courses.code
group by course_code
order by count(student_id) desc;

-- Q13 (names of students with a grade below 5, by name)
select name from students
inner join enrollments
    on students.id = enrollments.student_id
where enrollments.grade < 5;

-- Q14 (each student's name and total credits enrolled, most first, then by name)
select name, sum(credits) from enrollments
inner join students
    on enrollments.student_id = students.id
inner join courses
    on courses.code = enrollments.course_code
group by name
order by sum(credits) desc, name;

-- Q15 (names of students NOT enrolled in CSC10014, by name)
select name from students
inner join enrollments
    on students.id = enrollments.student_id
where name not in (
    select name from students
    inner join enrollments
        on students.id = enrollments.student_id
    where enrollments.course_code = 'CSC10014'
    group by name
)
group by name
order by name;

-- select name from enrollments
-- inner join students
--     on enrollments.student_id = students.id
-- inner join courses
--     on courses.code = enrollments.course_code
-- where enrollments.course_code = "CSC10014";
