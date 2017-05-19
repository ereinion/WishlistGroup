// ADD SLIDEDOWN ANIMATION TO DROPDOWN //
    $('.dropdown').on('show.bs.dropdown', function(e){
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
        $('.caret').addClass('rotate');
    });
    
    // ADD SLIDEUP ANIMATION TO DROPDOWN //
    $('.dropdown').on('hide.bs.dropdown', function(e){
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
        $('.caret').removeClass('rotate');
        $('.caret').css("transition", "0.7s");
        //document.getElementById("alert").innerHTML = '';
    });
    
    $(document).ready(function(){
       $("#one").show();
       $("#two").hide();
    });
    
    $( "#regClick" ).click(function() {
        
        $('#one').slideUp(500, function(){
            var div = $("#one").hide();
            $("#one").replaceWith(div);
            $('#two').slideDown(500);
            document.getElementById("alert").innerHTML = '';
        });
    });
        
    $('#dropDown .dropdown-menu').on({
        "click":function(e){
            e.stopPropagation();
         }
    });
        
    $( "#logClick" ).click(function() {
        
        $('#two').slideUp(500, function(){
            var div = $("#two").hide();
            $("#two").replaceWith(div);
            $('#one').slideDown(500);
        });
    });
    
    $(document).click(function(){
        window.setTimeout(function(){
            $("#one").show();
            $("#two").hide();
        }, '300');
    });
    
    $(document).ready(function(){
        $(".inputs").hide();
        $(".outputs").show();
    });
          
    $( "#push" ).click(function() {
        if ( $('.inputs').css('display') == 'none' )
        {
          $('.inputs').css('display','block');
          $('.outputs').css('display','none');
          $('.outputsbtn').css('display','none');
        }
        else
        {
          $('.inputs').css('display','none');
          $('.outputs').css('display','block');
          $('.outputsbtn').css('display','inline-block');
        }
    });
          
    $( "#profilebutton" ).click(function() {
        $('.inputs').css('display','none');
        $('.outputs').css('display','block');
        $('.outputsbtn').css('display','inline-block');
    });
    
    $( "#push" ).click(function() {
        $('.inputs input').val('');
    });
    
    $( "#sub" ).click(function() {
        $('.inputs').css('display','none');
        $('.outputs').css('display','block');
        $('.outputsbtn').css('display','inline-block');
    });