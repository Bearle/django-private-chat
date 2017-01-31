$(document).ready(function () {
    var websocket = null;

    function addNewMessage(packet) {
        var msgElem = generateMessage(packet);
        $('#messages').append(msgElem);
        scrollToLastMessage()
    }

    function addNewUser(packet) {
        $('#user-list').html('');
        packet.value.forEach(function (userInfo) {
            if (userInfo.username == getUsername()) return;
            var tmpl = Handlebars.compile($('#user-list-item-template').html());
            $('#user-list').append(tmpl(userInfo))
        });
    }

    function scrollToLastMessage() {
        var $msgs = $('#messages');
        $msgs.animate({"scrollTop": $msgs.prop('scrollHeight')})
    }

    function generateMessage(context) {
        var tmpl = Handlebars.compile($('#chat-message-template').html());
        return tmpl({msg: context})
    }


    function getUsername() {
        return $('#username').text()
    }

    function setupChatWebSocket() {
        websocket = new WebSocket($('#ws-server-path').val() + getUsername());
        websocket.onopen = function (event) {
            var onConnectPacket = JSON.stringify({
                type: "new-user",
                username: getUsername()
            });
            console.log('connected, sending:', onConnectPacket);
            websocket.send(onConnectPacket)
        };

        websocket.onclose = function (event) {
            console.log('disconnected');
            var onClosePacket = JSON.stringify({type: 'close'});
            websocket.send(onClosePacket)
        };

        websocket.onmessage = function (event) {
            var packet;

            try {
                packet = JSON.parse(event.data);
                console.log(packet)
            } catch (e) {
                console.log(e);
            }

            switch (packet.type) {
                case "users-changed":
                    addNewUser(packet);
                    break

                case "new-message":
                    addNewMessage(packet);
                    break;

                case "new-message":
                    console.log('some one is typing...');
                    break;

                default:
                    console.log('error: ', event)
            }
        }
    }

    function broadCastMessage(message) {
        var newMessagePacket = JSON.stringify({
            type: 'new-message',
            username: getUsername(),
            message: message
        });
        websocket.send(newMessagePacket)
    }

    $('#chat-message').keypress(function (e) {
        if (e.which == 13 && this.value) {
            broadCastMessage(this.value);
            this.value = "";
            return false
        }
    });

    $('#btn-send-message').click(function (e) {
        var $chatInput = $('#chat-message');
        var msg = $chatInput.val();
        if (!msg) return;
        broadCastMessage($chatInput.val());
        $chatInput.val('')
    });


    setupChatWebSocket();
    scrollToLastMessage()
});
