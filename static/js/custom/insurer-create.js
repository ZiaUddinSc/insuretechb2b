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

  $("#add-insurer-form").validate({
    rules: {
      insurer_name: {
        required: true,
      },
      address: {
        required: true,
      },
      bank: {
        required: true,
      },
      account_name: {
        required: true,
      },
      account_number: {
        required: true,
      },
      routing_number: {
        digits: true,
        minlength: 9,
        maxlength: 9,
        required: function () {
          return $('input[name="routing_number"]').val().length > 0;
        }
      }
    },
    messages: {
      insurer_name: {
        required: "Insurer Name is required.",
      },
      address: {
        required: "Address is required.",
      },
      bank: {
        required: "Bank Name is required.",
      },
      account_name: {
        required: "Account Name  is required.",
      },
      account_number: {
        required: "Account Number  is required.",
      },
      routing_number: {
        digits: "Only numbers allowed",
        minlength: "Routing number must be exactly 9 digits",
        maxlength: "Routing number must be exactly 9 digits"
      }
    },
    errorPlacement: function (error, element) {
      error.insertAfter(element);
    },
  });

  var form = $("#add-insurer-form");
  form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    labels: {
      finish: "Save",
    },
    onStepChanging: function (event, currentIndex, newIndex) {
      // Allow going back without validation
      if (currentIndex > newIndex) {
        $("#customSaveBtn").remove();
        $(".actions a[href='#next']").show();
        return true;
      }
      
     
      if (currentIndex === 1 && newIndex === 2) {
        let valid = true;
        $("#insure_contact_info tbody tr").each(function () {
          // Name field
          var name = $(this).find("input.nameField");
          if (name.val().trim() === "") {
            name.css("border", "2px solid red");
            valid = false;
          } else {
            name.css("border", "");
          }

          // Mobile
          var mobile = $(this).find("input.mobileField");
          if (
            mobile.val().trim() === "" ||
            !/^\d+$/.test(mobile.val().trim())
          ) {
            mobile.css("border", "2px solid red");
            valid = false;
          } else {
            mobile.css("border", "");
          }
          var emailField = $(this).find("input.emailField");
          if (emailField.val().trim() !== "") {   // validate only if not empty
            if (!isValidEmail(emailField.val().trim())) {
              emailField.css("border", "2px solid red");
              valid = false;
            }else {
              emailField.css("border", "");
            }
          }

        });

        if (valid) {
          $(".actions a[href='#next']").hide();
          $(".actions ul").append(
            '<li aria-hidden="false" id="customSaveBtn" aria-disabled="false"><a href="#next" role="menuitem">Save and Continue</a></li>'
          );
        }
        return valid;
      } else {
        // remove custom button and restore default
        $("#customSaveBtn").remove();
        if (currentIndex === 2 && newIndex === 3) {
          $(".actions a[href='#previous']").hide();
        }else{
            $(".actions a[href='#previous']").show();
        }
        $(".actions a[href='#next']").show();
      }

      form.validate().settings.ignore = ":disabled,:hidden";
      return form.valid();
    },
    onFinishing: function (event, currentIndex) {
      let valid = true;
      $("#contract-section .contract-info").each(function () {
        // Name field
        var contractTitle = $(this).find("input.contractTitle");
        if (contractTitle.val().trim() === "") {
          contractTitle.css("border", "2px solid red");
          valid = false;
        } else {
          contractTitle.css("border", "");
        }
        var policyType = $(this).find("select.policyType");
        if (policyType.val() === "") {
          policyType.css("border", "2px solid red");
          valid = false;
        } else {
          policyType.css("border", "");
        }
        var policyMode = $(this).find("select.policyMode");
        if (policyMode.val() === "") {
          policyMode.css("border", "2px solid red");
          valid = false;
        } else {
          policyMode.css("border", "");
        }
      });

      return valid;

      // form.validate().settings.ignore = ":disabled";
      // return form.valid();
    },
    onFinished: function (event, currentIndex) {
      let formData = new FormData();
      let insurer = $("#insurer_id").val();
      formData.append("insurer", insurer);
    $("#contract-section .contract-info").each(function(idx){
        let $row = $(this);
    
        // 1️⃣ Get the contract number from <p>
        let contractNo = $row.find("p[id^='contract_no_']").text();
        formData.append(`insurer_contract_no[${idx}]`, contractNo);
    
        // 2️⃣ Get all inputs, textareas, selects inside this row
        $row.find("input[name], textarea[name], select[name]").each(function(){
          let name = $(this).attr("name");
          let value = $(this).val();
          if ($(this).attr("type") === "file") {
            // File input
            let files = $(this)[0].files;
            let allowedTypes = ["application/pdf", "image/jpeg", "image/png"]; // allowed MIME types

            for (let i = 0; i < files.length; i++) {
              let file = files[i];
              if (allowedTypes.includes(file.type)) {
                formData.append(name, file);
              } else {
                alert("Invalid file type: " + file.name);
              }
            }
          } else {
            if(name!=='insurer'){
                formData.append(name, value);
            }
          }
        });
    });
      // $("#contract-section input[name],textarea[name], select[name], p[id^='contract_no_']").each(
      //   function(idx) {
      //     let contractNo = $row.find("p[id^='contract_no_']").text();
      //     formData.append(`insurer_contract_no[${idx}]`, contractNo);   
      //     $row.find("input[name], textarea[name], select[name]").each(function(){
      //     let name = $(this).attr("name");
      //     let value = $(this).val();
      //     if ($(this).attr("type") === "file") {
      //       // File input
      //       let files = $(this)[0].files;
      //       let allowedTypes = ["application/pdf", "image/jpeg", "image/png"]; // allowed MIME types

      //       for (let i = 0; i < files.length; i++) {
      //         let file = files[i];
      //         if (allowedTypes.includes(file.type)) {
      //           formData.append(name, file);
      //         } else {
      //           alert("Invalid file type: " + file.name);
      //         }
      //       }
      //     } else {
      //       formData.append(name, value);
      //     }
      //   });
      //   }
      // );

      $.ajax({
        url: "/b2bmanagement/create-insurer-policy/",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (resp) {
          if (resp.success) {
            window.location.replace("/b2bmanagement/insurer-view/");
          }
        },
        error: function () {
          alert("Error");
        },
      });
    },
  });

  $("#insure_contact_info").on("input change", "input, select", function (e) {
    e.preventDefault();
    var $el = $(this);

    // For inputs: check non-empty
    if ($el.is("input") && $el.val().trim() !== "") {
      $el.css("border", "");
    }

    // For selects: check value is not empty
    if ($el.is("select") && $el.val() !== "") {
      $el.css("border", "");
    }
  });
  $("#contract-section").on("input change", "input, select", function (e) {
    e.preventDefault();
    var $el = $(this);

    // For inputs: check non-empty
    if ($el.is("input") && $el.val().trim() !== "") {
      $el.css("border", "");
    }

    // For selects: check value is not empty
    if ($el.is("select") && $el.val() !== "") {
      $el.css("border", "");
    }
  });

  $(document).on("click", "#customSaveBtn", function (e) {
    e.preventDefault();
    const isValid = form.valid();
    if (isValid) {
      submitInsurerData(function (success) {
        if (success) {
          // move wizard forward manually
          form.children("div").steps("next");
        }
        return false;
      });
    }
  });

  function submitInsurerData(callback) {
    let formData = new FormData();
    $("#loader").show();
    $(".company-info-section :input[name],textarea[name], select[name]").each(
      function () {
        let name = $(this).attr("name");
        let value = $(this).val();
        if ($(this).attr("type") === "file") {
          let fileInput = this; // DOM element'
          let allowedTypes = ["application/pdf", "image/jpeg", "image/png"]; // allowed MIME typ
          if (fileInput.files && fileInput.files.length > 0) {
            let file = fileInput.files[0];
            if (!file) return;
            console.log(file.type);
            formData.append($(this).attr("name"), file);
          }
        } else {
          formData.append(name, value);
        }
      }
    );
    $(".bank-info-section :input[name],textarea[name], select[name]").each(
      function () {
        let name = $(this).attr("name");
        let value = $(this).val();
        formData.append(name, value);
      }
    );

    $("#insure_contact_info tbody tr").each(function (index) {
      let row = $(this);

      formData.append(`name[${index}]`, row.find('input[name="name[]"]').val());
      formData.append(
        `designation[${index}]`,
        row.find('select[name="designation[]"]').val()
      );
      formData.append(
        `mobile_no[${index}]`,
        row.find('input[name="mobile_no[]"]').val()
      );
      formData.append(
        `email[${index}]`,
        row.find('input[name="email[]"]').val()
      );
    });
    $(".errors li").remove();
    $.ajax({
      url: "/b2bmanagement/create-insurer/",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function (resp) {
        $("#loader").hide();

        if (resp.success) {
          callback(true); // ✅ allow next
          $.toast({
            heading: "Success",
            text: "Insurer Information has been saved successfully",
            showHideTransition: "slide",
            icon: "success",
            loaderBg: "#f96868",
            position: "top-right",
          });
          $("#insurer_id").val(resp?.data?.insurer?.id);
          $("#contract_no_0").html(resp?.data?.insurer?.insurer_code + "-A");
        } else {
          callback(false);
          $(".actions a[href='#next']").hide();
          $(".actions ul").append(
            '<li aria-hidden="false" id="customSaveBtn" aria-disabled="false"><a href="#next" role="menuitem">Save and Continue</a></li>'
          );
        }
      },
      error: function (xhr) {
        try {
          let res = JSON.parse(xhr?.responseText);
          $("#loader").hide();
          // Show general error message
          // Show field-specific errors
          if (res?.data) {
            Object.keys(res.data).forEach((field) => {
              res.data[field].forEach((msg) => {
                $(".errors").append(
                  `<li  class="li-style" style="color:red;text-transform:capitalize">${msg}</li>`
                );
              });
            });
          }
        } catch (e) {
          $("#loader").hide();
          console.error("Unexpected error:", xhr.responseText);
        }
        $("#loader").hide();
        callback(false); // ✅ allow next
        alert(JSON.stringify(xhr.responseText))
        // $.toast({
        //   heading: "Warning",
        //   text: xhr?.message || "Data didn't save",
        //   showHideTransition: "slide",
        //   icon: "warning",
        //   loaderBg: "#f96868",
        //   position: "top-right",
        // });
      },
    });
  }
  function isValidEmail(email) {
    // simple regex for email
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      let cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
})(jQuery);
