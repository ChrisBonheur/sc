/*jumbotron diaporama by bnhr*/
i = 0;
const diaporama = ()=>{
    let elt = $('.jumbotron')[i];
    $('.jumbotron').fadeOut(0);
    $(elt).css({
    "background": `url(${$('.jumbotron img')[i].getAttribute("src")}) no-repeat center center`,
    "background-size": "cover",
    }).fadeIn(2000);

    i++;
    if (i > ($('.jumbotron').length - 1)){
        i = 0;
    }
}

setInterval(diaporama, 10000);