(function ($) {
  "use strict";

  $.validator.addMethod(
    "extension",
    function (value, element, param) {
      param =
        typeof param === "string"
          ? param.replace(/,/g, "|")
          : "png|jpe?g|gif|webp";
      return (
        this.optional(element) ||
        value.match(new RegExp("\\.(" + param + ")$", "i"))
      );
    },
    "Please enter a file with a valid extension."
  );

  // $("#org-wizard-form").validate({
  //   rules: {
  //     organization_code: {
  //       required: true,
  //     },
  //     organization_name: {
  //       required: true,
  //     },
  //     organization_address: {
  //       required: true,
  //     },
  //     website: {
  //       required: true,
  //     },
  //     tin_number: {
  //       required: true,
  //     },
  //     bin_number: {
  //       required: true,
  //     },
  //     status: {
  //       required: true,
  //     },
  //     tin_file: {
  //       required: true, // custom rule
  //       extension: "jpg|jpeg|png|pdf",
  //     },
  //     bin_file: {
  //       required: true,
  //       extension: "jpg|jpeg|png|pdf",
  //     },
  //     bank: {
  //       required: true,
  //     },
  //     branch_name: {
  //       required: true,
  //     },
  //     account_number: {
  //       required: true,
  //     },
  //     account_name: {
  //       required: true,
  //     },
  //     partnership_type: {
  //       required: true,
  //     },
  //     enrollment_date: {
  //       required: true,
  //     },
  //     end_date: {
  //       required: true,
  //     },
  //   },
  //   messages: {
  //       organization_code: {
  //       required: "Organization Code is required.",
  //     },
  //     organization_name: {
  //       required: "Organization Name is required.",
  //     },
  //     organization_address: {
  //       required: "Organization Address is required.",
  //     },
  //     website: {
  //       required: "Website is required.",
  //     },
  //     tin_number: {
  //       required: "Tin Number is required.",
  //     },
  //     bin_number: {
  //       required: "Bin Number is required.",
  //     },
  //     tin_file: {
  //       required: "Tin File is required.",
  //       extension: "Allowed formats: jpg, jpeg, png, gif, webp.",
  //     },
  //     bin_file: {
  //       required: "Bin File is required.",
  //       extension: "Only image files (jpg, jpeg, png) are allowed.",
  //     },
  //     status: {
  //       required: "Status is required.",
  //     },
  //     bank: {
  //       required: "Bank Name is required.",
  //     },
  //     account_name: {
  //       required: "Account Name is required.",
  //     },
  //     account_number: {
  //       required: "Account Number is required.",
  //     },
  //     branch_name: {
  //       required: "Branch Name is required.",
  //     },
  //     partnership_type: {
  //       required: "Partnership type  is required.",
  //     },
  //     enrollment_date: {
  //       required: "Enrollment Date is required.",
  //     },
  //     end_date: {
  //       required: "End date is required.",
  //     },
  //   },
  //   errorPlacement: function (error, element) {
  //     error.insertAfter(element);
  //   },
  // });

  var form = $("#org-wizard-form");
  form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    labels: {
      finish: "Save",
    },
    onStepChanging: function (event, currentIndex, newIndex) {
      // Allow going back without validation
      // if (currentIndex > newIndex) {
      //   return true;
      // }
      // if (currentIndex === 1 && newIndex === 2) {
      //   const rows = $("#organization_contact_info tbody tr");
      //   if (rows.length === 0) {
      //     alert("Please add at least one member.");
      //     return false;
      //   }

      //   let valid = true;

      //   rows.each(function () {
      //     const name = $(this).find("input[name='contact_name[]']");
      //     const designation = $(this).find(
      //       "select[name='contact_designation[]']"
      //     );
      //     const contact_mobile_no = $(this).find(
      //       "input[name='contact_mobile_no[]']"
      //     );
      //     if (!name.val() || !designation.val() || !contact_mobile_no.val()) {
      //       name.addClass("error");
      //       designation.addClass("error");
      //       contact_mobile_no.addClass("error");
      //       valid = false;
      //     } else {
      //       name.removeClass("error");
      //       designation.removeClass("error");
      //       contact_mobile_no.removeClass("error");
      //     }
      //   });

      //   if (!valid) {
      //     alert("All member fields are required.");
      //   }

      //   return valid;
      // }
      // if (currentIndex === 2 && newIndex === 3) {
      //   const isValid = form.valid();
      //   return isValid;
      // }
      // if (currentIndex === 3 && newIndex === 4) {
      //   const isValid = form.valid();
      //   return isValid;
      // }
      // Validate current step fields
      form.validate().settings.ignore = ":disabled,:hidden";
      return form.valid();
    },
    onFinishing: function (event, currentIndex) {
      form.validate().settings.ignore = ":disabled";
      return form.valid();
    },
    onFinished: function (event, currentIndex) {
      let formData = $(this).serialize();
      $.ajax({
        url: '/b2bmanagement/create-new-organization/',
        method: 'POST',
        data: formData,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        processData: false,
        contentType: false,
        success: function(response) {
          // This code runs **when the AJAX request finishes successfully**
          alert('Data submitted successfully!');
          // You can do other things here:
          // - Clear the form
          // - Show a message
          // - Redirect user
        },
        error: function(xhr) {
          alert('Submission failed');
        }
      });
     
      alert("Submitted!");
    },
  });
  // $("#tin_file").on("change", function () {
  //   $(this).valid(); // validate again when file changes
  // });
  // $("#bin_file").on("change", function () {
  //   $(this).valid(); // validate again when file changes
  // });
  // $(document).on("change", 'select[name="contact_designation[]"]', function () {
  //   $(this).valid();
  // });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


})(jQuery);
