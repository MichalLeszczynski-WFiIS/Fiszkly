function get_answer(flashcard_id){
    var data = {flashcard_id: flashcard_id}
        $.ajax({
            type: 'POST',
            url: "/learning/get_answer/",
            data: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data){
                var parse_data = JSON.parse(data)
                $(".checker").css("display", "none");
                $(".is_correct_answer").css("display", "block");
                text = parse_data.answer;
                $(".flashcard").html(text);
            },
            statusCode:{
                401: function(responseObject, textStatus, jqXHR) {
                    $(".flashcard").html("401 You have to be logged in.")
                },
                500:function(responseObject, textStatus, jqXHR){
                    $(".flashcard").html("500 Server error")
                }
            },
        });
}

function save_answer(is_correct, flashcard_id, filter){
    var data = {is_correct: is_correct, flashcard_id: flashcard_id}
        next_url = "/learning/learn/" + filter
        $.ajax({
            type: 'POST',
            url: "/learning/save_answer/",
            data: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data){
                window.location.href = next_url
                console.log(next_url)
            },
            statusCode:{
                401: function(responseObject, textStatus, jqXHR) {
                    $(".flashcard").html("401 You have to be logged in.")
                },
                500:function(responseObject, textStatus, jqXHR){
                    $(".flashcard").html("500 Server error")
                }
            },
        });
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
}