/* ── Tab switcher ── */
  function switchTab(tab) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.sc-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');
    event.target.classList.add('active');
  }
 
  /* ── Populate profile from session ── */
  (function () {
    const session = Auth.getSession();
 
    // If not logged in, redirect to login page
    if (!session) {
      window.location.replace('login.html');
      return;
    }
 
    // Fill in name
    document.getElementById('profile-name').textContent = session.name;
 
    // Build a handle from the name, e.g. "Alex Chen" → "@AlexChen"
    const handle = '@' + session.name.replace(/\s+/g, '');
 
    // Format join date from session timestamp
    const joinDate = new Date(session.ts).toLocaleDateString('en-US', {
      month: 'long',
      year:  'numeric',
    });
 
    document.getElementById('profile-handle').textContent = `${handle} · joined ${joinDate}`;
 
    // Wire up log out
    document.getElementById('logoutBtn').addEventListener('click', () => {
      localStorage.removeItem('SC_SESSION');
      sessionStorage.removeItem('SC_SESSION');
      window.location.replace('index.html');
    });
  })();