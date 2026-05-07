async function login() {

  const username =
    document.getElementById("username").value;

  const password =
    document.getElementById("password").value;

  const resultBox =
    document.getElementById("result");

  // Empty Check
  if (username.trim() === "" || password.trim() === "") {

    resultBox.innerHTML =
      "⚠️ Please enter username and password.";

    return;
  }

  // Loading
  resultBox.innerHTML =
    "Logging in...";

  try {

    const response = await fetch(
      "https://8000-firebase-citizen-1778126565129.cluster-m7dwy2bmizezqukxkuxd55k5ka.cloudworkstations.dev/login",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          username: username,
          password: password
        })
      }
    );

    const data = await response.json();

    if (data.status === "success") {
      window.location.href = "index.html";
    }

    else {
      resultBox.innerHTML = data.message;
    }

  }

  catch (error) {

    console.log(error);

    resultBox.innerHTML =
      "❌ Backend connection failed.";

  }

}