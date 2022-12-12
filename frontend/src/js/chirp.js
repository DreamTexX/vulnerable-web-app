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
                    form.reset();
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
    let listItem = document.createElement("li");
    listItem.classList.add("flex", "flex-row", "gap-2", "shadow-sm", "rounded-xl", "p-3", "bg-white");
    // We can safely append html here, because there is no user input
    listItem.innerHTML = `
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path
                        d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z">
                    </path>
                </svg>
            </div>`;
    
    // Create a container for user input
    let container = document.createElement("div");
    container.classList.add("flex", "flex-col", "gap-1", "content")

    // create new childs for elements where user content will be placed:
    let usernameAndTimeRow = document.createElement("div");
    usernameAndTimeRow.classList.add("text-sm", "text-gray-400"); // Add classes for styling
    usernameAndTimeRow.innerText = `${item.username} ⋯ ${item.created_at}` // safely insert username and timestamp into element
    
    let contentRow = document.createElement("div");
    contentRow.innerText = item.content; // safely insert chirp content into element

    container.append(usernameAndTimeRow, contentRow) // Insert both elements into boostrapped template
    listItem.append(container);
    
    if (atTop) {
        chirpsList.prepend(listItem); // Add new chrip at top
    } else {
        chirpsList.append(listItem); // Add new chirp at bottom
    }
}