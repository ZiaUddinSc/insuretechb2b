$(document).ready(function () {

  const csrftoken = getCookie("csrftoken");


  $("#claim-form").validate({
    rules: {
      claim_for: {
        required: true,
      },
      beneficiary_search: {
        required: true,
      },
      beneficiary_name: {
        required: true,
      },
      ClaimType: {
        required: true,
      },
      BeneficiaryType: {
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
      claim_for: {
        required: "Please select Claim For",
      },
      beneficiary_search: {
        required: "Please enter beneficiary ID",
      },
      beneficiary_name: {
        required: "Please enter beneficiary name",
      },
      ClaimType: {
        required: "Please enter claim type",
      },
      BeneficiaryType: {
        required: "Please enter benefit type",
      },
      routing_number: {
        digits: "Only numbers allowed",
        minlength: "Routing number must be exactly 9 digits",
        maxlength: "Routing number must be exactly 9 digits"
      }
    },
    submitHandler: function (form) {
      let employee = $("#suggestions").attr("data-beneficiary");

      let formData = new FormData();
      $("#loader").show();
      formData.append("employee", employee);
      if ($("#section-maternity").is(":visible")) {

        let section = $("#section-maternity");
    
        section.find("input[type!='file'], select, textarea").each(function () {
    
            // Skip disabled inputs EXCEPT total_amount
            if ($(this).is(":disabled") && this.name !== "total_amount") {
                return;
            }
    
            if (this.name) {
                formData.append(this.name, $(this).val());
            }
        });
    
      }else{
        $(".section-visual:visible").each(function () {
          // Append text, textarea, select
          $(this)
            .find('input[type!="file"], select,input, textarea')
            .each(function () {
              if (this.name) {
                formData.append(this.name, this.value);
              }
            });
        });
      }

    
    
    
    
    
    
    
    

   

      $("#section-bank-details").each(function () {
        // Append text, textarea, select
        $(this)
          .find("select,input, textarea")
          .each(function () {
            if (this.name) {
              formData.append(this.name, this.value);
            }
          });
      });
      $(".benificiary-info").each(function () {
        // Append text, textarea, select
        $(this)
          .find("select,input, textarea")
          .each(function () {
            if (this.name) {
              formData.append(this.name, this.value);
            }
          });
      });
      $(".document-row").each(function (index) {
        // Append text, textarea, select
        let titleVal = $(this).find('select[name="documentType[]"]').val();
        let fileInput = $(this).find('input[name="documentFile[]"]')[0];

        formData.append(`documentType[${index}]`, titleVal);

        if (fileInput.files.length > 0) {
          formData.append(`documentFile[${index}]`, fileInput.files[0]);
        }
      });

      $.ajax({
        url: "/claim/create-claim-api/", // Django API endpoint
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        headers: {
          "X-CSRFToken": csrftoken,
        },
        processData: false,
        success: function (response) {
          $("#loader").hide();
          $.toast({
            heading: "Success",
            text: "Data saved successfully",
            showHideTransition: "slide",
            icon: "success",
            loaderBg: "#f96868",
            position: "top-right",
          });
          window.location.href = "/claim/claim-list/";
          $("#claim-submit").prop("disabled", false);
        },
        error: function (xhr) {
          $.toast({
            heading: "Warning",
            text: "failed to save data",
            showHideTransition: "slide",
            icon: "warning",
            loaderBg: "#f96868",
            position: "top-right",
          });
          $("#loader").hide();
          $("#submitBtn").prop("disabled", false);
        },
        complete: function () {
          $("#loader").hide();
        },
      });
    },
  });

  $(document).on("change", ".form-control-file", function () {
    let file = this.files[0];
    if (file) {
      let fileSizeMB = file.size / (1024 * 1024); // size in MB
      if (fileSizeMB > 6) {
        // 5 MB limit
        alert("File is too large! Max 6 MB allowed.");
        $(this).val(""); // clear the input
      } else {
        console.log("File size OK: " + fileSizeMB.toFixed(2) + " MB");
      }
    }
  });



  function calculateVisibleSectionTotal(visibleId) {
    if (!visibleId) return;

    let visibleSection = $('#' + visibleId);
    let total = 0;

    // 1️⃣ Sum all cost_amount inputs (room rent, surgery, etc.)
    visibleSection.find(".cost_amount").each(function () {
        let val = $(this).val().replace(/,/g, '');
        if ($.isNumeric(val)) total += parseFloat(val);
    });

    // 2️⃣ Add "Others" amount if checked (before discount)
    let othersAmount = parseFloat(visibleSection.find("input[name='others']").val()?.replace(/,/g, '') || 0);
    let othersChecked = visibleSection.find(".form-check-input").is(":checked");
    if (othersChecked && !isNaN(othersAmount)) total += othersAmount;

    // 3️⃣ Apply discount percentage
    let discountInput = visibleSection.find("input[name='discount_perchantage']");
    let discountPercentage = parseFloat(discountInput.val() ? discountInput.val().replace(/,/g, '') : 0);
    let discountAmount = 0;
    if (!isNaN(discountPercentage) && discountPercentage > 0) {
        discountAmount = (total * discountPercentage) / 100;
        if (discountAmount > total) {
            alert("Discount cannot be greater than total amount!");
            discountInput.val('0');
            visibleSection.find("input[name='discount']").val('0');
            visibleSection.find("input[name='total_amount']").val(total.toFixed(2));
            return;
        }
        total -= discountAmount;
        visibleSection.find("input[name='discount']").val(discountAmount.toFixed(2));
    } else {
        visibleSection.find("input[name='discount']").val('0');
    }

    // 4️⃣ Prevent negative total
    if (total < 0) total = 0;

    // 5️⃣ Update total_amount input
    visibleSection.find("input[name='total_amount']").val(total.toFixed(2));
}





  
    if($('#section-ipd:visible').length>0){
          $(document).on("input", '#section-ipd:visible .cost_amount,input[name="discount_perchantage"], input[name="others"]', function () {
            // Reformat input as comma-separated
            let val = $(this).val().replace(/,/g, '');
            if ($.isNumeric(val)) {
              $(this).val(val);
            }
            calculateVisibleSectionTotal('section-ipd');
          });
          $(document).on('change', '#section-ipd .form-check-input', function () {
            let section = $(this).closest('.section-visual').attr('id');
            if ($(this).is(':checked')) {
              $('.other-view').show();
            } else {
              $('.other-view').hide();
              // optional: clear others field
              $('#' + section).find("input[name='others']").val('');
            }
            calculateVisibleSectionTotal(section);
          });
    }
    $(document).on("input", '#section-opd:visible .cost_amount,input[name="discount_perchantage"], input[name="others"]', function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-opd');
    });
    $(document).on('change', '#section-opd:visible .form-check-input', function () {
      let section = $(this).closest('.section-visual').attr('id');
      if ($(this).is(':checked')) {
        $('.other-view').show();
      } else {
        $('.other-view').hide();
        // optional: clear others field
        $('#' + section).find("input[name='others']").val('');
      }
      calculateVisibleSectionTotal(section);
    });
   
  
    function calculateMaternityTotal(section) {
      let packageCost = parseFloat(section.find("input[name='package_cost']").val()) || 0;
  
      // Package cost active → ignore everything else
      if (packageCost > 0) {
          section.find("input[name='total_amount']").val(packageCost);
          return;
      }
  
      // Sum all regular cost inputs
      let total = 0;
      section.find(".cost_amount").each(function () {
          let val = parseFloat($(this).val());
          if (!isNaN(val)) total += val;
      });
  
      // Add others if enabled
     // 2️⃣ Add "Others" amount if checked (before discount)
    let othersAmount = parseFloat(section.find("input[name='others']").val()?.replace(/,/g, '') || 0);
    let othersChecked = section.find(".form-check-input").is(":checked");
    if (othersChecked && !isNaN(othersAmount)) total += othersAmount;

    // 3️⃣ Apply discount percentage
    let discountInput = section.find("input[name='discount_perchantage']");
    let discountPercentage = parseFloat(discountInput.val() ? discountInput.val().replace(/,/g, '') : 0);
    let discountAmount = 0;
    if (!isNaN(discountPercentage) && discountPercentage > 0) {
        discountAmount = (total * discountPercentage) / 100;
        if (discountAmount > total) {
            alert("Discount cannot be greater than total amount!");
            discountInput.val('0');
            section.find("input[name='discount']").val('0');
            section.find("input[name='total_amount']").val(total.toFixed(2));
            return;
        }
        total -= discountAmount;
        section.find("input[name='discount']").val(discountAmount.toFixed(2));
    } else {
      section.find("input[name='discount']").val('0');
    }

    // 4️⃣ Prevent negative total
    if (total < 0) total = 0;

    // 5️⃣ Update total_amount input
    section.find("input[name='total_amount']").val(total.toFixed(2));
  }
  
  
  // Package cost logic
  $(document).on("input", "#section-maternity:visible input[name='package_cost']", function () {
      let section = $("#section-maternity");
      let packageCost = $(this).val().trim();
  
      if (packageCost !== "") {
  
          section.find(".cost_amount").not($(this)).prop("disabled", true);
  
          section.find("input[name='is_other_description']").prop("disabled", true);
          section.find(".other-view input").prop("disabled", true);
          section.find(".other-view").hide();
  
          // Disable discount as well
          section.find("input[name='discount_perchantage']").prop("disabled", true);
  
      } else {
  
          section.find(".cost_amount").prop("disabled", false);
  
          section.find("input[name='is_other_description']").prop("disabled", false);
  
          if (section.find("input[name='is_other_description']").is(":checked")) {
              section.find(".other-view").show();
              section.find(".other-view input").prop("disabled", false);
          } else {
              section.find(".other-view").hide();
              section.find(".other-view input").prop("disabled", true);
          }
  
          // Enable discount again
          section.find("input[name='discount_perchantage']").prop("disabled", false);
      }
  
      calculateMaternityTotal(section);
  });
  
  
  // Other inputs recalc
  $(document).on("input", "#section-maternity:visible .cost_amount, #section-maternity input[name='others'], #section-maternity input[name='discount_perchantage']", function () {
      calculateMaternityTotal($("#section-maternity"));
  });
  
  
  // Others checkbox toggle
  $(document).on("change", "#section-maternity:visible input[name='is_other_description']", function () {
      let section = $("#section-maternity");
  
      if ($(this).is(":checked")) {
          section.find(".other-view").show();
          section.find(".other-view input").prop("disabled", false);
      } else {
          section.find(".other-view").hide();
          section.find(".other-view input").prop("disabled", true);
      }
  
      calculateMaternityTotal(section);
  });
  $(document).on("input", '#section-daycare:visible .cost_amount,input[name="discount_perchantage"], input[name="others"]', function () {
    // Reformat input as comma-separated
    let val = $(this).val().replace(/,/g, '');
    if ($.isNumeric(val)) {
      $(this).val(val);
    }
    calculateVisibleSectionTotal('section-daycare');
  });
  $(document).on('change', '#section-daycare:visible .form-check-input', function () {
    let section = $(this).closest('.section-visual').attr('id');
    if ($(this).is(':checked')) {
      $('.other-view').show();
    } else {
      $('.other-view').hide();
      // optional: clear others field
      $('#' + section).find("input[name='others']").val('');
    }
    calculateVisibleSectionTotal(section);
  });
  $(document).on("input", '#section-opd-optical:visible .cost_amount,input[name="discount_perchantage"], input[name="others"]', function () {
    // Reformat input as comma-separated
    let val = $(this).val().replace(/,/g, '');
    if ($.isNumeric(val)) {
      $(this).val(val);
    }
    calculateVisibleSectionTotal('section-opd-optical');
  });
  $(document).on('change', '#section-opd-optical:visible .form-check-input', function () {
    let section = $(this).closest('.section-visual').attr('id');
    if ($(this).is(':checked')) {
      $('.other-view').show();
    } else {
      $('.other-view').hide();
      // optional: clear others field
      $('#' + section).find("input[name='others']").val('');
    }
    calculateVisibleSectionTotal(section);
  });
  $(document).on("input", '#section-opd-dental:visible .cost_amount,input[name="discount_perchantage"], input[name="others"]', function () {
    // Reformat input as comma-separated
    let val = $(this).val().replace(/,/g, '');
    if ($.isNumeric(val)) {
      $(this).val(val);
    }
    calculateVisibleSectionTotal('section-opd-dental');
  });
  $(document).on('change', '#section-opd-dental:visible .form-check-input', function () {
    let section = $(this).closest('.section-visual').attr('id');
    if ($(this).is(':checked')) {
      $('.other-view').show();
    } else {
      $('.other-view').hide();
      // optional: clear others field
      $('#' + section).find("input[name='others']").val('');
    }
    calculateVisibleSectionTotal(section);
  });
  
  
  
    
  
  
    
    // if($('#section-maternity:visible').length>0){
    //   $(document).on("input", "#section-maternity:visible .cost_amount", function () {
    //     // Reformat input as comma-separated
    //     let val = $(this).val().replace(/,/g, '');
    //     if ($.isNumeric(val)) {
    //       $(this).val(val);
    //     }
    //     calculateVisibleSectionTotal('section-maternity');
    //   });
    // }
    // if($('#section-daycare:visible').length>0){
    //   $(document).on("input", "#section-daycare:visible .cost_amount", function () {
    //     // Reformat input as comma-separated
    //     let val = $(this).val().replace(/,/g, '');
    //     if ($.isNumeric(val)) {
    //       $(this).val(val);
    //     }
    //     calculateVisibleSectionTotal('section-daycare');
    //   });
    // }
    // if($('#section-opd-optical:visible').length>0){
    //   $(document).on("input", "#section-opd-optical:visible .cost_amount", function () {
    //     // Reformat input as comma-separated
    //     let val = $(this).val().replace(/,/g, '');
    //     if ($.isNumeric(val)) {
    //       $(this).val(val);
    //     }
    //     calculateVisibleSectionTotal('section-opd-optical');
    //   });
    // }
    // if($('#section-opd-dental:visible').length>0){
    //   $(document).on("input", "#section-opd-dental:visible .cost_amount", function () {
    //     // Reformat input as comma-separated
    //     let val = $(this).val().replace(/,/g, '');
    //     if ($.isNumeric(val)) {
    //       $(this).val(val);
    //     }
    //     calculateVisibleSectionTotal('section-opd-dental');
    //   });
    // }
    function calculateVisibleSectionAccidentalTotal(visibleId) {
      let total = 0;
      if (!visibleId) return;
    
      // Find visible section
      let visibleSection = $('#' + visibleId);
   
      // Get all cost_amount inputs (room rent, surgery, etc.)
      visibleSection.find(".cost_amount").each(function () {
        let val = $(this).val().replace(/,/g, '');
       
        if ($.isNumeric(val)) {
          total += parseFloat(val);
         
        }
      });
    
     
      // Prevent negative totals
      if (total < 0) total = 0;
      // Update total_amount input
      visibleSection.find("input[name='total_amount']").val(total.toFixed(2));
    }
    $(document).on("input", '#section-accidental:visible .cost_amount, input[name="others"]', function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionAccidentalTotal('section-accidental');
    });
    
    $('select[name="currency"]').change(function () {

      if (!$(this).is(':visible')) {
          return; // skip if hidden
      }
  
      let value = $(this).val();
  
      if (value === "BDT" || value === "") {
          $('input[name="exchange_rate"]').prop('readonly', true).val(1);
      } else {
          $('input[name="exchange_rate"]').prop('readonly', false).val('');
      }
  
  });
    
    
    $(document).on("input", "#section-ipd:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-ipd');
    });

    $(document).on("input", "#section-opd:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-opd');
    });
    $(document).on("input", "#section-maternity:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-maternity');
    });

    $(document).on("input", "#section-daycare:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-daycare');
    });
    $(document).on("input", "#section-opd-optical:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-opd-optical');
    });
    $(document).on("input", "#section-opd-optical:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-opd-optical');
    });
    $(document).on("input", "#section-opd-dental:visible .cost_amount", function () {
      // Reformat input as comma-separated
      let val = $(this).val().replace(/,/g, '');
      if ($.isNumeric(val)) {
        $(this).val(val);
      }
      calculateVisibleSectionTotal('section-opd-dental');
    });
  
    $(document).ready(function () {

      const admission = $('input[name="date_of_admission"]');
      const discharge = $('input[name="date_of_discharge"]');
  
      admission.on('change', function () {
          let admissionDate = new Date($(this).val());
  
          // Reset discharge if already selected
          discharge.val('');
  
          // Set minimum date if using datepicker
          if (discharge.hasClass('datepicker')) {
              discharge.datepicker('setStartDate', $(this).val());
          }
      });
  
      discharge.on('change', function () {
          let admissionDate = new Date(admission.val());
          let dischargeDate = new Date($(this).val());
  
          if (dischargeDate < admissionDate) {
              alert('Discharge date cannot be less than admission date!');
              $(this).val('');
          }
      });
  
    });

    // $('input[name="routing_number"]').on('input', function(){
    //   let value = $(this).val().trim();
  
    //   // ✅ If empty, no validation needed
    //   if(value === ''){
    //     $('#routingWarning').addClass('d-none');
    //     $(this).removeClass('is-invalid');
    //     return;
    //   }
  
    //   // ✅ Only validate when user types something
    //   if(value.length !== 9){
    //     $('#routingWarning').removeClass('d-none');
    //     $(this).addClass('is-invalid');
    //   }else{
    //     $('#routingWarning').addClass('d-none');
    //     $(this).removeClass('is-invalid');
    //   }
    // });
   
  
  
    

    
    

  // 👉 Format number with commas
  function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
