"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect

import hackbright

app = Flask(__name__)
app.secret_key = 'this-is-a-secret'


@app.route("/")
def homepage():
	"""Lists all students and projects."""

	students = hackbright.get_all_students()
	projects = hackbright.get_all_projects()

	for student in students:
		print student
		print type(student)


	print projects
	print type(projects)
	for project in projects:
		print project
		print type(project)

	return render_template("homepage.html", students=students,
											projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
    	                   first=first,
    	                   last=last,
    	                   github=github,
    	                   grades=grades)

    return html


@app.route("/student-search")
def get_student_form():
	"""Show form for searching for a student."""

	return render_template("student_search.html")


@app.route("/student-add")
def student_add():
	"""Show form for adding a student."""

	return render_template("student_add.html")


@app.route("/student-add-post", methods=['POST'])
def student_add_post():
    """Add a student."""

    first = request.form['first']
    last = request.form['last']
    github = request.form['github']

    hackbright.make_new_student(first, last, github)

    return render_template("student_add_post.html",
    					   first=first,
    					   last=last,
    					   github=github)


@app.route("/project")
def get_project():
	"""Displays info about a project."""

	title = request.args.get('title')

	title, desc, max_grade = hackbright.get_project_by_title(title)
	grades = hackbright.get_grades_by_title(title)

	html = render_template("project_info.html",
						   title=title,
						   desc=desc,
						   max_grade=max_grade,
						   grades=grades)

	return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
