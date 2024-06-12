//Autor: Đorđe Pajić

/**
 * Executes the specified function when the DOM content is fully loaded.
 * Sets up event listeners for input changes and button clicks.
 */
$(document).ready(function() {

    /**
     * Handles input changes on the "#predlogInput" element.
     * Toggles the "data-bs-toggle" attribute of the "#predlogButton" element based on input value.
     */
   $('#predlogInput').on('input', function() {
        var inputVal = $(this).val().trim();
        if (inputVal !== "") {
            $('#predlogButton').attr("data-bs-toggle", "modal");
        } else {
            $('#predlogButton').removeAttr("data-bs-toggle");
        }
    });


   /**
     * Resets the modal body content when the "#predloziFilm" modal is hidden.
    */
   $("#predloziFilm").on("hidden.bs.modal", function() {
        $(".modal-body").text("");

    });


    /**
     * Handles click events on the "#predlogButton" element.
     * Sends a request to add a movie suggestion and displays a modal with appropriate feedback.
     */
   $("#predlogButton").on("click", async function() {
       var imeFilma = $('#predlogInput').val().trim();
       if(imeFilma !== "") {
           try {
               await $.get("dodajPredlog?imeFilma="+imeFilma, function(response) {
                      var body = $('#predloziFilm .modal-body');
                       if ("success" in response) {

                            body.text("Tvoj predlog će biti uzet u razmatranje od strane administratora sajta!");
                       } else if ("error" in response && response["error"] === "Vec u ponudi") {
                            body.text("Traženi film je već u ponudi. Za više informacija pogledajte odeljak sa svim projekcijama.");
                       } else {
                            body.text("Već ste predložili dati film.");
                       }
                       $("#predloziFilm").modal("show");
               }
           )
           } catch (error) {
               console.error("Error:", error);
           }
       }
       return false
   });
});
