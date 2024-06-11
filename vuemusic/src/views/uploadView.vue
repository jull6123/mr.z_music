<template>
  <div>
    <el-row class="grid-content bg-purple-light" :gutter="20" style="margin-top: 30px;">
      <el-col :span="4"></el-col>
      <el-col :span="16">
        <el-card v-if="uploadMold==='music'">
          <el-steps :active="active" finish-status="success">
            <el-step title="上传音乐"></el-step>
            <el-step title="补充信息"></el-step>
            <el-step title="信息提交"></el-step>
          </el-steps>

          <el-card  v-if="active === 0">
            <input type="file" @change="handleFileChangeM">
            <div style="margin-top: 20px;">
              <el-button type="primary" @click="uploadMusic">上 传</el-button>
              <el-button type="primary" @click="delMusic">重 置</el-button>
              <el-button type="primary" @click="backS">返 回</el-button>
            </div>
          </el-card>


          <el-card v-if="active === 1">
            <img v-if="form.avatar" :src="form.avatarUrl" alt="Avatar" style="max-width: 200px;">
            <input type="file" @change="handleFileChangeA">

            <el-form label-width="80px" size="small" style="margin-top: 20px;">
              <el-form-item label="名称">
                <el-input v-model="form.name" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="歌手">
                <el-input v-model="form.singer" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="时长">
                <el-input v-model="form.duration_seconds" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="form.description" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="类型">
                <el-radio-group v-model="form.mold">
                  <el-radio :value="1"> 网络歌曲 </el-radio>
                  <el-radio :value="2"> 源音频 </el-radio>
                  <el-radio :value="3"> AI音频 </el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item style="text-align: left; margin-right: 150px">
                <el-button type="primary" @click="uploadPost">补 充</el-button>
                <el-button type="primary" @click="active = active +1">跳 过</el-button>
                <el-button type="primary" @click="backS"> 返 回 </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <el-card  v-if="active === 2">
            <div slot="header" class="clearfix">
              <h3 style="text-align: center">{{ form.name }}</h3>
            </div>
            <img v-if="form.avatar" :src="form.avatarUrl" alt="Avatar" style="max-width: 200px;">
            <div v-for="(value, key) in form" :key="key" class="text item" style="margin-top: 5px">
              <template v-if="key !== 'id' && key !== 'avatar' && key !== 'support' && key !== 'uid' && key !== 'mold'  && key !== 'avatarUrl'
                                 && key !== 'is_upload' && key !== 'url' && key !== 'auditContent'  && key !== 'msg'
                                  &&　key !== 'audit_id' && key !== 'pid' && key !== 'auditResult' && key !== 'duration_seconds'">
                {{ customKeys[key] }} :   {{ value }}
              </template>
            </div>
            <div style="padding-top: 30px; ">
              <el-card v-if="form.is_upload === 0">
                <div style="padding-top: 10px;text-align: right; margin-right: 150px">
                  <el-button type="primary" v-if="form.mold !== 2" @click="upload('music',form.id)"> 上 传 </el-button>
                  <el-button type="primary" @click="back"> 上一步 </el-button>
                  <el-button type="primary" @click="backS"> 返 回 </el-button>
                </div>
              </el-card>
              <el-card v-if="form.is_upload > 1">
                <div slot="header" class="clearfix">
                  <h3 style="text-align: center"> 审核结果 </h3>
                </div>
                <div v-for="(value, key) in form" :key="key" class="text item">
                  <template v-if="key === 'auditResult' && key === 'auditContent'">
                    {{ customKeys[key] }}:{{ value }}
                  </template>
                </div>
                <div style="padding-top: 10px; text-align: right; margin-right: 150px">
                  <el-button type="success" @click="backQ"> 确 认 </el-button>
                </div>
              </el-card>
              <el-card v-if="form.is_upload === 1">
                <div slot="header" class="clearfix">
                  <h3 style="text-align: center"> 正在审核中…… </h3>
                </div>
                <div style="padding-top: 10px; text-align: right; margin-right: 150px">
                  <el-button type="primary" @click="press"> 催 办 </el-button>
                  <el-button type="primary" @click="backS"> 返 回 </el-button>
                </div>
              </el-card>
            </div>
          </el-card>
        </el-card>


        <el-card v-if="uploadMold==='songList'">
          <el-steps :active="active" finish-status="success">
            <el-step title="补充信息"></el-step>
            <el-step title="信息提交"></el-step>
          </el-steps>

          <el-card v-if="active === 0">
            <img v-if="forms.avatar" :src="forms.avatarUrl" alt="Avatar" style="max-width: 200px;">
            <input type="file" @change="handleFileChangeAS">
            <el-form label-width="80px" size="small" style="margin-top: 20px;">
              <el-form-item label="名称">
                <el-input v-model="forms.name" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="forms.description" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button v-if="sid!==0" type="primary" @click="uploadPostS">修 改</el-button>
                <el-button v-if="sid===0" type="primary" @click="uploadPostS">新 建</el-button>
                <el-button v-if="sid!==0" type="primary" @click="active=active+1">跳 过</el-button>
                <el-button type="success" @click="backS">返 回</el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <el-card v-if="active === 1">
            <el-card class="box-card" >
              <div slot="header" class="clearfix">
                <h3 style="text-align: center">歌 单 歌 曲</h3>
              </div>
              <div style="margin-top: 5px">
                <el-table :data="songMusicList" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 30px">
                  <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="success" @click="delAnyById('musicCollect', scope.row.id)"> 删 除 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              <div style="padding-top: 30px; text-align: right;" >
                <el-button type="primary" @click="active = active + 1"> 确 认 </el-button>
                <el-button type="primary" @click="back"> 返 回 </el-button>
              </div>
            </el-card>
          </el-card>

          <el-card  v-if="active === 2">
            <div slot="header" class="clearfix">
              <h3 style="text-align: center">{{ forms.name }}</h3>
            </div>
            <img v-if="forms.avatar" :src="forms.avatarUrl" alt="Avatar" style="max-width: 200px;">
            <div v-for="(value, key) in forms" :key="key" class="text item">
              <template v-if="key !== 'id' && key !== 'avatar' && key !== 'audit_id' && key !== 'msg' && key !== 'avatarUrl'
                                 && key !== 'is_upload' && key !== 'uid' && key !== 'auditContent'
                                  && key !== 'support' && key !== 'auditResult'">
                {{ customKeys[key] }}:{{ value }}
              </template>
            </div>
            <div style=" padding-top: 30px;">
              <el-card v-if="forms.is_upload === 0">
                <div style="padding-top: 10px;">
                  <el-button type="primary" @click="upload('singList',forms.id)"> 上 传 </el-button>
                  <el-button type="primary" @click="backS"> 返 回 </el-button>
                </div>
              </el-card>
              <el-card v-if="forms.is_upload > 1">
                <div slot="header" class="clearfix">
                  <h3 style="text-align: center"> 审核结果 </h3>
                </div>
                <div v-for="(value, key) in forms" :key="key" class="text item">
                  <template v-if="key === 'auditResult' && key === 'auditContent'">
                    {{ customKeys[key] }}:{{ value }}
                  </template>
                </div>
                <div style="border-top: 1px dashed #ccc; padding-top: 10px;">
                  <el-button type="success" @click="backQ"> 确 认 </el-button>
                </div>
              </el-card>
              <el-card v-if="forms.is_upload === 1">
                <div slot="header" class="clearfix">
                  <h3 style="text-align: center"> 正在审核中…… </h3>
                </div>
                <div style="padding-top: 10px;">
                  <el-button type="primary" @click="press"> 催 办 </el-button>
                  <el-button type="primary" @click="backS"> 返 回 </el-button>
                </div>
              </el-card>
            </div>
          </el-card>

        </el-card>
      </el-col>
      <el-col :span="4"></el-col>
    </el-row>

  </div>
</template>

<script>
export default{
  name: 'upload',
  data(){
    return{
      uploadMold: this.$route.query.uploadMold,
      active: 0,
      musicFile: '',
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      form: {avatarUrl: ''},
      forms: {avatarUrl: ''},
      songMusicList: [],
      mid: this.$route.query.mid? this.$route.query.mid : 0,
      pid: this.$route.query.pid? this.$route.query.pid : 0,
      sid: this.$route.query.sid? this.$route.query.sid : 0,
      where: this.$route.query.where? this.$route.query.where : 'home',
      customKeys: {
        name: '名称',
        description: '描述',
        owner: '所属者',
        singer: '歌手',
        nameParent: '源音乐',
        userName: '上传者',
        username: '姓名',
        email: '邮箱',
        create_time: '创建时间',
        content: '审核结果',
        duration: '时长',
        auditResult: '审核情况',
        auditContent: '详细说明',
        number: '歌曲数量',
        avatar: '头像',
        mold_msg: '类型',
        is_upload_msg: '上传状态',
      }
    }
  },
  created() {
    this.load()
  },
  methods:{
    handleFileChangeM(event) {
      this.file = event.target.files[0];
    },
    handleFileChangeA(event) {
      console.log(event.target.files[0])
      this.form.avatar = event.target.files[0];
      this.form.avatarUrl = URL.createObjectURL(this.form.avatar);
    },
    handleFileChangeAS(event) {
      console.log(event.target.files[0])
      this.forms.avatar = event.target.files[0];
      this.forms.avatarUrl = URL.createObjectURL(this.forms.avatar);
    },
    load(){
      const formData1 = new FormData();
      formData1.append('type', "get")
      if (this.mid !== 0){
        formData1.append('mid', this.mid);
        fetch('http://127.0.0.1:9001/song/addMusic/', {
          method: 'POST',
          body: formData1
        })
            .then(response => response.json())
            .then(data => {
              if (data.code === 200){
                this.form = data.music
                // 正在审核:已上传，只可查看
                if (data.music.is_upload >= 1) this.active=2
                else if (data.music.is_upload === 0) this.active=1

                const storedAvatarUrl = data.music.avatar;
                if (storedAvatarUrl) {
                  this.form.avatarUrl = storedAvatarUrl;
                }
              }
              this.$notify({
                title: data.msg
              });
            })
      }
      if (this.sid !== 0){
        formData1.append('sid', this.sid);
        fetch('http://127.0.0.1:9001/songList/addSongList/', {
          method: 'POST',
          body: formData1
        })
            .then(response => response.json())
            .then(data => {
              if (data.code === 200){
                this.forms = data.songList
                if (data.songList.is_upload === 1) this.active=2
                else if (data.songList.is_upload === 0) this.active=0
                this.getSongListById(this.sid)

                const storedAvatarUrlS = data.songList.avatar;
                if (storedAvatarUrlS) {
                  this.forms.avatarUrl = storedAvatarUrlS;
                }
              }
              this.$notify({
                title: data.msg
              });
            })
      }
    },
    delMusic(){
      if (!this.file) {
        this.$notify({
          title: '--oops--',
          message: '请先选择文件',
          type: 'warning'
        });
        return;
      }
      if(this.mid !== 0){
        this.delAnyById('music', this.mid)
      }
    },
    uploadMusic(){
      if (!this.file) {
        this.$notify({
          title: '--oops--',
          message: '请先选择文件',
          type: 'warning'
        });
        return;
      }
      const formData = new FormData();
      formData.append('musicFile', this.file);
      formData.append('type', 'music');
      fetch('http://127.0.0.1:9001/song/addMusic/', {
        method: 'POST',
        body: formData
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.mid = data.mid
              this.active++
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    uploadPost(){
      const formDatas = new FormData();
      formDatas.append('type', 'post');
      formDatas.append('mid', this.mid);
      formDatas.append('userId', this.user.id);
      formDatas.append('name', this.form.name);
      formDatas.append('singer', this.form.singer);
      formDatas.append('description', this.form.description);
      formDatas.append('avatar', this.form.avatar);
      formDatas.append('duration', this.form.duration_seconds);
      formDatas.append('mold', this.form.mold);
      formDatas.append('pid', this.pid);
      fetch('http://127.0.0.1:9001/song/addMusic/', {
        method: 'POST',
        body: formDatas
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.mid = data.music.id
              this.form = data.music
              this.active++
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    uploadPostS(){
      const formDatass = new FormData();
      formDatass.append('type', 'edit');
      formDatass.append('userId', this.user.id);
      formDatass.append('sid', this.sid);
      formDatass.append('name', this.forms.name);
      formDatass.append('description', this.forms.description);
      formDatass.append('avatar', this.forms.avatar);
      fetch('http://127.0.0.1:9001/songList/addSongList/', {
        method: 'POST',
        body: formDatass
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.forms = data.songList
              this.sid = data.sid
              this.active++
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    upload(type,id){
      fetch('http://127.0.0.1:9001/upload/', {
        method: 'POST',
        body: JSON.stringify({type:type, id:id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.backQ()
            }
          })
    },
    getSongListById(sid){
      fetch('http://127.0.0.1:9001/getListById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({sid:sid}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.songMusicList = data.musicList
            }
          })
    },
    delAnyById(type, id){
      const data = {
        getType: type,
        id:id,
        userId:this.user.id,
        sid:this.sid,
      }
      fetch('http://127.0.0.1:9001/delById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.getSongListById(this.sid)
            }
          })
    },
    back(){
      this.active--
      this.load()
    },
    backQ(){
      this.active++
      setTimeout(() => {
      }, 1000);
      this.$router.push({path: '/userhome', query: {where: this.where}})
    },
    backS(){
      this.$router.push({path: '/userhome', query: {where: this.where}})
    },
    press(){
      this.$notify({
        title: "正在努力赶工中，请耐心等待！"
      });
    },
  }
}
</script>

<style scoped>
.headerBg {
  background: #eee !important;
}</style>