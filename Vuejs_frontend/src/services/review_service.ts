import type { Review } from "@/types/review_types";
import api from "./api";

export const reviewService = {
  create_review: async (rating: number, review_text: string, book_id: string) => {
    const {data} = await api.post('/review/book/' + book_id, {rating, review_text})
    return data
  },

  get_reviews_by_user: async (user_id: string) => {
    const {data} = await api.get<Review>('/review/get_user_reviews/' + user_id)
    return data
  },
  
  delete_review: async (review_uid: string) => {
    const {data} = await api.delete('/review/' + review_uid);
    return data
  },
  
  like_review: async (review_uid: string, user_uid: string) => {
      const {data} = await api.post(`user_review/user/${user_uid}/review/${review_uid}`)
      console.log(data);
      return data
  },

  unlike_review: async (review_uid: string, user_uid: string) => {
    const {data} = await api.delete(`user_review/user/${user_uid}/review/${review_uid}`)
    return data
  },

  get_user_likes: async (user_uid: string) => {
    const {data} = await api.get('/user_review/' + user_uid)
    console.log(data);
    return data
  }
}