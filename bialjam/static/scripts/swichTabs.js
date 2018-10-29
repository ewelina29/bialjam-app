$(document).ready(function () {
    $("#first-tab").click(function () {
        $("#first").css("display", "block");
        $("#second").css("display", "none");
        // $("#third").css("display", "none");
        $("#first-tab").css("background-color","#b1b1b1");
        $("#second-tab").css(   "background-color","#7B7979");
        // $("#inactiveTab").css(   "background-color","#7B7979");
    });
    $("#second-tab").click(function () {
        $("#first").css("display", "none");
        $("#second").css("display", "block");
        $("#third").css("display", "none");
        $("#first-tab").css("background-color","#7B7979");
        $("#second-tab").css(   "background-color","#b1b1b1");
        // $("#inactiveTab").css(   "background-color","#7B7979");

    });
    // $("#inactiveTab").click(function () {
    //     $("#first").css("display", "none");
    //     $("#second").css("display", "none");
    //     $("#third").css("display", "block");
    //     $("#activeTab").css(   "background-color","#7B7979");
    //     $("#inactiveTab").css(   "background-color","#7B7979");
    //     $("#inactiveTab").css("background-color","#b1b1b1");
    // });
});