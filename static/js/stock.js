document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('.main-title');
    const str = el.innerHTML.trim().split("");

    el.innerHTML = str.reduce((acc, curr) => {
        curr = curr.replace(/\s+/, '&nbsp;');
        return `${acc}<span class="char">${curr}</span>`;
    }, "");
});

// function radioCheck(id, data, url) {
//     let checkOption = document.querySelector(id);
//     checkOption.addEventListener('click', function() {
//         let result = putData(url, data);
//         // console.log(result)
//     });
// }

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

// async function putData(url=url, data=data) {
//     const init = {
//         method: 'PUT',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken
//         },
//         body: JSON.stringify(data),
//     };
//     return await fetch(url, init)
//         .then(response => {
//             if (response.ok) {
//                 return response.json();
//             } else {
//                 throw Error();
//             }
//         })
//         .then(data => {
//             console.log(data)
//         })
// }

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

