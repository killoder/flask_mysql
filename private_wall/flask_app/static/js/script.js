const replyBtns = document.querySelectorAll('.reply-btn');
const replyForms = document.querySelectorAll('.reply-form');

for (let i = 0; i < replyBtns.length; i++) {
    replyBtns[i].addEventListener('click', function () {
        // Hide the reply button
        replyBtns[i].style.display = 'none';

        // Hide all other reply forms
        for (let j = 0; j < replyForms.length; j++) {
            if (j !== i) {
                replyForms[j].style.display = 'none';
            }
        }
        // Show the corresponding reply form
        replyForms[i].style.display = 'block';
    });
}