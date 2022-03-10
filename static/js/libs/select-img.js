class SelectImg {
	constructor(el, el2) {
		this.el = el;
		this.el2 = el2;
		this.swiper = this._initSwiper();
		this.swiper2 = this._thumbSwiper();
	}

	_initSwiper() {
		return new Swiper(this.el, {
			loop: true,
			spaceBetween: 10,
			slidesPerView: 1,
			freeMode: true,
			watchSlidesProgress: true,
		});
	}

	_thumbSwiper() {
		return new Swiper(this.el2, {
			loop: true,
			spaceBetween: 10,
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-perv'
			},
			thumbs: {
				swiper: this.swiper
			}
		});
	}
}

