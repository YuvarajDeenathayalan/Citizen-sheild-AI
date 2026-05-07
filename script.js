async function detectScam() {

  const input =
    document.getElementById("scamInput").value;

  const resultBox =
    document.getElementById("result");

  // Empty Check
  if(input.trim() === "") {

    resultBox.innerHTML =
      "⚠️ Please enter a message.";

    return;
  }

  // Loading
  resultBox.innerHTML =
    "🔍 AI analyzing message...";

  try {

    const response = await fetch(
      "https://8000-firebase-citizen-1778126565129.cluster-m7dwy2bmizezqukxkuxd55k5ka.cloudworkstations.dev/detect-scam",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          message: input
        })
      }
    );

    // Convert Response
    const data = await response.json();

    // Show Result
    resultBox.innerHTML = `
      <h2>${data.risk}</h2>
      <p>Risk Score: ${data.score}%</p>
    `;

  }

  catch(error) {

    console.log(error);

    resultBox.innerHTML =
      "❌ Backend connection failed.";

  }

}