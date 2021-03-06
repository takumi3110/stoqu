document.addEventListener('DOMContentLoaded', function () {
	new Main();
});

class Main {
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
		this.hero = new HeroSlider('.swiper');
		this._paceDone();
	}

	_paceDone() {
		this._scrollInit();
	}

	_inviewAnimation(el, inview) {
		if (inview) {
			el.classList.add('.inview');
		} else {
			el.classList.remove('.inview');
		}
	}

	_toggleSlideAnimation(el, inview) {
		if (inview) {
			this.hero.start();
		} else {
			this.hero.stop();
		}
	}

	_scrollInit() {
		this.observers = new ScrollObserver('.swiper', this._toggleSlideAnimation.bind(this), {once: false});
		this.observers = new ScrollObserver('.appear', this._inviewAnimation);
		console.log(this.observers);
	}
}

function modal_form(el, url) {
	$(el).each(function () {
		$(this).modalForm({formURL: url});
	});
}