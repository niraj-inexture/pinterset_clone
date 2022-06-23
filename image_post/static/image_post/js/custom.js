function change(){
 var val = document.getElementById('id_save').getAttribute('id');
 if (val == "Save"){
    document.getElementById('id_save').setAttribute('value','Saved');
    document.getElementById('id_save').setAttribute('disabled',"disabled");
}
};


let sharebtn = [...document.getElementsByClassName('share-btn')]
let copybtn = [...document.getElementsByClassName('copy-btn')]
sharebtn[0].addEventListener("click", shareFunction);

function shareFunction() {
    let url =  window.location.href
    document.getElementById("txt").innerHTML = url;
    copybtn[0].setAttribute("data-link", url)
};

copybtn[0].addEventListener("click", myFunction);

function myFunction() {
 const link = copybtn[0].getAttribute('data-link')
 navigator.clipboard.writeText(link)
 copybtn[0].textContent='Copied'
};
