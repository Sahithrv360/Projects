console.log("Smart OS Resource Manager loaded");

function updateSystemData() {
    fetch("/system")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cpu").textContent = data.cpu + "%";
            document.getElementById("memory").textContent = data.memory + "%";
            document.getElementById("disk").textContent = data.disk + "%";
            document.getElementById("processes").textContent = data.processes;
        })
        .catch(error =>{
            console.error("Error : ",error)
        });
}
updateSystemData();