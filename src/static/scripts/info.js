const urlParams = new URLSearchParams(window.location.search);
const URL_NAME = urlParams.get("name");

/*---------------API_CALLS--------------------*/

async function getInfo() {
    /*Populates the fields with info from the /Info API endpoint*/
    document.getElementById("collection_name").innerText = URL_NAME;
    const response = await fetch("/api/Info?name=" + URL_NAME);

    if (response.ok) {
        const result = await response.json()
        document.getElementById("name").value = result["info"]["name"];
        document.getElementById("updated").checked = result["info"]["updated"];
        document.getElementById("creation_date").value = result["info"]["creation_date"];
        document.getElementById("modification_date").value = result["info"]["modification_date"];
        document.getElementById("description").value = result["info"]["description"];
        
    } else {
        await handleErrors(response);
    }
}

async function getBackups() {
    /*Fetches all backups for the inspected Collection and populates the 'backup_table' with them*/
    document.getElementById("collection_name").innerText = URL_NAME;
    const response = await fetch("/api/ListBackups?name=" + URL_NAME);
    if (response.ok) {
        const result = await response.json();
        let table = document.getElementById("backup_table");

        Object.entries(result["backup_entries"]).forEach(([name, body]) => {
            let tr = document.createElement("tr");
            
            let td1 = document.createElement("td");
            td1.innerText = name;

            let td2 = document.createElement("td");
            td2.innerText = body["date"];

            let td3 = document.createElement("td");
            td3.innerText = body["location"];
            
            let td4 = document.createElement("td");
            let button = document.createElement("input");
            button.type = "button";
            button.value = "Delete";
            button.onclick = () => deleteBackup(name);
            td4.appendChild(button);

            tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            table.appendChild(tr);
        });
    } else {
        await handleErrors(response);
    }
}

async function editCollection() {
    /*Sends a request to the /Edit endpoint with attributes to change, and reloads the page*/
    const response = await fetch("/api/Edit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            collection_name: URL_NAME,
            name: document.getElementById("name").value,
            description: document.getElementById("description").value,
            creation_date: document.getElementById("creation_date").value,
            modification_date: document.getElementById("modification_date").value,
            updated: document.getElementById("updated").checked
        })
    });

    if (response.ok) {
        window.location.href = "/info.html?name=" + document.getElementById("name").value;
    } else {
        await handleErrors(response);
    }
}

async function deleteCollection() {
    /*Deletes the collection whose name is in the ?name= url-bar */
    const response = await fetch("/api/Delete?name=" + URL_NAME, {method: "DELETE"});
    if (response.ok) {
        window.location.href = "/";
    } else {
        await handleErrors();
    }
}

async function deleteBackup(name) {
    /*Sends a request to delete the backup whose name is 'name', in the inspected Collection*/
    const response = await fetch("/api/Unbackup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            collection_name: document.getElementById("collection_name").innerText,
            backup_name: name,
        })
    });

    if (response.ok) {
        window.location.href = "/info.html?name=" + document.getElementById("collection_name").innerText;
    } else {
        await handleErrors(response);
    }
}

async function createBackupEntry() {
    /*Adds a backup with /Backup using info from the backup fields, and then reloads the page.*/
    let backup_date = document.getElementById("backup_date").value
    let jsonBody = {
            collection_name: document.getElementById("collection_name").innerText,
            backup_name: document.getElementById("backup_name").value,
            backup_location: document.getElementById("backup_location").value,
            backup_date: backup_date
        }
    if (backup_date == "") delete jsonBody["backup_date"];

    const response = await fetch("/api/Backup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonBody)
    });

    if (response.ok) {
        window.location.href = "/info.html?name=" + document.getElementById("name").value;
    } else {
        await handleErrors(response);
    }
}