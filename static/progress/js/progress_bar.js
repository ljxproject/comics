function progress() {
    run_ajax("start");

}

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则
    if (r != null) return unescape(r[2]);
    return null;
}

var key = GetQueryString("key");

function run_ajax(start) {

    var t = setTimeout(run_ajax, 1000);
    if (start == "start") {
        document.getElementById("progress_message").innerHTML = "等待上传";
    }
    else {
        $.ajax({
            dataType: 'json',
            type: "GET",
            url: "/adminx/check_progress",
            data: {"key": key},
            timeout: 5000,
            success: function (data, textStatus, jqXHR) {
                var message = data.data[1].toString();
                var num = data.data[0].toString();
                document.getElementById("progress_message").innerHTML = message;
                document.getElementById("progress_num").innerHTML = num + "%";
                document.getElementById("progress_num").style.width = num + "%";
                if (data.data[0] == 100) {
                    clearTimeout(t);
                }
                console.log(data);
                console.log(textStatus);
                console.log(jqXHR);
            },
            error: function (textStatus, jqXHR) {
                console.log("error");
                console.log(textStatus);
                console.log(jqXHR);
            }

        });
        var send_key = document.getElementById("submit");
        send_key.disabled = true;
    }

}

