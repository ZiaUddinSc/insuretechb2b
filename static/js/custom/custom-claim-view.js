$(document).ready(function () {
  const path = window.location.pathname;
  const parts = path.split("/");
  const id = parts[3];
  $("#claim-id").val(id);
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.9.179/pdf.worker.min.js";

  const canvas = document.getElementById("pdfCanvas");
  const ctx = canvas.getContext("2d");
  const scale = 1.5;
  let pdfDoc = null;
  let pageNum = 1;

  // Render PDF page function
  function renderPage(num) {
    pdfDoc.getPage(num).then((page) => {
      const viewport = page.getViewport({ scale: scale });
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      const renderContext = {
        canvasContext: ctx,
        viewport: viewport,
      };
      page.render(renderContext);
    });
  }

  function capitalizeFirstChar(str) {
    if (!str) return ""; // handle empty or null strings
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Load PDF function
  function loadPdf(url) {
    const lowerUrl = url.toLowerCase();
    const canvas = document.getElementById("pdfCanvas");
    const img = document.getElementById("imgViewer");
    if (lowerUrl.endsWith(".pdf")) {
      // PDF load
      canvas.style.display = "block";
      img.style.display = "none";
      pdfjsLib
        .getDocument(url)
        .promise.then((pdfDoc_) => {
          pdfDoc = pdfDoc_;
          pageNum = 1;
          renderPage(pageNum);
        })
        .catch((err) => {
          alert("Error loading PDF: " + err.message);
        });
    } else if (lowerUrl.match(/\.(jpg|jpeg|png|gif)$/)) {
      // Image load
      canvas.style.display = "none";
      img.src = url;
      img.style.display = "block";
    } else {
      alert("Unsupported file type: " + url);
    }
  }

  // Populate PDF list (replace this with AJAX call to your backend API)
  function loadPdfList(data) {
    const tbody = $("#pdfTable tbody");
    tbody.empty();
    if (data.length === 0) {
      tbody.append('<tr><td colspan="3">No Files found..</td></tr>');
      return;
    }
    data.forEach((pdf) => {
      const row = `
      <tr>
      <td>${pdf.document_type_display}</td>
        <td>
        <button type="button" class="btn btn-primary btn-rounded btn-fw viewPdfBtn" data-url="${pdf.document}">View</button>
        </td>
        <td> <a  href="${pdf.document}" download> 
        <button type="button" class="btn btn-primary btn-rounded btn-fw">Download</button>
        </a>
       
        </td>
       
        </td>
      </tr>`;
      tbody.append(row);
    });
  }

  $(
    ".natural_death_view,.accidental_death,.permanent_total_disability,.health_opd,.health_ipd,.health_maternity,.health_daycare,.health_opd_dental,.health_critical_illness"
  ).hide();

  $.ajax({
    url: "/claim/claim-details/" + id + "/",
    success: function (response) {
      data_status = "";
      if (response.file_status_display == "PENDING") {
        $("#claim-status").html(
          '<label class="badge badge-danger badge-pill">PENDING</label>'
        );
      } else if (response?.file_status_display === "Approved") {
        $("#claim-status").html(
          '<label class="badge badge-warning badge-pill">' +
            response?.file_status_display +
            "</label>"
        );
      } else {
        $("#claim-status").html(
          '<label class="badge badge-warning badge-pill">' +
            response?.file_status_display +
            "</label>"
        );
      }
      $("#member_id").text(response?.employee?.member_id);
      $("#member_name").text(response?.employee?.member_name);
      $("#bank_name").text(response?.bank?.name);
      $("#product_claim").text(response?.product?.name);
      $("#policy_type").text(response?.policy?.name);
      $.each(response, function (key, value) {
        $("#" + key).text(value);
      });
      $.each(response, function (key, value) {
        $("." + key).text(value);
      });
      if (
        response?.product?.name === "Life" &&
        response?.policy?.name === "Natural Death"
      ) {
        $("#nd_death_date").text(
          moment(response.death_date).format("DD-MM-YYYY")
        );
        $(".natural_death_view").show();
      } else if (
        response?.product?.name === "Life" &&
        response?.policy?.name === "Accidental Death"
      ) {
        $(".accidental_death").show();
      } else if (
        response?.product?.name === "Life" &&
        (response?.policy?.name === "Permanent Total Disability" ||
          response?.policy?.name === "Partial Disability")
      ) {
        $("#ptd_incident_date").text(
          moment(response.incident_date).format("DD-MM-YYYY")
        );
        $(".permanent_total_disability").show();
      } else if (
        response?.product?.name === "Health" &&
        response?.policy?.name === "Health - OPD"
      ) {
        $("#opd_treatement_date").text(
          moment(response.date_of_treatment).format("DD-MM-YYYY")
        );
        $(".health_opd").show();
      } else if (
        response?.product?.name === "Health" &&
        response?.policy?.name === "Health - IPD"
      ) {
        $("#ipd_date_of_admission").text(
          moment(response.date_of_admission).format("DD-MM-YYYY")
        );
        $("#ipd_date_of_dischargee").text(
          moment(response.date_of_discharge).format("DD-MM-YYYY")
        );
        $(".health_ipd").show();
      } else if (
        response?.product?.name === "Health" &&
        response?.policy?.name === "Health - Maternity"
      ) {
        $("#hm_date_of_admission").text(
          moment(response.date_of_admission).format("DD-MM-YYYY")
        );
        $("#hm_date_of_dischargee").text(
          moment(response.date_of_discharge).format("DD-MM-YYYY")
        );
        $(".health_maternity").show();
      } else if (
        response?.product?.name === "Health" &&
        response?.policy?.name === "Health - Daycare"
      ) {
        $("#hdc_date_of_admission").text(
          moment(response.date_of_admission).format("DD-MM-YYYY")
        );
        $("#hdc_date_of_dischargee").text(
          moment(response.date_of_discharge).format("DD-MM-YYYY")
        );
        $(".health_daycare").show();
      } else if (
        response?.product?.name === "Health" &&
        (response?.policy?.name === "Health - OPD-Optical" ||
          response?.policy?.name === "Health - OPD-Dental")
      ) {
        $("#hopd_date_of_treatment").text(
          moment(response.date_of_treatment).format("DD-MM-YYYY")
        );
        $(".health_opd_dental").show();
      } else {
        $("#hci_date_of_admission").text(
          moment(response.date_of_admission).format("DD-MM-YYYY")
        );
        $("#hci_date_of_dischargee").text(
          moment(response.date_of_discharge).format("DD-MM-YYYY")
        );
        $(".health_critical_illness").show();
      }

      let documents = response?.documents;
      loadPdfList(documents);
      // Open modal and load PDF on button click
      $(document).on("click", ".viewPdfBtn", function () {
        const url = $(this).data("url");
        $("#pdfModal").show();
        loadPdf(url);
      });
      // Close modal
      $("#closeModal").click(function () {
        $("#pdfModal").hide();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      });

      const tbody = $("#file-history tbody");
      tbody.empty(); // clear existing rows
      response.claim_history.forEach((item) => {
        // Create a table row

        const sender = item.sender
          ? capitalizeFirstChar(item.sender.username)
          : "N/A";
        const receiver = item.receiver
          ? capitalizeFirstChar(item.receiver.username)
          : "Not Received Yet";
        const sent_at = item.sent_at
          ? moment(item.sent_at).format("MMMM Do, YYYY h:mm A")
          : "Not Sent";
        const received = item.received_at
          ? moment(item.received_at).format("MMMM Do, YYYY h:mm A")
          : "N/A";
        const status = item?.status_display ?? "N/A";
        const remarks = item.remarks ? item.remarks : "N/A";
        const currentgroup = item.group ? item.group.name : "N/A";
        const row = `<tr>
          <td>${sender}</td>
          <td>${receiver}</td>
          <td>${sent_at}</td>
          <td>${received}</td>
          <td>${status}</td>
          <td>${currentgroup}</td>
          <td>${remarks}</td>

        </tr>`;
        tbody.append(row);
      });
    },
  });
});


$("#insurer_claim_officer_view").on("input", ".ok-update", function () {
  const row = $(this).closest("tr");
  const val = $(this).val().trim().toLowerCase();
  if (val === "update") {
    
    // Enable input fields in this row
      row.find(".supervisor_settled, .remarks_claim_supervisor").prop("readonly", false);
        row.find(".supervisor_settled").focus();

    // Autofocus
    row.find(".supervisor_settled").focus();
    row
    .find(".supervisor_settled, .remarks_claim_supervisor")
    .prop("disabled", false)
    .val("");
  } 
  
  else if (val === "ok") {
    const claimSettled = parseFloat(row.find(".claims_operation_settled").text()).toFixed(2) || "0.0";
    const claimDeduction = parseFloat(row.find(".deduction_amount").text()).toFixed(2) || "0.0";
    const claimRemarks = row.find(".supervisor-remarks").text().trim() || "";
    row.find(".supervisor_settled").val(claimSettled);
     row.find(".claim_supervisor_deduction").text(claimDeduction);
    row.find(".remarks_claim_supervisor").val(claimRemarks);
    row
      .find(".supervisor_settled, .remarks_claim_supervisor")
      .prop("disabled", true)
  } 
  
  else {
    // Disable inputs
    row
      .find(".supervisor_settled, .remarks_claim_supervisor")
      .prop("disabled", true)
      .val("");
  }
});


// When user types in OK/Update input
$(".ok-update").on("input", function () {
  const row = $(this).closest("tr");
  const val = $(this).val().trim().toLowerCase();

  if (val === "update") {
    // Enable input fields in this row
    row
      .find(".audit-settled, .audit-remarks, .claim-remarks")
      .prop("disabled", false)
      .removeAttr("disabled");

    // Autofocus to Audit Settled for easier data entry
    row.find(".audit-settled").focus();
  }else if(val === "ok"){
    const claimSettled = parseFloat(row.find(".claim_supervisor_settled").text()).toFixed(2) || "0.0";
    const claimDeduction = parseFloat(row.find(".claim_supervisor_deduction").text()).toFixed(2) || "0.0";
    const claim_remarks = row.find(".claim-remarks").text().trim() || "";
    // Set into audit fields
    row.find(".audit-settled").val(claimSettled);
    row.find(".audit-deduction").text(claimDeduction)
    row.find(".audit-remarks").val(claim_remarks)
  } 
  else {
    // Disable all inputs if not 'update'
    row
      .find(".audit-settled, .audit-remarks, .claim-remarks")
      .prop("disabled", true)
      .val("");
  }
});

// When typing in Audit Settled input
$(".audit-settled").on("input", function () {
  const row = $(this).closest("tr");
  const claimAmount = parseFloat(row.find(".claim_supervisor_settled").text().trim()) || 0;
  const settledAmount = parseFloat($(this).val()) || 0;
  // Check if settled > claim
  if (settledAmount > claimAmount) {
    alert("❌ Settled amount cannot be greater than the claimed amount!");
    $(this).val(claimAmount);
  }

  // Calculate deduction = claim - settled
  const deduction = claimAmount - (parseFloat($(this).val()) || 0);

  // Update the deduction cell
  row.find(".audit-deduction").text(deduction.toFixed(2));
});

function calculateTotals() {
  let totalSettled = 0;
  let totalClaimed = 0;
  $(".remarks").prop("disabled", true);
  let discountBDT = parseFloat($('.discount_bdt').last().text().trim()) || 0;
  $("#insurer_claim_officer_view tbody tr").each(function () {
    const claimed = parseFloat($(this).find(".claim_amount").text()) || 0;
    const settledInput = $(this).find(".setteled_amount");
    let settled = parseFloat(settledInput.val()) || 0;
    const deductionCell = $(this).find(".deduction_amount");
    const remarksField = $(this).find(".remarks");

    if ($(this).find(".claim_amount").length === 0) return; // skip header or total rows

    // 🔴 Prevent Settled > Claimed
    if (settled > claimed) {
      alert("⚠️ Settled amount cannot be greater than claimed amount.");
      settled = claimed;
      settledInput.val(settled.toFixed(2));
    }

    // Calculate deduction
    const deduction = claimed - settled;
    deductionCell.text(!isNaN(deduction) ? deduction.toFixed(2) : "");

    // Make remarks mandatory if settled < claimed
    // Enable remarks only if settled < claimed
    // Enable remarks only when deduction exists
    if (settled < claimed && settled > 0) {
      remarksField.prop("disabled", false);
      remarksField.attr("required", true);

      // Only highlight if remarks empty
      if (remarksField.val().trim() === "") {
        remarksField.css("border", "2px solid red");
      }
    } else {
      // Reset if not required
      remarksField.prop("disabled", true);
      remarksField.removeAttr("required");
      remarksField.css("border", "");
      remarksField.val("");
    }
    // Accumulate totals
    totalClaimed += claimed;
    totalSettled += settled;
  });
  let finalTotal = totalSettled - discountBDT;

  // Prevent negative value
  finalTotal = finalTotal < 0 ? 0 : finalTotal;
  // Update total settled amount
  $(".settled_total_amount").text(finalTotal.toFixed(2));
  $(document).on("input", ".remarks", function () {
    if ($(this).val().trim() !== "") {
      $(this).css("border", ""); // remove red border
    } else {
      $(this).css("border", "2px solid red"); // show again if cleared
    }
  });
  // Optional: update total deduction if needed
  const totalDeduction = totalClaimed - totalSettled;
  $(".total_deduction").text(totalDeduction.toFixed(2));
}

function calculateSuperVisorTotals() {
  let totalSettled = 0;
  let totalClaimed = 0;
  $(".remarks").prop("disabled", true);
  $("#insurer_claim_officer_view tbody tr").each(function () {
    const claimed = parseFloat($(this).find(".claims_operation_settled").text()) || 0;
    const settledInput = $(this).find(".supervisor_settled");
    let settled = parseFloat(settledInput.val()) || 0;
    const deductionCell = $(this).find(".claim_supervisor_deduction");
    const remarksField = $(this).find(".remarks");

    // if ($(this).find(".claims_operation_settled").length === 0) return; // skip header or total rows

    // 🔴 Prevent Settled > Claimed
    if (settled > claimed) {
      alert("⚠️ Settled amount cannot be greater than settled amount.");
      settled = claimed;
      settledInput.val(settled.toFixed(2));
    }

    // Calculate deduction
    const deduction = claimed - settled;
    deductionCell.text(!isNaN(deduction) ? deduction.toFixed(2) : "");

    // Make remarks mandatory if settled < claimed
    // Enable remarks only if settled < claimed
    // Enable remarks only when deduction exists
    if (settled < claimed && settled > 0) {
      remarksField.prop("disabled", false);
      remarksField.attr("required", true);

      // Only highlight if remarks empty
      if (remarksField.val().trim() === "") {
        remarksField.css("border", "2px solid red");
      }
    } else {
      // Reset if not required
      remarksField.prop("disabled", true);
      remarksField.removeAttr("required");
      remarksField.css("border", "");
      remarksField.val("");
    }
    // Accumulate totals
    totalClaimed += claimed;
    totalSettled += settled;
  });

  // Update total settled amount
  $(".settled_total_amount").text(totalSettled.toFixed(2));
  $(document).on("input", ".remarks", function () {
    if ($(this).val().trim() !== "") {
      $(this).css("border", ""); // remove red border
    } else {
      $(this).css("border", "2px solid red"); // show again if cleared
    }
  });
  // Optional: update total deduction if needed
  const totalDeduction = totalClaimed - totalSettled;
  $(".total_deduction").text(totalDeduction.toFixed(2));
}

$(document).on("input", ".setteled_amount", function () {
  calculateTotals();
});

// Trigger calculation on settled amount change
$(document).on("input", ".supervisor_settled", function () {
  // calculateSuperVisorTotals();
  const row = $(this).closest("tr");
  const claimAmount = parseFloat(row.find(".claims_operation_settled").text().trim()) || 0;
  const settledAmount = parseFloat($(this).val()) || 0;

  // Check if settled > claim
  if (settledAmount > claimAmount) {
    alert("❌ Settled amount cannot be greater than the claimed setteled amount!");
    $(this).val(claimAmount);
  }

  // Calculate deduction = claim - settled
  const deduction = claimAmount - (parseFloat($(this).val()) || 0);

  // Update the deduction cell
  row.find(".claim_supervisor_deduction").text(deduction.toFixed(2));
});

// Initial calculation
// calculateTotals();
$(document).ready(function(){
  $(".remarks").prop("disabled", true);

})
const csrftoken = getCookie("csrftoken");


$("#claim_submit_form").validate({
  
  rules: {
    status: {
      required: true,
    }
  },
  messages: {
    status: {
      required: "Please Select Status",
    },
  },
  submitHandler: function (form) {
    let items=[]
    let hasError = false; // flag to detect validation error
    let allowedStatuses = ["1"];
    let status = $("#file-status-status").val();
    if(allowedStatuses.includes(status)){

    if ($('#insurer_claim_officer_view').length){  
        $("#insurer_claim_officer_view tbody tr").each(function() {
      const item_name = $(this).find('.item_name').text().trim();
      if(item_name!==''){
       const claimed_amount = parseFloat($(this).find(".claim_amount").text()) || 0;
      let currency_amount
      let currencyEl = $(this).find(".currency_amount");
      if (currencyEl.length === 0) {
        // .currency_amount class NOT found → use claimed_amount
        currency_amount = claimed_amount;
    } else {
        // .currency_amount exists → parse the value
        currency_amount = parseFloat(currencyEl.text()) || 0;
    }
      var $td =$(this).find('.claims_operation_settled')
      var $input = $td.find('.setteled_amount');
      const settled_amount = $.trim($input.val()) !== "" ? $.trim($input.val())  : $.trim($td.text());          // use input value: $.trim($td.text());  
      const deduction = parseFloat($(this).find(".deduction_amount").text()) || 0;
      const supervisor_settled = parseFloat($(this).find(".supervisor_settled").val()) || 0;
      
      const claim_supervisor_deduction = parseFloat($(this).find(".claim_supervisor_deduction").text()) || 0;
      const remarksInput = $(this).find(".remarks");
      const remarks = remarksInput.val() ? remarksInput.val().trim() : "";
      const supervisorremarksInput = $(this).find(".remarks_claim_supervisor");
      const supervisorremarks = supervisorremarksInput.val() ? supervisorremarksInput.val().trim() : "";
      const isRemarksEnabled = !remarksInput.prop("disabled"); // check if remarks field is enabled
      
    if(supervisor_settled === 0 && claim_supervisor_deduction === 0){
    // Check remarks if enabled but empty
        if (isRemarksEnabled && remarks === "") {
          remarksInput.css("border", "2px solid red");
          alert("Please fill remarks for item: " + item_name);
          remarksInput.focus();
          hasError = true;
          return false; // stop loop immediately
        } else {
          remarksInput.css("border", ""); // remove red border if valid
        }
    }
    
      // Skip empty or invalid rows
      if (item_name && claimed_amount > 0) {
        items.push({
          item_name: item_name,
          currency_amount:currency_amount || 0,
          claimed_amount: claimed_amount || 0,
          settled_amount: settled_amount || 0,
          claim_supervisor_deduction:claim_supervisor_deduction || 0,
          claim_supervisor_settled:supervisor_settled || 0,
          deduction: deduction ||0,
          remarks: remarks || '',
          remarks_claim_supervisor:supervisorremarks || ''
        });
       }
      }
        });
    }
    if ($('#insurer_audit_officer_table').length){  
      $("#insurer_audit_officer_table tbody tr").each(function() {
      const item_name = $(this).find('.item_name').text().trim();

        if(item_name!==''){
        const claimed_amount = parseFloat($(this).find(".claim-amount").text()) || 0;

        let currency_amount
        let currencyEl = $(this).find(".currency_amount");
        if (currencyEl.length === 0) {
          // .currency_amount class NOT found → use claimed_amount
          currency_amount = claimed_amount;
      } else {
          // .currency_amount exists → parse the value
          currency_amount = parseFloat(currencyEl.text()) || 0;
      }
        const settled_amount = parseFloat($(this).find(".claims-settled").text()) || 0;
        const deduction = parseFloat($(this).find(".deduction_amount").text()) || 0;
        const audit_settled = parseFloat($(this).find(".audit-settled").val()) || 0;
        
        const audit_deduction = parseFloat($(this).find(".audit-deduction").text()) || 0;
        const claim_remarks = parseFloat($(this).find(".claim-remarks").text()) || 0;
        const supervisor_settled = parseFloat($(this).find(".claim_supervisor_settled").text()) || 0;
        const claim_supervisor_deduction = parseFloat($(this).find(".claim_supervisor_deduction").text()) || 0;
        const remarksInput = $(this).find(".audit-remarks");
        const remarks = remarksInput.val() ? remarksInput.val().trim() : "";
        const isRemarksEnabled = !remarksInput.prop("disabled"); // check if remarks field is enabled

      // Check remarks if enabled but empty
      if (isRemarksEnabled && remarks === "") {
        remarksInput.css("border", "2px solid red");
        alert("Please fill remarks for item: " + item_name);
        remarksInput.focus();
        hasError = true;
        return false; // stop loop immediately
      } else {
        remarksInput.css("border", ""); // remove red border if valid
      }
        // Skip empty or invalid rows
        if (item_name && claimed_amount > 0) {
          items.push({
            item_name: item_name,
            currency_amount:currency_amount || 0,
            claimed_amount: claimed_amount || 0,
            settled_amount: settled_amount || 0,
            deduction: deduction || 0,
            audit_deduction:audit_deduction || 0,
            audit_settled:audit_settled || 0,
            claim_supervisor_deduction:claim_supervisor_deduction|| 0,
            claim_supervisor_settled:supervisor_settled || 0,
            audit_remarks: remarks || '',
            claim_remarks: claim_remarks || ''
          });
          
        }
        }
      });
    }

    if ($('#insurer_claim_officer_view').length || $('#insurer_audit_officer_table').length){
      if (hasError) {
        return false;
      }
    }
  }
    
    // console.log(items)
    let formData = new FormData();
   
    let remarks = $("#remarks").val();
    let id = $("#claim-id").val();
    formData.append("status", status);
    formData.append("remarks", remarks);
    formData.append("id", id);
    formData.append("cost_items", JSON.stringify(items) );
    if($('.document-upload-section').length){
      $(".document-row").each(function (index) {
        // Append text, textarea, select
        let titleVal = $(this).find('select[name="documentType[]"]').val();
        let fileInput = $(this).find('input[name="documentFile[]"]')[0];

        formData.append(`documentType[${index}]`, titleVal);

        if (fileInput.files.length > 0) {
          formData.append(`documentFile[${index}]`, fileInput.files[0]);
        }
      });
  }
    
    $("#loader").show();
    // for (let pair of formData.entries()) {
    //   console.log(pair[0] + ':', pair[1]);
    // }
    $.ajax({
      url: "/claim/update-claim-status/", // Django API endpoint
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        "X-CSRFToken": csrftoken,
      },
      processData: false,
      success: function (response) {
       if(response.success){
        $("#loader").hide();
        window.location.replace('/claim/received-claim-list/')
       }else{
        $("#loader").hide();
        alert("Not updated")
       }
      },
      error: function (xhr) {
        $("#loader").hide();
      },
      complete: function () {
        $("#loader").hide();
      },
    });
  }
});

// Optionally handle item click
$(document).on("click", ".suggest-item", function () {
  $("#beneficiary-search").val($(this).text());
  const member_name = $(this).data("name");
  const member_id = $(this).data("id");
  $("#beneficiary_name").val(member_name);
  $("#suggestions").attr("data-beneficiary", member_id);
})

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
