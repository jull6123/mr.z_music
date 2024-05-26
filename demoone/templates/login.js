document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // 发送登录请求
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login/");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert("Login successful!");
                // 可以进行页面跳转等操作
            } else {
                alert("Invalid username or password");
            }
        } else {
            alert("Error: " + xhr.statusText);
        }
    };
    xhr.send(JSON.stringify({username: username, password: password}));
});
