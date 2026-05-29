import { type Book } from "./book_types"
import { type Review } from "./review_types"


export interface UserRegister{
  username: string,
  email: string,
  password: string,
  first_name: string,
  last_name: string
}

export interface User{
  uid: string,
  username: string,
  email: string,
  first_name: string,
  last_name: string,
  is_verified: boolean,
  password_hash: string,
  created_at: string,
  updated_at: string,
  avatar_url: string,
  role: string
}

export interface UserLogin{
  email: string,
  password: string
}

export interface UserBooks extends User{
  books: Book[],
  reviews: Review[]
}

export interface AuthResponse {
  message: string
  access_token: string
  refresh_token: string
  user: {
    uid: string,
    email: string,
    avatar_url: string,
    username: string,
    role: string
  }
}

export interface AuthUser {
  uid: string
  email: string
  avatar_url: string
  username: string
  role: string
}