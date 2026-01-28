$(document).ready(function () {
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
      tbody.append('<tr><td colspan="3">No Files found.</td></tr>');
      return;
    }
    data.forEach((pdf) => {
      const row = `
      <tr>
      <td>${pdf?.document_type_display}
      <input type="hidden" name="document_ids" value="${pdf?.document_type}"/>
      <input type="hidden" name="existing_ids" value="${pdf?.id}"/>
      </td>
        <td>
        <button type="button" class="btn btn-primary btn-rounded btn-fw viewPdfBtn" data-url="${pdf.document}">View</button>
        <button type="button" class="btn btn-danger btn-rounded btn-fw claimDocDelete" data-id="${pdf.id}">Delete</button>
        </td>
      </tr>`;
      tbody.append(row);
    });
  }

  const path = window.location.pathname;
  const parts = path.split("/");
  const id = parts[3];
  $("#claim-id").val(id);
  $("#beneficiary-search").on("keyup", function () {
    var query = $(this).val().trim();
    $("#beneficiary_name").val("");
    if (query.length > 1) {
      $.ajax({
        url: "/claim/suggest/",
        data: { term: query },
        success: function (data) {
          if (data.length > 0) {
            let html = "";
            data.forEach((item) => {
              html += `<div class="suggest-item" data-id="${item.id}" data-name="${item.member_name}">${item.member_id}</div>`;
            });
            $("#suggestions").html(html).show();
          } else {
            $("#suggestions").hide(); // No results, hide
          }
        },
      });
    } else {
      $("#suggestions").hide(); // Input too short, hide
    }
  });
  const csrftoken = getCookie("csrftoken");
  // Optionally handle item click
  $(document).on("click", ".suggest-item", function () {
    $("#beneficiary-search").val($(this).text());
    const member_name = $(this).data("name");
    const member_id = $(this).data("id");
    $("#beneficiary_name").val(member_name);
    $("#suggestions").attr("data-beneficiary", member_id);
    $("#suggestions").hide();
  });

  $("#update-claim-form").validate({
    rules: {
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
    },
    messages: {
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
    },
    submitHandler: function (form) {
      let formData = new FormData();
      $("#loader").show();
      let employee = $("#benificiary_id").val();
      let beneficiary_name = $("#beneficiary_name").val();
      formData.append("employee", employee);
      formData.append("beneficiary_name", beneficiary_name);
      formData.append("id", id);
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
        url: "/claim/update-claim-api/",
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
            text: "Data update successfully",
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

  $(document).on("click", ".claimDocDelete", function () {
    const row = $(this).closest("tr");
    const docId = $(this).data("id");
    if (!confirm("Are you sure you want to delete this file?")) {
      return;
    }
    $.ajax({
      url: "/claim/delete-claim-document",
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      data: {
        doc_id: docId,
      },
      success: function (response) {
        if (response.status === "ok") {
          row.remove();
        } else {
          alert("Delete failed");
        }
      },
    });
  });

  $(document).on("change", ".form-control-file", function () {
    let file = this.files[0];
    if (file) {
      let fileSizeMB = file.size / (1024 * 1024); // size in MB
      if (fileSizeMB > 2) {
        // 5 MB limit
        alert("File is too large! Max 2 MB allowed.");
        $(this).val(""); // clear the input
      } else {
        console.log("File size OK: " + fileSizeMB.toFixed(2) + " MB");
      }
    }
  });
  $(window).on("load", function () {
    $.ajax({
      url: "/claim/claim-details/" + id + "/",
      success: function (response) {
        $("#claim_for").val(response?.claim_for)
        $("#beneficiary-search").val(response?.employee?.member_id);
        $("#beneficiary_name").val(response?.employee?.member_name);
        $("#benificiary_id").val(response?.employee?.id);
        $("#ClaimType").val(response?.product?.id);
       
        $('select[name="ClaimType"]').val(response?.product?.id);
        const $select = $('select[name="BeneficiaryType"]')
        $select.empty().append('<option value="">-- Select Benefit Type --</option>')
        let policyId= response?.policy?.id
        $.ajax({
          url: '/b2bproduct/policy-details/?product_id='+response?.product?.id,  // Django URL to fetch policies
          success: function(response){
          let data = response.data
         
          options=`<option value="">-- Select Benefit Type --</option>`
          $.each(data, function(index, policy){
      
            let isSelected = (policy.id == policyId) ? 'selected' : '';
              options += '<option value="' + policy.id + '" ' + isSelected + '>' + policy.name + '</option>';
          });
          $select.html(options);
          $("#BeneficiaryType").trigger("change");
          }
        });
        if (
          response?.product?.name === "Life" &&
          response?.policy?.name === "Natural Death"
        ) {
          $("#BeneficiaryType").val(response?.policy?.name);
          $("#BeneficiaryType").trigger("change");
          var selectElem = $(".section-visual:visible").find(
            'select[name="currency"]'
          );
          selectElem.val(response.currency);
          $(".section-visual:visible").each(function () {
            // Append text, textarea, select
            $(this)
              .find("input")
              .each(function () {
                if (this.name == "total_amount") {
                  $('input[type="number"][name="total_amount"]').val(
                    response[this.name]
                  );
                }
                if (this.name == "death_date") {
                  $('input[type="text"][name="' + this.name + '"]').val(
                    moment(response.death_date).format("DD-MM-YYYY")
                  );
                } else {
                  $('input[type="text"][name="' + this.name + '"]').val(
                    response[this.name]
                  );
                }
              });
          });
        } else if (
          response?.product?.name === "Life" &&
          response?.policy?.name === "Accidental Death"
        ) {
          // $("#BeneficiaryType").val(response?.policy?.name);
          // $("#BeneficiaryType").trigger("change");
          var selectElem = $("#section-accidental").find(
            'select[name="currency"]'
          );
          selectElem.val(response.currency);
          $("#section-accidental").each(function () {
            // Append text, textarea, select
            $(this)
              .find("input")
              .each(function () {
                if (this.name == "total_amount") {
                  $('input[type="number"][name="total_amount"]').val(
                    response[this.name]
                  );
                }
                else {
                  $('input[type="text"][name="' + this.name + '"]').val(
                    response[this.name]
                  );
                }
              });
          });
        } else if (
          response?.product?.name === "Life" &&
          (response?.policy?.name  === "Permanent Total Disability" ||
          response?.policy?.name === "Partial Disability")
        ) {
          $("#BeneficiaryType").val(response?.policy?.name);
          $("#BeneficiaryType").trigger("change");
        } else if (
          response.claim_type === "health" &&
          response.beneficiary_type === "hopd"
        ) {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        } else if (
          response.claim_type === "health" &&
          response.beneficiary_type === "hipd"
        ) {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        } else if (
          response.claim_type === "health" &&
          response.beneficiary_type === "hm"
        ) {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        } else if (
          response.claim_type === "health" &&
          response.beneficiary_type === "hdc"
        ) {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        } else if (
          response.claim_type === "health" &&
          (response.beneficiary_type === "hopdo" ||
            response.beneficiary_type === "hopdd")
        ) {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        } else {
          $("#BeneficiaryType").val(response.beneficiary_type);
          $("#BeneficiaryType").trigger("change");
        }
        var selectBank = $("#section-bank-details").find('select[name="bank"]');
        selectBank.val(response?.bank?.id);
        selectBank.trigger("change");
        $("#section-bank-details").each(function () {
          // Append text, textarea, select
          $(this)
            .find("input")
            .each(function () {
              $('input[type="text"][name="' + this.name + '"]').val(
                response[this.name]
              );
            });
        });

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
      },
    });
  });

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
