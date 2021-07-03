
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

/**
 * this function verify all operators number selected blocs for same operator
 * if form is valid or no and return boolean
 * @param {object} selectedBlocDiv jquery object selected must contain an input and a span for errors
 * @param {string} operator chosen between : "mtn", "airtel" or "both" default operator
 */
const inputNumberTest = (selectedBlocDiv, operator="both") =>{
    let numbers = selectedBlocDiv.get()
    
    for (const element of numbers) {
        let inputValue = element.children[0].value;
        let spanErrorElt = element.children[1];
        let numberValid = null;
        let regexConform = null;
        //get regex by operator chosen
        if (operator == "mtn"){
            regexConform=/^(242)?06[0-9]{7}$/
        }else if(operator == "airtel"){
            regexConform=/^(242)?05[0-9]{7}$/
        }else if(operator == "both"){
            regexConform=/^(242)?(05|06)[0-9]{7}$/
        }else{
            console.error("Warning: The choice of operator must be 'airtel' or 'mtn'")
            return false
        }
        //verify regex integrity
        if (regexConform.test(inputValue) == false && inputValue != ''){
            $(spanErrorElt).removeClass('d-none');
            numberValid = false;
        }else{
            $(spanErrorElt).addClass("d-none");
            numberValid = true;
        }
        //response if number is invalid
        if (numberValid == false){
            return false
        }
    };

    return true
}

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

    //********************************PROFIL FORM TEST VALIDITY*********************/
    //==============================================================================
    const testAllNumbers = () => {
        let mtnIsValid = inputNumberTest($('.airtel-number'), "airtel");
        let airtelIsValid = inputNumberTest($('.mtn-number'), "mtn");
        let whatsapIsValid = inputNumberTest($('.whatsap-number'));
        if (!mtnIsValid || !airtelIsValid || !whatsapIsValid) {
            $('#save-update-profil-btn').attr('disabled', 'true');
        }else{
            $('#save-update-profil-btn').removeAttr('disabled');
        }
    }

    //Airtel number test
    $('.airtel-number input').on('input', () => {
        testAllNumbers();
    });

    //MTN number test
    $('.mtn-number input').on('input', () => {
        testAllNumbers();
    });

    //whatsap conform number test
    $('.whatsap-number input').on('input', () => {
        testAllNumbers();
    });

    //test all numbers on load page before input event test
    testAllNumbers();

    
    //======================SECURITY================================================================
    //verify new_password and confirm_newpassword input
        //set current password value empty
    $('[name=current_password]').val('');
    let newPassword = $('[name=new_password]')
    let confirmNewPassword = $('[name=confirm_new_password]')
    pswdError = true;
    confirmPswdError = true;
    
    const verifyIfPswdsAreSame = () => {
        let errorPswdText = $('.error-confirm-pswd');
        if (confirmNewPassword.val() != newPassword.val() && confirmNewPassword.val() != ""){
            errorPswdText.text('Les mots de passe diffèrent');
            confirmPswdError = true;
        }else if (confirmNewPassword.val() != newPassword.val() && confirmNewPassword.val() == ""){
            errorPswdText.text('')
            confirmPswdError = true;
        }else{
            errorPswdText.text('')
            confirmPswdError = false;
        }
    }

    //disable button submit for password form
    const makeDisabledBtn = () => {
        if (pswdError || confirmPswdError){
            $('#save-pswd-btn').addClass('disabled');
        }else{
            $('#save-pswd-btn').removeClass('disabled');
        }
    }

    newPassword.on('input', () => {
        let errorPswdText = $('.error-new-pswd');
        if(newPassword.val().length <= 5){
            errorPswdText.text('Mot de passe trop court !');
            pswdError = true;
        }else{
            errorPswdText.text('');
            pswdError = false;
        }
        verifyIfPswdsAreSame();
        makeDisabledBtn();
    });

    confirmNewPassword.on('input', () => {
        verifyIfPswdsAreSame();
        makeDisabledBtn();
    });
}

userMain();