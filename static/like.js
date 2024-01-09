// Add a listener to handle the click on the "like" button
    document.addEventListener('DOMContentLoaded', function () {
         // Select all elements with the class 'like-button'
        var likeButtons = document.querySelectorAll('.like-button');

          // Iterate over each button in the NodeList
        likeButtons.forEach(function (button) {
             // Add a click event listener to each button
            button.addEventListener('click', function () {
                 // Toggle the 'active' class to change the heart color
                button.classList.toggle('active');
            });
        });
    });
