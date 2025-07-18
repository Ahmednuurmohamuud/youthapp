
$(document).ready(function() {
    fetchcategory();
    

    $('#currentImage').attr('src', "/static/images/profile.jpeg");
   
     
 });
 
 function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function(){
        const output = document.getElementById('currentImage');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}
 
 
 
 
 
 $('#categoryForm').submit(function (e) {
    e.preventDefault();

    const id = $('#categoryId').val(); // Get the category ID (for update)
    const name = $('#categoryName').val(); // Get the category name
    const fileInput = $('#img')[0]; // Get the file input element
    const file = fileInput.files[0]; // Get the selected file (if any)

    // Create a FormData object to handle both file and text data
    const formData = new FormData();
    if (id) formData.append('id', id); // Add ID for updates
    formData.append('name', name); // Add the name field
    if (file) formData.append('img', file); // Add the file if provided

    let url = id ? '/category/update' : '/category/insert'; // Determine endpoint based on ID presence

    $.ajax({
        url: url,
        method: 'POST',
        data: formData,
        processData: false, // Prevent jQuery from processing FormData
        contentType: false, // Let the browser set the appropriate Content-Type
        success: function (response) {
            $('#myModal').modal('hide'); // Hide the modal
            $('#alertMessage').text(response.message).show(); // Show success message

            // Refresh the category list
            fetchcategory();

            // Hide the alert message and clear the form after 3 seconds
            setTimeout(function () {
                $('#alertMessage').text(response.message).hide();
                clearForm(); // Clear the form fields
            }, 3000);
        },
        error: function (response) {
            $('#alertMessages').text('Error: ' + response.responseJSON.message).show(); // Show error message
    setTimeout(function () {
        $('#alertMessages').hide(); // Hide the alert after 3 seconds
    }, 3000);
        }
    });
});


 // Function to clear the form data
 function clearForm() {
   $('#categoryForm')[0].reset();  // Reset the form fields
   $('#categoryId').val('');
   $('#currentImage').attr('src', "/static/images/profile.jpeg");  // Fallback if no image  // Clear the hidden id field, if any
 }
 
 
 
 $(document).on('click', '.editBtn', function() {
    const id = $(this).data('id');
    const name = $(this).data('name');
      // Get the image URL from the button's data attribute
    const imgv = $(this).data('imgv');  
    
    $('#categoryId').val(id);  // Set category ID in hidden input for update
    $('#categoryName').val(name);
    //$('#img').val(imgv);  // Set the img field in the form

    // Set the src of the current image preview in the modal
    if (imgv) {
        $('#currentImage').attr('src', "/static/images/" + imgv);  // Set the image source
    } else {
        $('#currentImage').attr('src', "/static/images/logo.png");  // Fallback if no image
    }

    // Show the modal
    $('#myModal').modal('show');
    $(currentImage).show();
});

 
 
 
 $(document).on('click', '.close', function() {
     
     clearForm();
     
   });
   
 
 
 
 
 
 
   var category = []; // Array to hold category data
 
   function fetchcategory() {
       $.ajax({
           url: '/category/select',
           method: 'POST',
           success: function(response) {
               category = response.category; // Store the fetched category data
               renderTable(category);
           }
       });
   }
 
   function renderTable(data) {
    $('#categoryTableBody').empty(); // Clear the table body
    $.each(data, function(index, category) {
        $('#categoryTableBody').append(`
            <tr>
                <td>${index + 1}</td>
                <td>${category.category_name}</td>
                <td>
                   <img src="/static/images/${category.category_img}" alt="Category Image" width="50" height="50">
                </td>
                <td>${category.category_img}</td>
                <td>
                    <button class="btn btn-warning btn-sm editBtn" data-id="${category.category_id}" data-name="${category.category_name}" data-img="${category.category_img}" data-imgv="${category.category_img}">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `);
    });
    updateShowingEntries(data.length);
}

 
   function updateShowingEntries(count) {
       $('#showingEntriesLabel').text('Showing ' + count + ' entries');
   }
 
   function handleSearch() {
       var query = $('#searchInput').val().toLowerCase();
       var filteredcategory = category.filter(function(category) {
           return category.category_name.toLowerCase().includes(query) ||
                  category.category_img.includes(query);
       });
       renderTable(filteredcategory);
   }
 
   $('#searchInput').on('input', handleSearch);
 
   // Initialize the table with category data
  
 
 
   
 
 