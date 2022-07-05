
function change(){
 var val = document.getElementById('id_save').getAttribute('id');
 if (val == "Save"){
    document.getElementById('id_save').setAttribute('value','Saved');
    document.getElementById('id_save').setAttribute('disabled',"disabled");
}
};

let share_btn = [...document.getElementsByClassName('share-btn')]
let copy_btn = [...document.getElementsByClassName('copy-btn')]

share_btn[0].addEventListener("click", shareFunction);
function shareFunction() {
    let url =  window.location.href
    document.getElementById("txt").innerHTML = url;
    copy_btn[0].setAttribute("data-link", url)
};

copy_btn[0].addEventListener("click", myFunction);

function myFunction() {
 const link = copy_btn[0].getAttribute('data-link')
 navigator.clipboard.writeText(link)
 copy_btn[0].textContent='Copied'
};
