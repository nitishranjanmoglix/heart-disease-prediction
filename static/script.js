async function sendPredictionRequest() {
    if (!validateForm()) {
        return;
    }
    // Get values from form inputs
    const age = document.getElementById('age').value;
    const sex = document.querySelector('input[name="sex"]:checked').value;
    const cp = document.getElementById('cp').value;
    const trestbps = document.getElementById('trestbps').value;
    const chol = document.getElementById('chol').value;
    const fbs = document.querySelector('input[name="fbs"]:checked').value;
    const restecg = document.getElementById('restecg').value;
    const thalach = document.getElementById('thalach').value;
    const exang = document.querySelector('input[name="exang"]:checked').value;
    const oldpeak = document.getElementById('oldpeak').value;
    const slope = document.getElementById('slope').value;
    const ca = document.getElementById('ca').value;
    const thal = document.getElementById('thal').value;

    // Create the JSON payload
    const payload = {
        age: parseInt(age),
        sex: parseInt(sex),
        cp: parseInt(cp),
        trestbps: parseInt(trestbps),
        chol: parseInt(chol),
        fbs: parseInt(fbs),
        restecg: parseInt(restecg),
        thalach: parseInt(thalach),
        exang: parseInt(exang),
        oldpeak: parseFloat(oldpeak),
        slope: parseInt(slope),
        ca: parseInt(ca),
        thal: parseInt(thal)
    };

    try {
        fetch('http://4.156.132.129:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(result => {
            if (result.prediction == 'true') {
                document.getElementById('result').innerText = 'The patient is likely to have heart disease';
            } else {
                document.getElementById('result').innerText = 'The patient is not likely to have heart disease';
            }
        });

    } catch (error) {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    }
}

function validateForm() {
    const age = parseInt(document.getElementById('age').value, 10);
    const trestbps = parseInt(document.getElementById('trestbps').value, 10);
    const chol = parseInt(document.getElementById('chol').value, 10);
    const thalach = parseInt(document.getElementById('thalach').value, 10);
    const oldpeak = parseFloat(document.getElementById('oldpeak').value);

    let valid = true;
    let errorMessage = '';

    // Validate Age
    if (isNaN(age) || age < 0 || age > 120) {
        valid = false;
        errorMessage += 'Age must be between 0 and 120.\n';
    }

    // Validate Resting Blood Pressure
    if (isNaN(trestbps) || trestbps < 50 || trestbps > 200) {
        valid = false;
        errorMessage += 'Resting blood pressure must be between 50 and 200.\n';
    }

    // Validate Cholesterol
    if (isNaN(chol) || chol < 100 || chol > 600) {
        valid = false;
        errorMessage += 'Cholesterol level must be between 100 and 600.\n';
    }

    // Validate Maximum Heart Rate
    if (isNaN(thalach) || thalach < 50 || thalach > 220) {
        valid = false;
        errorMessage += 'Maximum heart rate must be between 50 and 220.\n';
    }

    // Validate ST Depression
    if (isNaN(oldpeak) || oldpeak < 0 || oldpeak > 10) {
        valid = false;
        errorMessage += 'ST depression must be between 0 and 10.\n';
    }

    if (!valid) {
        alert(errorMessage);
    }

    return valid;
}
