//Autor: Jovan Babović

/**
 * Removes the registration form, opens a modal, and redirects to the home page after a delay.
 */
function closeFormAndOpenModal() {
    /** @type {HTMLFormElement} */
    var form = document.getElementById('registerForm');
    form.remove();

    /** @type {bootstrap.Modal} */
    var myModal = new bootstrap.Modal(document.getElementById('myModal'));
    myModal.show();

    setTimeout(function() {
        window.location.href = "{% url 'home' %}";
    }, 2000);
}