const output = document.getElementById("output");

// Get user input from the form
function getInputValues() {
    return {
        id: document.getElementById("itemId").value,
        name: document.getElementById("itemName").value,
        description: document.getElementById("itemDesc").value
    };
}

// Function to send a request to the FastAPI backend
async function sendRequest(url, method, data = null) {
    let options = { method, headers: { "Content-Type": "application/json" } };
    
    if (data) {
        options.body = JSON.stringify(data); // Convert JavaScript object to JSON
    }

    try {
        let response = await fetch(url, options);
        let result = await response.json();
        output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}

// CRUD Operations
function createItem() {
    let { id, name, description } = getInputValues();
    if (!id || !name || !description) {
        alert("Please fill all fields!");
        return;
    }
    sendRequest(`/items/${id}`, "POST", { name, description });
}

function getItems() {
    sendRequest("/items", "GET");
}

function updateItem() {
    let { id, name, description } = getInputValues();
    if (!id || !name || !description) {
        alert("Please fill all fields!");
        return;
    }
    sendRequest(`/items/${id}`, "PUT", { name, description });
}

function patchItem() {
    let { id, description } = getInputValues();
    if (!id || !description) {
        alert("Please provide ID and new description!");
        return;
    }
    sendRequest(`/items/${id}`, "PATCH", { description });
}

function deleteItem() {
    let { id } = getInputValues();
    if (!id) {
        alert("Please enter an ID to delete!");
        return;
    }
    sendRequest(`/items/${id}`, "DELETE");
}
