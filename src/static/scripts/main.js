let DETAILED_OVERVIEW = false;

/*--------------HELPER FUNCTIONS---------------*/

function clear_suggestions() {
    /*Clears all suggestions in the popup below the searchbar */
    const suggestions = document.getElementById("suggestions");
    Array.from(suggestions.children).forEach(option => {
        if (option.value !== "No Results") {
            option.remove();
        }
    });
}

function clearOverview() {
    /*Clears all elements in the overview table*/
    document.querySelectorAll("#overview > tr").forEach(element => {
        element.remove();
    });
}

function addOverviewRow(content, classname, link) {
    /*Adds a <tr> element with <td> elements for every element in 'content' and applies it to the table*/
    let tr = document.createElement("tr");
    content.forEach(element => {
        let td = document.createElement("td");
        if (link) {
            let atag = document.createElement("a");
            atag.href = "/info.html?name=" + content[0];
            atag.innerText = element;
            td.appendChild(atag);
        } else {
            td.innerText = element;
        }
        td.className = classname + " breakable_td";
        tr.appendChild(td);
    });
    document.getElementById("overview").appendChild(tr);
}

async function toggleOverviewType() {
    /*Rotates back and forth between showing a regular overview, and a detailed overview*/
    if(DETAILED_OVERVIEW) {
        clearOverview();
        updateOverview();
        document.getElementById("overview_h2").innerText = "Overview";
        DETAILED_OVERVIEW = false;
    } else {
        clearOverview();
        updateDetailedOverview();
        document.getElementById("overview_h2").innerText = "Detailed Overview";
        DETAILED_OVERVIEW = true;
    }
}

/*---------------API_CALLS--------------------*/

async function searchSuggestions(searchterm) {
    /*Populates the 'suggestions' table with searchresults from the /Search API*/
    const response = await fetch("/api/Search?case_sensitive=false&name=" + searchterm);
    if (response.ok) {
        const result = await response.json();
        Object.entries(result["search"]).forEach(([name, body]) => {
            option = document.createElement("li");
            atag = document.createElement("a");
            atag.href = "/info.html?name=" + name;
            atag.innerText = name + " | " + body.modification_date;
            option.appendChild(atag);
            document.getElementById("suggestions").appendChild(option);
        });
    }
}

window.onload = () => { /*We need to wait for the DOM elements to load*/
    document.getElementById("search_input").addEventListener("input", async function(event) {
        /*Clears suggestions between each key input before we add new content, preventing duplicates*/
        clear_suggestions();
        const searchterm = event.target.value;
        if (searchterm.length === 0) return;

        await searchSuggestions(event.target.value);
    });

    document.getElementById("search_input").addEventListener("blur", function(event) {
        /*We use setTimout and this roundabout way to not remove it before we can click it*/
        setTimeout(() => {
            const active = document.activeElement;
            const suggestions = document.getElementById("suggestions");
            if (!suggestions.contains(active)) {
                clear_suggestions();
            }
        }, 100);
    });
}



async function updateOverview() {
    /*Load in information about all DataCollections and displays them using 'addOverviewRow()'*/
    const response = await fetch("/api/Overview")
    if (response.ok) {
        const result = await response.json()
        
        result["overview"].forEach(element => {
            addOverviewRow([element.split(" | ")[0], element.split(" | ")[1], element.split(" | ")[2]], "overviewtd", true);
        });
        
    } else {
        handleErrors(response);
    }
}

async function updateDetailedOverview() {
    /*Load in detailed information and displays it using 'addOverviewRow()'*/
    const response = await fetch("/api/List")
    if (response.ok) {
        const result = await response.json()
        addOverviewRow(["Name", "Description", "Creation Date", "Modification Date", "Updated"], "detailedoverviewtd", false)
        Object.entries(result["overview"]).forEach(([name, body]) => {
            addOverviewRow([
                name,
                body["description"],
                body["creation_date"],
                body["modification_date"],
                body["updated"]
            ], "detailedoverviewtd", true)
        });
        
    } else {
        handleErrors(response);
    }
}

async function addCollection() {
    /*Calls /Collection API endpoint to add a new Collection with values from the input fields*/
    let creation_date = document.getElementById("creation_date").value;
    let modification_date = document.getElementById("modification_date").value;

    let jsonBody = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        creation_date: creation_date,
        modification_date: modification_date,
        updated: document.getElementById("updated").checked
    }
    if (creation_date == "") delete jsonBody["creation_date"]
    if (modification_date == "") delete jsonBody["modification_date"]

    const response = await fetch("/api/Collection", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonBody)
    });
    
    if (response.ok) {
        window.location.reload();
    } else {
        await handleErrors(response);
    }
}