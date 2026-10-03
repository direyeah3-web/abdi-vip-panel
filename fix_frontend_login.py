# fix_frontend_login.py - Beddel frontend-ka si uu ula shaqeeyo nidaamka cusub

with open("public/index.html", "r") as f:
    content = f.read()

# Beddelka handleLogin function
old_login_start = content.find("async function handleLogin(event) {")
old_login_end = content.find("async function handleRegister(event) {")

if old_login_start != -1 and old_login_end != -1:
    new_login_func = '''async function handleLogin(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const btn = event.target.querySelector('button');
        
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Signing in...';
        btn.disabled = true;
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            
            if (data.success) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                showDashboard();
            } else {
                alert('Login failed: ' + (data.message || data.error || 'Invalid credentials'));
                btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Enter console';
                btn.disabled = false;
            }
        } catch (error) {
            alert('Server error: ' + error.message);
            btn.innerHTML = '<i class="fa-solid fa-chevron-right"></i> Enter console';
            btn.disabled = false;
        }
    }
    
    '''
    new_content = content[:old_login_start] + new_login_func + content[old_login_end:]
    
    with open("public/index.html", "w") as f:
        f.write(new_content)
    print("✅ Frontend-ka login-ka waa la beddelay!")
else:
    print("❌ Ma helin handleLogin function")

