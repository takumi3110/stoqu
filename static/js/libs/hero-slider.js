class HeroSlider {
	constructor(el) {
		this.el = el;
		this.swiper = this._initSwiper();
	}

	_initSwiper() {
		return new Swiper(this.el, {
			loop: true,
			grabCursor: true,
			effect: 'cover-slide',
			slidesPerView: 1,
			// effect: 'cube',
			// cubeEffect: {
			// 	shadow: true,
			// 	slideShadows: true,
			// 	shadowOffset: 40,
			// 	shadowScale: 1.1,
			// },
			centeredSlides: true,
			speed: 1000,
		});
	}

	start(options = {}) {
		options = Object.assign({
			delay: 4000,
			disableOnInteraction: false,
		},
			options
		);
		this.swiper.params.autoplay = options;
		this.swiper.autoplay.start();
	}

	stop() {
		this.swiper.autoplay.stop();
	}
}