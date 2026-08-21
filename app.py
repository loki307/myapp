from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

# In-memory student data
students = [
    {"id": 1, "name": "Logesh", "course": "Cloud Computing", "marks": 85},
    {"id": 2, "name": "Arun", "course": "DevOps", "marks": 90}
]

# Home page - shows HTML UI
@app.route('/')
def home():
    return render_template('index.html', students=students)

# Add student via form
@app.route('/add', methods=['POST'])
def add_student_form():
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "name": request.form['name'],
        "course": request.form['course'],
        "marks": int(request.form['marks'])
    }
    students.append(new_student)
    return redirect('/')

# Delete student via link
@app.route('/delete/<int:student_id>')
def delete_student_web(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return redirect('/')
# Show edit form
@app.route('/edit/<int:student_id>')
def edit_student_form(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return render_template('edit.html', student=student)
    return redirect('/')

# Update student via form
@app.route('/edit/<int:student_id>', methods=['POST'])
def edit_student_web(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        student['name'] = request.form['name']
        student['course'] = request.form['course']
        student['marks'] = int(request.form['marks'])
    return redirect('/')

# ---- JSON API endpoints (for testing/interview demo) ----

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student_api():
    new_student = request.get_json()
    new_student["id"] = max([s["id"] for s in students], default=0) + 1
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        data = request.get_json()
        student.update(data)
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student_api(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)