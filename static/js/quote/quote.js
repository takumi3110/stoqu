document.addEventListener('DOMContentLoaded', function () {
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
		selectedCategory.addEventListener('change', function () {
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
		selectedSpec.addEventListener('change', function () {
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
		open.addEventListener('click', function () {
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
		this._observers = [];
		this._init();
	}

	set observers(val) {
		this._observers.push(val);
	}

	get observers() {
		return this._observers;
	}


	_init() {
		const checkBox = document.querySelectorAll('.checkBox');
		this._checkInit(checkBox);
		this._observers_init();
	}

	_checkInit(els) {
		els.forEach(el => {
			el.addEventListener('change', () => {
				this._checked(el);
			});
		});
	}

	_checked(el) {
		if (el.checked) {
			const value = el.value.split('-')
			const quoteItem = value[0];
			const orderItem = value[1];
			const destination = value[2];
			const url = 'http://127.0.0.1:8000/api/v1/quote/orderItem/' + orderItem + '/';
			let label = ''
			let data = {
				destination: destination,
				quote_item: quoteItem
			}
			if (el.name === 'ordered') {
				label = document.querySelector('label.ordered' + orderItem);
				data.ordered = true;
			} else if (el.name === 'arrived') {
				label = document.querySelector('label.arrived' + orderItem);
				data.arrived = true;
			} else if (el.name === 'delivered') {
				label = document.querySelector('label.delivered' + orderItem);
				data.delivered = true;
			}
			if (label.innerHTML.trim() === '') {
				const init = makePutInit(data);
				fetch(url, init)
					.then(response => {
						if (response.ok) {
							changeLabel(el, label);
							return response.json();
						} else {
							throw Error();
						}
					})
					.then(data => {
						console.log(data);
					});
			}
		}
	}

	_observers_init() {
		this.observers = new StatusCheck('#ordered', this._checked);
		this.observers = new StatusCheck('#arrived', this._checked);
		this.observers = new StatusCheck('#delivered', this._checked);
		console.log(this.observers);
	}
}

class StatusCheck {
	constructor(els, callBack) {
		this.els = document.querySelectorAll(els);
		this.callBack = callBack;
		this._init();
	}

	_init() {
		const els = this.els;
		const callBack = this.callBack;
		this._statusClick(els, callBack);
	}

	_statusClick(els, callBack) {
		const checked = callBack
		const nowStatus = document.querySelector('.status-now').innerHTML;
		for (let i = 1; i < 6; i++) {
			const status = document.querySelector('.status' + i);
			if (i <= Number(nowStatus)) {
				status.classList.add('active');
			}
			status.addEventListener('click', () => {
				if (i <= Number(status.id)) {
					status.classList.add('active');
					els.forEach(el => {
						this._allCheck(el, status);
						checked(el);
					});
					const data = this._data(status)
					this._statusUpdate(data);
				}
			});
		}
	}

	_allCheck(el, status) {
		const id = Number(status.id);
		if (id <= 3) {
			if (el.id === 'ordered') {
				el.checked = true;
			}
		} else if (id === 4) {
			if (el.id === 'arrived') {
				el.checked = true;
			}
		} else if (id === 5) {
			if (el.id === 'delivered') {
				el.checked = true;
			}
		}
	}

	_statusUpdate(data) {
		const pk = document.querySelector('.pk').innerHTML.trim();
		const url = 'http://127.0.0.1:8000/api/v1/quote/orderInfo/' + pk + '/';
		const finishDate = document.querySelector('.finish-date');
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
				if (data.finished) {
					const date = new Date(data.finished_at);
					finishDate.innerHTML = getDate(date);
				}

			});
	}

	_data(status) {
		const number = document.querySelector('.number').innerHTML;
		const ticket = document.querySelector('.ticket').innerHTML;
		const cart = document.querySelector('.cart').innerHTML;
		const id = status.id;
		let data = {
			status: status.id,
			number: number,
			ticket: ticket,
			cart: cart
		}
		if (Number(id) === 5) {
			data.finished = true;
		}
		return data
	}
}


function changeLabel(checkEl, el) {
	checkEl.disabled = true;
	checkEl.checked = true;
	const date = new Date();
	el.innerHTML = getDate(date);
}

function getDate(date) {
	const year = date.getFullYear();
	const month = date.getMonth() + 1;
	const day = date.getDate();
	const hour = date.getHours();
	const minutes = date.getMinutes();
	return year + '年' + month + '月' + day + '日' + hour + ':' + minutes;
}


function change_quantity(el, data, pk) {
	el.addEventListener('change', function () {
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

// function all_apply(pk) {
// 	const allApply = document.querySelector('.all-apply');
// 	const destinationInput = document.querySelectorAll('.destination');
// 	const destinationId = 'destination' + pk;
// 	allApply.addEventListener('change', function () {
// 		if (allApply.checked) {
// 			console.log('checked');
// 			// for(let input of destinationInput) {
// 			// 	input.id = destinationId;
// 			// }
// 		} else {
// 			console.log('none');
// 		}
// 	});
// }
