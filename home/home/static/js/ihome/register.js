function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = ""
var preImageCodeId = ""
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 1. 生成编号
    imageCodeId = generateUUID()
    // 2. 设置页面中图片验证码img标签的src属性
    var url = "/api/v1.0/imagecode?cur=" + imageCodeId + "&pre=" + preImageCodeId
    // 找到image-code标签下的img标签，并设置src的属性值
    $(".image-code>img").attr("src", url)
    preImageCodeId = imageCodeId

}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    var params = {
        "mobile": mobile,
        "image_code": imageCode,
        "image_code_id": imageCodeId
    }

    //  通过ajax方式向后端接口发送请求，让后端发送短信验证码
    $.ajax({
        url: "/api/v1.0/smscode/",
        type: "post",
        data: JSON.stringify(params),
        headers: {
            "X-CSRFToken": getCookie("csrf_token")  //获取当前浏览器中cookie中的csrf_token
        },
        contentType: "application/json",
        success: function (resp) {
            if (resp.errno == "0") {
                // 代表发送成功
                var num = 60
                var t = setInterval(function () {
                    if (num == 1) {
                        // 倒计时结束,将当前倒计时给清除掉
                        clearInterval(t)
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                        $(".phonecode-a").html("获取验证码")
                    }else {
                        // 正在倒计时
                        num -= 1
                        $(".phonecode-a").html(num + "秒")
                    }
                }, 1000, 60)
            }else {
                generateImageCode()
                // 将发送短信的按钮置为可以点击
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                // 发送短信验证码失败
                alert(resp.errmsg)
            }
        }
    })
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // 注册的提交(判断参数是否为空)
    
    $(".form-register").submit(function (e) {
        e.preventDefault()

        // 取到用户输入的内容
        var mobile = $("#mobile").val()
        var phonecode = $("#phonecode").val()
        var password = $("#password").val()
        var password2 = $("#password2").val()

        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!phonecode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!password) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (password != password2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }

        // var params = {
        //     "mobile": mobile,
        //     "phonecode": phonecode,
        //     "password": password,
        // }

        // 方式2：拼接参数
        var params = {}
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value
        })

        $.ajax({
            url:"/api/v1.0/user/register/",
            type: "post",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params),
            contentType: "application/json",
            success: function (resp) {
                if (resp.errno == "0"){
                    // 直接回到首页
                    location.href = "/index.html"
                }else {
                    $("#password2-err span").html(resp.errmsg)
                    $("#password2-err").show()
                }
            }
        })
    })
})
