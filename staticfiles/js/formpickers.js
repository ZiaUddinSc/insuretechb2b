(function($) {
  'use strict';
 
  if ($(".color-picker").length) {
    $('.color-picker').asColorPicker();
  }
  if ($(".datepicker").length) {
    $('.datepicker').datepicker({
      enableOnReadonly: true,
      todayHighlight: true,
      format: 'dd-mm-yyyy'
      // autoclose: true
    });
  }
  
})(jQuery);