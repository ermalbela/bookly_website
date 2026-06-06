export interface Review {
  uid: string
  rating: number
  review_text: string
  user_uid: string
  book_uid: string
  created_at: string
  updated_at: string
  user: {
    username: string
    avatar_url: string
  } | null
  likes_count: number
  is_liked: boolean
}

export interface ReviewCreate {
  rating: number
  review_text: string
}