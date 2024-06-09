

<template>
  <el-dialog
      v-model="dialogFormVisibleSAll"
      title="歌单"
      width="1000"
      align-center
  >
    <el-card class="box-card" :style="{ height: '400px' }">
      <div slot="header" class="clearfix">
        <h1 style="text-align: center">我的歌单</h1>
      </div>
      <div>
        <el-table :data="songListMine" border stripe :header-cell-class-name="'headerBg'" style="margin-top: 20px;">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="名称" width="140"></el-table-column>
          <el-table-column prop="type" label="类型"></el-table-column>
          <el-table-column prop="owner" label="所属者"></el-table-column>
          <el-table-column prop="audit_state_msg" label="审核状态"></el-table-column>
          <el-table-column label="操作" width="500" align="center">
            <template #default="scope">
              <el-button type="success" @click="audit(scope.row)"> 查 看 </el-button>
              <el-button type="primary" @click="audit(scope.row)"> 点 赞 </el-button>
              <el-button type="primary" @click="audit(scope.row)"> 收 藏 </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    <el-card class="box-card" :style="{ height: '400px' }">
      <div slot="header" class="clearfix">
        <h1 style="text-align: center">收藏歌单</h1>
      </div>
      <div>
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
      </div>
    </el-card>
    <template #footer>
      <div class="dialog-footer" v-if="searchDate.state === 'unAudited'">
        <el-button type="primary" @click="addSongList">新增歌单</el-button>
        <el-button type="primary" @click="viewSongList">查看歌单</el-button>
      </div>
    </template>
  </el-dialog>
</template>
<script setup>

</script>
<style scoped>

</style>