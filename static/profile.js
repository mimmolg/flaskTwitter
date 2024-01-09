   // Add an event listener for when the DOM content is loaded
    document.addEventListener('DOMContentLoaded', function () {
         // Set a timeout to hide the element after a certain period
        setTimeout(function () {
            // Select the element with the class 'notify'
            var notifyElement = document.querySelector('.notify');
             // Check if the element exists
            if (notifyElement) {
                 // Set the display style to 'none' to hide the element
                notifyElement.style.display = 'none';
            }
        }, 1000); // Set the time in milliseconds (5 seconds in this example)
    });
