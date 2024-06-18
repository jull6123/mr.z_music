<template>
  <!--注册界面-->
  <div class="wrapper">
    <div style="margin-top: 12%; margin-left: 40%; background-color: #fff; width: 350px; height: 330px; padding: 20px; border-radius: 10px">
      <div style="margin: 20px 0; text-align: center; font-size: 24px"><b>注 册</b></div>
      <el-form :model="user" :rules="rules" ref="userForm">
        <div style="display: flex;">
          <el-icon size="large" color="grey" style="margin-top: 5px; margin-right: 8px" >
            <User />
          </el-icon>
        <el-form-item prop="username">
          <el-input placeholder="请输入账号" size="medium" style="width: 280px;" :prefix-icon="el-icon-user"
                    v-model="user.username"></el-input>
        </el-form-item>
        </div>
        <div style="display: flex;">
          <el-icon size="large" color="grey" style="margin-top: 5px; margin-right: 8px" >
            <Message />
          </el-icon>
        <el-form-item prop="email">
          <el-input placeholder="请输入邮箱" size="medium" style="width: 280px;" :prefix-icon="el-icon-message"
                    v-model="user.email"></el-input>
        </el-form-item>
        </div>
        <div style="display: flex;">
          <el-icon size="large" color="grey" style="margin-top: 5px; margin-right: 8px" >
            <Lock />
          </el-icon>
        <el-form-item prop="password">
          <el-input placeholder="请输入密码" size="medium" style="width: 280px;" :prefix-icon="el-icon-lock"
                    show-password
                    v-model="user.password"></el-input>
        </el-form-item>
        </div>
        <el-form-item style="margin: 10px 0; text-align: right">
          <el-button type="primary" size="middle" autocomplete="off" @click="register" style="margin-left: 26px; margin-right: 93px">确认注册</el-button>
          <el-button type="warning" size="middle" autocomplete="off" @click="$router.push('/')">返回登陆</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "register",
  data() {
    return {
      user: {},
      rules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 10, message: '长度在 3 到 5 个字符', trigger: 'blur'}
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    register() {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {  // 表单校验合法
          fetch('http://127.0.0.1:9001/register/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.user),
          })
              .then(response => response.json())
              .then(data => {
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
  background-image: url("src/assets/image/background.png") ;
  background-size:100%;
  overflow: hidden;
  opacity: 0.75;
}
</style>
