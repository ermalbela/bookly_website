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
  }
}