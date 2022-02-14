document.getElementById("header-right-profile-trigger").addEventListener("click", function () {
    Array.from(document.getElementsByClassName("header-right-profile-dropdown")).forEach(function (element, index) {
        element.style.display = "block";
    })
})
