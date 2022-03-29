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
		// const category = this.selectedCategory;
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

class clickAllow {
	constructor() {
		this.open = document.querySelector('.open');
		this.allow = document.querySelector('.allow');
		this.main = document.querySelector('.main');
		this._init();
	}

	_init() {
		this._click();
	}

	_click() {
		const open = this.open;
		const allow = this.allow;
		const main = this.main;
		const text = open.innerHTML
		const newText = '閉じる<i class="fa-solid fa-angle-down allow selected"></i>'
		open.addEventListener('click', function() {
			if (main.classList.contains('toggle')) {
				this.innerHTML = newText;
				allow.classList.add('selected');
				main.classList.remove('toggle');
			} else {
				this.innerHTML = text;
				allow.classList.remove('selected');
				main.classList.add('toggle');
			}
		});
	}
}

class checkBoxObserver {
	constructor() {
		this.orderedCheckBox = document.querySelectorAll('.ordered');
		this.arrivedCheckBox = document.querySelectorAll('.arrived');
		this.deliveredCheckBox = document.querySelectorAll('.delivered');
		this._init();
	}

	_init() {
		const orderedCheckBox = this.orderedCheckBox;
		this._checked();
	}

	_checked(els) {
		els.forEach(el => {
			if (el.checked) {

			}
		})
	}

	_post(el) {

	}

}

function get_request(url) {
	let getInit = GetInit();
	return fetch(url, getInit)
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw Error();
			}
		})
		.then(data => {
			console.log(data)
		})
}

function ordered_check(data, pk) {
	const els = document.querySelectorAll('.ordered');
	const url = 'http://127.0.0.1:8000/api/v1/quote/orderItem/' + pk + '/';
	els.forEach(el => {
		el.addEventListener('change', function() {
			if (el.checked) {
				data.ordered = true;
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
						console.log(data.ordered);
					})
			}
		});
	});
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


function modal_form(el, url) {
	$(el).each(function() {
		$(this).modalForm({formURL: url});
	});
}
