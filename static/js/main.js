let slideIndex = 1;
let slideInterval;

function showSlides(n) {
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }

    // Убираем класс active у всех слайдов
    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }

    // Убираем активный класс у всех точек
    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }

    // Добавляем класс active текущему слайду
    if (slides[slideIndex - 1]) {
        slides[slideIndex - 1].classList.add("active");
    }
    // Добавляем активный класс для соответствующей точки
    if (dots[slideIndex - 1]) {
        dots[slideIndex - 1].classList.add("active");
    }
}

function changeSlide(n) {
    showSlides(slideIndex += n);
    resetInterval();
}

function currentSlide(n) {
    showSlides(slideIndex = n);
    resetInterval();
}

function resetInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(function() {
        changeSlide(1);
    }, 3000);
}

function openStatusModal(bookingId, currentStatus) {
    const modal = document.getElementById('statusModal');
    const bookingIdDisplay = document.getElementById('bookingIdDisplay');
    const bookingIdInput = document.getElementById('bookingIdInput');
    const statusSelect = document.getElementById('statusSelect');

    bookingIdDisplay.textContent = bookingId;
    bookingIdInput.value = bookingId;
    statusSelect.value = currentStatus;

    modal.style.display = "block";
}

function showReviewModal(reviewText, bookingId) {
    const modal = document.getElementById('reviewModal');
    const reviewTextDisplay = document.getElementById('reviewTextDisplay');
    const reviewBookingId = document.getElementById('reviewBookingId');

    if (reviewTextDisplay) {
        reviewTextDisplay.textContent = reviewText;
    }
    if (reviewBookingId) {
        reviewBookingId.textContent = bookingId;
    }
    if (modal) {
        modal.style.display = "block";
    }
}

function closeModal() {
    const modal = document.getElementById('statusModal');
    if (modal) {
        modal.style.display = "none";
    }
}

function closeReviewModal() {
    const modal = document.getElementById('reviewModal');
    if (modal) {
        modal.style.display = "none";
    }
}

function showReview(reviewText) {
    const modal = document.getElementById('reviewModal');
    const reviewTextElement = document.getElementById('reviewText');
    if (reviewTextElement) {
        reviewTextElement.textContent = reviewText;
    }
    if (modal) {
        modal.style.display = "block";
    }
}

function phoneMask(input) {
    let cursorPos = input.selectionStart || 0;
    let oldValue = input.value;

    let digits = oldValue.replace(/\D/g, '');

    if (digits.length > 0) {
        if (digits[0] === '8') {
            digits = '7' + digits.slice(1);
        } else if (digits[0] !== '7') {
            digits = '7' + digits;
        }
    }

    digits = digits.slice(0, 11);

    let formatted = '';
    if (digits.length > 0) formatted = '+' + digits[0];
    if (digits.length > 1) formatted += ' (' + digits.slice(1, 4);
    if (digits.length > 4) formatted += ') ' + digits.slice(4, 7);
    if (digits.length > 7) formatted += '-' + digits.slice(7, 9);
    if (digits.length > 9) formatted += '-' + digits.slice(9, 11);

    input.value = formatted;

    let digitsBeforeCursor = oldValue.slice(0, cursorPos).replace(/\D/g, '').length;
    let newCursorPos = 0;
    let countedDigits = 0;

    for (let i = 0; i < formatted.length; i++) {
        if (countedDigits === digitsBeforeCursor) {
            newCursorPos = i;
            break;
        }
        if (/\d/.test(formatted[i])) {
            countedDigits++;
        }
    }

    if (newCursorPos === 0 && digitsBeforeCursor > 0) {
        newCursorPos = formatted.length;
    }

    input.setSelectionRange(newCursorPos, newCursorPos);
}

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация слайдера
    if (document.getElementsByClassName('mySlides').length > 0) {
        showSlides(slideIndex);
        slideInterval = setInterval(function() {
            changeSlide(1);
        }, 3000);
    }

    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.onclick = function() {
            closeModal();
        };
    }

    const closeReviewBtn = document.querySelector('.close-review');
    if (closeReviewBtn) {
        closeReviewBtn.onclick = function() {
            closeReviewModal();
        };
    }

    window.onclick = function(event) {
        const statusModal = document.getElementById('statusModal');
        const reviewModal = document.getElementById('reviewModal');
        if (event.target == statusModal) {
            statusModal.style.display = "none";
        }
        if (event.target == reviewModal) {
            reviewModal.style.display = "none";
        }
    }

    const phoneInput = document.getElementById('id_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let cursorPos = this.selectionStart;
            let oldLength = this.value.length;
            phoneMask(this);
            let newLength = this.value.length;
            let diff = newLength - oldLength;
            if (diff > 0) {
                this.setSelectionRange(cursorPos + diff, cursorPos + diff);
            } else {
                this.setSelectionRange(cursorPos, cursorPos);
            }
        });

        phoneInput.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' || e.key === 'Delete') {
                setTimeout(() => {
                    phoneMask(this);
                }, 10);
            }
        });

        if (phoneInput.value) {
            phoneMask(phoneInput);
        }
    }

    const dateInput = document.querySelector('input[type="datetime-local"]');
    if (dateInput) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const hours = String(today.getHours()).padStart(2, '0');
        const minutes = String(today.getMinutes()).padStart(2, '0');
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        dateInput.min = minDateTime;
    }
});