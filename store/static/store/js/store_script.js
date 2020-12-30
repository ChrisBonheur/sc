$(function(){
    /****Responsive***** */
    let window_wdth = $(window).width();
    
    /**For the const position tags */
    const const_position = () =>{
        let avatar_width = $('.info-user img').width();
        let article_img_width_min = $('.list-article .card-img-top').width();
        let article_img_width = $('.detail_page .article .img_art').width();

        $('.info-user img').height(avatar_width)

        /**Setting height for article image */
        $('.list-article .card-img-top').height(article_img_width_min + (article_img_width_min / 4));
        $('.detail_page .user-articles .card-img-top').height(article_img_width_min + (article_img_width_min / 4));

    }

    /**Normal css without media */
    const_position();

    /********LIST ARTICLE */
    /**************style css */
    $('.card').css({
        'border': '0px'
    });

    /***DETAIL PAGE ***/
    /*show image*/
    $('.btn-img').on('click', (e) => {
        e.preventDefault();
        $('#show_img').show();
        $('.b_h').hide();
        
        // show img selected in #show_img
        let link_img = $(this).attr('id');
        console.log(link_img);

        $('#show_img .img_in').css({
            'background': `url('${link_img}') no-repeat center`,
            'background-size': 'contain'
        });
    });
    $('.x-circle img').on('click', () =>{
        $('#show_img').hide();
        $('.b_h').show();
    });

    
    
    /****************************************************************************** */
    /***SELL PAGE */
    let file_nbr = 0;
    const action_pics_add = () => {
        let browse = document.createElement('input')
        $(browse).attr({
            'type': 'file',
            'name': `file${file_nbr}`,
            'class': 'img_article'
        });
        $('.rowBloc1 .btn-list').append(browse);
        $(browse).hide()
        $(browse).click();

        let cancelButton = document.createElement('p')
        $(cancelButton).text('x');
        $(cancelButton).css({
            'cursor': 'pointer',
            'background': 'white',
            'width': '35px',
            'height': '35px',
            'color': 'black',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'border': '1px solid black',
            'border-radius': '50%',
            'position': 'relative',
            'top': '0%',
            'left': '70%'
        })

        $('.img_article').change(function(event){
            let url = URL.createObjectURL(event.target.files[0]);
            let divElt = document.createElement('div');

            $(divElt).attr({
                'class': 'col-2',
            }).css({
                'height': '180px',
                'background': `gray url("${url}") no-repeat center center`,
                'background-size': 'contain',
            });

            if (window_wdth <= 768){
                $(divElt).css({
                    'height': "70px",
                });

                $(cancelButton).css({
                    'width': '15px',
                    'height': '15px'
                })
            }

            $(divElt).append(cancelButton);
            // $(divElt).append(img);
            $('.upload_pics').append(divElt);

            $(cancelButton).on('click', () => {
                $(divElt).remove();
                file_nbr--;
                console.log(file_nbr)
            })
        }); 
    }
    
    /*action click on btn add pics**/
    let count_click = 0; //to count nber of click in button
    $('.add-pics-btn').on('click', () => {
        if (file_nbr < 6){
            action_pics_add();
            $('.sell_page .alert').text('');
            /*incremente file_nbr*/
            file_nbr++
        }else{
            $('.sell_page .alert').text('Vous ne pouvez ajouter plus de 6 photos');
        }

        count_click++;
        $('#count_click').val(count_click);
        console.log($('#count_click').val())
    });

});

