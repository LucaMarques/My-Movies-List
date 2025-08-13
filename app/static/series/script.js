document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('search-input');
    const suggestions = document.getElementById('search-suggestions');

    input.addEventListener('input', function () {
        const query = input.value.trim();
        if (query.length < 2) {
            suggestions.innerHTML = '';
            return;
        }

        fetch(`/sugestoes?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestions.innerHTML = '';
                data.forEach(filme => {
                    const div = document.createElement('div');
                    div.textContent = filme.titulo;
                    div.onclick = () => {
                        window.location.href = `/series/${filme.id}`;  // usa sua rota existente
                    };
                    suggestions.appendChild(div);
                });
            });
    });
});