/*Componnent dialog block*/
const showDialogConfirm = (title, link, text=$('.dialog_confirm .card-text').text()) => {
    $('.dialog_confirm .card-title').text(title);
    $('.dialog_confirm .card-text').text(text);
    $('.dialog_confirm .btn-danger').attr("href", link);
    //show dialog_confirm
    $('.dialog_confirm').removeClass("d-none");
}

/**
 * this function hidde element from DOM with time in ms
 * @param {jquery selection element from DOM} element 
 * @param {set time in ms before element hidden} timeOut 
 */
const hideElementWithTimeOut = (element, timeOut=3000) => {
    setTimeout(() => {
        element.slideUp(1000);
    }, timeOut);
}

/**
 * Show dialog block confirmation on click a link need a confirmation action 
 * before to continue, just add class ".dialog_confirm_before" with hidden span html inside
 * that will contain the warning message*/
const dialogEvent = () => {
    $('.dialog_confirm_before').on("click", (e) => {
        e.preventDefault();
        try {
            title = e.target.children[0].textContent;
            link = e.target.href
            showDialogConfirm(title, link)
        } catch (error) {
            console.error(`Set a hidden span with class "dialog_confirm_before" 
            that contain title of dialog confirmation in currentTarget
            like => <span class="dialog_confirm_before">Deleting article</span>`);
        }

        $('.dialog_confirm .btn-primary').on('click', () => {
            //if cancel, hide dialog confirm
            $('.dialog_confirm').addClass("d-none");
        });
    });
}


//set an active button style
const buttonActiveStyle = () => {
    let currentUrl = $.ajaxSettings.url;

    let links = $('.nav-link').get()
    links.forEach(link => {
        regex = /^http:\/\/127.0.0.1:8000\/gestion/

        if (currentUrl == link.href){
            $(link).addClass('active');
        }else if(regex.test(currentUrl)){
            $('.dashboard-link').addClass('active');
        }
    });
}
