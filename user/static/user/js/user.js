$(function(){
    /************PROFIL */
    const squareWidthHeight = (eltSelect) => {//make elt select in square form
        let widthElt = $(eltSelect).width();
        $(eltSelect).height(widthElt);
        return true;
    }

    $(window).on('resize', () => {
        squareWidthHeight('.bloc-param .row1 img');
    });

    squareWidthHeight('.bloc-param .row1 img');

    /**Event to change picture */
    $('.btn-change-img').on('click', (e) => {
        e.preventDefault();
        $('#avatar_img').click();
    });
    
    $('#avatar_img').on('change', (e) => {
        let url = URL.createObjectURL(event.target.files[0]);
        $('.img_chosen').attr({
            'src': url,
        });
    });

    /** change email event*/
    $('.btn-change-email').on('click', (e) => {
        e.preventDefault()
        let newMail = prompt('Entrez votre email');

        $('.show-mail').text(newMail);
        $('#email').val(newMail);
    });


    /*****update password */
    let btnElt1 = $('.bloc-param .row6 .btn1')
    let btnElt2 = $('.bloc-param .row6 .btn2')
    btnElt1.css('background', 'gray')
    
    $('.pwd1').on('input', (e) => {
        let inputElt = e.target
        
        if(inputElt.value.length < 4) {
            $(inputElt).css({
                'border': '2px solid red'
            })
            $('.pwd1-error').show()
            btnElt1.show()
            btnElt2.hide()
        }
        else if ($('.pwd2').val().length >= 1) {
            if (($('.pwd1').val() !== $('.pwd2').val())) {
                $('.pwd2-error').show();
                btnElt1.show()
                btnElt2.hide()   
            } else {
                $('.pwd2-error').hide();
                btnElt1.hide()
                btnElt2.show()               
            }
        }
        else{
            $(inputElt).css({
                'border': '1px solid gray'
            })
            $('.pwd1-error').hide()

            $('.pwd2').on('input', (e) => {
                if ( e.target.value !== $('.pwd1').val() ){
                    $('.pwd2-error').show();
                    btnElt1.show()
                    btnElt2.hide()
                }else{
                    $('.pwd2-error').hide();
                    btnElt1.hide()
                    btnElt2.show()
                }
            })
        }
    });
});