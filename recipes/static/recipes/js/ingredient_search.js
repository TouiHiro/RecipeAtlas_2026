document.addEventListener('DOMContentLoaded', function(){
    const form = document.querySelector('form');
    const warningBox = document.getElementById('ingredient-warning');

    function showWarning(message) {
        if (warningBox) {
            warningBox.textContent = message;
            warningBox.style.display = 'block';
            warningBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert(message);
        }
    }

    function clearWarning() {
        if (warningBox) {
            warningBox.textContent = '';
            warningBox.style.display = 'none';
        }
    }

    document.addEventListener('input', function(e){
        if(e.target.classList.contains('ingredient_search_input')){
            const input = e.target;
            const query = input.value.trim();
            const row = input.closest('.ingredient_row');
            const suggestionBox = row.querySelector('.suggestions_box');
            const hiddenIdInput = row.querySelector('.ingredient_id');

            hiddenIdInput.value = '';
            clearWarning();

            if(query === ''){
                suggestionBox.innerHTML = '';
                suggestionBox.style.display = 'none';
                return;
            }

            fetch(`/recipes/search_ingredients/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionBox.innerHTML = '';
                    if(data.results && data.results.length > 0){
                        suggestionBox.style.display = 'block';
                        data.results.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'suggestion_item';
                            div.textContent = item.name;
                            div.style.cssText = 'padding:8px; cursor:pointer; background: #fff; border-bottom:1px solid #eee;';

                            div.addEventListener('mouseenter', () => div.style.backgroundColor = '#f0f0f0');
                            div.addEventListener('mouseleave', () => div.style.backgroundColor = '#fff');

                            div.addEventListener('mousedown', function(ev){
                                ev.preventDefault();
                                input.value = item.name;
                                hiddenIdInput.value = item.id;
                                suggestionBox.innerHTML = '';
                                suggestionBox.style.display = 'none';
                                clearWarning();
                            });

                            suggestionBox.appendChild(div);
                        });
                    }else{
                        suggestionBox.style.display = 'none';
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });

    if(form){
        form.addEventListener('submit', function(e){
            const rows = document.querySelectorAll('.ingredient_row');
            for(const row of rows){
                const nameInput = row.querySelector('.ingredient_search_input');
                const idInput = row.querySelector('.ingredient_id');
                const weightInput = row.querySelector('input[name="weight[]"]');

                const nameVal = nameInput ? nameInput.value.trim() : '';
                const idVal = idInput ? idInput.value.trim() : '';
                const weightVal = weightInput ? weightInput.value.trim() : '';

                if(nameVal && !idVal){
                    e.preventDefault();
                    showWarning(`「${nameVal}」は登録されていない食材です。候補から選択してください。`);
                    nameInput.focus();
                    return;
                }

                if(weightVal && !idVal){
                    e.preventDefault();
                    showWarning('食材を候補から選択してください。');
                    nameInput.focus();
                    return;
                }
            }
            clearWarning();
        });
    }

    document.addEventListener('click', function(e){
        if(!e.target.closest('.search_wrapper')){
            document.querySelectorAll('.suggestions_box').forEach(box => {
                box.innerHTML = '';
                box.style.display = 'none';
            });
        }
    });
});