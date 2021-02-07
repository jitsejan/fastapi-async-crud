<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-b-modal.book-modal
        >
          Add Book
        </button>
        <br /><br />
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
                <ul>
                  <li v-for="(author, index) in book.authors" :key="index">
                    {{ author.name }}
                  </li>
                </ul>
              </td>
              <td>{{ book.publisher.name }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-update-modal
                    @click="editBook(book)"
                  >
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteBook(book)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal
      ref="addBookModal"
      id="book-modal"
      title="Add a new book"
      hide-footer
    >
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-title-group"
          label="Title:"
          label-for="form-title-input"
        >
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addBookForm.title"
            required
            placeholder="Enter title"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-author-group"
          label="Authors:"
          label-for="form-author-input"
        >
          <ul>
            <li v-for="(author, index) in authors" :key="index">
              <b-form-input
                id="form-author-input"
                type="text"
                value=""
                required
                v-model="author.name"
                placeholder="Enter author"
              >
              </b-form-input>
              <span>
                <font-awesome-icon :icon="['fas', 'user-minus']" class="icon alt" @click="remove(index)" v-show="index || ( !index && authors.length > 1)"/>
                <font-awesome-icon :icon="['fas', 'user-plus']" class="icon alt" @click="add()" v-show="index == authors.length-1" />
               </span>
            </li>
          </ul>
        </b-form-group>
        <b-form-group
          id="form-publisher-group"
          label="Publisher:"
          label-for="form-publisher-input"
        >
          <b-form-input
            id="form-publisher-input"
            type="text"
            v-model="addBookForm.publisher"
            required
            placeholder="Enter publisher"
          >
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal
      ref="editBookModal"
      id="book-update-modal"
      title="Update"
      hide-footer
    >
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group
          id="form-title-edit-group"
          label="Title:"
          label-for="form-title-edit-input"
        >
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="editForm.title"
            required
            placeholder="Enter title"
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          id="form-author-edit-group"
          label="Authors:"
          label-for="form-author-edit-input"
        >
          <div v-for="(author, index) in this.authors" :key="index">
            <b-form-input
              id="form-author-edit-input"
              type="text"
              required
              placeholder="Enter authors"
              :value="author.name.trim()"
            >
            </b-form-input>
            <span>
              <font-awesome-icon :icon="['fas', 'user-minus']" class="icon alt" @click="remove(index)" v-show="index || ( !index && authors.length > 1)"/>
              <font-awesome-icon :icon="['fas', 'user-plus']" class="icon alt" @click="add()" v-show="index == authors.length-1" />
              </span>
          </div>
        </b-form-group>
        <b-form-group
          id="form-publisher-edit-group"
          label="Publisher:"
          label-for="form-publisher-edit-input"
        >
          <b-form-input
            id="form-publisher-edit-input"
            type="text"
            v-model="editForm.publisher.name"
            required
            placeholder="Enter publisher"
          >
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
import Alert from "./Alert.vue";
import BookDataService from "../services/BookDataService";
import {
  faUserMinus,
  faUserPlus,
} from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";
library.add([faUserMinus, faUserPlus]);

export default {
  data() {
    return {
      authors: [{
        name: "",
      }],
      books: [],
      addBookForm: {
        title: "",
        publisher: "",
      },
      message: "",
      showMessage: false,
      editForm: {
        id: "",
        title: "",
        authors: [],
        publisher: "",
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    add () {
      this.authors.push({
        name: "",
      })
    },
    remove (index) {
      this.authors.splice(index, 1)
    },
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
          this.message = "Book added!";
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.authors = [
        {
          name: ""
        }
      ];
      this.addBookForm.title = "";
      this.addBookForm.authors = "";
      this.addBookForm.publisher = "";
      this.editForm.id = "";
      this.editForm.title = "";
      this.editForm.authors = "";
      this.editForm.publisher = "";
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      console.log(this.authors);
      const payload = {
        title: this.addBookForm.title,
        authors: this.authors,
        publisher: {
          name: this.addBookForm.publisher,
        },
      };
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
      this.authors = book.authors;
      console.log(this.authors);
      var authors_names = [];
      book.authors.forEach((author) => {
        authors_names.push(author.name.trim());
      });
      this.editForm.author_names = authors_names.join(", ");
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editForm.title,
        authors: this.authors,
        publisher: {
          name: this.editForm.publisher.name,
        },
      };
      console.log(payload);
      console.log(this.editForm.id);
      this.updateBook(payload, this.editForm.id);
    },
    updateBook(payload, bookID) {
      BookDataService.update(bookID, payload)
        .then(() => {
          this.getBooks();
          this.message = "Book updated!";
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
      this.getBooks();
    },
    removeBook(bookID) {
      BookDataService.delete(bookID)
        .then(() => {
          this.getBooks();
          this.message = "Book removed!";
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

<style>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 0 10px;
}
</style>