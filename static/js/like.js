$(document).ready(function() {
    $('.like_button').click(function() {
        var postID;
        postID = $(this).attr('data-postid');
        $.get('/city_stars/post/posts/like_post/',
            {'post_id': postID},
                function(data) {
                    $('#likes'+postID).html(data[0]);
                    $('#heart'+postID).attr("src", data[1]);
        })
    });
});
    