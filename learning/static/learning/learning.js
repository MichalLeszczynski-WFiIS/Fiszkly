function get_answer(flashcard_id){
    var data = {flashcard_id: flashcard_id}
    $.ajax({
        type: 'POST',
        url: "/learning/get_answer/",
        data: data,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function(data){
            var data = JSON.parse(data)
            $(".checker").css("display", "none");
            $(".is_correct_answer").css("display", "block");
            text = data.answer;
            text2 = data.dictionary_entry;
            $(".answer").css("display", "block");
            $(".definition").css("display", "block");
            $(".definition").html(text2);
            $(".answer").html(text);
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

function save_answer(is_correct, flashcard_id, category){
    var data = {is_correct: is_correct, flashcard_id: flashcard_id, category: category}
    $.ajax({
        type: 'POST',
        url: "/learning/save_answer/",
        data: data,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function(data){
            var data = JSON.parse(data)
            window.location.href = data.next_url
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