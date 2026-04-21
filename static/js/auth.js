/**
 * auth.js — SurviveChef authentication logic
 *
 * Responsibilities:
 *   • Client-side user registry  (localStorage: SC_USERS)
 *   • Session management         (localStorage / sessionStorage: SC_SESSION)
 *   • Password hashing           (Web Crypto API — SHA-256 + app salt)
 *   • Form validation            (email, name, password, confirm, terms)
 *   • Password strength meter
 *   • Live duplicate-email check
 *   • Login handler
 *   • Sign-up handler
 *   • Social sign-in stub
 *   • Session restore / redirect guard
 *   • Toast notification
 *
 * No dependencies — vanilla ES2018+, Web Crypto API.
 * Both login.html and signup.html load this single file.
 */

'use strict';

const Auth = (() => {

  /* ──────────────────────────────────────────
     CONSTANTS
  ────────────────────────────────────────── */
  const STORAGE_USERS   = 'SC_USERS';
  const STORAGE_SESSION = 'SC_SESSION';
  const PW_SALT         = 'SC_SALT_2025_survivechef';
  const MIN_PW_SCORE    = 2;   // out of 5 — anything below is rejected
  const FAKE_DELAY      = 750; // ms — simulates a network round-trip

  /* ──────────────────────────────────────────
     STORAGE
  ────────────────────────────────────────── */
  function getUsers() {
    try { return JSON.parse(localStorage.getItem(STORAGE_USERS)) || []; }
    catch { return []; }
  }

  function saveUsers(users) {
    localStorage.setItem(STORAGE_USERS, JSON.stringify(users));
  }

  function getSession() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_SESSION))
          || JSON.parse(sessionStorage.getItem(STORAGE_SESSION))
          || null;
    } catch { return null; }
  }

  /**
   * Persist a session.
   * @param {object}  user
   * @param {boolean} remember — true → localStorage, false → sessionStorage
   */
  function saveSession(user, remember) {
    const payload = JSON.stringify({
      uid:   user.uid,
      name:  user.name,
      email: user.email,
      ts:    Date.now(),
    });
    if (remember) {
      localStorage.setItem(STORAGE_SESSION, payload);
      sessionStorage.removeItem(STORAGE_SESSION);
    } else {
      sessionStorage.setItem(STORAGE_SESSION, payload);
      localStorage.removeItem(STORAGE_SESSION);
    }
  }

  /* ──────────────────────────────────────────
     CRYPTO
  ────────────────────────────────────────── */
  async function hashPassword(password) {
    const data    = new TextEncoder().encode(PW_SALT + password);
    const hashBuf = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hashBuf))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }

  /* ──────────────────────────────────────────
     VALIDATORS
  ────────────────────────────────────────── */
  const Validators = {
    name(v) {
      if (!v || v.trim().length < 2) return 'name must be at least 2 characters';
      if (v.trim().length > 60)      return 'name is too long';
      return null;
    },
    email(v) {
      if (!v || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()))
        return 'please enter a valid email address';
      return null;
    },
    password(v) {
      if (!v || v.length < 8)  return 'password must be at least 8 characters';
      if (v.length > 128)      return 'password is too long';
      return null;
    },
  };

  /* ──────────────────────────────────────────
     PASSWORD STRENGTH
  ────────────────────────────────────────── */
  const PW_LEVELS = [
    { pct:   0, color: '#E8E6DF', label: ''                    },
    { pct:  20, color: '#D4537E', label: '😬 too weak'         },
    { pct:  40, color: '#854F0B', label: '🤔 could be better'  },
    { pct:  60, color: '#D85A30', label: '👍 getting there'    },
    { pct:  80, color: '#3B6D11', label: '💪 strong'           },
    { pct: 100, color: '#3B6D11', label: '🔥 very strong!'     },
  ];

  function scorePassword(pw) {
    let s = 0;
    if (pw.length >= 8)           s++;
    if (pw.length >= 12)          s++;
    if (/[A-Z]/.test(pw))         s++;
    if (/[0-9]/.test(pw))         s++;
    if (/[^A-Za-z0-9]/.test(pw))  s++;
    return s; // 0-5
  }

  /**
   * Update the strength meter DOM elements.
   * @param {string}      pw
   * @param {HTMLElement} barEl
   * @param {HTMLElement} labelEl
   * @param {HTMLElement} wrapEl  — the container (toggled with hidden attr)
   */
  function renderPasswordStrength(pw, barEl, labelEl, wrapEl) {
    if (!pw) { wrapEl.hidden = true; return; }
    wrapEl.hidden = false;

    const score = scorePassword(pw);
    const level = PW_LEVELS[score] || PW_LEVELS[1];
    barEl.style.width           = level.pct + '%';
    barEl.style.backgroundColor = level.color;
    labelEl.textContent         = level.label;
    labelEl.style.color         = level.color;
  }

  /* ──────────────────────────────────────────
     FIELD UI HELPERS
  ────────────────────────────────────────── */
  function fieldError(inputId, errId, msg) {
    const input = document.getElementById(inputId);
    const err   = document.getElementById(errId);
    if (input) { input.classList.add('is-error'); input.classList.remove('is-valid'); }
    if (err)   err.textContent = '⚠️ ' + msg;
  }

  function fieldValid(inputId, errId) {
    const input = document.getElementById(inputId);
    const err   = document.getElementById(errId);
    if (input) { input.classList.remove('is-error'); input.classList.add('is-valid'); }
    if (err)   err.textContent = '';
  }

  function fieldReset(inputId, errId) {
    const input = document.getElementById(inputId);
    const err   = document.getElementById(errId);
    if (input) { input.classList.remove('is-error', 'is-valid'); }
    if (err)   err.textContent = '';
  }

  function showGlobalError(bannerId, msgId, msg) {
    const banner = document.getElementById(bannerId);
    const msgEl  = document.getElementById(msgId);
    if (!banner || !msgEl) return;
    msgEl.textContent = msg;
    banner.hidden = false;
  }

  function hideGlobalError(bannerId) {
    const banner = document.getElementById(bannerId);
    if (banner) banner.hidden = true;
  }

  /* ──────────────────────────────────────────
     BUTTON LOADING STATE
  ────────────────────────────────────────── */
  function setLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.classList.toggle('loading', loading);
  }

  /* ──────────────────────────────────────────
     TOAST
  ────────────────────────────────────────── */
  let _toastTimer = null;

  function _ensureToast() {
    let el = document.getElementById('scToast');
    if (el) return el;
    el = document.createElement('div');
    el.id = 'scToast';
    el.className = 'auth-toast';
    el.innerHTML = '<span id="scToastIcon"></span><span id="scToastMsg"></span>';
    document.body.appendChild(el);
    return el;
  }

  function showToast(type, icon, msg, duration = 3500) {
    const el  = _ensureToast();
    document.getElementById('scToastIcon').textContent = icon;
    document.getElementById('scToastMsg').textContent  = msg;
    el.className = `auth-toast ${type} show`;
    clearTimeout(_toastTimer);
    _toastTimer = setTimeout(() => el.classList.remove('show'), duration);
  }

  /* ──────────────────────────────────────────
     MISC UTILITIES
  ────────────────────────────────────────── */
  function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

  function genUID() {
    return 'SC_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
  }

  /* ──────────────────────────────────────────
     PASSWORD TOGGLE
  ────────────────────────────────────────── */
  function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.type    = input.type === 'password' ? 'text' : 'password';
    btn.textContent   = input.type === 'password' ? '👁' : '🙈';
    btn.setAttribute('aria-label', input.type === 'password' ? 'show password' : 'hide password');
  }

  /* ──────────────────────────────────────────
     LIVE DUPLICATE EMAIL CHECK  (sign-up)
  ────────────────────────────────────────── */
  function checkEmailDuplicate(inputId, errId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const email = input.value.trim().toLowerCase();
    if (!email || Validators.email(email)) return; // wait for valid format
    const dup = getUsers().find(u => u.email === email);
    if (dup) {
      fieldError(inputId, errId, 'an account with this email already exists');
    }
  }

  /* ──────────────────────────────────────────
     REDIRECT GUARD
  ────────────────────────────────────────── */
  function redirectIfLoggedIn(target) {
    if (getSession()) window.location.replace(target);
  }

  /* ──────────────────────────────────────────
     SOCIAL SIGN-IN STUB
  ────────────────────────────────────────── */
  function socialSignIn(provider) {
    showToast('info', '⏳', `${provider} sign-in coming soon!`);
    // TODO: replace with real OAuth redirect:
    // window.location.href = `/auth/${provider.toLowerCase()}`;
  }

  /* ══════════════════════════════════════════
     LOGIN HANDLER
  ══════════════════════════════════════════ */
  async function handleLogin() {
    const emailEl    = document.getElementById('loginEmail');
    const passwordEl = document.getElementById('loginPassword');
    const rememberEl = document.getElementById('rememberMe');

    const email    = (emailEl?.value    || '').trim().toLowerCase();
    const password =  passwordEl?.value || '';
    const remember =  rememberEl?.checked ?? true;

    // Reset previous state
    hideGlobalError('loginGlobalErr');
    fieldReset('loginEmail',    'loginEmailErr');
    fieldReset('loginPassword', 'loginPasswordErr');

    // Validate
    let valid = true;

    const emailErr = Validators.email(email);
    if (emailErr) { fieldError('loginEmail', 'loginEmailErr', emailErr); valid = false; }

    if (!password) { fieldError('loginPassword', 'loginPasswordErr', 'please enter your password'); valid = false; }

    if (!valid) return;

    setLoading('loginSubmitBtn', true);

    try {
      await delay(FAKE_DELAY);

      const users  = getUsers();
      const hashed = await hashPassword(password);
      const user   = users.find(u => u.email === email);

      if (!user) {
        fieldError('loginEmail', 'loginEmailErr', 'no account found with this email');
        setLoading('loginSubmitBtn', false);
        return;
      }

      if (user.passwordHash !== hashed) {
        fieldError('loginPassword', 'loginPasswordErr', 'incorrect password — please try again');
        setLoading('loginSubmitBtn', false);
        return;
      }

      // ✅ Success
      user.lastLogin = Date.now();
      saveUsers(users);
      saveSession(user, remember);

      setLoading('loginSubmitBtn', false);
      showToast('success', '👋', `welcome back, ${user.name.split(' ')[0]}!`);

      // Redirect after a short moment so the toast is visible
      setTimeout(() => window.location.replace('index.html'), 900);

    } catch (err) {
      console.error('[Login]', err);
      setLoading('loginSubmitBtn', false);
      showGlobalError('loginGlobalErr', 'loginGlobalErrMsg', 'something went wrong — please try again');
    }
  }

  /* ══════════════════════════════════════════
     SIGN-UP HANDLER
  ══════════════════════════════════════════ */
  async function handleSignup() {
    const name     = (document.getElementById('signupName')?.value    || '').trim();
    const email    = (document.getElementById('signupEmail')?.value   || '').trim().toLowerCase();
    const password =  document.getElementById('signupPassword')?.value || '';
    const confirm  =  document.getElementById('signupConfirm')?.value  || '';
    const agreed   =  document.getElementById('agreeTerms')?.checked   ?? false;

    // Reset previous state
    hideGlobalError('signupGlobalErr');
    ['signupName','signupEmail','signupPassword','signupConfirm'].forEach(id => {
      fieldReset(id, id + 'Err');
    });
    document.getElementById('agreeTermsErr').textContent = '';

    let valid = true;

    // Name
    const nameErr = Validators.name(name);
    if (nameErr) { fieldError('signupName', 'signupNameErr', nameErr); valid = false; }
    else fieldValid('signupName', 'signupNameErr');

    // Email
    const emailFmtErr = Validators.email(email);
    if (emailFmtErr) { fieldError('signupEmail', 'signupEmailErr', emailFmtErr); valid = false; }
    else {
      const dup = getUsers().find(u => u.email === email);
      if (dup) { fieldError('signupEmail', 'signupEmailErr', 'an account with this email already exists'); valid = false; }
      else fieldValid('signupEmail', 'signupEmailErr');
    }

    // Password
    const pwErr = Validators.password(password);
    if (pwErr) { fieldError('signupPassword', 'signupPasswordErr', pwErr); valid = false; }
    else if (scorePassword(password) < MIN_PW_SCORE) {
      fieldError('signupPassword', 'signupPasswordErr', 'please choose a stronger password');
      valid = false;
    } else fieldValid('signupPassword', 'signupPasswordErr');

    // Confirm
    if (!confirm) {
      fieldError('signupConfirm', 'signupConfirmErr', 'please confirm your password');
      valid = false;
    } else if (confirm !== password) {
      fieldError('signupConfirm', 'signupConfirmErr', 'passwords do not match');
      valid = false;
    } else fieldValid('signupConfirm', 'signupConfirmErr');

    // Terms
    if (!agreed) {
      const el = document.getElementById('agreeTermsErr');
      if (el) el.textContent = '⚠️ you must agree to the terms to continue';
      valid = false;
    }

    if (!valid) return;

    setLoading('signupSubmitBtn', true);

    try {
      await delay(FAKE_DELAY + 100);

      const hashed  = await hashPassword(password);
      const newUser = {
        uid:          genUID(),
        name,
        email,
        passwordHash: hashed,
        createdAt:    Date.now(),
        lastLogin:    Date.now(),
        savedRecipes: [],
        preferences:  {},
      };

      const users = getUsers();
      users.push(newUser);
      saveUsers(users);
      saveSession(newUser, true);

      setLoading('signupSubmitBtn', false);
      showToast('success', '🎉', `welcome to SurviveChef, ${name.split(' ')[0]}!`);

      setTimeout(() => window.location.replace('index.html'), 900);

    } catch (err) {
      console.error('[Signup]', err);
      setLoading('signupSubmitBtn', false);
      showGlobalError('signupGlobalErr', 'signupGlobalErrMsg', 'something went wrong — please try again');
    }
  }

  /* ──────────────────────────────────────────
     PUBLIC API
  ────────────────────────────────────────── */
  return {
    handleLogin,
    handleSignup,
    socialSignIn,
    togglePassword,
    renderPasswordStrength,
    checkEmailDuplicate,
    redirectIfLoggedIn,
    getSession,
    showToast,
  };

})();
