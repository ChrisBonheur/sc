
    /************PROFIL */
    /**
     * This function set any element from DOM to a square element
     * with four dimensions are same dimension
     * @param {dom select element} eltSelect 
     */
    const squareWidthHeight = (eltSelect) => {
        let widthElt = $(eltSelect).width();
        let heightElt = $(eltSelect).height();

        if (widthElt < heightElt){
            //if width is less than height set height is equal to width dimension
            $(eltSelect).height(widthElt)
            $(eltSelect).width(widthElt)
        }else{
            //if heigth is less than width set width is equal to height dimension
            $(eltSelect).width(heightElt);
            $(eltSelect).height(heightElt);
        }
        
        return true;
    }

    //set an active button link style
    const linkUserActiveStyle = () => {
        let currentUrl = $.ajaxSettings.url;

        let links = $('.param-link').get()
        links.forEach(link => {

            if (currentUrl == link.href){
                $(link).addClass('active-secondary');
            }
        });
    }
    

    /** change email event*/
    // $('.btn-change-email').on('click', (e) => {
    //     e.preventDefault()
    //     let newMail = prompt('Entrez votre email');

    //     $('.show-mail').text(newMail);
    //     $('#email').val(newMail);
    // });


    /*****update password */
    // let btnElt1 = $('.bloc-param .row6 .btn1')
    // let btnElt2 = $('.bloc-param .row6 .btn2')
    // btnElt1.css('background', 'gray')
    
    // $('.pwd1').on('input', (e) => {
    //     let inputElt = e.target
        
    //     if(inputElt.value.length < 4) {
    //         $(inputElt).css({
    //             'border': '2px solid red'
    //         })
    //         $('.pwd1-error').show()
    //         btnElt1.show()
    //         btnElt2.hide()
    //     }
    //     else if ($('.pwd2').val().length >= 1) {
    //         if (($('.pwd1').val() !== $('.pwd2').val())) {
    //             $('.pwd2-error').show();
    //             btnElt1.show()
    //             btnElt2.hide()   
    //         } else {
    //             $('.pwd2-error').hide();
    //             btnElt1.hide()
    //             btnElt2.show()               
    //         }
    //     }
    //     else{
    //         $(inputElt).css({
    //             'border': '1px solid gray'
    //         })
    //         $('.pwd1-error').hide()

    //         $('.pwd2').on('input', (e) => {
    //             if ( e.target.value !== $('.pwd1').val() ){
    //                 $('.pwd2-error').show();
    //                 btnElt1.show()
    //                 btnElt2.hide()
    //             }else{
    //                 $('.pwd2-error').hide();
    //                 btnElt1.hide()
    //                 btnElt2.show()
    //             }
    //         })
    //     }
    // });

const userMain = () => {
    //Action on click profil photo
    $('.show-menu-fixed').on('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        $('.fixed-bloc-links').toggleClass('d-none');
    });
    $(window).on('click', () =>{
        $('.fixed-bloc-links').addClass('d-none');
    });

    //style on active link
    linkUserActiveStyle();

    //make photo profil in square form then set rounded with bootstrap in file html
    $(window).on('resize', () => {
        squareWidthHeight('.img-square');
    });
    squareWidthHeight('.img-square');

    /**Event to change picture profile on profile page*/
    $('.btn-change-img').on('click', (e) => {
        e.preventDefault();
        $('#id_avatar').click();
    });
    $('#id_avatar').on('change', (e) => {
        let url = URL.createObjectURL(event.target.files[0]);
        $('.img_chosen').attr({
            'src': url,
        });
    });
}

userMain();