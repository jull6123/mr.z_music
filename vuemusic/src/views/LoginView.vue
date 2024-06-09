<template>
  <!--登录界面-->
  <div class="wrapper">
    <div style="margin: 150px auto; background-color: #fff; width: 400px; height: 250px; padding: 20px; border-radius: 10px">
      <div style="margin: 10px 0; text-align: center; font-size: 24px"><b>登 录</b></div>
      <el-form :model="user" :rules="rules" ref="userForm">
        <el-form-item prop="username">
          <el-input  size="medium" class="input" prefix-icon="el-icon-user"
                     v-model="user.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input size="medium" class="input" prefix-icon="el-icon-lock" show-password
                    v-model="user.password"></el-input>
        </el-form-item>

        <el-button type="warning" class="registerButton" autocomplete="off" text @click="$router.push('/register')">注册账号</el-button>
        <el-button class="loginButton"   type="primary"  autocomplete="off" @click="login">登录账号</el-button>

      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      choose:"",
      user: {},
      rules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 10, message: '长度在 3 到 5 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    login() {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {  // 表单校验合法
          fetch('http://127.0.0.1:9001/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.user),
          })
              .then(response => response.json())
              .then(data => {
                if (data.code === 200){
                  localStorage.setItem("user", JSON.stringify(data.user))
                  if(data.user.role === 0) this.$router.push('/adminHome');
                  else if(data.user.role === 2) this.$router.push('/auditHome');
                  else this.$router.push('/home');
                  // this.$router.push({path: "/uploadPost", query: {uploadMold: 'music', mid: 1}});
                  // this.$router.push({path: "/uploadPost", query: {uploadMold: 'music'}});
                  // this.$router.push({path: "/uploadPost", query: {uploadMold: 'songList', sid: 1}});
                  // this.$router.push({path: "/uploadPost", query: {uploadMold: 'songList'}});
                  // this.$router.push({path: "/person", query: {uid: 1}})
                }
                this.$notify({
                  title: data.msg
                });
              })
        }
      });
    }
  }
}
</script>

<style>
.wrapper {
  height: 100vh;
  background-image: linear-gradient(to bottom right, #FC466B, #3F5EFB);
  overflow: hidden;
}
.loginButton{
  height: 35px;
  width: 250px;
  margin-left: 125px;
  margin-top: 0px;
}
.registerButton{
  height: 10px;
  width: 65px;
  margin-top: 12px;
}
.input{
  margin: 7px 0;
  width: 250px;
  margin-left: 75px;
}

</style>