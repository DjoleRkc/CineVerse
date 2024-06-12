// Autori: Lana Jovanović, Đorđe Pajić, Nikola Ostojić


/**
 * Initializes the seating chart and reservation functionality.
 * @param {Event} event - The DOMContentLoaded event.
 */
document.addEventListener('DOMContentLoaded', () => {

    /**
     * An array containing row identifiers.
     * @type {string[]}
     */
    const rows = ['A', 'B', 'C', 'D', 'E'];

    /**
     * The number of columns in the seating chart.
     * @type {number}
     */
    const columns = 5;

    /**
     * The container element for the seating area.
     * @type {HTMLElement}
     */
    const seatingArea = document.querySelector('.seating-area');

    /**
     * The display element for selected seats.
     * @type {HTMLElement}
     */
    const selectedSeatsDisplay = document.getElementById('selectedSeatsDisplay');

    /**
     * The reservation button element.
     * @type {HTMLElement}
     */
    const rezervisiBtn = document.getElementById('rezervisiBtn');

    /**
     * @type {string[]}
     */
    let zauzetaSedistaNiz = []

    /**
     * The string representing occupied seats.
     * @type {string}
     */
    let zauzetaSedista = $(".seating-area").attr("data-rezSedista");
    
    for (let i = 0; i < zauzetaSedista.length; i = i + 2){

        zauzetaSedistaNiz.push( zauzetaSedista[i] + zauzetaSedista[i + 1] )

    }   


    rows.forEach(rowId => {
        /**
         * The div element representing a row.
         * @type {HTMLDivElement}
         */
        const rowElement = document.createElement('div');
        rowElement.classList.add('row');
        rowElement.id = `row-${rowId}`;

        /**
         * @type {HTMLDivElement}
         */
        const rowLabel = document.createElement('div');
        rowLabel.classList.add('row-label');
        rowLabel.textContent = rowId;
        rowElement.appendChild(rowLabel);

        for (let i = 0; i < columns; i++) {
            /**
             * The button element representing a seat.
             * @type {HTMLButtonElement}
             */
            const seatElement = document.createElement('button');
            seatElement.classList.add('seat');
            seatElement.id = `${rowId}${i + 1}`;

            if (zauzetaSedistaNiz.includes(seatElement.id)){
                seatElement.style.backgroundColor = 'red';
                seatElement.disabled = true;
            }
            
                

            rowElement.appendChild(seatElement);
        }
        seatingArea.appendChild(rowElement);
    });

    /**
     * The list of available seats.
     * @type {NodeListOf<HTMLButtonElement>}
     */
    const seats = document.querySelectorAll('.seat:not(.occupied)');

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            seat.classList.toggle('selected');
            updateSelectedCount();
        });
    });

    function updateSelectedCount() {
        /**
         * The list of selected seats.
         * @type {NodeListOf<HTMLButtonElement>}
         */
        const selectedSeats = document.querySelectorAll('.seat.selected');

         /**
         * The list of IDs of selected seats.
         * @type {string[]}
         */
        const selectedSeatsIds = Array.from(selectedSeats).map(seat => seat.id);

        /**
         * The text to display for selected seats.
         * @type {string}
         */
        const selectedSeatsText = selectedSeatsIds.length > 0 ? selectedSeatsIds.join(', ') : '';
        selectedSeatsDisplay.textContent = `Izabrana sedišta: ${selectedSeatsText}`;
    }

});

$(document).ready(function(){
    
    var selectedSeats;


    /**
     * Handles click event for the reservation button.
     */
    $("#rezervisiBtn").click(function(){
        selectedSeats = $('#selectedSeatsDisplay').text();
        selectedSeats = selectedSeats.replace("Izabrana sedišta: ", "")
        $("#Tekst").text("Odabrali ste sedišta " + selectedSeats + ". Kliknite na dugme za potvrdu radi potvrde rezervacije, nakon čega dobijate email obaveštenja sa svim informacijama.");
        $("#potvrda-modal").fadeIn();
    });

    $(".close").click(function(){
        $("#potvrda-modal").fadeOut();
    });

    $(".nazad-btn").click(function(){
        $("#potvrda-modal").fadeOut();
    });


    /**
     * Handles click event to close the modal when clicking outside of it.
     */
     $(window).on("click", function(event){
        if (event.target === $("#potvrda-modal")[0]) {
            $("#potvrda-modal").fadeOut();
        }
    });


    $("#potvrdiRezBtn").click(function(){

        if (selectedSeats.length === 0) {
            alert('Nista izabrali ni jedno mesto!');
            return;
        }

        let idpro = $(".movie-details").data("idprojekcije");
        let idsale = $(".movie-details").data("idsale");

        /**
         * The URL for the reservation confirmation.
         * @type {string}
         */
        const fullUrl = `potvrdaRezervacije?idpro=${idpro}&seats=${encodeURIComponent(selectedSeats)}&idsala=${idsale}`;

        $.ajax({
            type: 'POST',
            url: fullUrl,
            data: {
                'seats': JSON.stringify(selectedSeats)
            },
            success: function(response) {
                $("#potvrda-modal").fadeOut();
                location.reload();
            },
            error: function(error) {
                alert("Greška!");
            }
        });

    });

});
