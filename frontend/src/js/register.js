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
                async function (data) {
                    if (data.status != 201) throw new Error((await data.json()).error);
                    return data.json();
                }
            ).then(
                function (data) {
                    window.location.href = "/";
                }
            ).catch(
                function (err) {
                    errorField.innerText = err.error
                    errorField.classList.remove('hidden');
                }
            );

        return true;
    });
});