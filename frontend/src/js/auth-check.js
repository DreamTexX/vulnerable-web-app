let hiddenWhenAuthenticated;
let visibleWhenAuthenticated;
let chirpForm;

window.addEventListener('load', function(event) {
    hiddenWhenAuthenticated = this.document.querySelectorAll('.hide-when-logged-in');
    visibleWhenAuthenticated = this.document.querySelectorAll('.visible-when-logged-in');

    this.fetch('/api/accounts/@me')
        .then(
            function(data) {
                if (data.status != 200) throw new Error();
                return data.json()
            }
        )
        .then(
            function(data) {
                for (const element of hiddenWhenAuthenticated) {
                    element.classList.add('hidden');
                }
                for (const element of visibleWhenAuthenticated) {
                    element.classList.remove('hidden');
                }
                document.querySelector('.email').innerHTML = data.username;
            }
        )
        .catch(
            function (err) {
                for (const element of hiddenWhenAuthenticated) {
                    element.classList.remove('hidden');
                }
                for (const element of visibleWhenAuthenticated) {
                    element.classList.add('hidden');
                }
            }
        )
});