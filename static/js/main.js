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
                console.log('err - ', response)
                if (response.status === 400) {
                    $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                }
            }
        })
    }
     )
})
function delfile(){
    const divID="del-file"
    console.log('222', divID)
    $(divID).on('click', (e) => {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).data("url"),
            // url: '/file/delete/',
            data: $(this).serialize(),
            success: function () {
                console.log('+++', data);
            },
            error: function (response) {
                console.log('err - ', response);
            }
        });
    })
}

function delfile2(){
    $(".del-file").click(function(e){ 
        e.preventDefault();
        // let elem = document.getElementById('document_'+$(this).data('bk')+'_'+$(this).data('pg')); 
        let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
        document.getElementById(elem).remove(); 
        // return false; 
    });
}
$(document).ready(function (e) {
    delfile()
    delfile2()
    // $(".del-file").click(function(e){ 
    //     e.preventDefault();
    //     // let elem = document.getElementById('document_'+$(this).data('bk')+'_'+$(this).data('pg')); 
    //     let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
    //     document.getElementById(elem).remove(); 
    //     // return false; 
    // });

    $('#update-form').on('submit', function (e) {
        // e.preventDefault();
        let formData = new FormData(this)
        console.log('1111', formData)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            success: function () {
                console.log('+++');
            },
            error: function (response) {
                console.log('err - ', response);
            }
        });
    
    });
})
