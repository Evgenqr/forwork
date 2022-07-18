$(function ($) {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('#login-form').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            // headers: {'X-CSRFToken': getCookie('csrftoken')},
            dataType: 'json',
            success: function (response) {
                window.location.reload()
            },
            error: function (response) {
                console.log('log err - ', response)
                if (response.status === 400) {
                    $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                }
            }
        })
    }
     )
})

$(document).ready(function (e) {
    let arr_of_id = [];
    $(".del-file").click(function(e){ 
        arr_of_id.push($(this).data("pg"))
        let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
        document.getElementById(elem).remove(); 
        console.log('arr_of_id ', arr_of_id);
        return arr_of_id; 
    });


    $('#update-form').on('submit', function (e) {
        // e.preventDefault();
          $.post(this.action, {arr_of_id: arr_of_id}, function(data){
            console.log('ok ', arr_of_id);
        });
    });

    // $('.ext-search-btn1').click(function(){
    //     $('.ext-search1').slideToggle(300);      
    //     return false;
    // });

})
