import Books from "./pages/Books.vue";
import ViewBook from "./pages/BookDetail.vue";
import Profile from "./pages/Profile.vue";

export const sidebar_items = [
  {
    name: "Profile",
    path: "/profile",
    component: Profile
  },
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