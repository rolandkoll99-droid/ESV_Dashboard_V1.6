// ============================================================
// CHROME.JS – Dark Mode & Toast, gemeinsam fürs Dashboard
// ============================================================

let theme = localStorage.getItem('stockschuetzen_theme') || 'light';

function initTheme() {
    document.documentElement.setAttribute('data-theme', theme);
    const btn = document.getElementById('btnTheme');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌓';
}

function toggleTheme() {
    theme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('stockschuetzen_theme', theme);
    const btn = document.getElementById('btnTheme');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌓';
    toast(`🌓 ${theme === 'dark' ? 'Dark' : 'Light'} Mode`);
}

function toast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timeout);
    t._timeout = setTimeout(() => t.classList.remove('show'), 2500);
}

document.addEventListener('DOMContentLoaded', initTheme);

window.toggleTheme = toggleTheme;
window.toast = toast;
window.initTheme = initTheme;
