//date time picker by default 
//https://github.com/datejs/Datejs/wiki/Format-Specifiers
$(document).ready(function() {
    console.log("Hey dateTime")

    $('input[name="date"]').daterangepicker({
        timePicker: false,
        // timePicker24Hour:true,
        // singleDatePicker:true,
        autoUpdateInput: true,
        startDate: moment().startOf('hour'),
        endDate: moment().startOf('hour').add(48, 'hour'),
        locale: {
            cancelLabel: 'Clear'
        },
        ranges: {
            '48 hour': [ moment().startOf('hour'), moment().startOf('hour').add(48, 'hour')]
        },
        showCustomRangeLabel:false
    });

    // $('input[name="date"]').on('apply.daterangepicker', function(ev, picker) {
    //     $(this).val(moment().startOf('hour').format('MM/DD/YYYY'),"-",moment().startOf('hour').add(48, 'hour'));
    //     console.log(picker.startDate.format('MM/DD/YYYY HH:mm'))
    // });

    // $('input[name="date"]').on('cancel.daterangepicker', function(ev, picker) {
    //     $(this).val('');
    // });

  });
// $(function () {

//     var start = moment().subtract(29, 'days');
//     var end = moment();

//     function cb(start, end) {
//         $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
//     }

//     $('#reportrange').daterangepicker({
//         startDate: start,
//         endDate: end,
//         ranges: {
//             'Today': [moment(), moment()],
//             'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
//             'Last 7 Days': [moment().subtract(6, 'days'), moment()],
//             'Last 30 Days': [moment().subtract(29, 'days'), moment()],
//             'This Month': [moment().startOf('month'), moment().endOf('month')],
//             'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
//         }
//     }, cb);

//     cb(start, end);

// });