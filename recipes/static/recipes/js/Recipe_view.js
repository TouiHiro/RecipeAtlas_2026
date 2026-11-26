document.addEventListener('DOMContentLoaded', () => {
    const thumbnailArea = document.querySelector('#thumbnail_area');
    const fileInput = document.querySelector('#file_input');
    const thumbnailImg = document.querySelector('#thumbnail_img');
    const selectBtn = document.querySelector('#select_file_btn');
    const changeBtn = document.querySelector('#change_file_btn');

    if (!fileInput || !thumbnailImg) return;

    // 初期状態で src がなければ非表示
    if (!thumbnailImg.getAttribute('src')) {
        thumbnailArea.style.display = 'none';
    }

    if (changeBtn) {
        changeBtn.style.display = 'none';
    }

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];

        if (!file) {
            thumbnailImg.removeAttribute('src');
            thumbnailArea.style.display = 'none'; // キャンセル時に非表示へ戻す
            if (changeBtn) changeBtn.style.display = 'none';
            if (selectBtn) selectBtn.style.display = '';
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            thumbnailImg.src = e.target.result;
            thumbnailArea.style.display = 'block'; 
            if (changeBtn) changeBtn.style.display = 'inline-block';
            if (selectBtn) selectBtn.style.display = 'none';
        };

        reader.onerror = () => {
            thumbnailImg.removeAttribute('src');
            thumbnailImg.style.display = 'none';
            if (changeBtn) changeBtn.style.display = 'none';
            if (selectBtn) selectBtn.style.display = '';
        };

        reader.readAsDataURL(file);
    });

    if (changeBtn) {
        changeBtn.addEventListener('click', () => {
            fileInput.click();
        });
    }
});