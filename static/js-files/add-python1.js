document.addEventListener('DOMContentLoaded', function() {
    var addBtn = document.getElementById('add-items');

    addBtn.addEventListener('click', function() {
        var input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image';
        input.name = 'file';
        input.multiple = true;
        input.style.display = 'none';

        var emali = document.createElement('input');
        emali.type = 'hidden';
        emali.name = 'emali';
        emali.value = localStorage.getItem('emali');

        var form = document.createElement('form');
        form.id = 'uploadForm';
        form.method = 'POST';
        form.action = '/upload';
        form.enctype = 'multipart/form-data';

        form.appendChild(input);
        form.appendChild(emali); // Append the hidden input for 'emali'
        document.body.appendChild(form);

        input.click();

        input.addEventListener('change', function() {
            if (input.files && input.files.length > 0) {
                var selectedFiles = input.files;
                console.log('Selected files:', selectedFiles);

                // Optional: You can display the selected file names
                var fileNames = [];
                for (var i = 0; i < selectedFiles.length; i++) {
                    fileNames.push(selectedFiles[i].name);
                }
                console.log('Selected file names:', fileNames.join(', '));

                // Show loader or blur background
                document.getElementById('set').style.display = 'block';
                document.getElementById('for-blur').style.filter = 'blur(5px)';

                // Create a new FormData object
                
                // Create a new XMLHttpRequest object
                var xhr = new XMLHttpRequest();
                

                // Set up onload callback function
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        // Hide loader or remove blur
                        document.getElementById('set').style.display = 'none';
                        document.getElementById('for-blur').style.filter = 'blur(0px)';

                        // Redirect to circle_images.php
                        window.location.href = 'circle_image.php';
                    } else {
                        console.error('Upload error:', xhr.statusText);
                        // Handle errors as needed
                    }
                };

                // Set up onerror callback function
                xhr.onerror = function() {
                    console.error('Network error');
                    // Handle errors as needed
                };

                // Set up upload progress callback function
                xhr.upload.onprogress = function(event) {
                    if (event.lengthComputable) {
                        var percentComplete = (event.loaded / event.total) * 100;
                        console.log(percentComplete + '% uploaded');
                        // You can update a progress bar here if needed
                    }
                };

                // Send the FormData object to the server
                xhr.send(formData);

                // Cleanup: Reset the form and remove it from the document after submission
                form.reset();
                document.body.removeChild(form);
            }
        });

        // Prevent form submission on addBtn click
        addBtn.addEventListener('submit', function(e) {
            e.preventDefault();
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
        });
    });
});
