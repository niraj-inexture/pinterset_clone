$( function(){
    var availableTopics=[]

    $.ajax({
        url: "/user/topic-list/",
        method: "GET",
        success:function(data){
            startAutoComplete(data)
        }
    });

    function startAutoComplete(availableTopics){
        $( "#topic-search" ).autocomplete({
            source:availableTopics
        });
    }

 var owl = $('.owl-carousel');
owl.owlCarousel({
    items:1,
    loop:true,
    margin:10,
});


$(".delete-board-form").on("click",'.btn-board-del',function(){
    let id = $(this).attr("data-imgid");
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mythis=this
    mydata = {sid:id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/user/delete-board-post/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
            $(mythis).closest(".grid-item").fadeOut()
            location.reload()
            }
        }
    })
  });

  $(".create-board-btn").click(function(e){
    let t_id = $("select[name=topic").val();
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {topic_id:t_id,csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/user/create-board/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                location.reload()
            }
        }
    })
  });

 $(".board-del-btn").click(function(e){
    let t_id = $(this).attr("topic-del-id");
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {topic_id:t_id,csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/user/delete-board/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                location.reload()
            }
        }
    })
  });
});

function messageShow(){
    document.getElementById("messages").style.display = "none";
}
setTimeout("messageShow()",5000)
