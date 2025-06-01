  function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    const tagsContainer = document.getElementById('recipients-tags');
    const tagsInput = document.getElementById('recipients-input');
    const tagsHidden = document.getElementById('recipients-hidden');
    const feedback = document.getElementById('recipients-feedback');
    let tags = [];
    let selectedTagIndexes = [];

    function addTag(value) {
        value = value.trim().replace(/,$/, '');
        if (value) {
            const parts = value.split(',');
            const valid = parts.length === 2 && validateEmail(parts[0].trim());
            tags.push({text: value, valid});
        }
    }

    function renderTags() {
        tagsContainer.querySelectorAll('.tag').forEach(tag => tag.remove());
        let allValid = true;
        tags.forEach((tag, idx) => {
            const tagElem = document.createElement('span');
            tagElem.className = 'tag' + (tag.valid ? '' : ' invalid') + (selectedTagIndexes.includes(idx) ? ' selected' : '');
            tagElem.setAttribute('data-idx', idx);
            tagElem.innerHTML =
                (tag.valid ? '✔️ ' : '❌ ') + tag.text +
                `<span class="remove-tag" data-idx="${idx}" style="margin-left:8px;">&times;</span>`;
            tagsContainer.insertBefore(tagElem, tagsInput);
            if (!tag.valid) allValid = false;
        });
        tagsHidden.value = tags.map(t => t.text).join('\n');
        feedback.innerHTML = allValid || tags.length === 0
            ? ''
            : '<span style="color:#d32f2f;">Some recipients are invalid. Please fix or remove them.</span>';
    }

    tagsContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-tag')) {
            const idx = Number(e.target.dataset.idx);
            tags.splice(idx, 1);
            selectedTagIndexes = selectedTagIndexes.filter(i => i !== idx).map(i => i > idx ? i - 1 : i);
            renderTags();
            return;
        }
        if (e.target.classList.contains('tag')) {
            const idx = Number(e.target.getAttribute('data-idx'));
            if (e.ctrlKey || e.metaKey) {
                if (selectedTagIndexes.includes(idx)) {
                    selectedTagIndexes = selectedTagIndexes.filter(i => i !== idx);
                } else {
                    selectedTagIndexes.push(idx);
                }
            } else if (e.shiftKey && selectedTagIndexes.length > 0) {
                const last = selectedTagIndexes[selectedTagIndexes.length - 1];
                const [start, end] = [Math.min(last, idx), Math.max(last, idx)];
                selectedTagIndexes = [];
                for (let i = start; i <= end; i++) selectedTagIndexes.push(i);
            } else {
                selectedTagIndexes = [idx];
            }
            renderTags();
        } else {
            tagsInput.focus();
        }
    });

    tagsInput.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'a') {
            e.preventDefault();
            selectedTagIndexes = tags.map((_, idx) => idx);
            renderTags();
        } else if ((e.key === 'Delete' || e.key === 'Backspace') && selectedTagIndexes.length > 0 && tagsInput.value === '') {
            selectedTagIndexes.sort((a, b) => b - a).forEach(idx => tags.splice(idx, 1));
            selectedTagIndexes = [];
            renderTags();
        } else if (e.key === 'Enter' || e.key === 'Tab') {
            e.preventDefault();
            let value = tagsInput.value.trim();
            if (value.includes('\n')) {
                value.split('\n').forEach(line => addTag(line));
            } else {
                addTag(value);
            }
            tagsInput.value = '';
            renderTags();
        } else if (e.key === 'Backspace' && tagsInput.value === '' && tags.length > 0 && selectedTagIndexes.length === 0) {
            tags.pop();
            renderTags();
        }
    });

    tagsInput.addEventListener('paste', function(e) {
        e.preventDefault();
        let paste = (e.clipboardData || window.clipboardData).getData('text');
        paste.split('\n').forEach(line => addTag(line));
        tagsInput.value = '';
        renderTags();
    });

    document.getElementById('remove-selected').addEventListener('click', function() {
        selectedTagIndexes.sort((a, b) => b - a).forEach(idx => tags.splice(idx, 1));
        selectedTagIndexes = [];
        renderTags();
    });

    document.getElementById('remove-all').addEventListener('click', function() {
        tags = [];
        selectedTagIndexes = [];
        renderTags();
    });