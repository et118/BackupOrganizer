async function handleErrors(response) {
    const result = await response.json()
    document.getElementById("status").innerHTML = "";
    Object.entries(result["errors"]).forEach(([key, value]) => {
        const div = document.createElement("div");
        div.innerText = key + ": " + value;
        document.getElementById("status").appendChild(div);
    });
}
