//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    // startDate: 是一个js的对象 Date
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: new Date(Date.parse(startDate) + 86400000),
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search.html?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
}

$(document).ready(function(){
    // 默认显示注册/登录按钮
    $(".register-login").show();
    // 检查用户的登录状态
    $.get('/api/v1.0/session/', function (resp) {
        if (resp.errno == "0") {
            // 取数据进行判断是否有值
            if (resp.data.user_id && resp.data.name) {
                $(".register-login").hide();
                $(".user-name").html(resp.data.name)
                $(".user-info").show()
            }else {
                $(".register-login").show();
            }
        }
    })

    // 获取幻灯片要展示的房屋基本信息
    $.get("/api/v1.0/houses/index/", function (resp) {
        if (resp.errno == "0") {
            $(".swiper-wrapper").html(template("swiper-houses-tmpl", {"houses": resp.data}))
            // 数据设置完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });
        }
    })


    // 获取城区信息,获取完毕之后需要设置城区按钮点击之后相关操作
    $.get('/api/v1.0/areas/', function (resp) {
        if (resp.errno == "0") {
            $(".area-list").html(template("area-list-tmpl", {"areas": resp.data}))

            // 给所的城区的a标签添加点击事件
            $(".area-list a").click(function(e){
                // 给点击的按钮设置当前点击的城区名
                $("#area-btn").html($(this).html());
                // 给搜索按钮设置 area_id，以便在点击的时候去进入到搜索界面带上参数
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                // 给搜索按钮设置城区的名字
                $(".search-btn").attr("area-name", $(this).html());
                // 隐藏当前的弹出框
                $("#area-modal").modal("hide");
            });
        }
    })


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
})
