document.getElementById("predictForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const resultEl = document.getElementById("result");
  resultEl.innerText = "Predicting...";

  const data = {
    age: parseInt(document.getElementById("age").value),
    workclass: document.getElementById("workclass").value,
    fnlwgt: parseInt(document.getElementById("fnlwgt").value),
    education: document.getElementById("education").value,
    education_num: parseInt(document.getElementById("education_num").value),
    marital_status: document.getElementById("marital_status").value,
    occupation: document.getElementById("occupation").value,
    relationship: document.getElementById("relationship").value,
    race: document.getElementById("race").value,
    sex: document.getElementById("sex").value,
    capital_gain: parseInt(document.getElementById("capital_gain").value),
    capital_loss: parseInt(document.getElementById("capital_loss").value),
    hours_per_week: parseInt(document.getElementById("hours_per_week").value),
    native_country: document.getElementById("native_country").value
  };

  try {
    // Use relative URL — works on both localhost and Render
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.prediction === 1) {
      resultEl.innerHTML = '✅ <b style="color: #00d4bc;">Income: Above 50K</b>';
    } else if (result.prediction === 0) {
      resultEl.innerHTML = '📊 <b style="color: rgb(61, 209, 192);">Income: Under 50K</b>';
    } else {
      resultEl.innerText = "Prediction failed";
    }
  } catch (error) {
    resultEl.innerText = "API connection error: " + error.message;
  }
});
