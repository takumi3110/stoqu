document.addEventListener('DOMContentLoaded', function(){
	new SelectImg();
})

class SelectImg {
	constructor() {
		this._init();
	}

	_init() {
		const initImg = document.querySelector('.img0');
		initImg.classList.add('selected');
		this._imgClick();
	}

	_imgClick() {
		const subImg = document.querySelectorAll('.sub-img');
		subImg.forEach(el => {
			const className = '.' + el.classList[1];
			const subClass = document.querySelector(className);
			this._addSelected(subImg, subClass);
			this._addMainImg(subClass);
		});
	}

	_addSelected(els, el) {
		el.addEventListener('click', function() {
			els.forEach(el => {
				if (el.classList.contains('selected')) {
					el.classList.remove('selected');
					const selectedImg = document.querySelector('.selectedMainImg');
					selectedImg.remove();
				}
			});
			if (el.classList.contains('selected') === false) {
				this.classList.add('selected');
				const mainImg = document.querySelector('.main-img');
				const imgElement = document.createElement('img');
				imgElement.alt = 'main-image';
				imgElement.src = this.src;
				imgElement.className = 'selectedMainImg';
				mainImg.appendChild(imgElement);
			}
		});
	}

	_removeSelected(els) {
		els.forEach(el => {
			if (el.classList.contains('selected')) {
				el.classList.remove('selected');
			}
		});
	}

	_addMainImg(el) {
		const mainImg = document.querySelector('.main-img');
		if (el.classList.contains('selected')) {
			const imgElement = document.createElement('img');
			imgElement.alt = 'main-image';
			imgElement.src = el.src;
			imgElement.className = 'selectedMainImg';
			mainImg.appendChild(imgElement);
		}
	}
}

