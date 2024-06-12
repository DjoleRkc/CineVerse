// autor: Lana Jovanovic

/**
 * Executes the provided function when the DOM is fully loaded.
 *
 * This function checks if the modal status is set to "show" by checking the text content
 * of the element with the ID "modalStatus". If the status is "show", it displays the modal
 * with the ID "modalProjections".
 *
 * @function
 * @name documentReady
 * @memberof module:DOM
 */
$(document).ready(function(){
    if($("#modalStatus").text() === "show")
        $('#modalProjections').modal('show');
})