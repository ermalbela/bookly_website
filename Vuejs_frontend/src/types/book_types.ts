import type { Review } from "./review_types"
import type { Tag } from "./tag_types"

export interface Book {
  uid: string,
  title: string,
  author: string,
  publisher: string,
  published_date: string,
  page_count: number,
  language: string,
  created_at: string,
  updated_at: string,
}

export interface BookCreateModel {
  title: string,
  author: string,
  publisher: string,
  published_date: string,
  page_count: number,
  language: string,
}

export interface BookUpdateModel {
  title: string,
  author: string,
  publisher: string,
  page_count: number,
  language: string,
}

export interface BookDetail extends Book{
  reviews: Review[],
  tags: Tag[]
}