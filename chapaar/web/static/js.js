/**
 * Created by shahab on 2/3/18.
 */

var check = function() {
      if (document.getElementById('password').value ==
          document.getElementById('againpassword').value &&  document.getElementById('againpassword').value.length !== 0 && document.getElementById('password').value.length !== 0) {

          document.getElementById('password').style.backgroundColor = '#e6ffe6';
          document.getElementById('againpassword').style.backgroundColor = '#e6ffe6';

      } else if(document.getElementById('againpassword').value.length !== 0 && document.getElementById('password').value.length !== 0) {
      		document.getElementById('password').style.backgroundColor = '#ffd6cc';
          document.getElementById('againpassword').style.backgroundColor = '#ffd6cc';
      }
      else{
          document.getElementById('password').style.backgroundColor = 'white';
          document.getElementById('againpassword').style.backgroundColor = 'white';
      }
}



$('#form-signup').on('submit',function (e) {
    e.preventDefault();
    $.ajax({
        url: '/register/',
        cache: false,
        type: 'POST',
        data : $('#form-signup').serialize(),
        success: function(json_obj) {
        alert(json_obj.message);
    }
    });
});


$('.btn').on('click', function() {
    var $this = $(this);
  $this.button('loading');
    setTimeout(function() {
       $this.button('reset');
   }, 2000);
});


$('#form-signin').on('submit',function (e) {
    e.preventDefault();
    $.ajax({
        url: '/login/',
        cache: false,
        type: 'POST',
        data : $('#form-signin').serialize(),
        success: function(json_obj) {

        if (json_obj.response === '200')
        {
            window.location.href  = "";
        }
        else
        {
           alert(json_obj.message);
        }
    }
    });
});






$(document).ready(function() {
                $("#datepicker0").datepicker();

                $("#datepicker1").datepicker({
                    showOtherMonths: true,
                    selectOtherMonths: true,
                    isRTL: true,
                    dateFormat: "yy-m-d"
                });


                $("#datepicker2").datepicker({
                    showOtherMonths: true,
                    selectOtherMonths: true
                });

                $("#datepicker3").datepicker({
                    numberOfMonths: 3,
                    showButtonPanel: true
                });

                $("#datepicker4").datepicker({
                    changeMonth: true,
                    changeYear: true
                });

                $("#datepicker5").datepicker({
                    minDate: 0,
                    maxDate: "+14D"
                });

                $("#datepicker6").datepicker({
                    isRTL: true,
                    dateFormat: "d/m/yy"
                });
            });


$('#ismatching1').click(function() {
    if (document.getElementById('whynot1').readOnly === false)
        document.getElementById('whynot1').readOnly = true;
    else
        document.getElementById('whynot1').readOnly = false;

});


