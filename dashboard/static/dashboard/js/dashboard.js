   /*****DASHBOARD */
   $(window).click(() => {
    $('.panneau1').hide();
    $('.panneau2').hide();
    $('.panneau3').hide();
})
$('.dash-nav .cursor1').on('click', (e) => {
    e.stopPropagation();
    $('.panneau1').toggle()
    $('.panneau2').hide();
    $('.panneau3').hide();
});

$('.dash-nav .cursor2').on('click', (e) => {
    e.stopPropagation();
    $('.panneau2').toggle()
    $('.panneau1').hide();
    $('.panneau3').hide();
});

$('.dash-nav .cursor3').on('click', (e) => {
    e.stopPropagation();
    $('.panneau3').toggle();
    $('.panneau1').hide();
    $('.panneau2').hide();
});