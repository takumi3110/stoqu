document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('.main-title');
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
    // let radio = document.querySelectorall(el);
    // for (i = 0; i < radio.length - 1; i++) {
    //     if (radio.checked) {
    //         return true;
    //     } else {
    //         let result = false;
    //     }
    // }
// }
