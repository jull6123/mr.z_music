
<template>
    <el-container>
        <el-header>
          <el-row class="grid-content bg-purple-light" :gutter="20">
            <el-col :span="4"></el-col>
            <el-col :span="2" style="text-align: center" class="grid-content bg-purple-dark"><div style="margin-top: 12px">后台管理</div></el-col>
            <el-col :span="2" style="text-align: center"
                    :class="[getType==='user' && 'grid-content bg-purple']">
              <div  type="text" @click="userController" style="margin-top: 12px">用户管理</div>
            </el-col>
            <el-col :span="2" style="text-align: center"
                    :class="[getType==='music' && 'grid-content bg-purple']">
              <div type="text" @click="musicController" style="margin-top: 12px">歌曲管理</div>
            </el-col>
            <el-col :span="2" style="text-align: center"
                    :class="[getType==='songList' && 'grid-content bg-purple']">
              <div type="text" @click="songListController" style="margin-top: 12px">歌单管理</div>
            </el-col>
            <el-col :span="6"></el-col>
            <el-col :span="1" style="text-align: center">
              <div type="text" style="margin-top: 12px">{{ user.username }}</div>
            </el-col>
            <el-col :span="1" style="text-align: center">
              <div type="text" style="margin-top: 12px" @click="logout"> 退 出 </div>
            </el-col>
<!--            <el-col :span="4" style="text-align: center">-->
<!--              <el-dropdown style="width: 150px; cursor: pointer; text-align: right; margin-top: 12px">-->
<!--                <div style="display: inline-block">-->
<!--                  <span>{{ user.username }}</span><i class="el-icon-arrow-down" style="margin-left: 5px"></i>-->
<!--                </div>-->
<!--                <el-dropdown-menu slot="dropdown" style="width: 100px; text-align: center">-->
<!--                  <el-dropdown-item style="font-size: 14px; padding: 5px 0">-->
<!--                    <router-link to="/person" style="text-decoration: none">个人信息</router-link>-->
<!--                  </el-dropdown-item>-->
<!--                  <el-dropdown-item style="font-size: 14px; padding: 5px 0">-->
<!--                    <span style="text-decoration: none" @click="logout">退出</span>-->
<!--                  </el-dropdown-item>-->
<!--                </el-dropdown-menu>-->
<!--              </el-dropdown>-->
<!--            </el-col>-->
            <el-col :span="4"></el-col>
          </el-row>
        </el-header>
        <el-main>
          <el-row :gutter="20">
            <el-col :span="4"></el-col>
            <el-col :span="16" class="grid-contents bg-purple-light">
              <div>
                <!--        搜索部分        -->
                <div style="margin: 10px 0" v-if="getType==='user'">
                  <el-input style="width: 200px" placeholder="请输入姓名" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateU.serNameU"></el-input>
                  <el-input style="width: 200px" placeholder="请输入邮箱" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateU.serEmail"></el-input>
                  <el-select style="width: 200px" v-model="searchDateU.serDel" placeholder="请选择删除标志" class="ml-5">
                    <el-option label="未删除" :value="0"></el-option>
                    <el-option label="已删除" :value="1"></el-option>
                    <el-option label="全部"   :value="2"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateU.serRole" placeholder="请选择用户身份" class="ml-5">
                    <el-option label="管理员" :value="0"></el-option>
                    <el-option label="普通用户" :value="1"></el-option>
                    <el-option label="审核员" :value="2"></el-option>
                    <el-option label="全部"   :value="3"></el-option>
                  </el-select>

                  <el-button class="ml-5" type="primary" @click="userController">搜索</el-button>
                  <el-button type="warning" @click="resetU">重置</el-button>
                </div>

                <div style="margin: 10px 0"  v-if="getType==='music'">
                  <el-input style="width: 200px" placeholder="请输入姓名或歌手名" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateM.serNameM"></el-input>
                  <el-input style="width: 200px" placeholder="请输入描述" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateM.serDesc"></el-input>
                  <el-select style="width: 200px" v-model="searchDateM.serMold" placeholder="请选择歌曲类型" class="ml-5">
                    <el-option label="网络音乐" :value="1"></el-option>
                    <el-option label="源音频" :value="2"></el-option>
                    <el-option label="AI音乐"   :value="3"></el-option>
                    <el-option label="全部"   :value="4"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateM.serUpload" placeholder="请选择上传阶段" class="ml-5">
                    <el-option label="未上传" :value="0"></el-option>
                    <el-option label="审核中" :value="1"></el-option>
                    <el-option label="审核失败" :value="2"></el-option>
                    <el-option label="上传成功"   :value="3"></el-option>
                    <el-option label="全部"   :value="4"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateM.orderBy" placeholder="请选择排序字段" class="ml-5">
                    <el-option label="点赞数" value="support"></el-option>
                    <el-option label="歌曲时长" value="duration_time"></el-option>
                    <el-option label="创建时间" value="create_date"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateM.ascOrderBy" placeholder="请选择排序顺序" class="ml-5">
                    <el-option label="升序" value="asc"></el-option>
                    <el-option label="降序" value="desc"></el-option>
                  </el-select>
                  <el-button class="ml-5" type="primary" @click="musicController">搜索</el-button>
                  <el-button type="warning" @click="resetM">重置</el-button>
                </div>

                <div style="margin: 10px 0"  v-if="getType==='songList'">
                  <el-input style="width: 200px" placeholder="请输入姓名" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateS.serNameS"></el-input>
                  <el-input style="width: 200px" placeholder="请输入描述" suffix-icon="el-icon-message" class="ml-5"
                            v-model="searchDateS.serDescS"></el-input>
                  <el-select style="width: 200px" v-model="searchDateS.serUploadS" placeholder="请选择上传阶段" class="ml-5">
                    <el-option label="未上传" :value="0"></el-option>
                    <el-option label="审核中" :value="1"></el-option>
                    <el-option label="审核失败" :value="2"></el-option>
                    <el-option label="上传成功"   :value="3"></el-option>
                    <el-option label="全部"   :value="4"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateS.orderByS" placeholder="请选择排序字段" class="ml-5">
                    <el-option label="点赞数" value="support"></el-option>
                    <el-option label="歌曲数量" value="number"></el-option>
                    <el-option label="创建时间" value="create_date"></el-option>
                  </el-select>
                  <el-select style="width: 200px" v-model="searchDateS.ascOrderByS" placeholder="请选择排序顺序" class="ml-5">
                    <el-option label="升序" value="asc"></el-option>
                    <el-option label="降序" value="desc"></el-option>
                  </el-select>
                  <el-button class="ml-5" type="primary" @click="songListController">搜索</el-button>
                  <el-button type="warning" @click="resetS">重置</el-button>
                </div>


                <!--        表格部分        -->
                <el-table :data="userList" border stripe :header-cell-class-name="'headerBg'"
                          v-if="getType==='user'">
<!--                          @selection-change="handleSelectionChange" -->
<!--                  <el-table-column type="selection" width="55"></el-table-column>-->
                  <el-table-column prop="id" label="ID" width="80"></el-table-column>
                  <el-table-column prop="username" label="用户名" width="140"></el-table-column>
                  <el-table-column prop="role" label="角色"></el-table-column>
                  <el-table-column prop="email" label="邮箱"></el-table-column>
                  <el-table-column prop="description" label="描述"></el-table-column>
                  <el-table-column prop="create_time" label="创建时间"></el-table-column>
                  <el-table-column prop="delete_mark" label="删除标志"></el-table-column>
<!--                  <el-table-column label="操作" width="500" align="center">-->
<!--                    <template slot-scope="scope">-->
<!--                      <el-button type="primary" @click="lookMusicById(scope.row.id)"-->
<!--                                 >查看用户所有歌曲 <i class="el-icon-document"></i>-->
<!--                      </el-button>-->
<!--                      <el-button type="warning" @click="lookSongListById(scope.row.id)"-->
<!--                                 >查看用户所有歌单 <i class="el-icon-document"></i>-->
<!--                      </el-button>-->
<!--                      <el-button type="success" @click="handleEdit(scope.row)">查 看 <i class="el-icon-edit"></i></el-button>-->
<!--                    </template>-->
<!--                  </el-table-column>-->
                </el-table>

                <el-table :data="musicList" border stripe :header-cell-class-name="'headerBg'"
                          v-if="getType==='music'">
                  <el-table-column prop="id" label="ID" width="80"></el-table-column>
                  <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="description" label="描述"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="mold" label="歌曲类型"></el-table-column>
                  <el-table-column prop="is_upload" label="上传阶段"></el-table-column>
                  <el-table-column prop="parentName" label="衍生自"></el-table-column>
                  <el-table-column prop="userName" label="所属者"></el-table-column>
                </el-table>

                <el-table :data="songLists" border stripe :header-cell-class-name="'headerBg'"
                          v-if="getType==='songList'">
                  <el-table-column prop="id" label="ID" width="80"></el-table-column>
                  <el-table-column prop="name" label="歌单名" width="140"></el-table-column>
                  <el-table-column prop="description" label="描述"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数量"></el-table-column>
                  <el-table-column prop="is_upload" label="上传阶段"></el-table-column>
                  <el-table-column prop="userName" label="所属者"></el-table-column>
                </el-table>
              </div>
            </el-col>
            <el-col :span="4"></el-col>
          </el-row>
      </el-main>
    </el-container>
</template>

<script>
export default {
  name: "adminHomeView",
  data() {
    return {
      user:localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      userList:[],
      musicList:[],
      songLists:[],
      searchDateU:{
        serNameU: "",
        serEmail: "",
        serDel: 2,
        serRole: 3,
      },
      searchDateM:{
        serNameM: "",
        serDesc: "",
        serMold: 4,
        serUpload: 4,
        orderBy: "id",
        ascOrderBy: "asc",
      },
      searchDateS:{
        serNameS: "",
        serDescS: "",
        serUploadS: 4,
        orderByS: "id",
        ascOrderByS: "asc",
      },
      getType: 'user',
    }
  },
  computed: {

  },
  created() {
    this.userController()
  },
  methods: {
    userController(){
      this.getType = 'user'
      fetch('http://127.0.0.1:9001/serUserList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.searchDateU),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
             this.userList = data.userList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    resetU() {
      this.searchDateU.serNameU = ''
      this.searchDateU.serEmail = ''
      this.searchDateU.serDel = 2
      this.searchDateU.serRole = 3
      this.userController()
    },
    musicController(){
      this.getType = 'music'
      fetch('http://127.0.0.1:9001/serMusicList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.searchDateM),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.musicList = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    resetM() {
      this.searchDateM.serNameM = ''
      this.searchDateM.serDesc = ''
      this.searchDateM.serMold = 4
      this.searchDateM.serUpload = 4
      this.searchDateM.orderBy = ''
      this.searchDateM.ascOrderBy = ''
      this.musicController()
    },
    songListController(){
      this.getType = 'songList'
      fetch('http://127.0.0.1:9001/serSongLists/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.searchDateS),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.songLists = data.songLists
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    resetS() {
      this.searchDateS.serNameS = ''
      this.searchDateS.serDescS = ''
      this.searchDateS.serUploadS = 4
      this.searchDateS.orderByS = ''
      this.searchDateS.ascOrderByS = ''
      this.musicController()
    },
    logout() {
      localStorage.removeItem("user")
      this.$router.push("/")
      this.$message.success("退出成功")
    },
  }
}
</script>


<style scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 6px;
  min-height: 50px;
}
.grid-contents {
  border-radius: 6px;
  min-height: 2500px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.headerBg {
  background: #eee !important;
}
</style>
