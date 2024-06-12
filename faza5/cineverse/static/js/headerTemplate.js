/**
 * Autor:Đorđe Pajić
 * Highlights the active navigation link based on the current URL.
 *
 * When the DOM is fully loaded, this script determines which navigation link corresponds
 * to the current page URL and adds the "active" class to that link, indicating that it is
 * the active page.
 *
 * Steps:
 * 1. Retrieves the current URL path using `window.location.pathname`.
 * 2. Splits the URL path into an array of its components.
 * 3. Extracts the last component of the URL path.
 * 4. Searches for a navigation link element with an ID matching the extracted component.
 * 5. If such an element is found, adds the "active" class to it.
 *
 * Example:
 * If the current URL is `http://example.com/home`, this script will look for an element
 * with the ID "home" and add the "active" class to it.
 *
 * @function
 */

$(document).ready(function() {

    var currentUrl = window.location.pathname;


    var urlParts = currentUrl.split('/');

    var lastPart = urlParts[urlParts.length - 1];

    var navLink = $("#"+lastPart);

    if (navLink.length > 0) {
        navLink.addClass("active");
    }
});
