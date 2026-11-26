document.addEventListener('DOMContentLoaded', function () {
    const processContainer = document.getElementById('process_container');
    const addProcessBtn = document.getElementById('add_process_btn');

    if (!processContainer || !addProcessBtn) return;

    function updateProcessNum() {
        const rows = processContainer.querySelectorAll('.process_row');
        rows.forEach((row, index) => {
            const stepNum = index + 1;
            const numLabel = row.querySelector('.process_num_label');
            const numInput = row.querySelector('.process_num_input');
            const imgInput = row.querySelector('input[type="file"]');

            if (numLabel) numLabel.textContent = stepNum;
            if (numInput) numInput.value = stepNum;
            if (imgInput) imgInput.name = `process_img_${stepNum}`;
        });
    }

    // 初期表示時の番号を同期
    updateProcessNum();

    addProcessBtn.addEventListener('click', function () {
        const newRow = document.createElement('div');
        newRow.className = 'process_row';
        newRow.style.cssText = ' padding: 15px; margin-bottom: 10px; border-radius: 5px;';

        newRow.innerHTML = `
            <p>
                <strong>STEP <span class="process_num_label"></span></strong>
            </p>
            <input type="hidden" name="process_num[]" value="1" class="process_num_input">
            <p>
                詳細<br>
                <textarea name="process_detail[]" placeholder="手順の説明を入力" rows="3" required></textarea>
            </p>
            <div class="process_img_input">
                <p>
                    Image：<input type="file" name="process_img[]" accept="image/*">
                </p>
            </div>
            <div class="process_img_area">
                <img class="process_img" alt="プレビュー">
            </div>
            <button type="button" class="change_processfile_btn">
                画像を入れ替える
            </button>
            <button type="button" class="remove_process_btn" aria-label="手順削除">×</button>
        `;

        processContainer.appendChild(newRow);
        updateProcessNum();
    });

    processContainer.addEventListener('click', function (e) {
        const removeBtn = e.target.closest('.remove_process_btn');
        if (!removeBtn) return;

        const rows = processContainer.querySelectorAll('.process_row');
        if (rows.length > 1) {
            removeBtn.closest('.process_row').remove();
            updateProcessNum();
        } else {
            alert('手順は最低１つ必要です');
        }
    });
});