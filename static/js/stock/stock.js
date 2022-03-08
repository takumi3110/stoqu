document.addEventListener('DOMContentLoaded', function () {
    const hero = new HeroSlider('.swiper');
    hero.start();
    navTitle();
});

function navTitle() {
    const el = document.querySelector('.navigation__title');
    const str = el.innerHTML.trim().split("");
    el.innerHTML = str.reduce((acc, curr) => {
        curr = curr.replace(/\s+/, '&nbsp;');
        return `${acc}<span class="char">${curr}</span>`;
    }, "");
}

function formatDate(date, format) {
    const day = new Date(date);
    format = format.replace(/YYYY/, day.getFullYear());
    format = format.replace(/MM/, day.getMonth() + 1);
    format = format.replace(/DD/, day.getDate());
    return format;
}

const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
}
const csrfToken = getCookie('csrftoken');

function makePutInit(data) {
    return {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data),
    }
}

// function makePostInit(data) {
//     return {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken
//         },
//         body: JSON.stringify(data),
//     }
// }

// function GetInit() {
//     return {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken
//         },
//     }
// }

function changePrice(checkEl, totalEl, count) {
    totalEl.innerHTML = '';
    const tax = 1.10
    let price = 0;
    for (el of checkEl) {
        if (el.checked) {
            price += Number(el.value);
        }
    }
    let subTotal = price * count;
    let result = Math.round(subTotal * tax);
    totalEl.innerHTML = result.toLocaleString();
}


function linkClick(el, url) {
    el.addEventListener('click', function () {
        location.href = url;
    });
}

function checkSelect(checkEl, el) {
    checkEl.addEventListener('click', function () {
        const innerItem = document.querySelector('.select-item');
        if (checkEl.checked) {
            innerItem.innerHTML += el.innerHTML.trim();
        } else if (innerItem.childElementCount > 1) {
            let selectItem = document.querySelector('.select-item');
            innerItem.innerHTML = selectItem.innerHTML.trim().replace(el.innerHTML.trim(), '');
        } else {
            innerItem.innerHTML = '';
        }
        deleteCheck();
    });
}

function deleteCheck() {
    const nextBtn = document.querySelector('.next-btn');
    const checkList = document.querySelectorAll('.select-delete__check');
    let flag = false;
    checkList.forEach(function (val) {
        if (val.checked) {
            flag = true;
        }
    });
    nextBtn.disabled = !flag;
}

// class SelectDelete {
//     constructor(el) {
//         this.el = el;
//     }
// }

function tradeCheck() {
    const tradeHistory = document.querySelector('.order-detail__trade');
    const icon = document.querySelector('.order-detail__icon');
    tradeHistory.addEventListener('click', function () {
        icon.classList.toggle('selected');
    })
}

function quantity(el, value, selectedValue) {
    for (let i = 1; i <= value; i++) {
        let new_option = document.createElement('option');
        new_option.value = String(i);
        new_option.text = String(i);
        new_option.classList.add('cart__item__quantity');
        if (i === selectedValue) {
            new_option.selected = true;
        }
        el.appendChild(new_option);
    }
}


function quantityChange(el, data, pk) {
    el.addEventListener('change', function () {
        let url = 'http://127.0.0.1:8000/api/v1/stock/orderItem/' + pk + '/';
        let id = '#itemPrice' + pk;
        let itemPrice = document.querySelector(id);
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
                let tax = 1.10;
                let subtotal = Math.round(data.price * tax);
                itemPrice.innerHTML = subtotal.toLocaleString();
                totalPriceChange();

            });
    });
}

function totalPriceChange() {
    let itemPrice = document.querySelectorAll('.item-price');
    let totalPrice = document.querySelectorAll('.total-price');
    let price = 0;
    itemPrice.forEach(
        val => price += Number(val.innerHTML.replace(',', ''))
    );
    totalPrice.forEach(val => val.innerHTML = price.toLocaleString());
}

function changeRadio(radioEl, data, pk, date, quantity) {
    radioEl.addEventListener('click', function () {
        const url = 'http://127.0.0.1:8000/api/v1/stock/orderItem/' + pk + '/';
        const kittingPrice = document.querySelector('.total-kitting-price');
        const selectPlan = document.querySelectorAll('.select-plan');
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
                const schedule = formatDate(data.due_at, 'YYYY年MM月DD日');
                el.innerHTML = '';
                el.innerHTML = schedule;
            });
        changePrice(selectPlan, kittingPrice, quantity);
        const subTotalEl = document.querySelector('.subtotal-price').innerHTML;
        const afterKittingEl = document.querySelector('.total-kitting-price').innerHTML;
        const totalPriceEl = document.querySelector('.total-price');
        const subTotalPrice = Number(subTotalEl.trim().replace(',', ''));
        const afterKittingPrice = Number(afterKittingEl.trim().replace(',', ''));
        const totalPrice = subTotalPrice + afterKittingPrice;
        totalPriceEl.innerHTML = totalPrice.toLocaleString();
    });
}

function formSubmit() {
    const form = document.querySelector('form');
    form.addEventListener('submit', event =>
    event.target.querySelectorAll('input:disabled, select:disabled').forEach(
        e => e.disabled = false
    ));
}
