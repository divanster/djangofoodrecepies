document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const ratingValue = document.getElementById('rating_value');

    function setRating(rating) {
        ratingValue.value = rating;
        stars.forEach(star => {
            star.style.color = star.getAttribute('data-value') <= rating ? 'darkorange' : 'gold';
        });
    }

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute('data-value');
            setRating(rating);
        });

        star.addEventListener('mouseover', function () {
            const rating = this.getAttribute('data-value');
            stars.forEach(s => {
                s.style.color = s.getAttribute('data-value') <= rating ? 'darkorange' : 'gold';
            });
        });

        star.addEventListener('mouseout', function () {
            const rating = ratingValue.value || document.querySelector('.rating').getAttribute('data-rating');
            setRating(rating);
        });
    });

    // Initialize rating based on data-rating attribute
    const initialRating = document.querySelector('.rating').getAttribute('data-rating');
    if (initialRating) {
        setRating(initialRating);
    }
});
