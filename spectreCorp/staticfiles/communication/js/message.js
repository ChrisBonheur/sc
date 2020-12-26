$(function(){
    /***********NEW MESSAGE PAGE******** */
    $('.msg-zone input').on('input', () => {
        $('.msg-zone .btn2').hide();
        $('.msg-zone .btn1').show();

        if ($('.msg-zone input').val().length > 0){
            $('.msg-zone .btn1').hide();
            $('.msg-zone .btn2').show();
        }
    });

    let screen_height = $(window).height() - 105;//we dissmiss screen height with padding given in css
    $('.new-msg').height(screen_height);
    let heightBlankZone = (65 * screen_height) / 100; //we get 80% of window to place blank zone 
    $('.new-msg .blank-zone').height(heightBlankZone);

    let element = document.getElementById('content-msg');

    element.scrollTop = element.scrollHeight;
});