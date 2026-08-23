// ============================================================
//                         API URLS
// ============================================================

const API_URL = "http://127.0.0.1:5000/students";

const FACULTY_API = "http://127.0.0.1:5000/faculty";

const COURSE_API = "http://127.0.0.1:5000/courses";

const ATTENDANCE_API = "http://127.0.0.1:5000/attendance";

// ============================================================
//                         STUDENTS
// ============================================================

// ================= LOAD STUDENTS =================

async function loadStudents() {
  try {
    const response = await fetch(API_URL);

    if (!response.ok) {
      throw new Error("Failed to load students");
    }

    const students = await response.json();

    document.getElementById("studentCount").textContent = students.length;

    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    students.forEach((student) => {
      const row = `

                <tr>

                    <td>${student.id}</td>

                    <td>${student.name}</td>

                    <td>${student.email}</td>

                    <td>${student.phone || ""}</td>

                    <td>${student.department || ""}</td>

                    <td>${student.curr_year || ""}</td>

                    <td>${student.section || ""}</td>

                    <td>

                        <button
                            class="btn btn-warning btn-sm me-1"
                            onclick="editStudent(${student.id})">

                            Edit

                        </button>

                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteStudent(${student.id})">

                            Delete

                        </button>

                    </td>

                </tr>

            `;

      table.innerHTML += row;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load students.");
  }
}

// ================= ADD STUDENT =================

document
  .getElementById("studentForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const student = {
      name: document.getElementById("name").value,

      email: document.getElementById("email").value,

      phone: document.getElementById("phone").value,

      department: document.getElementById("department").value,

      curr_year: document.getElementById("year").value,

      section: document.getElementById("section").value,
    };

    try {
      const response = await fetch(API_URL, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(student),
      });

      if (!response.ok) {
        throw new Error("Failed to add student");
      }

      alert("Student added successfully!");

      document.getElementById("studentForm").reset();

      loadStudents();

      loadAttendanceStudents();
    } catch (error) {
      console.error(error);

      alert("Unable to add student.");
    }
  });

// ================= EDIT STUDENT =================

async function editStudent(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`);

    if (!response.ok) {
      throw new Error("Student not found");
    }

    const student = await response.json();

    document.getElementById("editId").value = student.id;

    document.getElementById("editName").value = student.name;

    document.getElementById("editEmail").value = student.email;

    document.getElementById("editPhone").value = student.phone || "";

    document.getElementById("editDepartment").value = student.department || "";

    document.getElementById("editYear").value = student.curr_year || "";

    document.getElementById("editSection").value = student.section || "";

    const modal = new bootstrap.Modal(
      document.getElementById("editStudentModal"),
    );

    modal.show();
  } catch (error) {
    console.error(error);

    alert("Unable to load student.");
  }
}

// ================= UPDATE STUDENT =================

async function updateStudent() {
  const id = document.getElementById("editId").value;

  const student = {
    name: document.getElementById("editName").value,

    email: document.getElementById("editEmail").value,

    phone: document.getElementById("editPhone").value,

    department: document.getElementById("editDepartment").value,

    curr_year: document.getElementById("editYear").value,

    section: document.getElementById("editSection").value,
  };

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(student),
    });

    if (!response.ok) {
      throw new Error("Failed to update student");
    }

    alert("Student updated successfully!");

    const modalElement = document.getElementById("editStudentModal");

    const modal = bootstrap.Modal.getInstance(modalElement);

    modal.hide();

    loadStudents();

    loadAttendanceStudents();
  } catch (error) {
    console.error(error);

    alert("Unable to update student.");
  }
}

// ================= DELETE STUDENT =================

async function deleteStudent(id) {
  const confirmation = confirm("Are you sure you want to delete this student?");

  if (!confirmation) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Failed to delete student");
    }

    alert("Student deleted successfully!");

    loadStudents();

    loadAttendanceStudents();

    loadAttendance();

    loadAttendanceReport();
  } catch (error) {
    console.error(error);

    alert("Unable to delete student.");
  }
}

// ============================================================
//                          FACULTY
// ============================================================

// ================= LOAD FACULTY =================

async function loadFaculty() {
  try {
    const response = await fetch(FACULTY_API);

    if (!response.ok) {
      throw new Error("Failed to load faculty");
    }

    const faculty = await response.json();

    document.getElementById("facultyCount").textContent = faculty.length;

    const table = document.getElementById("facultyTable");

    table.innerHTML = "";

    faculty.forEach((member) => {
      const row = `

                <tr>

                    <td>${member.id}</td>

                    <td>${member.name}</td>

                    <td>${member.email}</td>

                    <td>${member.phone || ""}</td>

                    <td>${member.department || ""}</td>

                    <td>${member.designation || ""}</td>

                    <td>

                        <button
                            class="btn btn-warning btn-sm me-1"
                            onclick="editFaculty(${member.id})">

                            Edit

                        </button>

                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteFaculty(${member.id})">

                            Delete

                        </button>

                    </td>

                </tr>

            `;

      table.innerHTML += row;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load faculty.");
  }
}

// ================= ADD FACULTY =================

document
  .getElementById("facultyForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const faculty = {
      name: document.getElementById("facultyName").value,

      email: document.getElementById("facultyEmail").value,

      phone: document.getElementById("facultyPhone").value,

      department: document.getElementById("facultyDepartment").value,

      designation: document.getElementById("facultyDesignation").value,
    };

    try {
      const response = await fetch(FACULTY_API, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(faculty),
      });

      if (!response.ok) {
        throw new Error("Failed to add faculty");
      }

      alert("Faculty added successfully!");

      document.getElementById("facultyForm").reset();

      loadFaculty();

      loadFacultyDropdown();

      loadAttendanceCourses();
    } catch (error) {
      console.error(error);

      alert("Unable to add faculty.");
    }
  });

// ================= EDIT FACULTY =================

async function editFaculty(id) {
  try {
    const response = await fetch(`${FACULTY_API}/${id}`);

    if (!response.ok) {
      throw new Error("Faculty not found");
    }

    const faculty = await response.json();

    document.getElementById("editFacultyId").value = faculty.id;

    document.getElementById("editFacultyName").value = faculty.name;

    document.getElementById("editFacultyEmail").value = faculty.email;

    document.getElementById("editFacultyPhone").value = faculty.phone || "";

    document.getElementById("editFacultyDepartment").value =
      faculty.department || "";

    document.getElementById("editFacultyDesignation").value =
      faculty.designation || "";

    const modal = new bootstrap.Modal(
      document.getElementById("editFacultyModal"),
    );

    modal.show();
  } catch (error) {
    console.error(error);

    alert("Unable to load faculty.");
  }
}

// ================= UPDATE FACULTY =================

async function updateFaculty() {
  const id = document.getElementById("editFacultyId").value;

  const faculty = {
    name: document.getElementById("editFacultyName").value,

    email: document.getElementById("editFacultyEmail").value,

    phone: document.getElementById("editFacultyPhone").value,

    department: document.getElementById("editFacultyDepartment").value,

    designation: document.getElementById("editFacultyDesignation").value,
  };

  try {
    const response = await fetch(`${FACULTY_API}/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(faculty),
    });

    if (!response.ok) {
      throw new Error("Failed to update faculty");
    }

    alert("Faculty updated successfully!");

    const modalElement = document.getElementById("editFacultyModal");

    const modal = bootstrap.Modal.getInstance(modalElement);

    modal.hide();

    loadFaculty();

    loadFacultyDropdown();

    loadAttendanceCourses();
  } catch (error) {
    console.error(error);

    alert("Unable to update faculty.");
  }
}

// ================= DELETE FACULTY =================

async function deleteFaculty(id) {
  const confirmation = confirm(
    "Are you sure you want to delete this faculty member?",
  );

  if (!confirmation) {
    return;
  }

  try {
    const response = await fetch(`${FACULTY_API}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Failed to delete faculty");
    }

    alert("Faculty deleted successfully!");

    loadFaculty();

    loadFacultyDropdown();

    loadCourses();

    loadAttendanceCourses();
  } catch (error) {
    console.error(error);

    alert("Unable to delete faculty.");
  }
}

// ============================================================
//                          COURSES
// ============================================================

// ================= LOAD COURSES =================

async function loadCourses() {
  try {
    const response = await fetch(COURSE_API);

    if (!response.ok) {
      throw new Error("Failed to load courses");
    }

    const courses = await response.json();

    document.getElementById("courseCount").textContent = courses.length;

    const table = document.getElementById("courseTable");

    table.innerHTML = "";

    courses.forEach((course) => {
      const row = `

                <tr>

                    <td>${course.id}</td>

                    <td>${course.course_code}</td>

                    <td>${course.course_name}</td>

                    <td>${course.department || ""}</td>

                    <td>${course.credits || ""}</td>

                    <td>
                        ${course.faculty_name || "Not Assigned"}
                    </td>

                    <td>

                        <button
                            class="btn btn-warning btn-sm me-1"
                            onclick="editCourse(${course.id})">

                            Edit

                        </button>

                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteCourse(${course.id})">

                            Delete

                        </button>

                    </td>

                </tr>

            `;

      table.innerHTML += row;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load courses.");
  }
}

// ================= LOAD FACULTY DROPDOWN =================

async function loadFacultyDropdown() {
  try {
    const response = await fetch(FACULTY_API);

    const faculty = await response.json();

    const dropdown = document.getElementById("courseFaculty");

    dropdown.innerHTML = `

            <option value="">
                Select Faculty
            </option>

        `;

    faculty.forEach((member) => {
      const option = document.createElement("option");

      option.value = member.id;

      option.textContent = member.name;

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= ADD COURSE =================

document
  .getElementById("courseForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const course = {
      course_code: document.getElementById("courseCode").value,

      course_name: document.getElementById("courseName").value,

      department: document.getElementById("courseDepartment").value,

      credits: document.getElementById("courseCredits").value,

      faculty_id: document.getElementById("courseFaculty").value,
    };

    try {
      const response = await fetch(COURSE_API, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(course),
      });

      if (!response.ok) {
        throw new Error("Failed to add course");
      }

      alert("Course added successfully!");

      document.getElementById("courseForm").reset();

      loadCourses();

      loadAttendanceCourses();
    } catch (error) {
      console.error(error);

      alert("Unable to add course.");
    }
  });

// ================= EDIT COURSE =================

async function editCourse(id) {
  try {
    const response = await fetch(`${COURSE_API}/${id}`);

    if (!response.ok) {
      throw new Error("Course not found");
    }

    const course = await response.json();

    document.getElementById("editCourseId").value = course.id;

    document.getElementById("editCourseCode").value = course.course_code;

    document.getElementById("editCourseName").value = course.course_name;

    document.getElementById("editCourseDepartment").value =
      course.department || "";

    document.getElementById("editCourseCredits").value = course.credits || "";

    await loadEditFacultyDropdown(course.faculty_id);

    const modal = new bootstrap.Modal(
      document.getElementById("editCourseModal"),
    );

    modal.show();
  } catch (error) {
    console.error(error);

    alert("Unable to load course.");
  }
}

// ================= LOAD EDIT FACULTY =================

async function loadEditFacultyDropdown(selectedFacultyId) {
  try {
    const response = await fetch(FACULTY_API);

    const faculty = await response.json();

    const dropdown = document.getElementById("editCourseFaculty");

    dropdown.innerHTML = `

            <option value="">
                Select Faculty
            </option>

        `;

    faculty.forEach((member) => {
      const option = document.createElement("option");

      option.value = member.id;

      option.textContent = member.name;

      if (String(member.id) === String(selectedFacultyId)) {
        option.selected = true;
      }

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= UPDATE COURSE =================

async function updateCourse() {
  const id = document.getElementById("editCourseId").value;

  const course = {
    course_code: document.getElementById("editCourseCode").value,

    course_name: document.getElementById("editCourseName").value,

    department: document.getElementById("editCourseDepartment").value,

    credits: document.getElementById("editCourseCredits").value,

    faculty_id: document.getElementById("editCourseFaculty").value,
  };

  try {
    const response = await fetch(`${COURSE_API}/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(course),
    });

    if (!response.ok) {
      throw new Error("Failed to update course");
    }

    alert("Course updated successfully!");

    const modalElement = document.getElementById("editCourseModal");

    const modal = bootstrap.Modal.getInstance(modalElement);

    modal.hide();

    loadCourses();

    loadAttendanceCourses();
  } catch (error) {
    console.error(error);

    alert("Unable to update course.");
  }
}

// ================= DELETE COURSE =================

async function deleteCourse(id) {
  const confirmation = confirm("Are you sure you want to delete this course?");

  if (!confirmation) {
    return;
  }

  try {
    const response = await fetch(`${COURSE_API}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Failed to delete course");
    }

    alert("Course deleted successfully!");

    loadCourses();

    loadAttendanceCourses();

    loadAttendance();

    loadAttendanceReport();
  } catch (error) {
    console.error(error);

    alert("Unable to delete course.");
  }
}

// ============================================================
//                        ATTENDANCE
// ============================================================

// ================= LOAD ATTENDANCE STUDENTS =================

async function loadAttendanceStudents() {
  try {
    const response = await fetch(API_URL);

    const students = await response.json();

    const dropdown = document.getElementById("attendanceStudent");

    if (!dropdown) {
      return;
    }

    dropdown.innerHTML = `

            <option value="">
                Select Student
            </option>

        `;

    students.forEach((student) => {
      const option = document.createElement("option");

      option.value = student.id;

      option.textContent = `${student.name} (${student.email})`;

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= LOAD ATTENDANCE COURSES =================

async function loadAttendanceCourses() {
  try {
    const response = await fetch(COURSE_API);

    const courses = await response.json();

    const dropdown = document.getElementById("attendanceCourse");

    if (!dropdown) {
      return;
    }

    dropdown.innerHTML = `

            <option value="">
                Select Course
            </option>

        `;

    courses.forEach((course) => {
      const option = document.createElement("option");

      option.value = course.id;

      option.textContent = `${course.course_code} - ${course.course_name}`;

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= LOAD ATTENDANCE =================

async function loadAttendance() {
  try {
    const response = await fetch(ATTENDANCE_API);

    if (!response.ok) {
      throw new Error("Failed to load attendance");
    }

    const attendance = await response.json();

    const table = document.getElementById("attendanceTable");

    if (!table) {
      return;
    }

    table.innerHTML = "";

    attendance.forEach((record) => {
      const statusClass =
        record.status === "Present" ? "bg-success" : "bg-danger";

      const row = `

                <tr>

                    <td>
                        ${record.id}
                    </td>

                    <td>
                        ${record.student_name}
                    </td>

                    <td>
                        ${record.course_code}
                        -
                        ${record.course_name}
                    </td>

                    <td>
                        ${record.attendance_date}
                    </td>

                    <td>

                        <span
                            class="badge ${statusClass}">

                            ${record.status}

                        </span>

                    </td>

                    <td>

                        <button
                            class="btn btn-warning btn-sm me-1"
                            onclick="editAttendance(${record.id})">

                            Edit

                        </button>


                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteAttendance(${record.id})">

                            Delete

                        </button>

                    </td>

                </tr>

            `;

      table.innerHTML += row;
    });
  } catch (error) {
    console.error(error);

    alert("Unable to load attendance.");
  }
}

// ================= ADD ATTENDANCE =================

document
  .getElementById("attendanceForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const attendance = {
      student_id: document.getElementById("attendanceStudent").value,

      course_id: document.getElementById("attendanceCourse").value,

      attendance_date: document.getElementById("attendanceDate").value,

      status: document.getElementById("attendanceStatus").value,
    };

    try {
      const response = await fetch(ATTENDANCE_API, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(attendance),
      });

      if (!response.ok) {
        throw new Error("Failed to add attendance");
      }

      alert("Attendance marked successfully!");

      document.getElementById("attendanceForm").reset();

      loadAttendance();

      loadAttendanceReport();
    } catch (error) {
      console.error(error);

      alert("Unable to mark attendance.");
    }
  });

// ================= EDIT ATTENDANCE =================

async function editAttendance(id) {
  try {
    const response = await fetch(`${ATTENDANCE_API}/${id}`);

    if (!response.ok) {
      throw new Error("Attendance record not found");
    }

    const record = await response.json();

    document.getElementById("editAttendanceId").value = record.id;

    document.getElementById("editAttendanceDate").value =
      record.attendance_date;

    document.getElementById("editAttendanceStatus").value = record.status;

    await loadEditAttendanceStudents(record.student_id);

    await loadEditAttendanceCourses(record.course_id);

    const modal = new bootstrap.Modal(
      document.getElementById("editAttendanceModal"),
    );

    modal.show();
  } catch (error) {
    console.error(error);

    alert("Unable to load attendance.");
  }
}

// ================= EDIT ATTENDANCE STUDENTS =================

async function loadEditAttendanceStudents(selectedStudentId) {
  try {
    const response = await fetch(API_URL);

    const students = await response.json();

    const dropdown = document.getElementById("editAttendanceStudent");

    dropdown.innerHTML = `

            <option value="">
                Select Student
            </option>

        `;

    students.forEach((student) => {
      const option = document.createElement("option");

      option.value = student.id;

      option.textContent = `${student.name} (${student.email})`;

      if (String(student.id) === String(selectedStudentId)) {
        option.selected = true;
      }

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= EDIT ATTENDANCE COURSES =================

async function loadEditAttendanceCourses(selectedCourseId) {
  try {
    const response = await fetch(COURSE_API);

    const courses = await response.json();

    const dropdown = document.getElementById("editAttendanceCourse");

    dropdown.innerHTML = `

            <option value="">
                Select Course
            </option>

        `;

    courses.forEach((course) => {
      const option = document.createElement("option");

      option.value = course.id;

      option.textContent = `${course.course_code} - ${course.course_name}`;

      if (String(course.id) === String(selectedCourseId)) {
        option.selected = true;
      }

      dropdown.appendChild(option);
    });
  } catch (error) {
    console.error(error);
  }
}

// ================= UPDATE ATTENDANCE =================

async function updateAttendance() {
  const id = document.getElementById("editAttendanceId").value;

  const attendance = {
    student_id: document.getElementById("editAttendanceStudent").value,

    course_id: document.getElementById("editAttendanceCourse").value,

    attendance_date: document.getElementById("editAttendanceDate").value,

    status: document.getElementById("editAttendanceStatus").value,
  };

  try {
    const response = await fetch(`${ATTENDANCE_API}/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(attendance),
    });

    if (!response.ok) {
      throw new Error("Failed to update attendance");
    }

    alert("Attendance updated successfully!");

    const modalElement = document.getElementById("editAttendanceModal");

    const modal = bootstrap.Modal.getInstance(modalElement);

    modal.hide();

    loadAttendance();

    loadAttendanceReport();
  } catch (error) {
    console.error(error);

    alert("Unable to update attendance.");
  }
}

// ================= DELETE ATTENDANCE =================

async function deleteAttendance(id) {
  const confirmation = confirm(
    "Are you sure you want to delete this attendance record?",
  );

  if (!confirmation) {
    return;
  }

  try {
    const response = await fetch(`${ATTENDANCE_API}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error("Failed to delete attendance");
    }

    alert("Attendance deleted successfully!");

    loadAttendance();

    loadAttendanceReport();
  } catch (error) {
    console.error(error);

    alert("Unable to delete attendance.");
  }
}

// ============================================================
//                    ATTENDANCE REPORT
// ============================================================

// ================= LOAD ATTENDANCE REPORT =================

async function loadAttendanceReport() {
  try {
    const response = await fetch(ATTENDANCE_API);

    if (!response.ok) {
      throw new Error("Failed to load attendance report");
    }

    const attendance = await response.json();

    const table = document.getElementById("attendanceReportTable");

    if (!table) {
      return;
    }

    table.innerHTML = "";

    // Group attendance by student

    const studentData = {};

    attendance.forEach((record) => {
      const studentId = record.student_id;

      if (!studentData[studentId]) {
        studentData[studentId] = {
          student_id: studentId,

          student_name: record.student_name,

          total: 0,

          present: 0,

          absent: 0,
        };
      }

      studentData[studentId].total++;

      if (record.status === "Present") {
        studentData[studentId].present++;
      } else {
        studentData[studentId].absent++;
      }
    });

    Object.values(studentData).forEach((student) => {
      const percentage =
        student.total > 0 ? (student.present / student.total) * 100 : 0;

      let badgeClass;

      if (percentage >= 75) {
        badgeClass = "bg-success";
      } else if (percentage >= 60) {
        badgeClass = "bg-warning text-dark";
      } else {
        badgeClass = "bg-danger";
      }

      const row = `

                    <tr>

                        <td>
                            ${student.student_id}
                        </td>


                        <td>
                            ${student.student_name}
                        </td>


                        <td>
                            ${student.total}
                        </td>


                        <td>
                            ${student.present}
                        </td>


                        <td>
                            ${student.absent}
                        </td>


                        <td>

                            <span
                                class="badge ${badgeClass}">

                                ${percentage.toFixed(2)}%

                            </span>

                        </td>

                    </tr>

                `;

      table.innerHTML += row;
    });
  } catch (error) {
    console.error(error);
  }
}

// ============================================================
//                      INITIAL LOAD
// ============================================================

loadStudents();

loadFaculty();

loadCourses();

loadFacultyDropdown();

loadAttendanceStudents();

loadAttendanceCourses();

loadAttendance();

loadAttendanceReport();
