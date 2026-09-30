// Site settings, hand-edited and read as-is by app.js (no build step needed).
// A .js file rather than .json so the page still works when opened from disk (file://).
const CONFIG = {
  // Set to false to remove the feedback form at the bottom of the page.
  showFeedbackForm: true,
  // Function URL of the feedback service's submit Lambda (see feedback-service/README.md).
  // Left empty, every submission shows the error toast.
  feedbackEndpoint: "https://gl2ui2iwfv3eabkajpgij6be2y0svcgb.lambda-url.us-east-2.on.aws/",
};
