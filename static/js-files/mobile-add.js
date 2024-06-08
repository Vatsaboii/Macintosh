document.addEventListener('DOMContentLoaded', function() {
    var addBtn = document.getElementById('mobile-add');

    addBtn.addEventListener('click', function() {
        var input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.name = 'file';
        input.multiple = true;
        input.style.display = 'none';
        var emali=document.createElement('input')
        emali.value=localStorage.getItem('emali')

        var form = document.createElement('form');
        form.id = 'uploadForm';
        form.method = 'POST';
        form.action = '/upload';
        form.enctype = 'multipart/form-data';

        form.appendChild(input);
        document.body.appendChild(form);
        input.click();

        input.addEventListener('change', function() {
            if (input.files && input.files.length > 0) {
                var selectedFiles = input.files;
                console.log('Selected files:', selectedFiles);

                for (var i = 0; i < selectedFiles.length; i++) {
                    var file = selectedFiles[i];
                    console.log('File name:', file.name);
                    console.log('File type:', file.type);
                    console.log('File size:', file.size, 'bytes');
                }


                form.submit();
                form.reset();
                document.body.removeChild(form);
            }
        });

        addBtn.addEventListener('submit', function(e) {
            e.preventDefault();
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            document.body.removeChild(form);
        });
    });
});
