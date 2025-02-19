import { BarcodeDetectorPolyfill } from "https://cdn.jsdelivr.net/npm/@undecaf/barcode-detector-polyfill@0.9.21/dist/main.js";
import { openModal } from "./modal.js";

const successAudio = new Audio("/static/audio/success.mp3");
const errorAudio = new Audio("/static/audio/error.mp3");
const viewElement = document.querySelector(".ticket-scanner__view");

const showResultButton = document.getElementById("show-result-button");
const customerEmailElement = document.getElementById("customer-email");
const customerNameElement = document.getElementById("customer-name");
const customerPostcodeElement = document.getElementById("customer-postcode");
const customerCountryElement = document.getElementById("customer-country");
const ticketPriceElement = document.getElementById("ticket-price");
const discountsUsedElement = document.getElementById("discounts-used");

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
let lastScannedResponse = null;

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
          successAudio.play();
          viewElement.classList.add("ticket-scanner__view--success");
          lastScannedResponse = await res.json();
          showResultButton.disabled = false;
        } else {
          errorAudio.play();
          viewElement.classList.add("ticket-scanner__view--error");
          lastScannedResponse = null;
          showResultButton.disabled = true;
        }

        setTimeout(() => {
          scanning = false;
          viewElement.classList.remove("ticket-scanner__view--error", "ticket-scanner__view--success");
        }, 1000);
      }
    })
    .catch((err) => {
      // Log an error if one happens
      console.error(err);
    });
};

// Run detect code function every 100 milliseconds
setInterval(detectCode, 100);

showResultButton.addEventListener("click", () => {
  if (!lastScannedResponse) {
    return;
  }

  customerEmailElement.textContent = lastScannedResponse.email;
  customerNameElement.textContent = lastScannedResponse.name;
  customerPostcodeElement.textContent = lastScannedResponse.postcode;
  customerCountryElement.textContent = lastScannedResponse.country;
  ticketPriceElement.textContent = lastScannedResponse.price;
  discountsUsedElement.textContent = lastScannedResponse.discount_used || "N/A";

  openModal("scan-result-modal");
});
