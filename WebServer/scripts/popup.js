/*
    Diese Datei ist aus einen meiner letzen Projekte d.h. auch auf Englisch.
*/

showPopupAnimation = "showPopupAnimation 0.3s"
hidePopupAnimation = "hidePopupAnimation 0.3s"

function addPopupButtonListeners() {
    buttons = document.getElementsByClassName("popupButton");
    popupCloseButtons = document.getElementsByClassName("popupCloseButton");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function() {
            showPopup(i);
        });
        popupCloseButtons[i].addEventListener("click", function() {
            hidePopup(i);
        });
    }
}

function showPopup(id) {
    popup = getPopups()[id];

    popup.style.visibility = "visible";
    popup.style.animation = showPopupAnimation;

    setTimeout(function() {
        popup.style.animation = null;
    }, 300);
}

function hidePopup(id) {
    popup = getPopups()[id];
    popup.style.animation = hidePopupAnimation;

    setTimeout(function() {
        popup.style.visibility = "hidden";
        popup.style.animation = null;
    }, 300)
}

function getPopups() {
    popups = document.getElementsByClassName("popup");
    return popups;
}