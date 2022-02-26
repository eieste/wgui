var max_values = {"rx": 0, "tx": 0}

window.setInterval(requestClientStatistics, 4000);

requestClientStatistics();

function safety_check(response) {
    if (response.status !== 200) {
        window.location.href = "/";
    }
}

function update_statistic(element, key, value) {
    element.querySelector(".rx").style.height = value.transfer_rx / max_values.rx * 100 + "%";
    element.querySelector(".tx").style.height = value.transfer_tx / max_values.tx * 100 + "%";

    if (value.latest_handshake == null) {
        element.querySelector(".indicator").style.backgroundColor = "red";
    } else {
        let handshake = new Date(0); // The 0 there is the key, which sets the date to the epoch
        handshake.setUTCSeconds(value.latest_handshake);
        let now = new Date();
        let last_contact = now.getTime() / 1000 - handshake.getTime() / 1000;
        if (last_contact > 300) {
            element.querySelector(".indicator").style.backgroundColor = "red";
        } else if (last_contact >= 200 && last_contact >= 300) {
            element.querySelector(".indicator").style.backgroundColor = "yellow";
        } else if (200 > last_contact) {
            element.querySelector(".indicator").style.backgroundColor = "green";
        }
    }
}

function requestClientStatistics() {
    let client_list = [];

    Array.prototype.forEach.call(document.getElementsByClassName("wgpeer"), (element) => {
        client_list.push(element.getAttribute("data-fname"));
    });

    fetch("/api/wireguard", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "clients": client_list
        })
    }).then(function (response) {
        safety_check(response);
        return response.json();
    }).then((data) => {

        Object.entries(data.clients).forEach(([key, value], index) => {
            if (max_values.rx <= value.transfer_rx) {
                max_values.rx = value.transfer_rx
            }
            if (max_values.tx <= value.transfer_tx) {
                max_values.tx = value.transfer_tx
            }
        });


        Object.entries(data.clients).forEach(([key, value], index) => {
            Array.prototype.forEach.call(document.getElementsByClassName("wgpeer"), (element) => {
                if (element.getAttribute("data-fname") === key) {
                    update_statistic(element, key, value);
                }
            });

        });
    }).catch(function (reason, response) {

    });
}
