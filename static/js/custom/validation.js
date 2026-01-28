
$(document).ready(function () {
  $(document).on("change", ".file-upload", function () {
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
});
