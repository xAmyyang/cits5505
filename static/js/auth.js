'use strict';

const Auth = (() => {
  const PW_LEVELS = [
    { pct: 0, color: '#E8E6DF', label: '' },
    { pct: 20, color: '#D4537E', label: '😬 too weak' },
    { pct: 40, color: '#854F0B', label: '🤔 could be better' },
    { pct: 60, color: '#D85A30', label: '👍 getting there' },
    { pct: 80, color: '#3B6D11', label: '💪 strong' },
    { pct: 100, color: '#3B6D11', label: '🔥 very strong!' },
  ];

  function scorePassword(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    return score;
  }

  function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.type = input.type === 'password' ? 'text' : 'password';
    button.textContent = input.type === 'password' ? '👁' : '🙈';
    button.setAttribute(
      'aria-label',
      input.type === 'password' ? 'show password' : 'hide password'
    );
  }

  function renderPasswordStrength(password, barEl, labelEl, wrapEl) {
    if (!password) {
      wrapEl.hidden = true;
      return;
    }

    wrapEl.hidden = false;
    const level = PW_LEVELS[scorePassword(password)] || PW_LEVELS[1];
    barEl.style.width = `${level.pct}%`;
    barEl.style.backgroundColor = level.color;
    labelEl.textContent = level.label;
    labelEl.style.color = level.color;
  }

  function showToast(type, icon, message) {
    const text = `${icon} ${message}`;
    if (type === 'error') {
      window.alert(text);
      return;
    }
    console.info(text);
  }

  function socialSignIn(provider) {
    showToast('info', '⏳', `${provider} sign-in coming soon!`);
  }

  return {
    renderPasswordStrength,
    socialSignIn,
    togglePassword,
  };
})();
