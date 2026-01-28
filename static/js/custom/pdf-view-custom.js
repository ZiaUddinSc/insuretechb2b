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
    }else if (lowerUrl.match(/\.(jpg|jpeg|png|gif)$/)) {
        // Image load
        canvas.style.display = "none";
        img.src = url;
        img.style.display = "block";
    } else {
        alert("Unsupported file type: " + url);
    }
  }

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
  
});


