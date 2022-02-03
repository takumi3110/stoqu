document.addEventListener('DOMContentLoaded', function() {
    const el = document.querySelector('.main-title');
    const str = el.innerHTML.trim().split("");

    el.innerHTML = str.reduce((acc, curr) => {
        curr = curr.replace(/\s+/, '&nbsp;');
        return `${acc}<span class="char">${curr}</span>`;
    }, "");
});

function radioCheck(id, postData, url) {
    let checkOption = document.querySelector(id);
        checkOption.addEventListener('click', function() {
            console.log(document.querySelector(id).value);
            ajaxPost(postData, url);
        });
}

function ajaxPost(postData, url) {
    // kittingPrice.textContent = "";
    // const init = {method: 'GET'};
    const init = {
        method: 'POST',
        // credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    };
    fetch(url, init)
        .then(response => {
            if(response.ok) {
                return response.json();
            } else {
                throw Error();
            }
        })
        .then(data => {
            let price = 0;
            for(const orderItem of data.results) {
                price += orderItem.kitting_plan.price;
                // kittingPrice.innerHTML = '￥' + price.toLocaleString();
            }
        })
        .catch (error => {
            console.log(error);
        });
}