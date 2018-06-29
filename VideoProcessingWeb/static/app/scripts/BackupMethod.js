jQuery.fn.wait = function (func, times, interval) {
    var _times = times || -1, //100次
        _interval = interval || 20, //20毫秒每次
        _self = this,
        _selector = this.selector, //选择器
        _iIntervalID; //定时器id
    if (this.length) { //如果已经获取到了，就直接执行函数
        func && func.call(this);
    }
    else {
        _iIntervalID = setInterval(function () {
            if (!_times) { //是0就退出
                clearInterval(_iIntervalID);
            }
            _times <= 0 || _times--; //如果是正数就 --

            _self = $(_selector); //再次选择
            if (_self.length) { //判断是否取到
                func && func.call(_self);
                clearInterval(_iIntervalID);
            }
        }, _interval);
    }
    return this;
}

$('html').ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X - CSRFToken", getCookie('csrftoken'));
    }
});


var SlideFrame = document.getElementById("DocFrame");
if (SlideFrame.attachEvent) {
    SlideFrame.attachEvent("onload", function () {
        //alert("Local iframe is now loaded.");
        //$("#ExternalHeaderFullTopBars",document.frames['DocFrame'].document).hide();
        //$("#AppHeaderPanel",document.frames['DocFrame'].document).hide();
        //$("#EditingThumbnailsPanel",document.frames['DocFrame'].document).width("10px");
        //$.RegisterSlideClick();
        //
        //alert($("#PptEditingStatusBar\\.SlideInformation-Medium14",document.frames['DocFrame'].document).html());
        //$("#PptEditingStatusBar.SlideInformation-Medium14",document.frames['DocFrame'].document).find("span:first-child").bind('DOMNodeInserted', function(e) {
        //    alert();
        //});
    });
} else {
    SlideFrame.onload = function () {
        //alert("Local iframe is now loaded.");
        //$.RegisterSlideClick();
        //

    };
}

$("#PptEditingStatusBar\\.SlideInformation-Medium14 span:eq(0)", document.frames['DocFrame'].document).waitStatusBar(function () {
    SlidePageCount = $.GetSlidePageCount();
    //chindren(),find()不支持bind(),html()
    var thisStatusBar = $("#PptEditingStatusBar\\.SlideInformation-Medium14 span:eq(0)", document.frames['DocFrame'].document);
    thisStatusBar.bind('DOMNodeInserted', function (e) {
        //alert(thisStatusBar.html());               
        //alert($.GetSlidePage()+"/"+SlidePageCount+"//"+$.GetSlidePageCount());
        //
        var tempCurrentSlidePage = $.GetSlidePage();
        if (tempCurrentSlidePage != CurrentSlidePage) {
            CurrentSlidePage = tempCurrentSlidePage;
            if ($("[PPTPagination=" + CurrentSlidePage + "]").html() != null && $("[PPTPagination=" + CurrentSlidePage + "]").html() != undefined) {
                //alert(("#FullTextPanel").scrollTop);
                //alert($("[PPTPagination=" + CurrentSlidePage + "]").offset().top);
                //alert($("#FullTextPanel").scrollTop());
                //$("#FullTextPanel").scrollTop($("[PPTPagination=" + CurrentSlidePage + "]").offset().top);
                if ($(".SentenceCurrentSkip").html() != null && $(".SentenceCurrentSkip").html() != undefined) {
                    $(".SentenceCurrentSkip").attr("class", "SentenceDefault");
                }
                else { }
                $("[PPTPagination=" + CurrentSlidePage + "]").attr("class", "SentenceCurrentSkip");
            }
            else { }
        }
        else { }
        var tempSlidePageCount = $.GetSlidePageCount();
        if (tempSlidePageCount != SlidePageCount) {
            if (SlidePageCount == 0) {
                SlidePageCount = tempSlidePageCount;
            }
            else if (tempSlidePageCount - SlidePageCount == 1) {
                var NewPaginationNum = $.GetSlidePage() + 1;
                var PPTIdList = new Array();
                for (var i = NewPaginationNum; i <= tempSlidePageCount; i++) {
                    if ($("[PPTPagination=" + i + "]").html() != null && $("[PPTPagination=" + i + "]").html() != undefined) {
                        PPTIdList.push($("[PPTPagination=" + i + "]").attr("id"));
                    }
                }
                for (var j = 0; j < PPTIdList.length; j++) {
                    var tempNewPagination = parseInt($("[id=" + PPTIdList[j] + "]").attr("PPTPagination")) + 1;
                    $("[id=" + PPTIdList[j] + "]").attr("PPTPagination", tempNewPagination);
                    $("[id=" + PPTIdList[j] + "]").children("button").text("S" + tempNewPagination + "-");
                }
                SlidePageCount = tempSlidePageCount;
            }
            else if (tempSlidePageCount - SlidePageCount == -1) {
                if ($("[PPTPagination=" + $.GetSlidePage() + "]").html() != null && $("[PPTPagination=" + $.GetSlidePage() + "]").html() != undefined) {
                    //del 
                    $("[PPTPagination=" + $.GetSlidePage() + "]").children("button").remove();
                    //alert($("[PPTPagination=" + $.GetSlidePage() + "]").children("button").text());
                    $("[PPTPagination=" + $.GetSlidePage() + "]").attr("PPTPagination", 0);

                    $("[PPTPagination=" + $.GetSlidePage() + "]").children("button").remove();
                }
                var PPTIdList = new Array();
                for (var i = $.GetSlidePage() + 1; i <= tempSlidePageCount; i++) {
                    if ($("[PPTPagination=" + i + "]").html() != null && $("[PPTPagination=" + i + "]").html() != undefined) {
                        PPTIdList.push($("[PPTPagination=" + i + "]").attr("id"));
                    }
                }
                for (var j = 0; j < PPTIdList.length; j++) {
                    var NewPagination = parseInt($("[id=" + PPTIdList[j] + "]").attr("PPTPagination")) - 1;
                    $("[id=" + PPTIdList[j] + "]").attr("PPTPagination", NewPagination);
                    $("[id=" + PPTIdList[j] + "]").children("button").text("S" + NewPagination + "-");
                }
                SlidePageCount = tempSlidePageCount;
            }
            else { }
        }
        else { }
    });

});
//

$("#PptEditingStatusBar.SlideInformation-Medium14", document.frames['DocFrame'].document).find("span:first-child").wait(function () {
    alert($("#PptEditingStatusBar.SlideInformation-Medium14", document.frames['DocFrame'].document).find("span:first-child").html());
});

$("#DocFrame").ready(function () {
    setTimeout(function () {
        //chindren(),find()不支持bind(),html()
        $("#PptEditingStatusBar\\.SlideInformation-Medium14 span:eq(0)", document.frames['DocFrame'].document).bind('DOMNodeInserted', function (e) {
            alert($("#PptEditingStatusBar\\.SlideInformation-Medium14 span:eq(0)", document.frames['DocFrame'].document).html());
        });
    }, 10000);
})  



/*  ThisDiv = "<div id="+JsonData[i].type+"_"+ CurrentSubId + "'></div>"
                $("#" + container).append(ThisDiv);
                $("#TitleItem_" + JsonData[i].index).attr("class", "SubTitleBox");
                $("#TitleItem_" + JsonData[i].index).append("<span></span>");
                $("#TitleItem_" + JsonData[i].index).children("span").attr("id", "TitleTextItem_" + JsonData[i].index);
                $("#TitleItem_" + JsonData[i].index).children("span").attr("class", "SentenceCurrent");
                //$("#TitleItem_" + SubTitleCount).children("span").width($("#TitleItem_" + SubTitleCount).width()-120);
                $("#TitleItem_" + JsonData[i].index).children("span").width(466);
                $("#TitleItem_" + JsonData[i].index).children("span").attr("contentEditable", "true");
                $("#TitleItem_" + JsonData[i].index).children("span").text(JsonData[i].content)
                $("#TitleItem_" + JsonData[i].index).children("span").focus(function () {
                    //CurrentFocusItem = "TitleItem_" + SubTitleCount;
                    //$(this).attr("class", "SentenceBeginningOfParagraphCurrent");  
                    $(this).attr("class", "SentenceCurrent");
                });
                $("#TitleItem_" + JsonData[i].index).children("span").blur(function () {
                    //$(this).attr("class", "SentenceBeginningOfParagraphDefault");
                    $(this).attr("class", "SentenceDefault");
                    //alert($(this).parent(".SubTitleBox").attr("id").split("_")[1]);
                    var TitleId = $(this).parent(".SubTitleBox").attr("id").split("_")[1];
                    $("#TitleLi_" + TitleId).text($(this).text());
                });
                //DelBtn
                $("#TitleItem_" + JsonData[i].index).prepend("<button></button>");
                $("#TitleItem_" + JsonData[i].index).children("button").attr("type", "button");
                $("#TitleItem_" + JsonData[i].index).children("button").attr("class", "btn btn-primary btn-xs SubTitleDelBtn");
                $("#TitleItem_" + JsonData[i].index).children("button").text("T-");
                $("#TitleItem_" + JsonData[i].index).children("button").click(function () {
                    var TitleId = $(this).parent(".SubTitleBox").attr("id").split("_")[1];
                    $.SubTitleDelClick(TitleId);
                });
                //SubTitleNavi
                var ThisLi = "<li id='TitleLi_" + JsonData[i].index + "'></li>";
                $("#SubTitlePanel").append(ThisLi);
                $("#TitleLi_" + JsonData[i].index).attr("class", "SubTitleLi");
                $("#TitleLi_" + JsonData[i].index).text(JsonData[i].content);
                $.RegisterSubTitleClick(JsonData[i].index); */