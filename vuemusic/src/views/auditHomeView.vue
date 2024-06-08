
<template>
  <el-container>
    <el-header>
      <el-row class="grid-content bg-purple-light" :gutter="20">
        <el-col :span="4"></el-col>
        <el-col :span="2" style="text-align: center" class="grid-content bg-purple-dark"><div style="margin-top: 12px">审核管理</div></el-col>
        <el-col :span="2" style="text-align: center"
                :class="[searchDate.state==='unAudited' && 'grid-content bg-purple']">
          <div  type="text" @click="getUn" style="margin-top: 12px">待完成</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[searchDate.state==='Audited' && 'grid-content bg-purple']">
          <div type="text" @click="getEd" style="margin-top: 12px">已完成</div>
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
          <div>
            <!--        搜索部分        -->
            <div style="margin: 10px 0">
              <el-select style="width: 200px" v-model="searchDate.type" placeholder="请选择审核类型" class="ml-5">
                <el-option label="歌曲" value="muisc"></el-option>
                <el-option label="歌单" value="songList"></el-option>
              </el-select>
              <el-button class="ml-5" type="primary" @click="load">搜索</el-button>
              <el-button type="warning" @click="reset">重置</el-button>
            </div>

            <!--        表格部分        -->
            <el-table :data="auditList" border stripe :header-cell-class-name="'headerBg'">
              <el-table-column prop="id" label="ID" width="80"></el-table-column>
              <el-table-column prop="name" label="名称" width="140"></el-table-column>
              <el-table-column prop="type" label="类型"></el-table-column>
              <el-table-column prop="owner" label="所属者"></el-table-column>
              <el-table-column prop="audit_state" label="审核状态"></el-table-column>
              <el-table-column prop="audit_state" label="审核状态">
                <template slot-scope="scope">
                  <el-tag type="primary" v-if="scope.row.audit_state === 0">未开始</el-tag>
                  <el-tag type="warning" v-if="scope.row.audit_state === 1">歌曲审核中</el-tag>
                  <el-tag type="primary" v-if="scope.row.audit_state === 2">歌单审核中</el-tag>
                  <el-tag type="primary" v-if="scope.row.audit_state === 3">不予上传</el-tag>
                  <el-tag type="primary" v-if="scope.row.audit_state === 4">可上传</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="500" align="center">
                <template slot-scope="scope">
                  <el-button v-if="searchDate.state === 'unAudited'" type="primary" @click="audit(scope.row)"> 审 核 <i class="el-icon-edit"></i></el-button>
                  <el-button v-if="searchDate.state === 'Audited'" type="success" @click="audit(scope.row)"> 查 看 <i class="el-icon-edit"></i></el-button>
                </template>
              </el-table-column>
            </el-table>

<!--            审核弹窗-->
            <el-dialog title="歌曲信息" :visible.sync="dialogFormVisibleM" width="60%">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span>{{ form.name }}</span>
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
                <div style="border-top: 1px dashed #ccc; padding-top: 10px;" v-if="searchDate.state === 'unAudited'">
                  <el-button type="primary" @click="auditRuselt(form, 'success')">审核通过</el-button>
                  <el-button type="primary" @click="auditRuselt(form, 'failure')">不予通过</el-button>
                </div>
              </el-card>
            </el-dialog>

            <el-dialog title="用户信息" :visible.sync="userNameDialogVisible" width="30%">
              <el-card class="box-card">
                <div v-for="(value, key) in user1" :key="key" class="text item">
                  <template v-if="key !== 'id' && key !== 'avatar'
                        && key !== 'delete_mark'">
                    {{ customKeys[key] }}:{{ value }}
                  </template>
                </div>
              </el-card>
            </el-dialog>

            <!-- Form -->
            <el-dialog title="补充失败原因" :visible.sync="contentDialogVisible">
              <el-form>
                <el-form-item label="原因">
                  <el-input type="textarea" v-model="content" autocomplete="off"></el-input>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="contentDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveContent(content, 'failure')">确 定</el-button>
              </div>
            </el-dialog>

            <el-dialog title="歌单信息" :visible.sync="dialogFormVisibleS" width="60%">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span>{{ form.name }}</span>
                </div>
                <div v-for="(value, key) in form" :key="key" class="text item">
                  <template v-if="key !== 'id' && key !== 'avatar'
                            &&　key !== 'aid' && key !== 'type'">
                    <span v-if="key !== 'owner'">{{ customKeys[key] }}:</span>
                    <span v-else @click="handleUserNameClick(form.uid)">{{ customKeys[key] }}:</span>{{ value }}
                  </template>
                </div>
                <div style="border-top: 1px dashed #ccc; padding-top: 10px;" v-if="searchDate.state === 'unAudited'">
                  <el-button type="primary" @click="auditRuselt(form, 'success')">审核通过</el-button>
                  <el-button type="primary" @click="auditRuselt(form, 'failure')">不予通过</el-button>
                  <el-button type="success" @click="dialogFormVisibleS = false"> back </el-button>
                </div>
              </el-card>
            </el-dialog>

          </div>
        </el-col>
        <el-col :span="4"></el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "auditHomeView",
  data() {
    return {
      user:localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      auditList:[],
      form:[],
      user1:[],
      content:'',
      dialogFormVisibleS: false,
      dialogFormVisibleM: false,
      userNameDialogVisible: false,
      contentDialogVisible: false,
      searchDate:{
        user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
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
    load(){
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
              this.auditList = data.auditList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    reset() {
      this.searchDate.type = 'music'
      this.searchDate.state = 'unAudited'
      this.load()
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
      this.updateResult(this.user, this.form, content, result)
    },
    auditRuselt(form, result){
      if (result == 'failure'){
        this.contentDialogVisible = true;
      }
      else(
          this.updateResult(this.user, this.form, this.content, result)
      )
    },
    updateResult(user, form, content, state){
      fetch('http://127.0.0.1:9001/audit/auditResult/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user, form, content, state),
      })
          .then(response => response.json())
          .then(data => {
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
</style>
