<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Authors</th>
              <th scope="col">Publisher</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>
                <div v-for="(author, index) in book.authors" :key="index">
                  {{ author.name }}
                </div>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.book-update-modal
                          @click="editBook(book)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteBook(book)">
                      Delete
                  </button>
                </div>
              </td>
              <td>{{ book.publisher }} </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal"
            id="book-modal"
            title="Add a new book"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Authors:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.authors"
                          required
                          placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-publisher-group"
                      label="Publisher:"
                      label-for="form-publisher-input">
            <b-form-input id="form-publisher-input"
                          type="text"
                          v-model="addBookForm.publisher"
                          required
                          placeholder="Enter publisher">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
            id="book-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Authors:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.authors"
                          required
                          placeholder="Enter authors">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-publisher-edit-group"
                      label="Publisher:"
                      label-for="form-publisher-edit-input">
            <b-form-input id="form-publisher-edit-input"
                          type="text"
                          v-model="editForm.publisher"
                          required
                          placeholder="Enter publisher">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import Alert from './Alert.vue';
import BookDataService from "../services/BookDataService";

export default {
  data() {
    return {
      books: [],
      addBookForm: {
        title: '',
        author: '',
        publisher: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        title: '',
        authors: '',
        publisher: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getBooks() {
      BookDataService.getAll()
        .then((res) => {
          this.books = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      BookDataService.create(payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.authors = '';
      this.addBookForm.publisher = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.authors = '';
      this.editForm.publisher = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        title: this.addBookForm.title,
        authors: this.addBookForm.authors,
        publisher: this.addBookForm.publisher
      };
      console.log(payload);
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.editForm = book;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
      };
      this.updateBook(payload, this.editForm.id);
    },
    updateBook(payload, bookID) {
      BookDataService.update(bookID, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    removeBook(bookID) {
      BookDataService.delete(bookID)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
  },
  created() {
    this.getBooks();
  },
};
</script>