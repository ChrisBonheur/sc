/*Componnent dialog block*/
const showDialogConfirm = (title, link, text=$('.dialog_confirm .card-text').text()) => {
    $('.dialog_confirm .card-title').text(title);
    $('.dialog_confirm .card-text').text(text);
    $('.dialog_confirm .btn-danger').attr("href", link);
    //show dialog_confirm
    $('.dialog_confirm').removeClass("d-none");
}

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

const main = () => { 
    //==============================================
    //script for app store
    const linkAppStore = '/static/store/js/main.js';
    $.getScript(linkAppStore)
    .done((script, textStatus) => {
        //launch main of app store
        mainStore();
    })
    .fail((jqxhr, settings, exception) =>{
        console.error(`Can't find ${linkAppStore}`);
    });

    dialogEvent();
}

$(() => {
    main();
})
