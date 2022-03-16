document.addEventListener('DOMContentLoaded', function() {
	new category();
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

	_normalSpec() {
		this.cpu.value = 'i5';
		this.memory.value = 8;
		this.storage.value = 128;
	}

	_normalPlusSpec() {
		this.cpu.value = 'i5';
		this.memory.value = 16;
		this.storage.value = 128;
	}

	_highSpec() {
		this.cpu.value = 'i7';
		this.memory.value = 16;
		this.storage.value = 256;
	}
}
