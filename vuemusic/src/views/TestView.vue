<template>
  <div id="login_box">
    <h2>login</h2>
      <div id="input-box">
        <input type="text" v-model="username" name="username" placeholder="用户名">
      </div>
      <div id="input-box">
        <input type="password" v-model="password" name="pwd" placeholder="密码">
      </div>
      <button type="button" @click="submitForm">submit</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    submitForm() {
      // 获取用户名和密码
      var username = this.username;
      var password = this.password;
      fetch('http://127.0.0.1:9001/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username ,password:password}),
      })
    }
  }
}
</script>



<style scoped>
#login_box {
  width: 40%;
  height: 600px;
  background-color: #00000060;
  margin: auto;
  margin-top: 10%;
  text-align: center;
  border-radius: 10px;
  padding: 50px 50px;
}

h2 {
  color: #ffffff90;
  margin-top: 5%;
}

#input-box {
  margin-top: 5%;
}

span {
  color: #fff;
}

input {
  border: 0;
  width: 60%;
  font-size: 15px;
  color: #fff;
  background: transparent;
  border-bottom: 2px solid #fff;
  padding: 5px 10px;
  outline: none;
  margin-top: 10px;
}

button {
  margin-top: 50px;
  margin-left: 20px;
  width: 30%;
  height: 30px;
  border-radius: 10px;
  border: 0;
  color: #fff;
  text-align: center;
  line-height: 30px;
  font-size: 15px;
  background-image: linear-gradient(to right, #226c6d, #330867);
}

#sign_up {
  margin-top: 45%;
  margin-left: 60%;
}

a {
  margin-top: 50px;
  margin-left: 20px;
  width: 30%;
  height: 30px;
  border-radius: 10px;
  border: 0;
  color: #fff;
  text-align: center;
  line-height: 30px;
  font-size: 15px;
  background-image: linear-gradient(to right, #226c6d, #330867);
}
</style>