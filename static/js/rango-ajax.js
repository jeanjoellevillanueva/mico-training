console.log("AJAX FILE LOADED");

$(document).ready(function() {
    console.log("JS READY");

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

    $('#search-input').keyup(function() {
        console.log("AJAX TRIGGERED");

        var query;
        query = $(this).val();

        $.get('/rango/suggest/', 
            {'suggestion': query},
             function(data) {
            console.log("AJAX RESPONSE RECEIVED");
            console.log("UPDATING SEARCH RESULTS");
                $('#search-results').html(data);
             }
        ); 
    });

    $('.rango-page-add').click(function() {
        console.log("ADD BUTTON CLICKED");
        var categoryid = $(this).attr('data-categoryid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var clickedButton = $(this);

        $.get('/rango/search_add_page/',
            {'category_id': categoryid, 'title': title, 'url': url},
            function(data) {
                $('#page-listing').html(data);
                clickedButton.hide();
            }

        );
    }); 
});