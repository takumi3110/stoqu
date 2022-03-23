document.addEventListener('DOMContentLoaded', function() {
	// new category();
})

class category {
	constructor() {
		this.selectedCategory = document.querySelector('#pcCategory');
		this.cpu = document.querySelector('#detailCpu');
		this.memory = document.querySelector('#detailMemory');
		this.storage = document.querySelector('#detailStorage');
		this._init();
	}

	_init() {
		this._changeCategory();
		this._changeSpec();
	}


	_changeCategory() {
		const tenKey = document.querySelector('.ten-key');
		const selectedCategory = this.selectedCategory;
		tenKey.style.display = 'none';
		selectedCategory.addEventListener('change', function() {
			if (this.value === 'note') {
				tenKey.style.display = 'block';
			} else {
				tenKey.style.display = 'none';
			}
		});
	}

	_changeSpec() {
		const category = this.selectedCategory;
		const selectedSpec = document.querySelector('#spec');
		const spec = document.querySelector('.spec-detail');
		const cpu = this.cpu;
		const memory = this.memory;
		const storage = this.storage;
		selectedSpec.addEventListener('change', function(){
			spec.style.display = 'block';
			if (this.value === 'normal') {
				cpu.value = 'i5';
				memory.value = 8;
				storage.value = 128;
			} else if (this.value === 'plus') {
				cpu.value = 'i5';
				memory.value = 16;
				storage.value = 128;
			} else if (this.value === 'high') {
				cpu.value = 'i7';
				memory.value = 16;
				storage.value = 256;
			}
		});
	}
}

function change_quantity(el, data, pk) {
	el.addEventListener('change', function() {
		const url = 'http://127.0.0.1:8000/api/v1/quote/quoteItem/' + pk + '/';
		data.quantity = this.value;
		const init = makePutInit(data);
		fetch(url, init)
			.then(response => {
				if (response.ok) {
					return response.json();
				} else {
					throw Error();
				}
			})
			.then(data => {
				console.log(data.quantity);
			});
	});
}

function all_apply(pk) {
	const allApply = document.querySelector('.all-apply');
	const destinationInput = document.querySelectorAll('.destination');
	const destinationId = 'destination' + pk;
	allApply.addEventListener('change', function() {
		if (allApply.checked) {
			console.log('checked');
			// for(let input of destinationInput) {
			// 	input.id = destinationId;
			// }
		} else {
			console.log('none');
		}
	});
}

//
// function over_ten(el) {
// 	const new_input = document.createElement('input');
// 	new_input.type = 'number';
// 	new_input.name = 'quantity';
// 	new_input.required = true;
// 	new_input.min = '1';
// 	new_input.classList.add('form-control')
//
// }

function modal_form(el, url) {
	$(el).each(function() {
		$(this).modalForm({formURL: url});
	});
}