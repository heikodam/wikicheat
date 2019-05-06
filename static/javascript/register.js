$("#register-btn").click(function(){
    console.log("function called");
    if(!$("#full_name").val()){
        console.log("in if")
        $("#form-error-msg").html("Please enter your full name");
    } 
    // check if gender
    else if (!$("input[name='gender']:checked").val()){
        $("#form-error-msg").html("Please Select a gender");
    } 
    
    else if (!$("#email").val()){
        $("#form-error-msg").html("Please enter your email");
    } 
    
    else if (!$("#password").val()){
        $("#form-error-msg").html("Please enter password");
    } 
    
    else if (!$("#confirm_password").val()){
        $("#form-error-msg").html("Please confirm your password");
    }

    else if ($("#confirm_password").val() != $("#password").val()){
        $("#form-error-msg").html("The Passwords you enterd do not match");
    }

    else if (!$("input[name='data_protection']:checked").val()){
        $("#form-error-msg").html("Please accept our conditions");
    }

    else {
        $("#form-error-msg").html("");
        $('form#registration-form').submit();
    }
});