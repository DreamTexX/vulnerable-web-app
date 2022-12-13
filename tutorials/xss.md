# XSS Tutorial

#### 0. (optional) Switch the branch 
```console
git stash
```
```console
git checkout fix-sql-injections
```

### 1. Use XSS to change the behavior of the site.
- Login as user1 with email "use1@email.com" and password "user1"
- Write a comment
- Try to insert html code like `<p></p>`
- See how the comment looks like
- Html tags are not shown which means that they are interpreted
- Try to execute javascript with `<script></script>`
- Write the following comment:
```html
Hover over these two sweet huskies, and something good will happen:
<img 
    src="https://images.wallpaperscraft.com/image/single/husky_puppies_couple_leisure_52671_1920x1200.jpg" 
    onmouseover="document.body.style.backgroundImage = \'url(https://media.tenor.com/IvyuPtEfzhoAAAAC/matrix.gif)\'">
```
> Be aware that you need to escape some special characters inside the python string <br/>
> `'` needs to be `\'`
- (optional) Write more comments that use XSS and permanently change something.
> ideas: change background; register a user with a name that is an image; show a video; remove the content after the user logs in

<br/>

### 2. Repair the application, so that it is not possible to use XSS.
- Take a look at 
    - [frontend/src/js/chirp.js](../frontend/src/js/chirp.js)
    - [frontend/src/js/auth-check.js](../frontend/src/js/auth-check.js)
- The main task is to replace `innerHtml` with `innerText` 

<br/>

- But there are also some other aspects to be aware of in [chirp.js](../frontend/src/js/chirp.js)
- The method `addChirp()` adds a new comment to the page
- The chirps are put inside a string which contains html and uses input without validation or escaping
- This string is inserted with `innerHtml` which is why the whole string is interpreted as html including the input
- Extract the part from the string which contains the input
> You could replace the whole string with seperate elements but the svg has some complex contents, so it might be easier to keep the svg part as string and add it also as `innerHtml` to the corresponding parent element 
<br/>

> Don't forget to create the outer list and to add the svg to it
- For all extracted parts create new elements
> You can create a Html element with `document.createElement("name_of_element")` <br/>
> You can add classes to an element with `element.classList.add("flex", "flex-col", "gap-1", "content")` <br/>

> Add elements at the end of a list with `element.append(otherElement1, otherElement2);` <br/>
> Add elements at the beginning of a list with `element.prepend(otherEelemnt1, otherElement2);` <br/>
- Insert the input into these elements with `innerText` instead of `innerHtml` so it is escaped
- Now try again to create an XSS comment

