// Fetch mentors from the backend and display them
fetch('/mentors')
    .then(response => response.json())
    .then(mentors => {
        const mentorList = document.getElementById('mentor-list');
        mentors.forEach(mentor => {
            const listItem = document.createElement('li');
            listItem.textContent = `${mentor.name} - ${mentor.field}`;
            mentorList.appendChild(listItem);
        });
    });

// Example of adding a new mentor via POST request
const newMentor = {
    name: 'New Mentor',
    field: 'New Field'
};

fetch('/mentors', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(newMentor)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
