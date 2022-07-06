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

// ----------------------------

$(function () {
    $(".del-file").click(function (e) {
        e.preventDefault();
        var data = "station";
        $.ajax = ({
            method: "GET",
            url: '/testajax/',
            data: {'data': data},
            success: function (data) 
                {console.log(data);},
            error: function (xhr, status, error) 
                {console.log(error);}
    });
});
})
// --------------------------



// function delfile(){
//     const divID="del-file"
//     $(divID).on('click', (e) => {
//         e.preventDefault();
//         $.ajax({
//             type: 'POST',
//             url: $(this).data("url"),
//             // url: '/file/delete/',
//             data: $(this).serialize(),
//             success: function () {
//                 console.log('del +++', data);
//             },
//             error: function (response) {
//                 console.log('del err - ', response);
//             }
//         });
//     })
// }

// function id_filese_for_delete(){
//     let arr_of_id = [];
//     $(".del-file").click(function(e){ 
//         e.preventDefault();
//         // let elem = document.getElementById('document_'+$(this).data('bk')+'_'+$(this).data('pg')); 
//         arr_of_id.push($(this).data("pg"))
//         console.log('id ', $(this).data("pg"));
//         let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
//         document.getElementById(elem).remove(); 
//         console.log('arr_of_id ', arr_of_id);
//         return arr_of_id; 
//     });
// }

    // $(".del-file").click(function(e){ 
    //     e.preventDefault();
    //     // let elem = document.getElementById('document_'+$(this).data('bk')+'_'+$(this).data('pg')); 
    //     let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
    //     document.getElementById(elem).remove(); 
    //     // return false; 
    // });


$(document).ready(function (e) {
    // delfile()
    // id_filese_for_delete()
    // let arr_of_id = [];
    // $('.del-file122').click(function() {
    //     var i = $(this).data("pg")
    //     // $('.del-file').each(function() {   
    //     // arr_of_id.push(i);
    //     //  })
    //     let elem = 'document_'+$(this).data('bk')+'_'+$(this).data('pg');
    //     document.getElementById(elem).remove(); 
    //     var data = 'llklkk'
    //     $.ajax({
    //       method: "GET",
    //     //   type:  this.method,
    //       url: '/testajax/',
    //     //   this.action,
    //     //   data: arr_of_id,
    //     //   data : {'arr_of_id' : [arr_of_id]},
    //       data : {'data': data},
    //     //   dataType: "text",
    //       success: function(data) {
    //         // arr_of_id.push(i);
    //         // console.log('success arr_of_id for delete ', arr_of_id);
    //         console.log('---', data)

       
    //        },
    //       error: function(status, error) {
    //         console.log('error ', status);
    //       }
    //     })


    //   });

    $('#update-form').on('submit', function (e) {
        // e.preventDefault();
        // let formData = new FormData(this)
        // console.log('formData ', formData)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            success: function () {
                console.log('upd +++');
            },
            error: function (response) {
                console.log('upd err - ', response);
            }
        });
    });
})