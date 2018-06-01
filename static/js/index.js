$(document).ready(function() {
    $(".friends-msg-btn").click(function() {
        $(this).next().toggleClass("isHidden");
    });
    
    $("#my-new-msg").click(function() {
        $("#my-new-msg-popup").toggleClass("popup-hide");
    });

    $("#my-new-msg-cancel").click(function() {
        $("#my-new-msg-popup").toggleClass("popup-hide");
    })


});