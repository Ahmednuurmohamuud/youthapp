
$(document).ready(function() {
    fetcharticle();
    

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
 
 
 
 
 
 $('#articleForm').submit(function (e) {
    e.preventDefault();

    const id = $('#articleId').val(); // Get the article ID (for update)
    const title = $('#tname').val(); // Get the article name
    const author = $('#aname').val();
    const scontent = $('#scontent').val();
    const content = $('#content').val();
    const c_id = $('#c_id').val();
    const fileInput = $('#img')[0]; // Get the file input element
    const file = fileInput.files[0]; // Get the selected file (if any)

    // Create a FormData object to handle both file and text data
    const formData = new FormData();
    if (id) formData.append('id', id); // Add ID for updates
    formData.append('tname', title); // Add the name field
    formData.append('aname', author);
    formData.append('scontent', scontent);
    formData.append('content', content);
    formData.append('c_id', c_id);
    if (file) formData.append('img', file); // Add the file if provided

    let url = id ? '/article/update' : '/article/insert'; // Determine endpoint based on ID presence

    $.ajax({
        url: url,
        method: 'POST',
        data: formData,
        processData: false, // Prevent jQuery from processing FormData
        contentType: false, // Let the browser set the appropriate Content-Type
        success: function (response) {
            $('#myModal').modal('hide'); // Hide the modal
            $('#alertMessage').text(response.message).show(); // Show success message

            // Refresh the article list
            fetcharticle();

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
   $('#articleForm')[0].reset();  // Reset the form fields
   $('#articleId').val('');
   $('#currentImage').attr('src', "/static/images/profile.jpeg");  // Fallback if no image  // Clear the hidden id field, if any
   $('#c_id').val("")
 }
 
 
 
 $(document).on('click', '.editBtn', function() {
    const id = $(this).data('id');
    const title = $(this).data('title');
    const author = $(this).data('author');
    const scontent = $(this).data('scontent');
    const content = $(this).data('content');
    const c_id = $(this).data('c_id');
      // Get the image URL from the button's data attribute
    const imgv = $(this).data('imgv');  
    
    $('#articleId').val(id);  // Set article ID in hidden input for update
    $('#tname').val(title);
    $('#aname').val(author);  // Set article ID in hidden input for update
    $('#scontent').val(scontent);
    $('#content').val(content);  // Set article ID in hidden input for update
    $('#c_id').val(c_id).trigger('change');

  
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
   
 
 
 
 
 
 
   var article = []; // Array to hold article data
 
   function fetcharticle() {
       $.ajax({
           url: '/article/select',
           method: 'POST',
           success: function(response) {
               article = response.article; // Store the fetched article data
               renderTable(article);
           }
       });
   }
 
   function renderTable(data) {
    $('#articleTableBody').empty(); // Clear the table body
    $.each(data, function(index, article) {
        $('#articleTableBody').append(`
            <tr>
                <td>${index + 1}</td>
                <td>${article.article_title}</td>
                <td>${article.article_author}</td>
                <td>${article.article_c_name}</td>
                <td>${article.article_scontent}</td>
                
                
                <td>
                   <img src="/static/images/${article.article_img}" alt="article Image" width="50" height="50">
                </td>
               
                <td>
                    <button class="btn btn-warning btn-sm editBtn" data-id="${article.article_id}" data-title="${article.article_title}" data-author="${article.article_author}"
                     data-scontent="${article.article_scontent}" data-content="${article.article_content}" data-c_id="${article.article_c_id}" data-imgv="${article.article_img}">
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
       var filteredarticle = article.filter(function(article) {
           return article.article_name.toLowerCase().includes(query) ||
                  article.article_img.includes(query);
       });
       renderTable(filteredarticle);
   }
 
   $('#searchInput').on('input', handleSearch);
 
   // Initialize the table with article data
  
 
 
   
 
 