(function($) {
  'use strict';
 
  if ($(".color-picker").length) {
    $('.color-picker').asColorPicker();
  }
    $('.datepicker').datepicker({
      enableOnReadonly: true,
      todayHighlight: true,
      format: 'dd-mm-yyyy'
      // autoclose: true
    });
  
  
})(jQuery);