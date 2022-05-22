// $(".del-bookmark").click(function(){ 
//     $(this).closest(".item").remove(); 
//     return false; 
//   });


$(".del-bookmark").click(function (e) { 
    removeEl(e.target);
    return false;
});

function removeEl(el) {
    $(el).parent().parent().remove(); 
};