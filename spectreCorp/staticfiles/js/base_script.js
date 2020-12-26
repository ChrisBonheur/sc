/*****lOAD PAGE */
let screenHeight = $(window).height();
$('.load-deco').height(screenHeight);

$(function(){
    /****load event of all button linkl */
    $('a, .load-style').on('click', (e) => {
        $('.pages-content').toggle();
        $('.load-deco').toggle();

        if ($('#mobile-menu').show()){
            $('#mobile-menu').hide();
        }
    })


    /****Responsive***** */
    let window_wdth = $(window).width();
    
    /**For the const position tags */
    const const_position = () =>{
        let search_element_height = $('#search-element').height();
        let search_element_width = $('#search-element').width();
        let avatar_width = $('.info-user img').width();

        $('.valid-search').css({
            'position': 'fixed',
            'marginTop': `${search_element_height}px`,
            'width': `${search_element_width}px`,
            'background': 'red',
        });
    }

    /**Normal css without media */
    const_position();

    /**responsive media query */
    if (window_wdth <= 992){
        $('.navbar').hide();
    }else{
        $('.navbar').show();
    }

    $(window).on('resize', () => {
        const_position()
        if (window_wdth <= 992){
            $('.navbar').hide();
        }else{
            $('.navbar').show();
        }
    }); 

    /***********Event */
    /*******menu gestion */
    $('.menu-icon').on('click', ()=> {
        $('.b_h').toggle();
        $('#mobile-menu').toggle();
        /****Show scroller giving div height */
        let height_screen = $(window).height()
        $('#mobile-menu').css({'height': `${height_screen - 50}px`, 'overflow-y': 'scroll'});
        $(".btn1").toggle();
        $(".btn2").toggle();
    });

    /*****Event with avatar click */
    $('.img-user').on('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        $('.profil-menu').toggle()
    }).css('cursor', 'pointer');

    $(window).click(() => {
        $('.profil-menu').hide()
    });
     console.log("dssq")
    /**Event to serch article */
    $('#search-elt').on('input', () => {
        let input_text = $('#search-elt').val();
        $('.result-search-zone').text(`Rechercher  "${input_text}"`);
        $('.result-search-zone').show(2);
        $('#cancel-search').show();

        if (input_text.length == 1){
            $('.result-search-zone').css({'cursor': 'inherit', 'background': 'gray'});
        }
        else if(input_text.length >= 2){
            $('.result-search-zone').css({'cursor': 'pointer', 'background': '#124b98'});
        }
        else{
            $('.result-search-zone').hide();
            $('#cancel-search').css('display', 'none');
        }
    });
    $('#cancel-search').on('click', (e) => {
        e.preventDefault();
        $('#cancel-search').css('display', 'none');
        $('#search-elt').val('')
        $('.result-search-zone').css('display', 'none');
    });
    $('#search-elt').on('click', () => {
        $('#search-elt').val('')
    })
    
    $('.result-search-zone').on('click', () => {
        $('#valid-search').click()
    });

    /**Alert notif canncel */
    $('.remove-notif').on('click', (e) => {
        let liElt = e.target.parentNode 
        $(liElt).fadeOut()
    })
});

