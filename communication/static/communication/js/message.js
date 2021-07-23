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
    //we dissmiss screen height with height header and 20 to get stable page
    let screen_height = $(window).height() - $('header').height() - 20;
    console.log(screen_height)
    console.log($('header').height())
    $('.new-msg-page').height(screen_height);
    let heightMessages = (70 * screen_height) / 100; //we get 80% of window to place blank zone 
    $('.bloc-messages').height(heightMessages);

    let element = document.getElementsByClassName('bloc-messages')[0];
    console.log(element)
    element.scrollTop = element.scrollHeight;
});