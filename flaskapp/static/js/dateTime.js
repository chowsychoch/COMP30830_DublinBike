//date time picker by default 
//https://github.com/datejs/Datejs/wiki/Format-Specifiers
$(document).ready(function() {

    $('input[name="daterange"]').daterangepicker({
        timePicker: true,
        timePicker24Hour:true,
        singleDatePicker:true,
        autoUpdateInput: true,
        locale: {
            cancelLabel: 'Clear'
        }
    });
  
    $('input[name="daterange"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY HH:mm'));
        console.log(picker.startDate.format('MM/DD/YYYY HH:mm'))
    });
  
    $('input[name="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
  
  });
