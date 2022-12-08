window.addEventListener('load', function(event) {
    let form = document.querySelector('form');
    let errorField = document.querySelector('.errors');

    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        errorField.classList.add('hidden');
        errorField.innerText = '';

        let data = new FormData(ev.target);
        fetch('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(data)),
            headers: {
                'content-type': 'application/json',
            },
        })
            .then(
                function (data) {
                    if (data.status != 201) throw new Error();
                }
            ).then(
                function (data) {
                    window.location.href = "/";
                }
            ).catch(
                function (err) {
                    console.log(err);
                    errorField.innerText = "Please provide all fields!"
                    errorField.classList.remove('hidden');
                }
            );

        return true;
    });
});