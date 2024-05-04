<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Motilitycapture</title>
    <style>
      /* Your CSS styles */
    </style>
  </head>
  <body>
    <div class="cam overflow-hidden text-red-900">
      <div>
        <h1>testing</h1>
        <video id="uploadedVideo" class="img-sperm" controls autoplay>
          <source src="" type="video/mp4" class="img-sperm" />
          Your browser does not support the video tag.
        </video>
      </div>
      <div class="capture-side">
        <button id="uploadBtn" class="capture">Upload Video</button>
        <button id="processBtn" class="capture">Process Video</button>
        <div alig="center">
          <!-- Input fields for displaying processed data -->
          <input
            id="total"
            type="number"
            class="capture"
            name="total"
            placeholder="Total Sperms Count"
            readonly
          />
          <input
            id="high_speed"
            type="number"
            class="capture"
            name="a"
            placeholder="High Speed Sperms Count"
            readonly
          />
          <input
            id="medium_speed"
            type="number"
            class="capture"
            name="b"
            placeholder="Medium Speed Sperms Count"
            readonly
          />
          <input
            id="low_speed"
            type="number"
            class="capture"
            name="c"
            placeholder="Low Speed Sperms Count"
            readonly
          />
          <input
            id="dead"
            type="number"
            class="capture"
            name="d"
            placeholder="Dead Sperms Count"
            readonly
          />
        </div>
      </div>
    </div>

    <!-- File input and upload button -->
    <input type="file" id="fileInput" style="display: none" />
    <button id="uploadFileBtn" style="display: none">Upload</button>

    <script>
      // Function to handle file upload
      function handleFileUpload(file) {
        const formData = new FormData();
        formData.append("video", file);

        fetch("http://127.0.0.1:7000/upload", {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Upload failed");
            }
            return response.json();
          })
          .then((data) => {
            console.log("Upload successful:", data);
            // Enable the process button after successful upload
            document.getElementById("processBtn").disabled = false;
            // Set the source of the uploaded video element
            document.getElementById("uploadedVideo").src = data.url;
            alert(data.filename);
            localStorage.setItem("filename", data.filename);
          })
          .catch((error) => {
            console.error("Error uploading file:", error);
          });
      }

      // Function to process the video
      function processVideo() {
        const filename = localStorage.getItem("filename");
        fetch("http://127.0.0.1:7000/process-video", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ filename: filename }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
            // Fill input fields with processed data
            document.getElementById("total").value = data.total;
            document.getElementById("high_speed").value = data.high_speed;
            document.getElementById("medium_speed").value = data.medium_speed;
            document.getElementById("low_speed").value = data.low_speed;
            document.getElementById("dead").value = data.dead;
          })
          .catch((error) => {
            console.error(
              "There was a problem with the fetch operation:",
              error
            );
          });
      }

      // Event listener for file input change
      document
        .getElementById("fileInput")
        .addEventListener("change", (event) => {
          const file = event.target.files[0];
          if (file) {
            handleFileUpload(file);
          }
        });

      // Event listener for upload button click
      document.getElementById("uploadBtn").addEventListener("click", () => {
        document.getElementById("fileInput").click();
      });

      // Event listener for process button click
      document
        .getElementById("processBtn")
        .addEventListener("click", processVideo);
    </script>
  </body>
</html>
