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

  $("#add-org-form").validate({
    rules: {
      organization_name: {
        required: true,
      },
      organization_address: {
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
      organization_name: {
        required: "Organization Name is required.",
      },
      organization_address: {
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

  var form = $("#add-org-form");
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
      // $(".steps ul li.first").addClass("disabled");

      if (currentIndex === 1 && newIndex === 2) {
       
        let valid = true;
        $("#org_contact_info tbody tr").each(function () {
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
          if (emailField.val().trim() !== "") {
            // validate only if not empty
            if (!isValidEmail(emailField.val().trim())) {
              emailField.css("border", "2px solid red");
              valid = false;
            } else {
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
        } else {
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
        var policyName = $(this).find("input.policyName");
        if (policyName.val().trim() === "") {
          policyName.css("border", "2px solid red");
          valid = false;
        } else {
          policyName.css("border", "");
        }
        // var policyType = $(this).find("select.policyType");
        // if (policyType.val() === "") {
        //   policyType.css("border", "2px solid red");
        //   valid = false;
        // } else {
        //   policyType.css("border", "");
        // }
        // var policyMode = $(this).find("select.policyMode");
        // if (policyMode.val() === "") {
        //   policyMode.css("border", "2px solid red");
        //   valid = false;
        // } else {
        //   policyMode.css("border", "");
        // }
        var insurerValue= $(this).find("select.InsurerField");
        if (insurerValue.val() === "") {
          insurerValue.css("border", "2px solid red");
          insurerValue.focus();
          valid = false;
        } else {
          insurerValue.css("border", "");
        }

        
      });

      return valid;

      // form.validate().settings.ignore = ":disabled";
      // return form.valid();
    },
    onFinished: function (event, currentIndex) {
      let formData = new FormData();
      $("#contract-section .contract-info").not('.single-entry-form').each(
        function (index) {
          let contract_no = $(this).find("#contract_no_" + index).text().trim()
          console.log(contract_no)
          formData.append("contract_no_" + index, contract_no);
          $(this).find('input[name],textarea[name], select[name]').each(function () {
          let name = $(this).attr("name");
          let value = $(this).val();
          console.log($(this).attr("type"));
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
            formData.append(name, value);
          }
          })
        }
      );
      let organization_id = $("#organization_id").val();
      formData.append("organization", organization_id);
      $.ajax({
        url: "/b2bmanagement/create-organization-policy/",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: "POST",
        data: formData,
        contentType: false,
        processData: false,
        success: function (resp) {
          if (resp.success) {
            window.location.replace("/b2bmanagement/b2b-organization-list/");
          }
        },
        error: function () {
          alert("Error");
        },
      });
    },
  });

  $("#org_contact_info").on("input change", "input, select", function (e) {
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
  $(document).on("change", ".InsurerField", function (e) {
    e.preventDefault();
    let id =$(this).val()
    var input =$(this).closest(".row").find(".insurerCode")  
    $.ajax({
      url: "/b2bmanagement/insurer-details/"+id+'/',
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      type: "GET",
      success: function (resp) {
        if (resp.success) {
          input.val(resp?.data?.insurer_code); 
        }
      },
      error: function () {
        alert("Error");
      },
    });
  });
  $(document).on("click", ".saveContinue", function (e) {
    e.preventDefault();   
    let currentPlanDiv = $(this).closest(".plan-row:visible");
    let isValid = validateForm()
    // // currentPlanDiv.addClass("d-none");

    // // let nextPlanDiv = currentPlanDiv.next(".plan-row");
    // let isValid = validateForm()
    //       //  if(isValid){
                saveCurrentPlan(currentPlanDiv, function (success) {
                    currentPlanDiv.addClass("d-none");
                    let nextPlanDiv = currentPlanDiv.next(".plan-row");
                    if (nextPlanDiv.length) {
                        nextPlanDiv.removeClass("d-none");
                          $.toast({
                            heading: "Sucessfully",
                            text: "Plan saved successfully",
                            showHideTransition: "slide",
                            icon: "success",
                            loaderBg: "#f96868",
                            position: "top-right",
                          });
                    } else {
                        $.toast({
                          heading: "Sucessfully",
                          text: "All plans completed!",
                          showHideTransition: "slide",
                          icon: "success",
                          loaderBg: "#f96868",
                          position: "top-right",
                        });
                        if (nextPlanDiv.length) {
                          nextPlanDiv.removeClass("d-none");
                        }

                    }
                });
    //       //  }

     
    
  });

  $(document).on("input", ".coverageAmount, .premiumRate, .premiumAmount, .insuredBeneficiary", function(e) {
    e.preventDefault(); 
    var $el = $(this);
    // For inputs: check non-empty
    if ($el.is("input") && $el.val().trim() !== "") {
      $el.css("border", "");
    }
    let row = $(this).closest("tr");    
    let coverage = parseFloat(row.find(".coverageAmount").val()) || 0;
    let rate = parseFloat(row.find(".premiumRate").val()) || 0;
    let premium = parseFloat(row.find(".premiumAmount").val()) || 0;
    let beneficiary = parseFloat(row.find(".insuredBeneficiary").val()) || 0;

    // If premium rate changes → calculate premium amount
    if ($(this).hasClass("premiumRate") || $(this).hasClass("coverageAmount")) {
      if (coverage > 0 && rate > 0) {
          premium = coverage * (rate/100);
          row.find(".premiumAmount").val(premium.toFixed(2));
          if (row.find(".premiumAmount").is("input") && row.find(".premiumAmount").val().trim() !== "") {
            row.find(".premiumAmount").css("border", "");
          }
      }
    }

    // If premium amount changes → calculate premium rate
    if ($(this).hasClass("premiumAmount") && coverage > 0) {
        rate = (premium / coverage) * 100;
        row.find(".premiumRate").val(rate.toFixed(2));
        if (row.find(".premiumRate").is("input") && row.find(".premiumRate").val().trim() !== "") {
          row.find(".premiumRate").css("border", "");
        }
    }
    // Calculate total = premium * beneficiary
    let total = premium * beneficiary;
    row.find(".total").val(total.toFixed(2));
    // --- Gross Total Calculation ---
    let grossTotal = 0;
    $(this).closest(".contract-info").find(".total").each(function() {
        grossTotal += parseFloat($(this).val()) || 0;
    });
    let $contract = $(this).closest(".contract-info"); // current contract
    $contract.find(".grossTotal").val(grossTotal.toFixed(2)); 
  });

  // Save & Exit click
  $(document).on("click", ".saveExit", function (e) {
    e.preventDefault();   
    let currentPlanDiv = $(this).closest(".plan-row:visible");
    let isValid = validateForm()
    // currentPlanDiv.addClass("d-none");
    // if(isValid){
          saveCurrentPlan(currentPlanDiv, function (success) {

              $.toast({
                heading: "Suucessfully",
                text: "Plan saved successfully",
                showHideTransition: "slide",
                icon: "success",
                loaderBg: "#f96868",
                position: "top-right",
              });
              currentPlanDiv.addClass("d-none");
            

          });
    //  }     
  });
  $(document).on('click', '.saveSingleEntry', function (e) {
    let currentDiv=$(this).closest('.contract-info')
    let currentIndex=currentDiv.attr('data-index')
    let contract_no =$('#contract_no_'+currentIndex).text()
    let org_id =$('#organization_id').val()
    let formData = new FormData();
    formData.append('organization', org_id);
    formData.append('org_contract_id', contract_no);
    currentDiv.find(".single-entry-form:visible").find("input[name],textarea[name], select[name]").each(
      function () {
        let name = $(this).attr("name");
        let value = $(this).val();
        console.log(name,value)
        formData.append(name, value);
      }
    );
    $.ajax({
      url: "/claim/employee/",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function (resp) {
        $("#loader").hide();

        if (resp.success) {
          $.toast({
            heading: "Success",
            text:  resp?.message,
            showHideTransition: "slide",
            icon: "success",
            loaderBg: "#f96868",
            position: "top-right",
          });
          currentDiv.find('input[name],textarea[name], select[name]').val('')
        } else {
          $.toast({
            heading: "Warning",
            text: resp?.message,
            showHideTransition: "slide",
            icon: "warning",
            loaderBg: "#f96868",
            position: "top-right",
          });
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
          console.log("Unexpected error:", xhr.responseText);
        }
        $("#loader").hide();
        $.toast({
          heading: "Warning",
          text:  "Data didn't save",
          showHideTransition: "slide",
          icon: "warning",
          loaderBg: "#f96868",
          position: "top-right",
        });
      },
    });
    // find('input[type="text"], input[type="number"], textarea, select').val('');
  });
  function validateForm(){
    let valid = true
    var organization = $('#company-plan-form').find("select#organization");
      if (organization.val() === "") {
        organization.css("border", "2px solid red");
        valid = false;
      } else {
        organization.css("border", "");
      }
    $(".companyPlan tbody tr:visible").each(function () {

      var policyType = $(this).find("select.policyType");
      if (policyType.val() === "") {
        policyType.css("border", "2px solid red");
        valid = false;
      } else {
        policyType.css("border", "");
      }
      var coverageType = $(this).find("select.coverageType");
      if (coverageType.val() === "") {
        coverageType.css("border", "2px solid red");
        valid = false;
      } else {
        coverageType.css("border", "");
      }
      var coverageAmount = $(this).find("input.coverageAmount");
      if (coverageAmount.val() === "") {
        coverageAmount.css("border", "2px solid red");
        valid = false;
      } else {
        coverageAmount.css("border", "");
      }
    var premiumRate = $(this).find("input.premiumRate");
      if (premiumRate.val() === "") {
        premiumRate.css("border", "2px solid red");
        valid = false;
      } else {
        premiumRate.css("border", "");
      }
      var premiumAmount = $(this).find("input.premiumAmount");
      if (premiumAmount.val() === "") {
        premiumAmount.css("border", "2px solid red");
        valid = false;
      } else {
        premiumAmount.css("border", "");
      }
      var insuredBeneficiary = $(this).find("input.insuredBeneficiary");
      if (insuredBeneficiary.val() === "") {
        insuredBeneficiary.css("border", "2px solid red");
        valid = false;
      } else {
        insuredBeneficiary.css("border", "");
      }
    });
    return valid
  }


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

    $("#org_contact_info tbody tr").each(function (index) {
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
      url: "/b2bmanagement/create-new-organization/",
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
            text: "Data saved successfully",
            showHideTransition: "slide",
            icon: "success",
            loaderBg: "#f96868",
            position: "top-right",
          });
          $("#organization_id").val(resp?.data?.organization?.id);
          $("#contract_no_0").html(resp?.data?.organization?.organization_code+'-A');
        } else {
          callback(false);
          $(".actions a[href='#next']").hide();
          $(".actions ul").append(
            '<li aria-hidden="false" id="customSaveBtn" aria-disabled="false"><a href="#next" role="menuitem">Save and Continue</a></li>'
          );
        }
      },
      error: function (xhr) {
        $("#loader").hide();
        try {
          let res = JSON.parse(xhr?.responseText);
          let errorMsg = res?.message;
            try {
                let match = errorMsg.match(/\{(.+)\}/); // get the content inside {}
                if (match) {
                    let objStr = "{" + match[1] + "}";
                    // Convert single quotes to double quotes for JSON parsing
                    objStr = objStr.replace(/'/g, '"');
                    let errorsObj = JSON.parse(objStr);

                    // Combine all error messages
                    let messages = [];
                    for (let field in errorsObj) {
                        messages.push(field + ": " + errorsObj[field].map(e => e.string || e).join(", "));
                    }
                    errorMsg = messages.join(" | ");
                }
            } catch(e) {
                console.log("Error parsing message", e);
            }
            let match = errorMsg.match(/ErrorDetail\(string='(.+?)'/);

            let newErrorMsg = match ? match[1] : match;
            $.toast({
              heading: "Warning",
              text: newErrorMsg,
              showHideTransition: "slide",
              icon: "warning",
              loaderBg: "#f96868",
              position: "top-right",
            });
          
        } catch (e) {
          $.toast({
            heading: "Warning",
            text:  "Something went wrong.",
            showHideTransition: "slide",
            icon: "warning",
            loaderBg: "#f96868",
            position: "top-right",
          });
          $("#loader").hide();
          callback(false); // ✅ allow next
        
        }

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
  
  function saveCurrentPlan(currentPlanDiv, callback) {
    let currentIndex=currentPlanDiv.closest('.contract-info').attr('data-index')
    let contract_no =$('#contract_no_'+currentIndex).text()
    let planId = currentPlanDiv.data("id");
    let table = currentPlanDiv.closest('.contract-info').find(".companyPlan");
    // Extract the plan name from the <h3>
    let planName = currentPlanDiv.find(".companyPlan thead th:first").text().replace("Plan - ", "").trim();
    // collect all input values
    let formData = new FormData();
    formData.append("plan", planId);
    formData.append("plan_type_name", planName);
    formData.append("company_plan_id", $('#company_plan_id_'+currentIndex).val());
    formData.append("contract_no", contract_no);
    formData.append("organization", $('#organization_id').val());
    let fileInput = $("tbody tr:visible").find("input[type='file']")[0];
    if (fileInput && fileInput.files.length > 0) {
        let file = fileInput.files[0]; // single file
        console.log("Selected file:", file.name);
        formData.append("upload_document_file", file);
    }
    table.find("tbody tr:visible").each(function (index) {
      let policy_type = $(this).find('select[name="product_type[]"]').val();
      if(policy_type){
      let coverage_type = $(this).find('select[name="coverage_type[]"]').val();
      let coverage_amount = $(this).find('input[name="coverage_amount[]"]').val();
      let premium_rate = $(this).find('input[name="premium_rate[]"]').val();
      let premium_amount = $(this).find('input[name="premium_amount[]"]').val();
      let insured_beneficiary_no = $(this).find('input[name="insured_beneficiary_no[]"]').val();
      let total = $(this).find('input[name="total[]"]').val();
        
      formData.append(`policy_type[${index}]`, policy_type);
      formData.append(`coverage_type[${index}]`, coverage_type);
      formData.append(`coverage_amount[${index}]`, coverage_amount);
      formData.append(`premium_rate[${index}]`, premium_rate);
      formData.append(`premium_amount[${index}]`, premium_amount);
      formData.append(`insured_beneficiary_no[${index}]`, insured_beneficiary_no);
      formData.append(`total[${index}]`, total);
  
      }
    
         
    });
       
    $.ajax({
      type: "POST",
      url: "/b2bmanagement/company-plan-create/", // your API endpoint
      data: formData,
      processData: false,
      contentType: false,
      headers: {//<==
        "X-CSRFTOKEN": getCookie("csrftoken")//<==
      },
      processData: false,
      success: function (response) {
          if(response.success){
              $('#company_plan_id_'+currentIndex).val(response?.data?.id)
              if (callback) callback(); // callback to handle next step
          }
      },
      error: function () {
        $.toast({
          heading: "Warning",
          text: "Data didn't saved successfully",
          showHideTransition: "slide",
          icon: "warning",
          loaderBg: "#f96868",
          position: "top-right",
        });
      }
  });
  }

})(jQuery);
