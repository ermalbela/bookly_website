import Books from "./pages/Books.vue";
import ViewBook from "./pages/BookDetail.vue";

export const sidebar_items = [
  {
    name: "Books",
    path: "/books",
    component: Books
  },
  {
    name: "Tags",
    path: "/tags",
    component: Books
  },
]