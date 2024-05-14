<template>
  <div>
    <div class="uploadfile">
      <div class="upload-demo">
        <el-upload
          class="upload-demo"
          :before-upload="beforeUpload"
          action=""
          :show-file-list="false"
          list-type="picture-card"
          :http-request="uploadFile"
          multiple
          :limit="10"
          :file-list="toBeUploadedFiles"
          accept=".txt, .pdf"
        >
          <i slot="default" class="el-icon-plus"></i>
        </el-upload>
      </div>
      <div class="wait-upload">
        <div
          class="upload-list"
          v-for="(file, index) in toBeUploadedFiles"
          :key="index"
        >
          <li>
            <div class="filename">
              &nbsp;&nbsp;{{ file.title }}.{{ file.file_type }}
            </div>

            <div class="el-icon-close" @click="deleteFile(index)"></div>
          </li>
        </div>
      </div>
    </div>
    <div class="btn">
      <div v-waves class="button" @click="sureOpenDialogVisible = true">
        <i class="el-icon-upload2"></i>
      </div>
      <span class="text">&nbsp;&nbsp;&nbsp;支持上传txt文件和pdf文件</span>
    </div>

    <el-dialog title="提示" :visible.sync="sureOpenDialogVisible" width="30%">
      <span>您是否愿意公开该文献</span>
      <span v-waves slot="footer" class="dialog-footer">
        <el-button @click="notOpenArticle">否</el-button>
        <el-button type="primary" @click="openArticle">是</el-button>
      </span>
    </el-dialog>

    <div style="float: left" class="file_list">
      <ul>
        <li style="display: flex; align-items: center;">
          <h3>已上传通过文献</h3>
        <el-switch
          v-model="readPublicLibrary"
          active-text="查看所有公开的文献"
          @change="switchLibrary"
        >
        </el-switch>
      </li>
        <li>
          <el-table
            :data="successFiles"
            @row-click="handdle"
            style="width: 100%"
            :row-style="{ height: '50px' }"
            v-loading="loading"
          >
            <el-table-column prop="title" label="文献名" width="160">
            </el-table-column>
            <el-table-column prop="user_name" label="上传人" width="120">
            </el-table-column>
            <el-table-column prop="create_time" label="上传时间" width="120">
            </el-table-column>
            <el-table-column prop="open_level" label="是否公开" width="120">
              <template slot-scope="scope">
                <span v-if="scope.row.open_level == 1">是</span>
                <span v-else>否</span>
              </template>
            </el-table-column>
            <el-table-column align="right">
              <template slot-scope="scope">
                <span
                  class="el-icon-delete delete"
                  @click="handleDelete($event, scope.row)"
                ></span>
                &nbsp; &nbsp;
                <span
                  class="el-icon-download download"
                  @click="handleDownload($event, scope.row)"
                ></span>
              </template>
            </el-table-column>
          </el-table>
        </li>
      </ul>
      <div class="box" style="height: 20px"></div>
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="params.page"
        :page-size="params.pageSize"
        layout="prev, pager, next"
        :total="total"
        class="pagination"
      >
      </el-pagination>
    </div>
    <custom-modal
      :visible="visible"
      :data="fileDetail"
      @close="handleClose"
    ></custom-modal>
  </div>
</template>
<script>
import { uploadFile, getAllFiles, getFileDetail, deleteFile } from "api/file";
import CustomModal from "components/CustomModal.vue";
import { saveAs } from "file-saver";
import waves from "@/directive/waves";
export default {
  name: "UploadFile",
  components: { CustomModal },
  directives: { waves },
  data() {
    return {
      //   tableDate: [],
      toBeUploadedFiles: [],
      successFiles: [],
      total: 0,
      params: {
        page: 1,
        pageSize: 4,
        role: this.$store.getters.getUser,
      },
      visible: false,
      fileDetail: {},
      loading: true,
      sureOpenDialogVisible: false,
      openLevel: 1, //默认公开
      publicLibrary: 0,
      readPublicLibrary: false, //默认不查看公开文献库,和publicLibrary同状态
    };
  },
  computed: {},
  methods: {
    handleDownload(event, row) {
      event.stopPropagation();
      //下载文件
      this.getFileDetail(row.document_id);
      const blob = new Blob([this.fileDetail.content], {
        type: "text/plain;charset=utf-8",
      });
      saveAs(blob, this.fileDetail.title + ".txt");
    },
    handleDelete(event, row) {
      event.stopPropagation();
      //删除文件
      this.$confirm("确定要从文献库中永久删除此文件?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          deleteFile({ document_id: row.document_id }).then((res) => {
            if (res.status == 200) {
              this.$message.success("删除成功");
              this.getAllFiles();
            }
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    openArticle() {
      this.sureOpenDialogVisible = false;
      this.openLevel = 1;
      this.submit();
    },
    notOpenArticle() {
      this.sureOpenDialogVisible = false;
      this.openLevel = 0;
      this.submit();
    },
    submit() {
      //逐个文件上传
      if (this.toBeUploadedFiles.length == 0) {
        this.$message.error("请先选择文件");
        return;
      }
      this.toBeUploadedFiles.forEach((file) => {
        // uploadFile({
        //   title: file.title,
        //   content: file.content,
        // }).then((res) => {
        //   console.log(res);
        //   if (res.status == 200) {
        //     this.$message.success("上传成功");
        //     this.toBeUploadedFiles = [];
        //     this.getAllFiles();
        //   }
        // });
        uploadFile({
          title: file.title,
          file_type: file.file_type,
          content: file.content,
          open_level: this.openLevel,
        });
        this.$message.success("上传成功");
        this.toBeUploadedFiles = [];
      });
      setTimeout(() => {
      this.getAllFiles();
    }, 500); // 等待 500 毫秒后刷新
    },
    beforeUpload(file) {
      //读取文件名和内容并且添加到fileList中
      //读取文件名和内容并且添加到fileList中
      const fileType = file.name.split(".").pop();
      console.log(fileType);
      if (fileType != "txt" && fileType != "pdf") {
        this.$message.error("文件类型错误, 只能上传txt或pdf文件");
      } else if (fileType == "txt") {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = (e) => {
          this.toBeUploadedFiles.push({
            title: file.name.split(".")[0],
            file_type: "txt",
            content: e.target.result,
          });
        };
      } else if (fileType == "pdf") {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
          const base64String = e.target.result.replace(
            /^data:(.*;base64,)?/,
            ""
          );
          if (base64String.length % 4 > 0) {
            base64String += "=".repeat(4 - (base64String.length % 4));
          }
          this.toBeUploadedFiles.push({
            title: file.name.split(".")[0],
            file_type: "pdf",
            content: base64String,
          });
        };
      }
    },
    handleSizeChange(v) {
      this.params.pageSize = v;
      this.loading = true;
      this.getAllFiles();
    },
    handleCurrentChange(v) {
      this.params.page = v;
      this.loading = true;
      this.getAllFiles();
    },
    switchLibrary() {
      this.publicLibrary = this.readPublicLibrary ? 1 : 0;
      this.getAllFiles();
    },
    getAllFiles() {
      this.params.page=1;
      getAllFiles({
        page: this.params.page,
        pageSize: this.params.pageSize,
        role: this.params.role,
        publicLibrary: this.publicLibrary,
      }).then((res) => {
        this.successFiles = res.data.data.current_page_data;
        this.total =
          res.data.data.pagination.total_pages * this.params.pageSize;
        this.loading = false;
      });
    },
    getFileDetail(document_id) {
      getFileDetail({ document_id: document_id }).then((res) => {
        this.fileDetail = res.data.data;
      });
    },
    handdle(row) {
      this.visible = true;
      this.getFileDetail(row.document_id);
    },
    handleClose() {
      this.visible = false;
    },
    uploadFile() {},
    deleteFile(index) {
      //删除待上传文件
      this.toBeUploadedFiles.splice(index, 1);
    },
  },
  created() {
    //获取文献库所有文献
    this.getAllFiles();
  },
};
</script>
<style scoped>
.filename {
  float: left;
}
.block :deep(.el-cascader) {
  width: 170px;
}
.block {
  margin-top: 20px;
}
h3 {
  float: left;
  width: 442px;
  padding: 0 10px;
}
.uploadfile {
  display: flex;
  height: 210px;
  width: 100%;
}
.upload-demo {
  margin-left: 20px;
  margin-top: 18px;
}
.wait-upload {
  width: 300px;
  height: 120px;
  margin-left: 30px;
  margin-top: 35px;
  overflow-y: scroll;
}
.upload-list {
  height: 20px;
  width: 250px;
  background-color: #e9e9e9;
  margin-bottom: 3px;
  line-height: 20px;
}
.el-icon-close {
  cursor: pointer;
  height: 20px;
  line-height: 20px;
  float: right;
  margin-right: 5px;
}
.el-icon-close :hover {
  color: #5e85bf;
}
.btn {
  position: absolute;
  left: 520px;
  top: 230px;
}
.btn .button {
  width: 52px;
  height: 32px;
  line-height: 32px;
  background-color: #a3b6f7;
  text-align: center;
  border-radius: 5px;
  font-size: 20px;
  cursor: pointer;
  float: left;
  color: #fff;
}
.btn .button:hover {
  background-color: #809cf5;
}
.text {
  font-size: 12px;
  float: left;
}
.file_list {
  margin: 30px;
}
.el-pagination {
  text-align: center;
}
.el-table::before {
  z-index: inherit;
}
.upload {
  border-radius: 20px;
  background-color: #5e85bf;
  color: #fff;
}
.delete {
  cursor: pointer;
  font-size: 18px;
}
.delete:hover {
  color: #5e85bf;
}

.download {
  cursor: pointer;
  font-size: 20px;
}
.download:hover {
  color: #5e85bf;
}
.el-table {
  cursor: pointer;
}
</style>
