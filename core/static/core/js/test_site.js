const desc = document.getElementById('description');
const btn = document.getElementById('toggleBtn');

btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', !expanded);
    btn.textContent = expanded ? 'Read more' : 'Read less';
    desc.classList.toggle('expanded');
});