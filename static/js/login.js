const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () =>{
    container.classList.add("active");
});
loginBtn.addEventListener('click', () =>{
    container.classList.remove("active");
});


// Sign In button loading state
    document.querySelector('.sign-in form').addEventListener('submit', function() {
        const btn = this.querySelector('button');
        btn.textContent = 'Signing In...';
        btn.disabled = true;
    });

    // Sign Up button loading state
    document.querySelector('.sign-up form').addEventListener('submit', function() {
        const btn = this.querySelector('button');
        btn.textContent = 'Creating Account...';
        btn.disabled = true;
    });