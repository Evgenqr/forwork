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

// --------------------------



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

   $(function () {
    $("#ajax").click(function (e) {
        // e.preventDefault();
        var text = "kkkk";
        $.ajax = ({
            // method: "GET",
            type: this.method,
            url: "/testajax/",
            data: $(this).serialize(), 
            // data: {data: text},
            success: function (response) 
                {console.log(response);},
            error: function (xhr, status, error, response) 
                {console.log(error);
                console.log(response.responseJSON.errors);}
    });
});
})



    $('#update-form').on('submit', function (e) {
        e.preventDefault();
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



//     $('#update-form').on('submit', function (e) {
//         e.preventDefault();
//         // let formData = new FormData(this)
//         // console.log('formData ', formData)
//         // var data = "kkkk";
//         var menuId = "009";

//         $.ajax({
//             // type: this.method,
            
//             url: this.action,
//             method: 'post',
//             // dataType: "text",
//             data: {text: 'Текст'},
//             // data: { name: "John", location: "Boston" },
//             // data: {id : menuId},
//             // $(this).serialize(),
//             success: function () {
//                 console.log('upd +++');
//             },
//             error: function (response, error) {
//                 console.log('upd err - ', error);
//             }
//         });
//     });
// })