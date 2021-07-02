const main = () => { 
    //script utils for global project
    let globalUtilsLink = "/static/js/utils.js";
    $.getScript(globalUtilsLink)
    .done((script, textStatus) => {
        //dialog init
        dialogEvent();
        
        /**Hide message alert with timeout */
        hideElementWithTimeOut($(".top-alerts"), 4000);
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
        console.error(`Can't found ${linkAppStore}`);
    });

    //===============================================
    //script for dashboard
    const linkAppDashboard = '/static/dashboard/js/dashboard.js';
    $.getScript(linkAppDashboard)
        .done((script, textStatus) => {
            console.log(`${linkAppDashboard} succesfull loaded`);
        })
        .fail((jqxhr, settings, exception) => {
            console.error(`Can't found ${linkAppDashboard}`);
        })
}

$(() => {
    main();
})