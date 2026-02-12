document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[name="book"]');
    var bookItems = document.querySelectorAll('.book-list li');
    var allCheckbox = document.getElementById('all');

    function filterBooks() {
        var selectedCategories = [];
        
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked && checkbox.value !== 'all') {
                selectedCategories.push(checkbox.value);
            }
        });

        if (selectedCategories.length === 0) {
            bookItems.forEach(function(item) {
                item.style.display = 'block';
            });
        } else {
            bookItems.forEach(function(item) {
                var itemCategories = item.getAttribute('data-category') || '';
                var categoryList = itemCategories.split(' ');
                var shouldShow = selectedCategories.some(function(cat) {
                    return categoryList.indexOf(cat) !== -1;
                });
                item.style.display = shouldShow ? 'block' : 'none';
            });
        }
    }

    allCheckbox.addEventListener('change', function() {
        if (this.checked) {
            checkboxes.forEach(function(checkbox) {
                if (checkbox.value !== 'all') {
                    checkbox.checked = false;
                }
            });
        }
        filterBooks();
    });

    checkboxes.forEach(function(checkbox) {
        if (checkbox.value !== 'all') {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    allCheckbox.checked = false;
                }
                filterBooks();
            });
        }
    });

    filterBooks();
});
