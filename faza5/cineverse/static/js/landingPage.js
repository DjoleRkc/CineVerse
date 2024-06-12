/**
 * Autor: Đorđe Pajić
 * Executes actions when the DOM is fully loaded.
 */
$(document).ready(function(){

	/**
     * Fetches images for the carousel and initializes the modal with movie suggestions.
 	*/
	const $carouselInner = $('.carousel-inner');

	$.ajax({
		url: 'dohvatiSlike',
		method: 'GET',
		success: function(slike){
			$.each(slike, function(i, slika){
				const $div = $('<div>').addClass('carousel-item');
				if(i === 0){
					$div.addClass('active');
				}

				const $img = $('<img>').attr('src', '/static/images/carousel/'+slika).attr('alt', slika);

				$div.append($img);

				$carouselInner.append($div);

			})
		}
	})
	
	/**
         * Listens for a click event on the "Suggest Movie" button and initiates the process of suggesting a movie.
	 */
	document.getElementById('predloziButton').addEventListener('click', async function() {
		let filmovi = document.getElementById('filmInput').value.trim();
		let zanrovi = document.getElementById('zanrInput').value.trim();

		if (filmovi === "" && zanrovi === ""){
			return;
		}

		let bazaFilmovi;

		try {

			document.getElementById("MODAL").innerHTML = "";

			const response = await fetch("ucitajFilmove");
			const data = await response.json();
	
			bazaFilmovi = data.filmovi;
	
			let message = `Suggest the best possible movie from this list called X:(${bazaFilmovi}) based on my favorite movies (${filmovi}) and preferred genres (${zanrovi}). Movies have greater priority for making the suggestion. Your response should be just the name of the movie from the list X, without any punctuation.`;
	
			const gptResponse = await callChatGPT(message);
			let nazivFilma = gptResponse.choices[0].message.content;
	

			const filmResponse = await fetch(`ucitajOdredjeniFilm?parametar=${nazivFilma}`);
			const filmData = await filmResponse.json();


		
			const modalHeader = $('<div class="modal-header"></div>');
			const modalTitle = $('<h4 class="modal-title" style="color: #ffb448;"></h4>');
			const modalLink = $(`<a href='pregledFilmaNO?parametar=${filmData.naziv}' class="predlog-link">Predlog: ${filmData.naziv} </a>`);
			const closeButton = $('<button type="button" class="btn-close" data-bs-dismiss="modal"></button>');
			modalTitle.append(modalLink);
			modalHeader.append(modalTitle, closeButton);


			const modalBody = $('<div class="modal-body text-center"></div>');
			const modalLinkSecond = $(`<a href="pregledFilmaNO?parametar=${filmData.naziv}" class=""></a>`);
			const modalImage = $('<img src=' + filmData.slika + 'alt="">');
			const cardInfo1 = $('<p class="card-info">Kratak sadržaj: ' + filmData.krataksadrzaj + '</p>');
			const cardInfo2 = $('<p class="card-info">Ocena korisnika: ' + filmData.ocenakorisnika + ' ★</p>');
			const cardInfo3 = $('<p class="card-info">IMDB ocena: ' + filmData.ocenaimdb + ' ★</p>');
			const cardInfo4 = $('<p class="card-info">' + filmData.zanrovi + ' | ' + filmData.trajanje +'min</p>');
			modalLinkSecond.append(modalImage);
			modalBody.append(modalLinkSecond, cardInfo1, cardInfo2, cardInfo3, cardInfo4);


			$(".modal-content").append(modalHeader);
			$(".modal-content").append(modalBody);
			
			$(".modal-content").show();



		} catch (error) {
			alert("Error occured, try again!")
		}
	});


	

});



/**
     * Calls the OpenAI API to generate a response based on the provided message.
     * @async
     * @function
     * @param {string} message - The message for which a response is generated.
     * @returns {Promise} - A promise that resolves to the response from the OpenAI API.
 */
function callChatGPT(message) {
	const api_key = api_key
	const headers = {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${api_key}`,
	};
	const data = JSON.stringify({
		'model': 'gpt-3.5-turbo-0125',
		'messages': [
			{'role': 'system', 'content': 'You are a helpful assistant.'},
			{'role': 'user', 'content': message},
		],
	});

	return fetch('https://api.openai.com/v1/chat/completions', {
		method: 'POST',
		headers: headers,
		body: data
	})
	.then(response => response.json());
}