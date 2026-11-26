document.addEventListener('DOMContentLoaded', () => {
    const processContainer = document.querySelector('#process_container');
    if (!processContainer) return;

    // 各行の初期状態をセットアップする関数
    const initProcessRow = (row) => {
        const previewArea = row.querySelector('.process_img_area');
        const previewImg = row.querySelector('.process_img');
        const changeBtn = row.querySelector('.change_processfile_btn');

        if (previewArea && previewImg && !previewImg.getAttribute('src')) {
            previewArea.style.display = 'none';
        }
        if (changeBtn) {
            changeBtn.style.display = 'none';
        }
    };

    // ページ読み込み時に既存の行を初期化
    processContainer.querySelectorAll('.process_row').forEach(initProcessRow);

    // 後から追加された行にも対応するため、コンテナ単位で初期化を監視
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains('process_row')) {
                    initProcessRow(node);
                }
            });
        });
    });
    observer.observe(processContainer, { childList: true });

    // ファイル選択時のプレビュー表示（動的に追加された input にも対応）
    processContainer.addEventListener('change', (event) => {
        const fileInput = event.target.closest('input[type="file"]');
        if (!fileInput) return;

        const row = fileInput.closest('.process_row');
        if (!row) return;
        const imgInput = row.querySelector('.process_img_input');
        const previewArea = row.querySelector('.process_img_area');
        const previewImg = row.querySelector('.process_img');
        const changeBtn = row.querySelector('.change_processfile_btn');

        if (!previewImg) return;

        const file = fileInput.files[0];

        if (!file) {
            previewImg.removeAttribute('src');
            // if (previewArea) previewArea.style.display = 'none';
            if (changeBtn) changeBtn.style.display = 'none';
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imgInput.style.display = 'none';
            if (previewArea) previewArea.style.display = 'block';
            if (changeBtn) changeBtn.style.display = 'inline-block';
        };

        reader.onerror = () => {
            previewImg.removeAttribute('src');
            if (previewArea) previewArea.style.display = 'none';
            if (changeBtn) changeBtn.style.display = 'none';
        };

        reader.readAsDataURL(file);
    });

    // 「画像を入れ替える」ボタンクリックで行内のファイル選択を開く
    processContainer.addEventListener('click', (event) => {
        const changeBtn = event.target.closest('.change_processfile_btn');
        if (!changeBtn) return;

        const row = changeBtn.closest('.process_row');
        const fileInput = row ? row.querySelector('input[type="file"]') : null;
        if (fileInput) {
            fileInput.click();
        }
    });
});