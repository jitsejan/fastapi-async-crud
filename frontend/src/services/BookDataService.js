import http from "../http-common";

class BookDataService {
  getAll() {
    return http.get("/books");
  }

  get(id) {
    return http.get(`/books/${id}`);
  }

  create(data) {
    console.log(data);
    return http.post("/books", data);
  }

  update(id, data) {
    return http.put(`/books/${id}`, data);
  }

  delete(id) {
    return http.delete(`/books/${id}`);
  }
}

export default new BookDataService();