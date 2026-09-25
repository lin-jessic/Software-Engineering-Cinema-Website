<script>
const slides = document.querySelectorAll('.ad-slide');
const prev = document.querySelector('.prev');
const next = document.querySelector('.next');
let index = 0;

function showSlide(i) {
  slides.forEach(s => s.classList.remove('active'));
  slides[i].classList.add('active');
}

prev.addEventListener('click', () => {
  index = (index === 0) ? slides.length - 1 : index - 1;
  showSlide(index);
});

next.addEventListener('click', () => {
  index = (index === slides.length - 1) ? 0 : index + 1;
  showSlide(index);
});
</script>