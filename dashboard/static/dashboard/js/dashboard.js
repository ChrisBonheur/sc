   /*****DASHBOARD */
//action to click menu-down
$('.down-menu').on('click', () => {
    $('.dash-menu').toggleClass('d-none');
    $('.down-menu').attr('src', () => {
        if ($('.dash-menu').hasClass('d-none')){
            return '/static/node_modules/bootstrap-icons/icons/menu-up.svg'
        }else{
            return '/static/node_modules/bootstrap-icons/icons/menu-down.svg'
        }
    });
});