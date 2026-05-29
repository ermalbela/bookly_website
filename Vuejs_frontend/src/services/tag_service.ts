import api from "./api"


export const tagService = {
  add_tag_to_book: async (book_uid: string, tag_uid: string) => {
    const {data} = await api.post(`/book_tag/book/${book_uid}/tag/${tag_uid}`)
    console.log(data);
    return data
  },

  get_all_tags: async () => {
    const {data} = await api.get('/tag/get_all_tags');
    console.log(data) 
    return data;
  },

  create_tag: async (name: string) => {
    const {data} = await api.post('/tag/create_tag', {name})
    return data;
  },

  remove_tag_from_book: async (book_uid: string, tag_uid: string) => {
    await api.delete(`/book_tag/book/${book_uid}/tag/${tag_uid}`)
  },

  delete_tag: async (tag_uid: string) => {
    await api.delete(`/tag/remove_tag/${tag_uid}`)
  }
}