async function postJSON(url, body){
  const r = await fetch(url, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)
  });
  return r.json();
}

document.addEventListener('DOMContentLoaded', ()=>{
  const loginForm = document.getElementById('loginForm');
  if(loginForm){
    loginForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const res = await postJSON('/api/login',{email,password});
      if(res.error){ alert(res.error); return; }
      window.location.href = '/dashboard';
    });
  }

  const signupForm = document.getElementById('signupForm');
  if(signupForm){
    signupForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const res = await postJSON('/api/signup',{name,email,password});
      if(res.error){ alert(res.error); return; }
      alert('Account created. Please login.');
      window.location.href = '/login';
    });
  }
});
