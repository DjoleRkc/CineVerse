
function initialize() {
    var selectedSeats = []; // Array to store selected seats

    // Event listener for the "Potvrdi Rezervaciju" button
    document.getElementById('potvrdiRez').addEventListener('click', function() {
        var checkboxes = document.querySelectorAll('.sediste-box:checked');
        selectedSeats = [];
        checkboxes.forEach(function(checkbox) {
            selectedSeats.push(checkbox.id);
        });

        // Display selected seats in the order confirmation modal
        var selectedSeatsDisplay = document.getElementById('selectedSeats');
        selectedSeatsDisplay.innerHTML = '';
        if (selectedSeats.length > 0) {
            selectedSeatsDisplay.innerHTML = '<p>Odabrana sedišta:</p><ul>';
            selectedSeats.forEach(function(seat) {
                selectedSeatsDisplay.innerHTML += '<li>' + seat + '</li>';
            });
            selectedSeatsDisplay.innerHTML += '</ul>';
        } else {
            selectedSeatsDisplay.innerHTML = '<p>Niste odabrali sedište.</p>';
        }
    });
}

function disableDropdownPropagation() {
    var dropdowns = document.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initialize();
    disableDropdownPropagation();
});


        document.addEventListener('DOMContentLoaded', function() {
            var dropdowns = document.querySelectorAll('.dropdown-menu');
            dropdowns.forEach(function(dropdown) {
                dropdown.addEventListener('click', function(e) {
                e.stopPropagation();
                });
            });

            var potvrdiButton = document.getElementById('potvrdiRez');

            document.getElementById('potvrdiRez').addEventListener('click', function() {
                    var selectedSeats = document.querySelectorAll('.sediste-box:checked');
                    var seatsList = "";
                    selectedSeats.forEach(function(seat) {
                        var seatNumber = seat.parentNode.textContent.trim().match(/[0-9]+[A-Za-z]+/);
                        if (seatNumber) {
                            seatsList += seatNumber[0] + ", ";
                        }
                    });
                    if (seatsList.length > 0) {
                        seatsList = seatsList.slice(0, -2);
                        document.getElementById('selectedSeats').textContent = seatsList;
                    } else {
                        document.getElementById('selectedSeats').textContent = "Niste izabrali nijedno sedište.";
                    }
                });

                potvrdiButton.disabled = true
                document.querySelectorAll('.sediste-box').forEach(function(seatCheckbox) {
            seatCheckbox.addEventListener('change', function() {
                var atLeastOneChecked = Array.from(document.querySelectorAll('.sediste-box')).some(function(seatCheckbox) {
                    return seatCheckbox.checked;
                });
                potvrdiButton.disabled = !atLeastOneChecked;
            });
            });
        });

// Path: rezervisiKartu.html