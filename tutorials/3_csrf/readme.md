# CSRF Tutorial

#### 0. (optional) Switch the branch 
```
git stash
```
```
git checkout fix-sql-injections
```

### 1. Use CSRF to create a link pointing to another site
> In this example the approach is very similar to an XSS attack and you use the same weak point of the application

- Login as user1 with email "use1@email.com" and password "user1"
- Instead of an image insert a link `<a href="link-to-website.com">link</a>` into the comment
- Look at the link preview at the bottom of the browser
- Try to change the previewed link without changing the actual destination
> The previewed link is taken from `href` inside the `<a>` tag 
<br/>

> You are able to set an href with javascript with `window.location.href = 'http://random-url.com'`

- Find a way to create a link, so that the preview refers to the application URL http://localhost:8080
- Add an `onClick` to the link tag which directs an user to another page, despite a different preview
> Be aware that you need to escape some special characters inside the python string <br/>
> `'` needs to be `\'`
- Try to steal the session cookie by adding it as a parameter to the URL
> You can read the session cookies in Javascript with `document.cookie`
<br/>

> You can encode http parameters with `encodeURIComponent(string_to_be_encoded)`
- Use a random URL which does not exist
- Click on the link 
- Now look at the URL if the session cookie is attached
