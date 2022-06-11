// function removeEl(el) {
//     $(el).parent().parent().remove(); 
// };

$(document).ready(function() {
    // CSRF code
       function getCookie(name) {
           var cookieValue = null;
           var i = 0;
           if (document.cookie && document.cookie !== '') {
               var cookies = document.cookie.split(';');
               for (i; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) === (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       var csrftoken = getCookie('csrftoken');
   
       function csrfSafeMethod(method) {
           // these HTTP methods do not require CSRF protection
           return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
       }
       $.ajaxSetup({
           crossDomain: false, // obviates need for sameOrigin test
           beforeSend: function(xhr, settings) {
               if (!csrfSafeMethod(settings.type)) {
                   xhr.setRequestHeader("X-CSRFToken", csrftoken);
               }
           }
       });
   
       $('#del-file').on('click', function(e) {
           e.preventDefault();
           var $this = $(this),
               data = $this.data();
   
   
           $this.hide();
           $.ajax({
               url: 'deletefile',
               method: 'POST',
               data: data,
               success: function(d) {
                   console.log(d);
               },
               error: function(d) {
                   console.log(d);
               }
           });
       });
   });