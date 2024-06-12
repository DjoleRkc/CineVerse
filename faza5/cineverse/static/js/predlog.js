//Autor: Nikola Ostojić


/**
 * Executes the specified function when the DOM content is fully loaded.
 * Adds an event listener to the "predloziButton" element, triggering a modal display when clicked.
 */
document.addEventListener('DOMContentLoaded', function() {
    /**
     * Handles the click event on the "predloziButton" element.
     * Retrieves the movie and genre inputs, and displays a modal if at least one of them is provided.
     */
    document.getElementById("predloziButton").addEventListener("click", function() {
        /** @type {string} */
        var filmInput = document.getElementById("filmInput").value.trim();

        /** @type {string} */
        var zanrInput = document.getElementById("zanrInput").value.trim();
        

        if (filmInput === "" && zanrInput === "") {
            return; 
        } else {

            /** @type {bootstrap.Modal} */
            var myModal = new bootstrap.Modal(document.getElementById('personalizovanPredlog'));
            myModal.show();
        }
    });
});