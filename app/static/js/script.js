document.addEventListener('DOMContentLoaded', () => {
  const carrossel = document.querySelector('.carrossel');
  let isDown = false;
  let startX;
  let scrollLeft;

  carrossel.addEventListener('mousedown', (e) => {
    isDown = true;
    carrossel.style.cursor = 'grabbing';
    startX = e.pageX - carrossel.offsetLeft;
    scrollLeft = carrossel.scrollLeft;
  });

  carrossel.addEventListener('mouseleave', () => {
    isDown = false;
    carrossel.style.cursor = 'grab';
  });

  carrossel.addEventListener('mouseup', () => {
    isDown = false;
    carrossel.style.cursor = 'grab';
  });

  carrossel.addEventListener('mousemove', (e) => {
    if(!isDown) return;
    e.preventDefault();
    const x = e.pageX - carrossel.offsetLeft;
    const walk = (x - startX) * 2; 
    carrossel.scrollLeft = scrollLeft - walk;
  });

  carrossel.addEventListener('touchstart', (e) => {
    isDown = true;
    startX = e.touches[0].pageX - carrossel.offsetLeft;
    scrollLeft = carrossel.scrollLeft;
  });

  carrossel.addEventListener('touchend', () => {
    isDown = false;
  });

  carrossel.addEventListener('touchmove', (e) => {
    if(!isDown) return;
    const x = e.touches[0].pageX - carrossel.offsetLeft;
    const walk = (x - startX) * 2;
    carrossel.scrollLeft = scrollLeft - walk;
  });
});