


function changeBgImg(){
    var elems = document.getElementsByClassName('filelogo');
    for (var i = 0; i < elems.length; i++) {

        elem = elems[i].innerText.split(' ')[0].split('.')
        // console.log('+++ ', elem);
        file_ext = elem[elem.length-1]
        if (file_ext=='pdf'){
            elems[i].style.backgroundImage = "url('/static/img/pdf.svg')";
        }
        else if (file_ext=='txt'){
            elems[i].style.backgroundImage = "url('/static/img/text.svg')";
        }
        else if (file_ext=='doc' || file_ext=='docx' || file_ext=='rtf') {
            elems[i].style.backgroundImage = "url('/static/img/word.svg')";
        }
        else if (file_ext=='xls' || file_ext=='xlsx') {
            elems[i].style.backgroundImage = "url('/static/img/excel.svg')";
        }
        else if (file_ext=='ppt' || file_ext=='pptx') {
            elems[i].style.backgroundImage = "url('/static/img/power-point.svg')";
        }
        else if (file_ext=='png' || file_ext=='bmp' || file_ext=='gif' || file_ext=='jpg') {
            elems[i].style.backgroundImage = "url('/static/img/image-picture.svg')";
        }
        else if (file_ext=='zip' || file_ext=='zip') {
            elems[i].style.backgroundImage = "url('/static/img/power-point.svg')";
        }

        else {
            elems[i].style.backgroundImage = "url('/static/img/power-point.svg')";
        }
	}
}


changeBgImg();


