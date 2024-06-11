'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let bookId = button.getAttribute('data-book-id');
    let bookTitle = button.getAttribute('data-book-title');
    let newUrl = `/books/delete/${bookId}`;
    let form = document.getElementById('deleteModalForm');
    let modalBookTitle = document.getElementById('modalBookTitle');

    form.action = newUrl;
    modalBookTitle.textContent = bookTitle;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);

document.addEventListener('DOMContentLoaded', function () {
    var easyMDE = new EasyMDE({element: document.getElementById('description')});
});