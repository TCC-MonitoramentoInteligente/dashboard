
// $(function process() {
//   $('a#process_input').bind('click', function() {
//     $.getJSON('/background_process', {
//       proglang: $('input[name="proglang"]').val(),
//     }, function(data) {
//       $("#result").text(data.result);
//     });
//     return false;
//   });
// });
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('new message', function(msg) {
    // $('#messages').append($('<li>').text(msg));
    // $('#messages').contentEditable.replace(msg);
     document.getElementById("content").innerHTML = msg;
     var itm = document.getElementById("message");
    var cln = itm.cloneNode(true);

    document.getElementById('messages').appendChild(cln);
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