function get_answer(flashcard_id){
    var data = {flashcard_id: flashcard_id}
        console.log(data);
        $.ajax({
            type: 'POST',
            url: "/learning/get_answer/",
            data: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data){
                var parse_data = JSON.parse(data)
                $(".check_button").css("display", "none");
                $(".is_correct_answer").css("display", "block");
                text = "";
                for (var key in parse_data.answer)
                {
                    text += parse_data.answer[key] + '<br>';
                }
                $(".flashcard").html(text);
            },
            statusCode:{
                401: function(responseObject, textStatus, jqXHR) {
                    $(".flashcard").html("Have to log in ")
                },
                500:function(responseObject, textStatus, jqXHR){
                    $(".flashcard").html("Server error")
                }
            },
        });
}

function save_answer(is_correct, flashcard_id){
    var data = {is_correct: is_correct, flashcard_id: flashcard_id}
        console.log(data);
        $.ajax({
            type: 'POST',
            url: "/learning/save_answer/",
            data: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data){
                var parse_data = JSON.parse(data)
                window.location.href = parse_data.next_url
            },
            statusCode:{
                401: function(responseObject, textStatus, jqXHR) {
                    $(".flashcard").html("Have to log in ")
                },
                500:function(responseObject, textStatus, jqXHR){
                    $(".flashcard").html("Server error")
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