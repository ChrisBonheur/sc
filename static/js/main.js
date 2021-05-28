const main = () => { 
    //script utils for global project
    let globalUtilsLink = "/static/js/utils.js";
    $.getScript(globalUtilsLink)
    .done((script, textStatus) => {
        dialogEvent();
    })
    .fail((jqxhr, settings, exception) => {
        console.error(`Can't find ${globalUtilsLink}`);
    });

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
}

$(() => {
    main();
})