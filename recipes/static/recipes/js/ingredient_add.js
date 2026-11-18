document.getElementById('add_ingredient_btn').addEventListener('click',function(){
    const container = document.getElementById('ingredient_container');

    const firstRow = container.querySelector('.ingredient_row');
    const newRow = firstRow.cloneNode(true);

    newRow.querySelectorAll('input').forEach(input => {
        input.value = '';
    });

    container.appendChild(newRow);
});

document.getElementById('ingredient_container').addEventListener('click',function(e){
    if (e.target.classList.contains('remove_row_btn')){
        const container = document.getElementById('ingredient_container');
        const rows = container.querySelectorAll('.ingredient_row');

        if(rows.length > 1){
            e.target.closest('.ingredient_row').remove();
        }else{
            alert('最低１つの材料が必要です');
        }
    }
});