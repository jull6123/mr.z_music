<template>
  <!--用户首页-->
  <div class="fullscreen-background "></div>
  <div class="bg-white2"></div>
  <div class="common-layout">
    <el-container>
      <el-button size="large" text style="width: 500px;margin-left: 550px;background: rgba(5,5,5,0);" @click="Helprouter">
        <span style="font-size: 36px;color: aliceblue;">实现你的音乐梦想</span>
      </el-button>
      <el-main>
        <div>
          <el-row :gutter="10">
            <el-col :span="1" :style="{opacity:myopacity}"><div class="grid-content bg-white"></div></el-col>
            <el-button size="large" round="true" style="width: 120px;"  @click="Playingrouter">
              <span style="vertical-align: middle;">音乐播放器</span>
            </el-button>
            <el-button size="large" round="true"  style="width: 120px;" @click="Airouter">
              <span style="vertical-align: middle;">AI录歌</span>
            </el-button>
            <el-button size="large" round="true"  style="width: 120px;" @click="Uploadrouter">
              <span style="vertical-align: middle;">上传音乐</span>
            </el-button>
            <el-col :span="4" :style="{opacity:myopacity}"><div class="grid-content bg-white"></div></el-col>
            <div>
              <el-input v-model="input" style="width: 360px;"placeholder="输入你想录的歌，实现你的音乐梦想" size = "large" clearable/>
              <el-button type="primary" size="large">
                <el-icon style="vertical-align: middle">
                  <Search />
                </el-icon>
                <span style="vertical-align: middle"> 搜索 </span>
              </el-button>
            </div>
            <el-col :span="4" :style="{opacity:myopacity}"><div class="grid-content bg-white"></div></el-col>
            <div>
            </div>
          </el-row>
        </div>
      </el-main>
      <el-footer class="footer">
      </el-footer>
    </el-container>
  </div>
  <div>
  </div>
</template>

<script>
export default{
  name: 'userHomeView',
  data(){
    return{
      input:"",
      myopacity:0,
      value1:50,
    }
  },
  methods:{
    Playingrouter(){
      this.$router.push({name:'Playing'});
    },
    Helprouter(){
      this.$router.push({name:'help'});
    },
    Airouter(){
      this.$router.push({name:'Ai'});
    },
    Uploadrouter(){
      this.$router.push({path: "/uploadPost", query: {uploadMold: 'music'}});
    },
  }
}
</script>

<style scoped>
.silder{
  position:fixed;
  bottom: 8%;
}
.header{
  font-size: 36px;
  margin: auto;
  color: #ffffff;
}
.button{
  border-radius: 30px;
}
.button_font{
  color: #ffffff;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-white{
  background: rgb(255, 255, 255);
}
.bg-white2 {
  background: #514d4d;
  opacity: 30%;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -998; /* 确保背景在其他内容之下 */
}
.fullscreen-background {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -999; /* 确保背景在其他内容之下 */
  background-image: url('../assets/image/beijing2.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.footer{
  position:fixed;
  bottom: 5%;
}
</style>