document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const titleField = document.getElementById("event_title");
  const dateField = document.getElementById("event_date");
  const descField = document.getElementById("event_description");
  const imageField = document.getElementById("event_image");

  function createErrorElement(field) {
    let errorElem = field.nextElementSibling;
    if (!errorElem || !errorElem.classList.contains("error-message")) {
      errorElem = document.createElement("div");
      errorElem.classList.add("error-message");
      errorElem.style.color = "red";
      errorElem.style.fontSize = "0.9em";
      errorElem.style.marginTop = "4px";
      field.insertAdjacentElement("afterend", errorElem);
    }
    return errorElem;
  }

  const errorTitle = createErrorElement(titleField);
  const errorDate = createErrorElement(dateField);
  const errorDesc = createErrorElement(descField);
  const errorImage = createErrorElement(imageField);

  form.addEventListener("submit", (e) => {
    let valid = true;

    errorTitle.textContent = "";
    errorDate.textContent = "";
    errorDesc.textContent = "";
    errorImage.textContent = "";

    if (titleField.value.trim().length < 3) {
      errorTitle.textContent = "Event title must be at least 3 characters.";
      valid = false;
    }

    if (!dateField.value) {
      errorDate.textContent = "Event date is required.";
      valid = false;
    }

    if (descField.value.trim().length > 0 && descField.value.trim().length < 5) {
      errorDesc.textContent = "Description must be at least 5 characters if provided.";
      valid = false;
    }

    if (imageField.files.length > 0) {
      const file = imageField.files[0];
      if (!file.type.startsWith("image/")) {
        errorImage.textContent = "Uploaded file must be an image.";
        valid = false;
      }
    }

    if (!valid) {
      e.preventDefault();
    }
  });
});
