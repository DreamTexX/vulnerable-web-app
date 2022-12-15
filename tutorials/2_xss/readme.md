# XSS Tutorial

#### 0. (optional) Switch the branch 
```console
git stash
```
```console
git checkout fix-sql-injections
```

### 1. Use XSS to change the behavior of the site.
- Login as user1 with email "user1@email.com" and password "user1"
- Write a comment
- Try to insert html code like `<p></p>` or `<h1></h1>`
- See how the comment looks like
> If you can´t see the Html tags it means that it is interpreted
- Try to execute Javascript with `<script></script>`
- Write a comment that shows an image and by hovering over it the background changes to a matrix
> You can use the image element `<img>`
<br/>

> This is an example image: `https://images.wallpaperscraft.com/image/single/husky_puppies_couple_leisure_52671_1920x1200.jpg`
<br/>

> You can use `onmouseover=""` inside `<img>` which is triggered by hovering over the image
<br/>

> You can change the background to a matrix with `document.body.style.backgroundImage = 'url(https://media.tenor.com/IvyuPtEfzhoAAAAC/matrix.gif)'`

> Be aware that you need to escape some special characters <br/>
> `'` needs to be `\'`
- (optional) Write more comments that use XSS and permanently change something.
    - change background
    - register a user with a name that is an image
    - play a video
    - remove the content after the user logs in
    - ...

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
> You can add classes to an element with `element.classList.add("class1", "class2")` <br/>

> Add elements at the end of a list with `element.append(otherElement1, otherElement2);` <br/>
> Add elements at the beginning of a list with `element.prepend(otherEelemnt1, otherElement2);` <br/>
- Insert the input into these elements with `innerText` instead of `innerHtml` so it is escaped properly
- Now try again to create an XSS comment

