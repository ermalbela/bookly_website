export interface Review {
  uid: string
  rating: number
  review_text: string
  user_uid: string
  book_uid: string
  created_at: string
  updated_at: string
}

export interface ReviewCreate {
  rating: number
  review_text: string
}