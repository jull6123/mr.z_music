<template>
  <div>
    <el-row class="grid-content bg-purple-light" :gutter="20" style="margin-top: 30px;">
      <el-col :span="6"></el-col>
      <el-col :span="12">
        <el-card style="margin-top: 20px">
          <img v-if="form.avatar && !showPasswordFormItem" :src="form.avatarUrl" alt="Avatar" style="max-width: 200px;">
          <input type="file" v-if="!showPasswordFormItem" @change="handleFileChange">

          <!--    <el-upload-->
          <!--        class="avatar-uploader"-->
          <!--        :action="'http://localhost:9091/'"-->
          <!--        :show-file-list="false"-->
          <!--        :on-success="handleAvatarSuccess"-->
          <!--    >-->
          <!--      <img v-if="form.avatar  && !showPasswordFormItem" :src="form.avatar" class="avatar">-->
          <!--      <i v-else class="el-icon-plus avatar-uploader-icon"></i>-->
          <!--    </el-upload>-->
          <el-form label-width="80px" size="small" style="margin-top: 20px;">
            <el-form-item label="用户名">
              <el-input v-model="form.username" disabled autocomplete="off"></el-input>
            </el-form-item>

            <el-form label-width="120px" size="small" :model="form" :rules="rules" ref="pass" v-if="showPasswordFormItem">
              <el-form-item label="原密码" prop="password">
                <el-input v-model="form.password" autocomplete="off" show-password></el-input>
              </el-form-item>
              <el-form-item label="新密码" prop="newPassword">
                <el-input v-model="form.newPassword" autocomplete="off" show-password></el-input>
              </el-form-item>
              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input v-model="form.confirmPassword" autocomplete="off" show-password></el-input>
              </el-form-item>
            </el-form>

            <el-form-item label="描述" v-if="!showPasswordFormItem">
              <el-input v-model="form.description" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" v-if="!showPasswordFormItem">
              <el-input v-model="form.email" disabled autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="角色" v-if="user.role === 0" >
              <el-radio-group v-model="form.role">
                <el-radio :label=0>管理员</el-radio>
                <el-radio :label=1>普通用户</el-radio>
                <el-radio :label=2>审核员</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button v-if="user.role !== 0" type="danger" @click="togglePasswordFormItem">{{ message }}</el-button>
              <el-button type="primary" @click="save">保 存</el-button>
              <el-button type="success" @click="back">返 回</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="6"></el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Person",
  data() {
    return {
      message: "修改密码",
      showPasswordFormItem: false,
      form: {avatarUrl: ''},
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      uid: this.$route.query.uid,
      rules: {
        password: [
          { required: true, message: '请输入原密码', trigger: 'blur' },
          { min: 3, message: '长度不少于3位', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 3, message: '长度不少于3位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 3, message: '长度不少于3位', trigger: 'blur' }
        ],
      }
    }
  },
  // mounted() {
  //   const storedAvatarUrl = ''
  //   showAvater(storedAvatarUrl, avatarUrl)
  //   if (storedAvatarUrl) {
  //     this.form.avatarUrl = storedAvatarUrl;
  //   }
  // },
  created() {
    if(this.uid !== 0)
      this.load()
    else{
      this.form = this.user
    }
  },
  methods: {
    load(){
      const formData1 = new FormData();
      formData1.append('id', this.uid);
      formData1.append('type', "get")
      fetch('http://127.0.0.1:9001/updateperson/', {
        method: 'POST',
        body: formData1
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.form = data.user
              const storedAvatarUrl = data.user.avatar;
              if (storedAvatarUrl) {
                this.form.avatarUrl = storedAvatarUrl;
              }
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    handleFileChange(event) {
      this.form.avatar = event.target.files[0];
      this.form.avatarUrl = URL.createObjectURL(this.form.avatar);
    },
    togglePasswordFormItem() {
      if(this.showPasswordFormItem === true){
        this.message = "修改密码"
      }else{
        this.message = "修改个人信息"
      }
      this.showPasswordFormItem = !this.showPasswordFormItem;
    },
    save() {
      const formData = new FormData();
      formData.append('id', this.form.id);
      if(this.showPasswordFormItem === true)
        this.$refs.pass.validate((valid) => {
          if (valid) {
            if (this.form.newPassword !== this.form.confirmPassword) {
              this.$message.error("2次输入的新密码不相同")
              return false
            }
            formData.append('type', 'pwd');
            formData.append('oldPassword', this.form.password);
            formData.append('password', this.form.newPassword);
            fetch('http://127.0.0.1:9001/updateperson/', {
              method: 'POST',
              body: formData
            })
                .then(response => response.json())
                .then(data => {
                  if (data.code === 200){
                    localStorage.setItem("user", JSON.stringify(data.user))
                  }
                  this.$notify({
                    title: data.msg
                  });
                })
          }
        })
      else{
        formData.append('type', 'edit');
        formData.append('description', this.form.description);
        formData.append('avatar', this.form.avatar);
        formData.append('role', this.form.role);
        fetch('http://127.0.0.1:9001/updateperson/', {
          method: 'POST',
          body: formData
        })
            .then(response => response.json())
            .then(data => {
              if (data.code === 200){
                localStorage.setItem("user", JSON.stringify(data.user))
              }
              this.$notify({
                title: data.msg
              });
            })
      }
    },
    back(){
      if(this.user.role === 0) this.$router.push('/ahome');
      else if(this.user.role === 1) this.$router.push('/uhome');
      else this.$router.push('/ahome');
    },
    handleAvatarSuccess(res) {
      this.form.avatar = res
    }
  }
}
</script>

<style scoped>

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
</style>
