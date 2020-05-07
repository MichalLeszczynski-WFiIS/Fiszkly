
function save_answer(id){
    var data = {id: id}
        console.log(data);
        $.ajax({
            type: 'POST',
            url: "/learning/save_answer/",
            data: data,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data){
                var parse_data = JSON.parse(data)
                if(parse_data.is_correct)
                {
                    $(".flashcard").html("Correct answer")
                    $(".flashcard").css("background-color", "green");
                }
                else
                {
                    $(".flashcard").html("Wrong answer")
                    $(".flashcard").css("background-color", "red");
                }
                $(".button").show()
                $(".button").css("display", "block");
                $(".button").click(function(){
                    window.location.href = "/learning/test/" + parse_data.next_word_id;
                  });
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