document.addEventListener('DOMContentLoaded', function() {
	new category();
})

class category {
	constructor() {
		this._init();
	}

	_init() {
		this._changeTenKey();
	}


	_changeTenKey() {
		const tenKey = document.querySelector('.ten-key');
		const categoryEl = document.querySelector('.pc-category');
		categoryEl.addEventListener('change', function() {

			tenKey.classList.remove('hidden');
		});
	}
}
