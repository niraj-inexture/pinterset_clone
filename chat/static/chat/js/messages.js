let loc = window.location
let wsStart = 'ws://'
if (loc.protocol === 'https:'){
    wsStart = 'wss://'
}
console.log(wsStart)
let endpoint = wsStart + location.host + location.pathname

let socket = new WebSocket(endpoint)
let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#message-form')
const USER_ID = $('#logged-in-user').val()

socket.onopen = async function(e){
    console.log('open',e)
    send_message_form.on('submit',function(e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()
        let data = {
            'message':message,
            'sent_by':USER_ID,
            'send_to':send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('open',e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message,sent_by_id,thread_id)
}

socket.onerror = async function(e){
    console.log('open',e)
}

socket.onclose = async function(e){
    console.log('open',e)
}

function newMessage(message, sent_by_id,thread_id){
    if ($.trim(message) === ''){
        return false;
    }
     let message_element;
     let chat_id = 'chat_' + thread_id
     const d = new Date();
     const weekday = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
     let day = weekday[d.getDay()]
     let img_url = $('.u_img').attr('src')
     if (sent_by_id==USER_ID){
        message_element =
            '<div class="d-flex mb-4 replied">'
                +'<div class="msg_cotainer_send">'
                    +message
                    +'<span class="msg_time_send">'+d.getDate()+" "+day+", "+d.getHours()+":"+d.getMinutes()+'</span>'
                +'</div>'
                +'<div class="img_cont_msg">'
                    +'<img src="'+img_url+'" class="rounded-circle user_img_msg">'
                +'</div>'
            +'</div>'
     }
     else{
        message_element =
        '<div class="d-flex mb-4 received">'
        +'<div class="img_cont_msg">'
                +'<img src="'+img_url+'" class="rounded-circle user_img_msg">'
                +'</div>'
            +'<div class="msg_cotainer">'
                +message
                +'<span class="msg_time_send">'+d.getDate()+" "+day+", "+d.getHours()+":"+d.getMinutes()+'</span>'
            +'</div>'
        +'</div>'
     }


	 let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}

$('.contact-li').on('click', function (){
    $('.contacts .active').removeClass('active')
    $(this).addClass('active')

    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')
})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

$(document).ready(function(){
    $(".chat-div").on("click",'.chat-del-btn',function(){
    let t_id = $(this).attr("thread-id");
    let csr = $("input[name=csrfmiddlewaretoken").val();
    mythis=this
    mydata = {thread_id:t_id, csrfmiddlewaretoken:csr}
    $.ajax({
        url: "/chat/delete-chat/",
        method: "POST",
        data: mydata,
        success:function(data){
            if (data.status == 1){
            location.reload()
            }
        }
    })
  });
})