/**Create article script ==================================================== */
/**Add pic file and show it in create article page form*/
const add_suplementary_pics = () =>{
    file_nbr++;
    let inputElt = document.createElement('input');
    let cancelButton = document.createElement('p');
    
    $(inputElt)
        .attr({
            'type': "file",
            'class': "image-files" ,
            'name': "",
        })
        .change((e) => {
            let url = URL.createObjectURL(event.target.files[0]);
            let divElt = document.createElement('div');

            $(divElt).attr({
                'class': 'col-2',
            }).css({
                'height': '180px',
                'background': `gray url("${url}") no-repeat center center`,
                'background-size': 'contain',
                'heigh': "78px"
            });
            
            $(divElt).append(cancelButton);
            $('.upload_pics').append(divElt);
            
            //create cancel button to remove picture added
            $(cancelButton)
                .addClass('btn-cancel')
                .text('x')
                .on('click', () => {
                    $(divElt).remove();
                    $(inputElt).remove();
                    file_nbr--;
                    console.log(file_nbr);
                });
        });

    $(inputElt).hide();//hide input file
    $(inputElt).click();//execute input Elt
    $('.pictures-sup').append(inputElt);
}


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

/**
 * create a proportional block element by given a height percentage
 * @param {*} element : dom element selected with jquery
 * @param {*} height_percentage : the percentage height 
 */
const create_block_proportion = (element, height_percentage) => {
    const set_height_proportion = () => {
        //get element width
        let article_bg_img_width = element.innerWidth() ;
        let article_bg_img_height = (height_percentage * article_bg_img_width) / 100;
        //set element height with the height found
        element.innerHeight(article_bg_img_height);
    }
    set_height_proportion();
    $(window).resize(() => {
        set_height_proportion();
    })
}

const mainStore = () => {
    /**set of link page of store app */
    let baseLink = 'http://127.0.0.1:8000/';
    let homePageLink = baseLink + 'store/';
    let myArticlsPageLink = baseLink + 'store/mes-articles-ajoutés/';
    let createArticlePageLink = baseLink + 'store/poster-un-article/';

    //create equitable background image for article card
    create_block_proportion($('.article .background-img'), 100);

    if ($.ajaxSettings.url == homePageLink || $.ajaxSettings.url == baseLink)
    {
        //show the first jumbotron before the set interval begin in 5000 ms
        $('.jumbotron:first').css({
            "background": `gray url(${$('.jumbotron img')[0].getAttribute("src")}) no-repeat center center`,
            "background-size": "contain", 
        }).fadeIn();
        //lauch diaporama
        setInterval(diaporama, 5000);
    }
    //==========================================================================================
    else if ($.ajaxSettings.url == createArticlePageLink) 
    {
        //script for create article page
        file_nbr = 1;//number of file added
        //event to add picture 
        $('.add-pics-btn').on('click', (e) => {
            e.preventDefault();
            if (file_nbr <= 4){
                add_suplementary_pics(file_nbr);
                $('.pictures-sup .alert').addClass('d-none');
            }else{
                $('.pictures-sup .alert').removeClass('d-none');
            }
            console.log(file_nbr);
        });

        //Event on click button save article
        $('.save-btn').on('click', (e) => {
            e.preventDefault();
            
            //for each input add name attribut with i number
            $.map($('.image-files'), (el, ind) => {
                //add 1 to index, coz name of input begin to image_1 not image_0
                $(el).attr("name", `image_${ind + 1}`);
            })    
            
            //create new button submit to continue action to save
            let btnElt = document.createElement('button');
            $(btnElt).attr("type", "submit").hide();
            $('.form-box-btn').append(btnElt);
            //execute new button
            $(btnElt).click();
        });
    }
}