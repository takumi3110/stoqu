document.addEventListener('DOMContentLoaded', function() {
	new category();
})

class category {
	constructor() {
		this._init();
	}

	_init() {
		this._changeCategory();
		this._changeSpec();
	}


	_changeCategory() {
		const tenKey = document.querySelector('.ten-key');
		const selectedCategory = document.querySelector('#pcCategory');
		selectedCategory.addEventListener('change', function() {
			if (this.value === 'note') {
				tenKey.style.display = 'block';
			} else {
				tenKey.style.display = 'none';
			}
		});
	}

	_changeSpec() {
		const spec = document.querySelector('.pc-spec');

	}
}
