
var msg_template = "<div class=\"media text-muted pt-3\" id=\"msg_content\">" +
    "        </div>";

var content_msg_template = "<p class=\"media-body pb-3 mb-0 small lh-125 border-bottom border-gray\">" +
    "<strong class=\"d-block text-gray-dark\">@username</strong>" +
    "            Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.\n" +
    "          </p>";

var content = "<div class=\"media text-muted pt-3\" id=\"msg_content\">" +
"<p class=\"media-body pb-3 mb-0 small lh-125 border-bottom border-gray\" id=\"content\">" +
    "<strong class=\"d-block text-gray-dark\">@username</strong>" +
    "            Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.\n" +
    "          </p>" +
     "        </div>";

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('event', function(list) {
    // for (var i=0; len=list.length; i++){
    //     document.getElementById("content").innerHTML = list[i];
    //     console.log(list[i]);
    //     var itm = document.getElementById("message");
    //     var cln = itm.cloneNode(true);
    //     document.getElementById('messages').appendChild(cln);
    // }
    var messages = document.getElementById("messages");
    var message = document.createElement('div');
    message.setAttribute("class", "media-body pb-3 mb-0 small lh-125 border-bottom border-gray");
    var content_msg = document.createElement('div');
    var img = document.getElementById("img-hidden");
    var clon = img.cloneNode(true);
    // message.innerHTML = msg_tem;
    content_msg.innerHTML = content_msg_template;
    message.appendChild(clon);
    message.appendChild(content_msg);
    messages.appendChild(message);
    // messages.insertBefore(clon, message);
    // messages.insert

});

// <script type=text/javascript>
// $(function() {
//   $('a#process_input').bind('click', function() {
//     $.getJSON('/background_process', {
//       proglang: $('input[name="proglang"]').val(),
//     }, function(data) {
//       $("#result").text(data.result);
//     });
//     return false;
//   });
// });
// </script>