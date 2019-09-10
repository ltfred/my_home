function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 在页面加载完毕向后端查询用户的信息
    $.get("/api/v1.0/user/profile/", function (resp) {
        if (resp.errno == "0") {
            // 展示数据
            $("#user-avatar").attr("src", resp.data.avatar_url)
            $("#user-name").val(resp.data.name)
        } else if (resp.errno == "4101") {
            location.href = "/login.html"
        } else {
            alert(resp.errmsg)
        }
    })

    //  管理上传用户头像表单的行为
    $("#form-avatar").submit(function (e) {
        e.preventDefault()
        // 上传头像
        $(this).ajaxSubmit({
            url: "/api/v1.0/user/avatar/",
            type: "post",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0") {
                    $("#user-avatar").attr("src", resp.data.avatar_url)
                } else if (resp.errno == "4101") {
                    location.href = "/login.html"
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    })

    // 管理用户名修改的逻辑

    $("#form-name").submit(function (e) {
        e.preventDefault()

        var name = $("#user-name").val()

        if (!name) {
            alert("请输入用户名")
            return
        }

        // 用户信息(用户名)修改
        $.ajax({
            url: "/api/v1.0/user/profile/",
            type: "post",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify({"name": name}),
            contentType: "application/json",
            success: function (resp) {
                if (resp.errno == "0") {
                    showSuccessMsg()
                } else if (resp.errno == "4101") {
                    location.href = "/login.html"
                } else {
                    $(".error-msg").show()
                }
            }
        })
    })

})

