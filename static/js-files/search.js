// Select all elements with the class 'container-circle'
var circles = document.querySelectorAll('.container-circle');

// Loop through each element, set the cursor style, and add an event listener
circles.forEach(function(circle) {
    circle.style.cursor = 'pointer'; // Set cursor to pointer

    circle.addEventListener('click', function() {
        // Log the clicked element to the console
        console.log(this);

        // Create a form element
        var form = document.createElement('form');
        form.action = '/search';
        form.method = 'POST'; // Specify the method if needed (POST/GET)

        // Create an input element
        var input = document.createElement('input');
        input.type = 'hidden'; // Set type to hidden so it doesn't display
        input.name = 'id'; // Name of the input to be sent to the server
        input.value = this.id; // Set the value to the ID of the clicked element

        // Append the input to the form
        form.appendChild(input);

        // Append the form to the body
        document.body.appendChild(form);

        // Submit the form
        form.submit();
    });
});
