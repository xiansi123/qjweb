$(function() {
    $("#userName").focus(function() {
        //获取地址文本框的值
        var text_value = $(this).val(); 
        if(text_value == "Username"){
            $(this).val("");
        }
    })

    $("#userName").blur(function() {
        var text_value = $(this).val();
        if(text_value == ""){
            $(this).val("Username");
        }
    })
    
    
    $("#showPassword").focus(function() {
        $("#password").show().focus();
        $("#password").val("");
        $("#showPassword").hide();
    })

    
    $("#password").blur(function() {
        if($("#password").val() == "") {
            $("#showPassword").show();
            $("#password").hide();
        }
    })
});