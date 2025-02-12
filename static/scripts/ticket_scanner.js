import { BarcodeDetectorPolyfill } from "https://cdn.jsdelivr.net/npm/@undecaf/barcode-detector-polyfill@0.9.21/dist/main.js";

try {
  window["BarcodeDetector"].getSupportedFormats();
} catch {
  window["BarcodeDetector"] = BarcodeDetectorPolyfill;
}

const video = document.getElementById("cameraView");

// Check if device has camera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  // Use video without audio
  const constraints = {
    video: true,
    audio: false,
  };

  // Start video stream
  navigator.mediaDevices.getUserMedia(constraints).then((stream) => (video.srcObject = stream));
}

// Create new barcode detector
const barcodeDetector = new BarcodeDetector({ formats: ["qr_code"] });

let scanning = false;

// Detect code function
const detectCode = () => {
  // Start detecting codes on to the video element
  barcodeDetector
    .detect(video)
    .then(async (codes) => {
      if (scanning) return;

      // If no codes exit function
      if (codes.length === 0) return;

      for (const barcode of codes) {
        // Log the barcode to the console
        const code = barcode.rawValue;
        scanning = true;
        const res = await fetch(`/scan-tickets-api/${code}`, {
          method: "POST",
        });
        if (res.ok) {
          alert(`Scanned in ticket with code ${code}!`);
        } else {
          alert("Failed to scan in ticket!");
        }

        scanning = false;
      }
    })
    .catch((err) => {
      // Log an error if one happens
      console.error(err);
    });
};

// Run detect code function every 100 milliseconds
setInterval(detectCode, 100);
