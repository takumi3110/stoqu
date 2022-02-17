document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('.navigation__title');
    const str = el.innerHTML.trim().split("");
    el.innerHTML = str.reduce((acc, curr) => {
        curr = curr.replace(/\s+/, '&nbsp;');
        return `${acc}<span class="char">${curr}</span>`;
    }, "");
});

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

function makeInit(data) {
    return {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data),
    }
}

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
    el.addEventListener('click', function() {
        location.href = url;
    });
}

function checkSelect(checkEl, el) {
    checkEl.addEventListener('click', function() {
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
    checkList.forEach(function(val) {
        if (val.checked) {
            flag = true;
        }
    });
    nextBtn.disabled = !flag;
}

class SelectDelete {
    constructor(el) {
        this.el = el;
    }
}

function tradeCheck() {
    const tradeHistory = document.querySelector('.order-detail__trade');
    const icon = document.querySelector('.order-detail__icon');
    tradeHistory.addEventListener('click', function() {
        icon.classList.toggle('selected');
    })
}
