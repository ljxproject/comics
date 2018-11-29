var key = GetQueryString("key");
var next = GetQueryString("next");
var start_time;
var task_id;
var uploader = WebUploader.create({           //创建上传控件
    swf: 'path_of_swf/Uploader.swf', //swf位置，这个可能与flash有关
    server: '/xadmin/mangaupload/',                 //接收每一个分片的服务器地址
    chunked: true,                            //是否分片
    chunkSize: 20 * 1024 * 1024,              //每个分片的大小，这里为20M
    chunkRetry: 3,                            //某分片若上传失败，重试次数
    threads: 1,                               //线程数量，考虑到服务器，这里就选了1
    duplicate: true,                          //分片是否自动去重
});

$("form[method='post']").submit(function (event) {
    task_id = WebUploader.Base.guid();        //产生task_id
    start_time = (new Date()).getTime();
    var file = $("#id_file")[0].files;
    uploader.addFiles(file);
    uploader.upload();
    $('#submit')[0].disabled = true;
    event.preventDefault();

});

$(document).ready(function () {
    uploader.on('uploadBeforeSend', function (obj, data) {
        data.task_id = task_id;
        data.csrfmiddlewaretoken = $("input:hidden[name='csrfmiddlewaretoken']").val();

    });
    uploader.on('uploadStart', function (file) {
        if (key == undefined) {
            var p = $("<div class='alert alert-dismissable alert-info'></div>").text("无效key");
            p.insertBefore($("#progress_message"));
            uploader.cancel(file)
        }
    });
    uploader.on('startUpload', function () {       //开始上传时，调用该方法
        $('.progress-bar').css('width', '0%');
        $('.progress-bar').text('0%');
        $('#progress_message').text("开始上传");

    });
    uploader.on('uploadProgress', function (file, percentage) { //一个分片上传成功后，调用该方法
        $('.progress-bar').css('width', (percentage * 100 - 1) / 2 + '%');
        $('.progress-bar').text(Math.floor((percentage * 100 - 1) / 2) + '%');
        $('#progress_message').text("正在上传");

    });

    uploader.on('uploadSuccess', function (file, response) { //整个文件的所有分片都上传成功，调用该方法
        //上传的信息（文件唯一标识符，文件名）
        var data = {
            'task_id': task_id, 'filename': file.source['name'], 'key': key,
            'next': next, "st": start_time
        };
        $.get('/xadmin/mangaupload-success/', data,
            function (data) {
                if (typeof(data) == "string") {
                    var err = $(data).find("pre").text();
                    var msg = $(data).find("div[class='alert alert-dismissable alert-danger']");
                    if (err) {
                        if ($('pre').length > 0) {
                            $('pre').text(err);
                        }
                        else {
                            var p = $('<pre></pre>').text(err);
                            p.insertBefore($("#progress_message"));
                        }
                    }
                    if (msg) {
                        if ($("div[class='alert alert-dismissable alert-danger']").length > 0) {
                            $("div[class='alert alert-dismissable alert-danger']").replaceWith(msg);
                        } else {
                            msg.insertBefore($("#progress_message"));
                        }
                    }
                    $('#submit')[0].disabled = false;
                    $('#id_file').val("");
                }
                else {
                    var url = data["url"];
                    setTimeout(function () {
                        alert("已成功上传");
                        window.location.href = url;
                    }, 2000);

                }
            },);
        $('.progress-bar').css('width', '50%');
        $('.progress-bar').text('50%');
        $('#progress_message').text("上传完毕，等待后台解析");
        progress();
    });

    uploader.on('uploadError', function (file) {   //上传过程中发生异常，调用该方法
        $('.progress-bar').css('width', '100%');
        $('.progress-bar').text('100%');
        $('#progress_message').text("上传失败");

    });

    uploader.on('uploadComplete', function (file) {//上传结束，无论文件最终是否上传成功，该方法都会被调用
        $('.progress-bar').removeClass('active progress-bar-striped');
    });
});


function progress() {
    run_ajax("start");

}

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则
    if (r != null) return unescape(r[2]);
    return null;
}


function run_ajax(start) {

    var t = setTimeout(run_ajax, 1000);
    if (start == "start") {
        $('#progress_message').text("上传完毕，等待后台解析");
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
    }

}

