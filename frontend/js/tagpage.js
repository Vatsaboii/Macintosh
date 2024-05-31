document.addEventListener("DOMContentLoaded", function () {
    const buttonContainer = document.querySelector(".button-container");
    let translateValue = 0; // Initial translation value

    document.querySelectorAll(".image-button").forEach((button) => {
        button.addEventListener("click", function () {
            // Adjust translate value based on button click
            const buttonWidth = button.offsetWidth + 10; // Width of button + gap
            translateValue += buttonWidth;
            buttonContainer.style.transform = `translateX(-${translateValue}px)`;
        });
    });
});
