<template>
  <div>
    <div style="display: flex; align-items: center">
      
      <md-input
        v-model="question"
        class="input-with-select"
        icon="el-icon-search"
        name="title"
        :placeholder="placeholderText"
        @keyup.enter.native="getSearchResult"
        @input="highlightKeyword(question)"
        @click.native="placeholderText = ''"
      >
        <i class="el-icon-search el-input__icon" style="color: #4338ca"></i>
        <span class="text" style="color: #4338ca">请输入提问</span>
      </md-input>

      <el-switch
        v-model="readPublicLibrary"
        active-text="在公开的库中检索"
        @change="switchLibrary"
        class="search-switch"
      >
      </el-switch>
      
      <el-button
        type="primary"
        @click="getAllAnswer"
        v-waves
        class="getallAnswer-button"
        >查询</el-button
      >
    </div>

    <div class="table">
      <el-table
        :data="pairs"
        border
        max-height="525"
        class="tableClass"
        style="width: 100%"
        tooltip-effect="light"
        v-loading="loading"
      >
        <el-table-column
          type="String"
          label="提问"
          :show-overflow-tooltip="Boolean('true')"
          width="490px"
        >
          <template slot-scope="scope">
            <p v-html="highlightText(scope.row.question)"></p>
          </template>
        </el-table-column>
        <el-table-column
          prop="answer"
          label="回答"
          :show-overflow-tooltip="Boolean('true')"
          width="260px"
        ></el-table-column>
        <el-table-column
          prop="title"
          label="来源文献"
          :show-overflow-tooltip="Boolean('true')"
          width="185px"
        >
          <template scope="scope">
            <div @click="lookUpFile(scope.row)">{{ scope.row.title }}.txt</div>
          </template>
        </el-table-column>
        <el-table-column align="center">
          <template slot-scope="scope">
            <span
              class="el-icon-edit edit"
              @click="handleEdit($event, scope.row)"
            ></span>

            &nbsp; &nbsp;
            <span
              class="el-icon-delete delete"
              @click="handleDelete($event, scope.row)"
            ></span>
          </template>
        </el-table-column>
      </el-table>
    </div>
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
      v-show="isAll"
    >
    </el-pagination>
    <el-dialog title="问答对" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="问题" :label-width="formLabelWidth">
          <el-input v-model="form.question" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="回答" :label-width="formLabelWidth">
          <el-input v-model="form.answer" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">保 存</el-button>
      </div>
    </el-dialog>
    <custom-modal
      :visible="visible"
      :data="fileDetail"
      :keywords="highlightKeywords_pair"
      @close="handleClose"
    ></custom-modal>
  </div>
</template>
<script>
import { getAllAnswer, deleteAnswer, updateAnswer, search } from "@/api/answer";
import { getFileDetail } from "@/api/file";
import CustomModal from "components/CustomModal.vue";
import MdInput from "components/MDinput";
import waves from "@/directive/waves";
export default {
  name: "Answer",
  components: { CustomModal, MdInput },
  directives: { waves },
  data() {
    return {
      pairs: [],
      question: "",
      placeholderText: "请输入提问",
      total: 100,
      isAll: true,
      params: {
        page: 1,
        pageSize: 10,
      },
      dialogFormVisible: false,
      form: {
        id: "",
        question: "",
        answer: "",
      },
      formLabelWidth: "50px",
      loading: true,
      highlightKeywords: [],
      highlightKeywords_pair: [],
      fileDetail: {},
      visible: false,
      readPublicLibrary: false,
      publicSearch: 0,
    };
  },
  methods: {
    getAllAnswer() {
      this.isAll = true;
      getAllAnswer({
        page: this.params.page,
        pageSize: this.params.pageSize,
        publicSearch: this.publicSearch,
      }).then((res) => {
        this.pairs = res.data.data.current_page_data;
        this.total =
          res.data.data.pagination.total_pages * this.params.pageSize;
        this.loading = false;
      });
    },
    getSearchResult() {
      this.params.page = 1;
      this.params.pageSize = 10;
      this.isAll = false;
      this.loading = true;
      search({
        question: this.question,
        publicSearch: this.publicSearch,
      }).then((res) => {
        this.pairs = res.data.data;
        this.loading = false;
      });
    },
    switchLibrary() {
      this.publicSearch = this.readPublicLibrary ? 1 : 0;
    },
    handleSizeChange(v) {
      this.params.pageSize = v;
      this.loading = true;
      this.getAllAnswer();
    },
    handleCurrentChange(v) {
      this.params.page = v;
      this.loading = true;
      this.getAllAnswer();
    },
    handleDelete(event, row) {
      event.stopPropagation();
      //删除文件
      this.$confirm("确定要删除此问答对?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          deleteAnswer({ id: row.id }).then((res) => {
            if (res.status == 200) {
              this.$message.success("删除成功");
              this.getAllAnswer();
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
    handleEdit(event, row) {
      event.stopPropagation();
      this.dialogFormVisible = true;
      this.form.id = row.id;
      this.form.question = row.question;
      this.form.answer = row.answer;
    },
    save() {
      updateAnswer(this.form).then((res) => {
        if (res.status == 200) {
          this.$message.success("修改成功");
          this.getSearchResult();
          this.dialogFormVisible = false;
        }
      });
    },
    highlightText(text) {
      // 将关键词用 <span> 标签包裹并添加样式
      const regex = new RegExp(this.highlightKeywords.join("|"), "gi");
      return text.replace(regex, `<span style="color: red;">$&</span>`);
    },
    highlightKeyword(text) {
      // 根据输入框的内容拆分关键词为数组
      this.highlightKeywords = text.split(" ").map((keyword) => keyword.trim());
    },
    getFileDetail(document_id) {
      getFileDetail({ document_id: document_id }).then((res) => {
        this.fileDetail = res.data.data;
      });
    },
    lookUpFile(row) {
      this.visible = true;
      this.getFileDetail(row.document_id);
      let pair = row.question + " " + row.answer;
      //去掉标点符号
      pair = pair.replace(/[^\w\s]/gi, "");
      this.highlightKeywords_pair = pair
        .split(" ")
        .map((keyword) => keyword.trim());
    },
    handleClose() {
      this.visible = false;
    },
  },
  created() {
    this.getAllAnswer();
  },
};
</script>
<style scoped>
.input-with-select {
  width: 500px;
  margin-top: 40px;
  margin-left: 30px;
}

.el-icon-search {
  cursor: pointer;
  font-size: 20px;
}
.el-icon-search:hover {
  color: #5e85bf;
}
.getallAnswer-button {
  /* position: absolute; */
  margin-left: 300px;
  /* top: 110px; */
  /* background-color: #809cf5; */
}

.search-switch {
  margin-top: 40px;
}
.table {
  margin: 0 auto;
  margin-top: 15px;
  width: 1100px;
  height: 525px;
}
.tableClass {
  width: 100%;
  height: 100%;
  border-collapse: collapse;
  border: 1px solid #ebeef5;
}
.tableClass .cell {
  padding: 0 !important;
  height: 5px;
  line-height: 20px !important;
  text-align: center;
}
.el-pagination {
  text-align: center;
}
.delete {
  cursor: pointer;
  font-size: 18px;
}
.delete:hover {
  color: #5e85bf;
}

.edit {
  cursor: pointer;
  font-size: 18px;
}
.edit:hover {
  color: #5e85bf;
}
div :deep(.el-table--border)::after,
div :deep(.el-table--group)::after,
div :deep(.el-table)::before {
  background-color: transparent;
}
</style>
