/*jumbotron diaporama by bnhr*/
i = 1; //begin by jumbotron at position 2, the first is alredy load before setinterval
const diaporama = ()=>{
    let elt = $('.jumbotron')[i];
    $('.jumbotron').fadeOut(0);
    $(elt).css({
    "background": ` gray url(${$('.jumbotron img')[i].getAttribute("src")}) no-repeat center center`,
    "background-size": "contain",
    }).fadeIn(2000);

    i++;
    if (i > ($('.jumbotron').length - 1)){
        i = 0;
    }
}

/**===========================================================
 * details page script*/
//change principal figure on click
$(".img-sup-item").on("click", (e) => {
    //remove border on all img
    $(".img-sup-item").removeClass('border-2');
    //add border on curent selected element
    $(e)[0].target.classList.add("border-2");
    //replace principale figure by current selected
    $("#figure-img-principal").attr("src", e.target.src);
})


const mainStore = () => {
    let baseLink = 'http://127.0.0.1:8000/'
    let homePageLink = baseLink + 'store/'
    
    if ($.ajaxSettings.url == homePageLink){
        //show the first jumbotron before the set interval begin in 5000 ms
        $('.jumbotron:first').css({
            "background": `gray url(${$('.jumbotron img')[0].getAttribute("src")}) no-repeat center center`,
            "background-size": "contain", 
        }).fadeIn();
        //lauch diaporama
        setInterval(diaporama, 5000);
    }
}