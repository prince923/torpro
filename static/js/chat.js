
$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").on("submit", function() {  // 点击提交时执行
        newMessage($(this));
        return false;
    });
    $("#messageform").on("keypress", function(e) {  // 回车提交时执行
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    updater.start();   // 开始 WebSocket
});

function newMessage(form) {     // 发送新消息给服务器
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    $("input[name='body']").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/ws";
        updater.socket = new WebSocket(url);  // 初始化 WebSocket
        updater.socket.onmessage = function(event) {  // 获取到服务器的信息时响应
            updater.showMessage(JSON.parse(event.data));
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        // node.hide();
        $("#inbox").append(node);  // 添加消息 DIV 到页面
        // node.slideDown();
    }
};
