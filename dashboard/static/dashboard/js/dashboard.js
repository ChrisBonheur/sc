   /*****DASHBOARD */
//action to click menu-down
$('.down-menu').on('click', () => {
    $('.dash-menu').toggleClass('d-none');
    $('.down-menu').attr('src', () => {
        if ($('.dash-menu').hasClass('d-none')){
            return '/static/node_modules/bootstrap-icons/icons/menu-up.svg'
        }else{
            return '/static/node_modules/bootstrap-icons/icons/menu-down.svg'
        }
    });
});

//==============================================================================================
//Form account mobile money script
//MTN
ValidForm = true;

const verifyNumberIntegrity = (numberValue, ErrorSelectorEltToShow, regexConform=/^(242)?06[0-9]{7}$/) => {
    let regex = regexConform;
    ErrorSelectorEltToShow.addClass("d-none");
    ValidForm = true;

    if (regex.test(numberValue) == false){
        ErrorSelectorEltToShow.removeClass('d-none');
        ValidForm = false;
    }
}

const verifyNumbersSimilar = (numberValue1, numberValue2, ErrorSelectorEltToShow) => {
    ErrorSelectorEltToShow.addClass('d-none');
    ValidForm = true;

    if (numberValue1 != numberValue2){
        ErrorSelectorEltToShow.removeClass('d-none');
        ValidForm = false;
    }
    
    if (numberValue1 == "" && numberValue2 == ""){
        ValidForm = true;
    }
}

const disabledVerification = () => {
    //verify that one of number is given
    let mtnNumber = $('[name=mtn_account_number]').val();
    let mtnConfirm = $('[name=confirm_number_mtn]').val();

    let airtelNumber = $('[name=airtel_account_number]').val();
    let airtelConfirm = $('[name=confirm_number_airtel]').val();
    if ((mtnNumber == "" && mtnConfirm == "") && (airtelNumber == "" && airtelConfirm == "")){
        ValidForm = false
    }

    if (ValidForm){
        $('.valid-number-btn').removeAttr('disabled');
    }else{
        $('.valid-number-btn').attr('disabled', 'true');
    }
}

$('[name=mtn_account_number]').on("input", (e) => {
    verifyNumberIntegrity(e.target.value, $('.error-mtn-number'));

    let valueNumber1 = $('[name=confirm_number_mtn]').val();
    verifyNumbersSimilar(valueNumber1, e.target.value, $('.error-equal-mtn'));
    disabledVerification();
});

$('[name=confirm_number_mtn]').on('input', (e) => {
    let valueNumber1 = $('[name=mtn_account_number]').val();
    verifyNumbersSimilar(valueNumber1, e.target.value, $('.error-equal-mtn'));

    disabledVerification();
});

//AIRTEL
$('[name=airtel_account_number]').on("input", (e) => {
    verifyNumberIntegrity(e.target.value, $('.error-airtel-number'), /^(242)?(05|04)[0-9]{7}$/);

    let valueNumber1 = $('[name=confirm_number_airtel]').val();
    verifyNumbersSimilar(valueNumber1, e.target.value, $('.error-equal-airtel'));

    disabledVerification();

});

$('[name=confirm_number_airtel]').on('input', (e) => {
    let valueNumber1 = $('[name=airtel_account_number]').val();
    verifyNumbersSimilar(valueNumber1, e.target.value, $('.error-equal-airtel'));

    disabledVerification();

});


//=========================================================================================
//Bought Processing script
//change text of label number on event "change"
operatorSelect = "mtn";
$('[name=operator]').on('change', (e) => {
    let radioValue = e.target.value;
    operatorSelect = radioValue;
    if (radioValue == "mtn"){
        $('.label-number').text('Numéro mtn mobile money')
    }else if(radioValue == "airtel"){
        $('.label-number').text('Numéro airtel money')
    }
});

//verification of number integrity
let btnValidNumber = $('#btn-valid-number');
let regex = null;

$('.form-number-input').on('input', () => { 
    if (operatorSelect == "mtn"){
        regex = /^(242)?06[0-9]{7}$/;    
        if (regex.test($('.form-number-input').val())){
            $('.error-operator-number').text('');
            btnValidNumber.removeAttr('disabled')
        }else{
            $('.error-operator-number').text('Numéro MTN non conforme');
            btnValidNumber.attr('disabled', "true");
        }
    }else{
        regex = /^(242)?05[0-9]{7}$/;    
        if (regex.test($('.form-number-input').val())){
            $('.error-operator-number').text('');
            btnValidNumber.removeAttr('disabled')
        }else{
            $('.error-operator-number').text('Numéro Airtel non conforme');
            btnValidNumber.attr('disabled', "true");
        }
    }
})

//=============Active style for current link in dashboard====
let dashLinks = $('.dash-link').get();
let currentLink = $.ajaxSettings.url;

dashLinks.forEach(link => {
    if (currentLink == link.href){
        $(link).addClass('active');
    }
});