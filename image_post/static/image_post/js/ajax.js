$(document).ready(function(){

$(".grid-item").on("click",'.btn-del',function(){
    let id = $(this).attr("data-sid");
    console.log(id)
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mythis=this
    mydata = {sid:id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/delete-save-post/",
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

  $(".col-md-2").on("click",'.btn-all-del',function(){
    let id = $(this).attr("data-sid");
    console.log(id)
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mythis=this
    mydata = {uid:id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/delete-all-save-post/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                $(".grid").html('')
                location.reload()
            }
        }
    })
  });

  $(".follow-div").on("click",'.btn-follow',function(){
    var u_id = $('#user_id').val()
    var f_id = $('#id_follow_user').val()
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {uid:u_id,fid:f_id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/follow/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                $('.btn-follow').removeClass( "btn-follow" ).addClass('btn-unfollow')
                $('.btn-unfollow').attr('value','Unfollow')
                $('#followers').html(data.data+' followers')
            }
        }
    })
  });

  $(".follow-div").on("click",'.btn-unfollow',function(){
    var u_id = $('#user_id').val()
    var f_id = $('#id_follow_user').val()
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {uid:u_id,fid:f_id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/unfollow/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                $('.btn-unfollow').removeClass( "btn-unfollow" ).addClass('btn-follow')
                $('.btn-follow').attr('value','Follow')
                $('#followers').html(data.data+' followers')
            }
        }
    })
  });

  $(".grid-item").on("click",'.btn-history-del',function(){
    let img_id = $(this).attr("data-img-id");
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mythis=this
    mydata = {imgid:img_id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/image-history/",
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

  $(".like-div").on("click",'.btn-like',function(){
    var u_id = $('#user').val()
    console.log(u_id)
    var f_id = $('#like_user_id').val()
    var i_id = $('#image_id').val()
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {uid:u_id,fid:f_id,imgid:i_id,csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/like/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                $('.btn-like').removeClass( "btn-like" ).addClass('btn-unlike')
                $('.btn-unlike').attr('value','Unlike')
                $('#likes').html(data.data+' likes')
            }
        }
    })
  });

$(".like-div").on("click",'.btn-unlike',function(){
    var u_id = $('#user').val()
    var f_id = $('#like_user_id').val()
    var i_id = $('#image_id').val()
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mydata = {uid:u_id,fid:f_id,imgid:i_id,csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/img/unlike/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
                $('.btn-unlike').removeClass( "btn-unlike" ).addClass('btn-like')
                $('.btn-like').attr('value','Like')
                $('#likes').html(data.data+' likes')
            }
        }
    })
  });

  });