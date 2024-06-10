
<template>
  <!--审核-->
  <el-container>
    <el-header>
      <el-row class="grid-content bg-purple-light" :gutter="20">
        <el-col :span="4"></el-col>
        <el-col :span="2" style="text-align: center" class="grid-content bg-purple-dark"><div style="margin-top: 12px">审核管理</div></el-col>
        <el-col :span="2" style="text-align: center"
                :class="[searchDate.state==='unAudited' && 'grid-content bg-purple']">
<!--          <div  type="text" @click="getUn" style="margin-top: 12px">待完成</div>-->
          <el-dropdown trigger="click">
            <div class="el-dropdown-link mx-1" size="large" type="text" @click="getUn" style="margin-top: 12px">待完成<el-icon class="el-icon--right"><arrow-down /></el-icon></div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :class="[searchDate.state==='music' && 'grid-content bg-purple']" @click="getMU" >歌 曲</el-dropdown-item>
                <el-dropdown-item :class="[searchDate.state==='songList' && 'grid-content bg-purple']" @click="getSO">歌 单</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[searchDate.state==='Audited' && 'grid-content bg-purple']">
          <el-dropdown trigger="click">
            <div class="el-dropdown-link mx-1" size="large" type="text" @click="getEd" style="margin-top: 12px">已完成<el-icon class="el-icon--right"><arrow-down /></el-icon></div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :class="[searchDate.state==='music' && 'grid-content bg-purple']" @click="getMU" >歌 曲</el-dropdown-item>
                <el-dropdown-item :class="[searchDate.state==='songList' && 'grid-content bg-purple']" @click="getSO">歌 单</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-col>
        <el-col :span="8"></el-col>
        <el-col :span="1" style="text-align: center">
          <div type="text" style="margin-top: 12px">{{ user.username }}</div>
        </el-col>
        <el-col :span="1" style="text-align: center">
          <div type="text" style="margin-top: 12px" @click="logout"> 退 出 </div>
        </el-col>
        <el-col :span="4"></el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="4"></el-col>
        <el-col :span="16" class="grid-contents bg-purple-light">

            <!--        表格部分        -->
          <el-table :data="tableData" border stripe :header-cell-class-name="'headerBg'" style="margin-top: 20px;">
            <el-table-column prop="id" label="ID" width="80"></el-table-column>
            <el-table-column prop="name" label="名称" width="140"></el-table-column>
            <el-table-column prop="type" label="类型"></el-table-column>
            <el-table-column prop="owner" label="所属者"></el-table-column>
            <el-table-column prop="audit_state_msg" label="审核状态"></el-table-column>
            <el-table-column label="操作" width="500" align="center">
              <template #default="scope">
                <el-button v-if="searchDate.state === 'unAudited'" type="primary" @click="audit(scope.row)"> 审 核 <i class="el-icon-edit"></i></el-button>
                <el-button v-if="searchDate.state === 'Audited'" type="success" @click="audit(scope.row)"> 查 看 <i class="el-icon-edit"></i></el-button>
              </template>
            </el-table-column>
          </el-table>


<!--          歌曲信息审核-->
          <el-dialog
              v-model="dialogFormVisibleM"
              width="1000"
              align-center
          >
            <el-card class="box-card" :style="{ height: '400px' }">
              <div slot="header" class="clearfix">
                <h1 style="text-align: center">{{ form.name }}</h1>
              </div>
              <div v-for="(value, key) in form" :key="key" class="text item">
                <template v-if="key !== 'id' && key !== 'avatar' && key !== 'url'
                                && key !=='name' && key !== 'pid' && key !== 'uid'
                                &&　key !== 'aid' && key !== 'type' && key !== 'content'">
                  <span v-if="key !== 'userName'">{{ customKeys[key] }}:</span>
                  <span v-else @click="handleUserNameClick(form.uid)">{{ customKeys[key] }}:</span>{{ value }}
                </template>
                <template v-if="key === 'content'">
                  <span v-if="searchDate.state === 'Audited'">{{ customKeys[key] }}:</span>{{ value }}
                </template>
              </div>
            </el-card>
            <template #footer>
              <div class="dialog-footer" v-if="searchDate.state === 'unAudited'">
                <el-button type="primary" v-if="form.uid !== 0 " @click="this.userNameDialogVisible = true">用户信息</el-button>
                <el-button type="primary" @click="auditRuselt(form, 'success')">审核通过</el-button>
                <el-button type="primary" @click="auditRuselt(form, 'failure')">不予通过</el-button>
              </div>
            </template>
          </el-dialog>

<!--          歌单信息审核-->
          <el-dialog
              v-model="dialogFormVisibleS"
              width="1000"
              align-center
          >
            <el-card class="box-card" :style="{ height: '400px' }">
              <div slot="header" class="clearfix">
                <h1 style="text-align: center">{{ form.name }}</h1>
              </div>
              <div v-for="(value, key) in form" :key="key" class="text item">
                <template v-if="key !== 'id' && key !== 'avatar'
                            &&　key !== 'aid' && key !== 'type'">
                  <span v-if="key !== 'owner'">{{ customKeys[key] }}:</span>
                  <span v-else @click="handleUserNameClick(form.uid)">{{ customKeys[key] }}:</span>{{ value }}
                </template>
              </div>
            </el-card>
            <template #footer>
              <div class="dialog-footer">
                <el-button type="primary" @click="getallMusics(form)">具体歌曲</el-button>
                <el-button type="primary" v-if="searchDate.state === 'unAudited'" @click="auditRuselt(form, 'success')">审核通过</el-button>
                <el-button type="primary" v-if="searchDate.state === 'unAudited'" @click="auditRuselt(form, 'failure')">不予通过</el-button>
                <el-button type="success" @click="dialogFormVisibleS = false"> back </el-button>
              </div>
            </template>
          </el-dialog>


<!--          用户信息-->
          <el-dialog
              v-model="userNameDialogVisible"
              title="用户信息"
              width="1000"
              align-center
          >
            <el-card class="box-card">
              <div v-for="(value, key) in user1" :key="key" class="text item">
                <template v-if="key !== 'id' && key !== 'avatar'
                        && key !== 'delete_mark'">
                  {{ customKeys[key] }}:{{ value }}
                </template>
              </div>
            </el-card>
          </el-dialog>


<!--          审核失败原因填写-->
          <el-dialog
              v-model="contentDialogVisible"
              title="补充原因"
              width="1000"
              align-center
          >
            <el-form>
              <el-form-item label="原因">
                <el-input type="textarea" v-model="content" autocomplete="off"></el-input>
              </el-form-item>
            </el-form>
            <template #footer>
              <div class="dialog-footer">
                <el-button @click="contentDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveContent(content, 'failure')">确 定</el-button>
              </div>
            </template>
          </el-dialog>


<!--          歌单具体歌曲列表-->
          <el-dialog
              v-model="dialogFormVisibleSAll"
              width="1000"
              align-center
          >
            <el-card class="box-card" :style="{ height: '400px' }">
              <div slot="header" class="clearfix">
                <h1 style="text-align: center">--歌 单 歌 曲--</h1>
              </div>
              <div>
                <el-table :data="allMusics" border stripe :header-cell-class-name="'headerBg'">
                  <el-table-column prop="id" label="ID" width="80"></el-table-column>
                  <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="description" label="描述"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="mold" label="歌曲类型"></el-table-column>
                  <el-table-column prop="parentName" label="衍生自"></el-table-column>
                  <el-table-column prop="userName" label="所属者"></el-table-column>
                  <el-table-column prop="auditorName" label="审核员"></el-table-column>
                </el-table>
              </div>
            </el-card>
          </el-dialog>

        </el-col>
        <el-col :span="4"></el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { computed, ref } from 'vue'
import {
  ArrowDown,
  Check,
  CircleCheck,
  CirclePlus,
  CirclePlusFilled,
  Plus,
} from '@element-plus/icons-vue'

export default {
  name: "auditHomeView",
  data() {
    return {
      tableData:[],
      user:localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      form:[],
      user1:[],
      allMusics:[],
      content:'',
      dialogFormVisibleS: false,
      dialogFormVisibleM: false,
      userNameDialogVisible: false,
      contentDialogVisible: false,
      dialogFormVisibleSAll: false,
      searchDate:{
        user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
        userId: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")).id : 0,
        type: "music",
        state: "unAudited",
      },
      customKeys: {
        name: '名称',
        description: '描述',
        owner: '所属者',
        singer: '歌手',
        mold: '类型',
        nameParent: '源音乐',
        userName: '上传者',
        username: '姓名',
        email: '邮箱',
        create_time: '创建时间',
        content: '审核结果',
      }
    }
  },
  created() {
    this.load()
  },
  methods: {
    getSO(){
      this.searchDate.type = 'songList'
      this.load()
    },
    getMU(){
      this.searchDate.type = 'music'
      this.load()
    },
    load(){
      console.log(this.searchDate.state, this.searchDate.type)
      fetch('http://127.0.0.1:9001/getAuditList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.searchDate),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.tableData = data.auditList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    getUn(){
      this.searchDate.state = 'unAudited'
    },
    getEd(){
      this.searchDate.state = 'Audited'
    },
    audit(row){
      // 显示审核弹窗
      fetch('http://127.0.0.1:9001/audit/auditById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(row),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              if (row.type === "songList"){
                this.form = data.songList
                this.dialogFormVisibleS = true
              }else{
                this.form = data.music
                this.dialogFormVisibleM = true
              }
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    logout() {
      localStorage.removeItem("user")
      this.$router.push("/")
      this.$message.success("退出成功")
    },
    handleUserNameClick(uid) {
      const formData1 = new FormData();
      formData1.append('id', uid);
      formData1.append('type', "get")
      fetch('http://127.0.0.1:9001/updateperson/', {
        method: 'POST',
        body: formData1
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.user1 = data.user
              this.userNameDialogVisible = true;
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    saveContent(content, result){
      this.updateResult(this.user, this.form, content, 'failure')
    },
    auditRuselt(form, result){
      if (result == 'failure'){
        this.contentDialogVisible = true;
      }
      else(
          this.updateResult(this.user, this.form, 'success', 'success')
      )
    },
    updateResult(user, form, content, state){
      const data = {
        userId:user.id,
        aid: form.aid,
        type:form.type,
        content:content,
        state:state,
      }
      console.log(data)
      fetch('http://127.0.0.1:9001/audit/auditResult/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            this.$notify({
              title: data.msg
            });
          })
    },
    getallMusics(form){
      fetch('http://127.0.0.1:9001/getListById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form.iid),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.dialogFormVisibleSAll = true;
              this.allMusics = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    }
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
.el-dropdown-link {
  cursor: pointer;
}
.el-icon-arrow-down {
  font-size: 12px;
}
.demonstration {
  display: block;
  color: #8492a6;
  font-size: 14px;
  margin-bottom: 20px;
}
.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
.block-col-2 .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}

.block-col-2 .el-dropdown-link {
  display: flex;
  align-items: center;
}
</style>
