document.addEventListener('DOMContentLoaded', function(){
    const processContainer = document.getElementById('process_container');
    const addProcessBtn = document.getElementById('add_process_btn');

    function updateProcessNum(){
        const rows = processContainer.querySelectorAll('.process_row');
        rows.forEach((row, index) => {
            const stepNum = index + 1;
            const numLabel = row.querySelector('.process_num_label');
            const numInput = row.querySelector('.process_num_input');

            if(numLabel) numLabel.textContent = stepNum;
            if(numInput) numInput.value = stepNum;
        });
    }

    addProcessBtn.addEventListener('click', function(){
        const newRow = document.createElement('div');
        newRow.className = 'process_row';
        newRow.style.cssText = 'border: 1px solid #ddd; padding: 15px;margin-bottom:10px; border-radius:5px;';

        newRow.innerHTML = `
            <p><strong>手順 <span class="process_num_label"></span></strong></p>
            <input type="hidden" name="process_num[]" value="" class="process_num_input">
            
            <p>手順の詳細:<br>
                <textarea name="process_detail[]" placeholder="手順の説明を入力" rows="3" style="width: 100%;" required></textarea>
            </p>
            <p>手順の画像: <input type="file" name="process_img[]"></p>
            
            <button type="button" class="remove_process_btn">この手順を削除</button>
        `;

        processContainer.appendChild(newRow);
        updateProcessNum();
    });
    
    processContainer.addEventListener('click', function(e){
        if(e.target.classList.contains('remove_process_btn')){
            const rows = processContainer.querySelectorAll('.process_row');

            if(rows.length > 1){
                e.target.closest('.process_row').remove();
                updateProcessNum();
            }else{
                alert('手順は最低１つ必要です');
            }
        }
    });
});