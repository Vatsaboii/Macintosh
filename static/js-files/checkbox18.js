document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('.checkbox-wrapper-19 input[type="checkbox"]');
    var download = document.getElementById('download');
    var copy = document.getElementById('copy');
    var share = document.getElementById('share');
    var del = document.getElementById('delete');

    // Function to update checkedImages array
    function updateCheckedImages() {
        var checkedImages = [];
        checkboxes.forEach(function(cb) {
            if (cb.checked) {
                checkedImages.push(cb.id); // Assuming checkbox value is the photo address
            }
        });
        return checkedImages;
    }

    // Checkbox change event listener
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
           // Assuming this is inside a function or event handler that handles checkbox changes or similar
var checkedImages = updateCheckedImages();

if (checkedImages.length > 0) {
    // Show buttons when at least one checkbox is checked
    if (window.matchMedia('(max-width: 768px)').matches) {
        // For screens with max-width 768px, show only download and delete buttons
        download.style.display = 'block';
        del.style.display = 'block';

        // Hide other buttons
        share.style.display = 'none';
        copy.style.display = 'none';
    } else {
        // For screens larger than 768px, show all buttons
        download.style.display = 'block';
        share.style.display = 'block';
        copy.style.display = 'block';
        del.style.display = 'block';
    }
} else {
    // Hide all buttons when no checkboxes are checked
    download.style.display = 'none';
    share.style.display = 'none';
    copy.style.display = 'none';
    del.style.display = 'none';
}

        });
    });

    // Download button click event listener
    download.addEventListener('click', function() {
        var checkedImages = updateCheckedImages();

        if (checkedImages.length > 0) {
            checkedImages.forEach(function(imageUrl) {
                // Create a link element
                imageUrl1='static/'+imageUrl
                var a = document.createElement('a');
                a.href = imageUrl1; // Set the href to the image URL
                a.download = imageUrl1; // Set the download attribute to the image URL

                // Append the link to the body
                document.body.appendChild(a);

                // Trigger a click event on the link
                a.click();

                // Remove the link from the body
                document.body.removeChild(a);
            });
        } else {
            // If no checkboxes are checked, notify the user
            alert('Please select at least one image to download.');
        }
    });

    // Delete button click event listener
     del.addEventListener('click', function() {
        var checkedImages = updateCheckedImages();

        if (checkedImages.length > 0) {
            var form = document.createElement('form');
            form.action = 'js-files/delete.php';
            form.method = 'post';

            var input = document.createElement('input');
            input.type = 'hidden'; // Use hidden input type for passing data
            input.value = JSON.stringify(checkedImages); // Convert array to JSON string
            input.name = 'delete_items';

            form.appendChild(input);
            document.body.appendChild(form);

            form.submit(); // Submit the form

            // Optional: Remove the form from the body after submission
            document.body.removeChild(form);
        } else {
            // If no checkboxes are checked, notify the user
            alert('Please select at least one image to delete.');
        }
    });
});
