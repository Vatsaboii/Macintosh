const URL = "http://127.0.0.1:5000/api";

function togglePassword(inputId) {
    const inputField = document.getElementById(inputId);
    const passwordToggle = document.querySelector(`#${inputId} + .password-toggle`);

    if (inputField.type === "password") {
        inputField.type = "text";
        passwordToggle.textContent = "Hide";
    } else {
        inputField.type = "password";
        passwordToggle.textContent = "Show";
    }
}

document.getElementById("signupform").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("signupUsername").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const confirmPassword = document.getElementById("signupConfirmPassword").value;
    const terms = document.getElementById("signupTerms").checked;
    const messageElement = document.getElementById("message");

    // Clear previous messages
    messageElement.textContent = "";

    if (password !== confirmPassword) {
        messageElement.textContent = "Passwords do not match!";
        messageElement.style.color = "red";
        return;
    }

    if (!terms) {
        messageElement.textContent = "You must agree to the terms and conditions!";
        messageElement.style.color = "red";
        return;
    }

    const jsonData = {
        username: `${username}`,
        password: `${password}`,
    };

    const response = await fetch(`${URL}/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
    });

    const data = await response.json();

    if (response.code == 200) {
        localStorage.setItem("email", email);
        messageElement.textContent = "Signup successful!";
        messageElement.style.color = "green";
    } else {
        messageElement.textContent = `${data["message"]}`;
        messageElement.style.color = "red";
    }
});
