document.getElementById("detect-btn").addEventListener("click", async function() {
    const disease = document.getElementById("disease-type").value;
    const dna = document.getElementById("dna-code").value;

    if (!disease || !dna) {
        alert("yaara code vann disease vann ade vani be kya bemair chess!");
        return;
    }

    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = "<p>🕵️‍♀️ AI Detective is analyzing...</p>";
    resultBox.classList.add("show");

    try {
        const response = await fetch("/detect", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ disease: disease, dna: dna })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.innerHTML = `
                <h3>🩺 Detected: ${data.disease_name}</h3>
                <p><strong>Anomaly:</strong> ${data.anomaly}</p>
                <p><strong>Explanation:</strong> ${data.explanation}</p>
            `;
        } else {
            resultBox.innerHTML = `<p style="color:red">❌ ${data.error}</p>`;
        }
    } catch (error) {
        resultBox.innerHTML = "<p style='color:red'>⚠️ Oops! Server is sleeping or not running.</p>";
    }
});