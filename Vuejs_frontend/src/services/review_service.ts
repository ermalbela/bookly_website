import type { Review, ReviewCreate } from "@/types/review_types";
import api from "./api";
import type { ProfileResponse } from "@/types/user_types";

export const reviewService = {
  create_review: async (rating: number, review_text: string, book_id: string): Promise<ReviewCreate> => {
    const { data } = await api.post<ReviewCreate>('/review/book/' + book_id, { rating, review_text })
    return data
  },

  get_reviews_by_user: async (user_id: string): Promise<Review[]> => {
    const { data } = await api.get<Review[]>('/review/get_user_reviews/' + user_id)
    return data
  },

  delete_review: async (review_uid: string): Promise<void> => {
    await api.delete<void>('/review/' + review_uid)
  },

  like_review: async (review_uid: string, user_uid: string): Promise<void> => {
    await api.post<void>(`user_review/user/${user_uid}/review/${review_uid}`)
  },

  unlike_review: async (review_uid: string, user_uid: string): Promise<void> => {
    await api.delete<void>(`user_review/user/${user_uid}/review/${review_uid}`)
  },

  get_user_likes: async (user_uid: string): Promise<ProfileResponse> => {
    const { data } = await api.get<ProfileResponse>('/user_review/' + user_uid)
    return data
  }
}