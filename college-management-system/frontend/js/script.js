const API_URL = "http://127.0.0.1:5000/students";


// ================= LOAD STUDENTS =================

async function loadStudents() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Failed to load students");
        }

        const students = await response.json();


        // Update student count
        document.getElementById("studentCount").textContent =
            students.length;


        // Get table
        const table = document.getElementById("studentTable");

        table.innerHTML = "";


        // Display students
        students.forEach(student => {

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

    }

    catch (error) {

        console.error(error);

        alert("Unable to load students.");

    }

}



// ================= ADD STUDENT =================

document
    .getElementById("studentForm")
    .addEventListener("submit", async function(event) {

        event.preventDefault();


        const student = {

            name:
                document.getElementById("name").value,

            email:
                document.getElementById("email").value,

            phone:
                document.getElementById("phone").value,

            department:
                document.getElementById("department").value,

            curr_year:
                document.getElementById("year").value,

            section:
                document.getElementById("section").value

        };


        try {

            const response = await fetch(API_URL, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(student)

            });


            if (!response.ok) {

                throw new Error(
                    "Failed to add student"
                );

            }


            alert("Student added successfully!");


            // Clear form
            document
                .getElementById("studentForm")
                .reset();


            // Refresh table
            loadStudents();

        }

        catch (error) {

            console.error(error);

            alert("Unable to add student.");

        }

    });



// ================= EDIT STUDENT =================

async function editStudent(id) {

    try {

        const response =
            await fetch(`${API_URL}/${id}`);


        if (!response.ok) {

            throw new Error(
                "Student not found"
            );

        }


        const student =
            await response.json();


        // Put student data into modal

        document.getElementById("editId").value =
            student.id;

        document.getElementById("editName").value =
            student.name;

        document.getElementById("editEmail").value =
            student.email;

        document.getElementById("editPhone").value =
            student.phone || "";

        document.getElementById("editDepartment").value =
            student.department || "";

        document.getElementById("editYear").value =
            student.curr_year || "";

        document.getElementById("editSection").value =
            student.section || "";


        // Open Bootstrap modal

        const modal =
            new bootstrap.Modal(
                document.getElementById(
                    "editStudentModal"
                )
            );

        modal.show();

    }

    catch (error) {

        console.error(error);

        alert("Unable to load student.");

    }

}



// ================= UPDATE STUDENT =================

async function updateStudent() {

    const id =
        document.getElementById("editId").value;


    const student = {

        name:
            document.getElementById("editName").value,

        email:
            document.getElementById("editEmail").value,

        phone:
            document.getElementById("editPhone").value,

        department:
            document.getElementById("editDepartment").value,

        curr_year:
            document.getElementById("editYear").value,

        section:
            document.getElementById("editSection").value

    };


    try {

        const response =
            await fetch(`${API_URL}/${id}`, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(student)

            });


        if (!response.ok) {

            throw new Error(
                "Failed to update student"
            );

        }


        alert(
            "Student updated successfully!"
        );


        // Close modal

        const modalElement =
            document.getElementById(
                "editStudentModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        modal.hide();


        // Refresh table

        loadStudents();

    }

    catch (error) {

        console.error(error);

        alert("Unable to update student.");

    }

}



// ================= DELETE STUDENT =================

async function deleteStudent(id) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this student?"
        );


    if (!confirmation) {
        return;
    }


    try {

        const response =
            await fetch(`${API_URL}/${id}`, {

                method: "DELETE"

            });


        if (!response.ok) {

            throw new Error(
                "Failed to delete student"
            );

        }


        alert(
            "Student deleted successfully!"
        );


        // Refresh table

        loadStudents();

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete student.");

    }

}
// ================= FACULTY =================

const FACULTY_API =
    "http://127.0.0.1:5000/faculty";


// ================= LOAD FACULTY =================

async function loadFaculty() {

    try {

        const response =
            await fetch(FACULTY_API);

        if (!response.ok) {
            throw new Error("Failed to load faculty");
        }

        const faculty =
            await response.json();


        // Update faculty count

        document.getElementById(
            "facultyCount"
        ).textContent = faculty.length;


        // Get table

        const table =
            document.getElementById(
                "facultyTable"
            );

        table.innerHTML = "";


        // Display faculty

        faculty.forEach(member => {

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

    }

    catch (error) {

        console.error(error);

        alert("Unable to load faculty.");

    }

}

// ================= ADD FACULTY =================

document
    .getElementById("facultyForm")
    .addEventListener("submit", async function(event) {

        event.preventDefault();


        const faculty = {

            name:
                document.getElementById(
                    "facultyName"
                ).value,

            email:
                document.getElementById(
                    "facultyEmail"
                ).value,

            phone:
                document.getElementById(
                    "facultyPhone"
                ).value,

            department:
                document.getElementById(
                    "facultyDepartment"
                ).value,

            designation:
                document.getElementById(
                    "facultyDesignation"
                ).value

        };


        try {

            const response =
                await fetch(FACULTY_API, {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(faculty)

                });


            if (!response.ok) {

                throw new Error(
                    "Failed to add faculty"
                );

            }


            alert(
                "Faculty added successfully!"
            );


            document
                .getElementById("facultyForm")
                .reset();


            loadFaculty();

        }

        catch (error) {

            console.error(error);

            alert(
                "Unable to add faculty."
            );

        }

    });
// ================= INITIAL LOAD =================

loadStudents();
loadFaculty();

// ================= EDIT FACULTY =================

async function editFaculty(id) {

    try {

        const response =
            await fetch(`${FACULTY_API}/${id}`);


        if (!response.ok) {

            throw new Error(
                "Faculty not found"
            );

        }


        const faculty =
            await response.json();


        // Put data into modal

        document.getElementById(
            "editFacultyId"
        ).value = faculty.id;


        document.getElementById(
            "editFacultyName"
        ).value = faculty.name;


        document.getElementById(
            "editFacultyEmail"
        ).value = faculty.email;


        document.getElementById(
            "editFacultyPhone"
        ).value =
            faculty.phone || "";


        document.getElementById(
            "editFacultyDepartment"
        ).value =
            faculty.department || "";


        document.getElementById(
            "editFacultyDesignation"
        ).value =
            faculty.designation || "";


        // Open Bootstrap modal

        const modal =
            new bootstrap.Modal(
                document.getElementById(
                    "editFacultyModal"
                )
            );

        modal.show();

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to load faculty."
        );

    }

}
// ================= UPDATE FACULTY =================

async function updateFaculty() {

    const id =
        document.getElementById(
            "editFacultyId"
        ).value;


    const faculty = {

        name:
            document.getElementById(
                "editFacultyName"
            ).value,

        email:
            document.getElementById(
                "editFacultyEmail"
            ).value,

        phone:
            document.getElementById(
                "editFacultyPhone"
            ).value,

        department:
            document.getElementById(
                "editFacultyDepartment"
            ).value,

        designation:
            document.getElementById(
                "editFacultyDesignation"
            ).value

    };


    try {

        const response =
            await fetch(
                `${FACULTY_API}/${id}`,
                {

                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(faculty)

                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to update faculty"
            );

        }


        alert(
            "Faculty updated successfully!"
        );


        // Close modal

        const modalElement =
            document.getElementById(
                "editFacultyModal"
            );


        const modal =
            bootstrap.Modal.getInstance(
                modalElement
            );


        modal.hide();


        // Refresh faculty table

        loadFaculty();

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to update faculty."
        );

    }

}
// ================= DELETE FACULTY =================

async function deleteFaculty(id) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this faculty member?"
        );


    if (!confirmation) {

        return;

    }


    try {

        const response =
            await fetch(
                `${FACULTY_API}/${id}`,
                {

                    method: "DELETE"

                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to delete faculty"
            );

        }


        alert(
            "Faculty deleted successfully!"
        );


        // Refresh table

        loadFaculty();

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to delete faculty."
        );

    }

}