const fields = [
    'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
    'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
];

window.onload = () => {
    const inputsDiv = document.getElementById('inputs');
    fields.forEach(field => {
        const labelText = field.replace(/_/g, ' ');
        const html = `
            <label for="${field}">${labelText}</label>
            <input type="number" name="${field}" step="any" required>
        `;
        inputsDiv.insertAdjacentHTML('beforeend', html);
    });

    document.getElementById('wineForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        const messageDiv = document.getElementById('message');
        const resultDiv = document.getElementById('result');
        const categoryDiv = document.getElementById('category');

        if (!messageDiv || !resultDiv || !categoryDiv) {
            console.error("One or more output elements (message/result/category) not found in the DOM.");
            return;
        }

        messageDiv.innerText = "Please wait while we predict the wine quality... 🍷";
        resultDiv.innerText = "";
        categoryDiv.innerText = "";

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            messageDiv.innerText = "";

            if (result.quality !== undefined) {
                resultDiv.innerText = `Predicted Wine Quality: ${result.quality}`;
                categoryDiv.innerText = `Category: ${result.category}`;
            } else {
                resultDiv.innerText = `Error: ${result.error}`;
            }
        } catch (error) {
            messageDiv.innerText = "Something went wrong. Please try again.";
            console.error("Prediction error:", error);
        }
    });
};
