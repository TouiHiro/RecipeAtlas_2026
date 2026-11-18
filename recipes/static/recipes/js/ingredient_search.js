document.addEventListener('DOMContentLoaded', function(){
    document.addEventListener('input', function(e){
        if(e.target.classList.contains('ingredient_search_input')){
            const input = e.target;
            const query = input.value.trim();
            // closestメソッドは呼び出した要素自身、またはその祖先要素の中から
            // 指定したCSSセレクタに一致する最も近い要素を検索して返す
            const row = input.closest('.ingredient_row');
            const suggestionBox = row.querySelector('.suggestions_box');
            const hiddenIdInput = row.querySelector('.ingredient_id');

            hiddenIdInput.value = '';

            if(query === ''){
                suggestionBox.innerHTML = '';
                suggestionBox.style.display = 'none';
                return;
            }
            // viewsのsearch_ingredientsにgetリクエストを送信
            // .thenは非同期処理が成功したときにその結果を受け取って
            // 次の処理を事項するためのPromiseインスタンスのメソッド
            fetch(`/recipe/search_ingredients/?q=${encodeURIComponent(query)}`)
                // サーバからからのresponseをjsonオブジェクトに変換する
                .then(response => response.json())
                // 変換されたデータを受け取り画面を更新する処理
                .then(data => {
                    // 前回の検索結果が残らないようにクリア
                    suggestionBox.innerHTML = '';
                    if( data.results && data.results.length > 0){
                        suggestionBox.style.display = 'block';
                        data.results.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'suggestion_item';
                            div.textContent = item.name;
                            div.style.cssText = 'padding:8px; cursor:pointer; background: #fff; border-bottom:1px solid #eee;';

                            div.addEventListener('mouseenter', () => div.style.backgroundColor = '#f0f0f0');
                            div.addEventListener('mouseleave', () => div.style.backgroundColor = '#fff');

                            div.addEventListener('click', function(){
                                input.value = item.name;
                                hiddenIdInput.value = item.id;
                                suggestionBox.innerHTML = '';
                                suggestionBox.style.display = 'none';
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

    document.addEventListener('click', function(e){
        if(!e.target.closest('.search_wrapper')){
            document.querySelectorAll('.suggestions_box').forEach(box => {
                box.innerHTML = '';
                box.style.display = 'none';
            });
        }
    });
});