
(function () {
    const session = Auth.getSession();
    if (!session) return; // not logged in — keep default buttons
 
    const firstName = session.name.split(' ')[0];
    const authArea  = document.getElementById('sc-nav-auth');
 
    authArea.innerHTML = `
      <a href="#" class="sc-nav-link">recipes</a>
      <a href="#" class="sc-nav-link">community</a>
      <a href="#" class="sc-nav-link">saved</a>
      <span class="sc-nav-user">👋 hi, ${firstName}!</span>
      <button class="sc-nav-btn ghost" id="logoutBtn">log out</button>
    `;
 
    document.getElementById('logoutBtn').addEventListener('click', () => {
      localStorage.removeItem('SC_SESSION');
      sessionStorage.removeItem('SC_SESSION');
      window.location.reload();
    });
  })();