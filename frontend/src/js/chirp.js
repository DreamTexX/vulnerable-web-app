let chirpsList;

window.addEventListener('load', function (event) {
    chirpsList = document.querySelector('.chirps');
    fetchChirps();

    let form = document.querySelector('form');
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        let data = new FormData(ev.target);
        fetch('/api/posts', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(data)),
            headers: {
                'content-type': 'application/json',
            },
        })
            .then(
                function (data) {
                    if (data.status != 201) throw new Error();
                    return data.json();
                }
            ).then(
                function (data) {
                    addChirp(data, true);
                }
            ).catch(
                function (err) {
                    console.log(err);
                }
            );

        return true;
    });
});

function fetchChirps() {
    chirpsList.innerHTML = '';
    fetch('/api/posts')
        .then(
            function (data) {
                return data.json();
            }
        )
        .then(
            function (data) {
                for (const item of data) {
                    addChirp(item);
                }
            }
        )
        .catch(
            function (err) {
                console.log(err);
            }
        )
}

function addChirp(item, atTop = false) {
    let text = `
    <li class="flex flex-row gap-2 shadow-sm rounded-xl p-3 bg-white">
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path
                    d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z">
                </path>
            </svg>
        </div>
        <div class="flex flex-col gap-1">
            <div class="text-sm text-gray-400">
                ${item.username} &ctdot; ${item.created_at}
            </div>
            <div>
                ${item.content}
            </div>
        </div>
    </li>
    `;
    
    if (atTop) {
        chirpsList.innerHTML = text + chirpsList.innerHTML;
    } else {
        chirpsList.innerHTML += text;
    }
}