console.log("AJAX FILE LOADED");

$(document).ready(function() {
    console.log("READY");

    $('#like_btn').click(function() {
        console.log("CLICKED");

        var categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/', {
            'category_id': categoryIdVar
        }, function(data) {
            console.log("SERVER RESPONSE:", data);

            $('#like_count').html(data);
            $('#like_btn').hide();
        });

    });
});